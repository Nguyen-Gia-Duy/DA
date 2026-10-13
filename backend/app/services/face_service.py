import base64
import cv2
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.app.core.config import settings
from backend.app.core.security import encrypt_face_embedding, decrypt_face_embedding
from backend.app.models.student import Student
from backend.app.models.face_profile import FaceProfile
from backend.app.models.audit_log import AuditLog
from backend.app.ai.face_detector import detector
from backend.app.ai.face_embedding import embedding_extractor
from backend.app.ai.image_quality import quality_analyzer
from backend.app.ai.face_security import security_guard

class FaceService:

    @staticmethod
    def decode_base64_image(image_base64: str) -> np.ndarray:
        try:
            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]
            image_data = base64.b64decode(image_base64)
            np_arr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Không thể giải mã dữ liệu ảnh")
            return img
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Dữ liệu ảnh base64 không hợp lệ: {e}")

    @classmethod
    def analyze_live_pose(cls, image_base64: str) -> Dict[str, Any]:
        """Phân tích thời gian thực góc quay và chất lượng ảnh để kích hoạt tự động chụp"""
        image = cls.decode_base64_image(image_base64)
        detected_faces = detector.detect_faces(image)

        if len(detected_faces) == 0:
            return {
                "face_detected": False,
                "pose_type": "UNKNOWN",
                "yaw_angle": 0.0,
                "roll_angle": 0.0,
                "is_clear": False,
                "is_bright": False,
                "quality_score": 0.0,
                "feedback": "Không tìm thấy khuôn mặt trong khung hình."
            }

        if len(detected_faces) > 1:
            return {
                "face_detected": True,
                "pose_type": "MULTIPLE",
                "yaw_angle": 0.0,
                "roll_angle": 0.0,
                "is_clear": False,
                "is_bright": False,
                "quality_score": 0.0,
                "feedback": f"Phát hiện {len(detected_faces)} khuôn mặt. Vui lòng chỉ một người đứng trước camera."
            }

        target_face = detected_faces[0]
        bbox = target_face["bbox"]
        kps = target_face.get("kps")
        quality = quality_analyzer.evaluate(image, bbox, kps)
        pose = quality["pose"]

        feedback = "Khuôn mặt chuẩn góc."
        if not quality["passed"]:
            feedback = quality["error_message"]
        elif pose["pose_type"] == "FRONTAL":
            feedback = "Khuôn mặt trực diện chuẩn."
        elif pose["pose_type"] == "LEFT":
            feedback = "Khuôn mặt nghiêng sang trái."
        elif pose["pose_type"] == "RIGHT":
            feedback = "Khuôn mặt nghiêng sang phải."

        return {
            "face_detected": True,
            "pose_type": pose["pose_type"],
            "yaw_angle": pose["yaw_angle"],
            "roll_angle": pose["roll_angle"],
            "is_clear": quality["blur_score"] >= quality_analyzer.blur_threshold,
            "is_bright": bool(40.0 <= quality["brightness_score"] <= 225.0),
            "quality_score": quality["overall_score"],
            "feedback": feedback
        }

    @classmethod
    def register_face_profile(
        cls, db: Session, student_id: int, image_base64: str, consent_biometric: bool, user_id: int,
        image_left_base64: Optional[str] = None, image_right_base64: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Kiểm tra sự đồng ý xử lý dữ liệu sinh trắc học
        if not consent_biometric:
            raise HTTPException(
                status_code=400,
                detail="Bạn cần đồng ý với điều khoản thu thập và xử lý dữ liệu sinh trắc học để tiếp tục."
            )

        # 2. Kiểm tra sinh viên có tồn tại
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ sinh viên.")

        # 3. Giải mã và xử lý ảnh trực diện (Frontal Image)
        image_front = cls.decode_base64_image(image_base64)
        detected_faces = detector.detect_faces(image_front)
        face_check = security_guard.check_single_face(len(detected_faces))
        if not face_check["valid"]:
            raise HTTPException(status_code=400, detail=f"Ảnh trực diện: {face_check['reason']}")

        target_front = detected_faces[0]
        quality_front = quality_analyzer.evaluate(image_front, target_front["bbox"], target_front.get("kps"))
        if not quality_front["passed"]:
            raise HTTPException(status_code=400, detail=f"Ảnh trực diện: {quality_front['error_message']}")

        face_crop_front = detector.crop_face(image_front, target_front["bbox"])
        liveness_front = security_guard.check_frequency_liveness(face_crop_front)
        if not liveness_front["is_live"]:
            raise HTTPException(status_code=400, detail=f"Cảnh báo sinh trắc học: {liveness_front['reason']}")

        # Trích xuất embedding trực diện
        if target_front.get("raw_face") is not None:
            emb_front = embedding_extractor.extract_from_raw_face(target_front["raw_face"])
        else:
            emb_front = embedding_extractor.extract_deterministic_fallback(face_crop_front)

        embeddings_list = [emb_front]

        # 4. Xử lý ảnh quay trái nếu có
        if image_left_base64:
            try:
                img_left = cls.decode_base64_image(image_left_base64)
                det_left = detector.detect_faces(img_left)
                if len(det_left) == 1:
                    crop_l = detector.crop_face(img_left, det_left[0]["bbox"])
                    raw_l = det_left[0].get("raw_face")
                    emb_l = embedding_extractor.extract_from_raw_face(raw_l) if raw_l else embedding_extractor.extract_deterministic_fallback(crop_l)
                    if emb_l is not None:
                        embeddings_list.append(emb_l)
            except Exception as e:
                pass

        # 5. Xử lý ảnh quay phải nếu có
        if image_right_base64:
            try:
                img_right = cls.decode_base64_image(image_right_base64)
                det_right = detector.detect_faces(img_right)
                if len(det_right) == 1:
                    crop_r = detector.crop_face(img_right, det_right[0]["bbox"])
                    raw_r = det_right[0].get("raw_face")
                    emb_r = embedding_extractor.extract_from_raw_face(raw_r) if raw_r else embedding_extractor.extract_deterministic_fallback(crop_r)
                    if emb_r is not None:
                        embeddings_list.append(emb_r)
            except Exception as e:
                pass

        # 6. Tổng hợp vector đặc trưng đa góc (Fused L2 Normalized Embedding)
        fused_embedding = np.mean(embeddings_list, axis=0)
        fused_embedding = embedding_extractor.normalize_embedding(fused_embedding)

        # 7. Mã hóa vector embedding bằng AES-256 GCM trước khi lưu trữ
        encrypted_bytes = encrypt_face_embedding(fused_embedding)

        # 8. Lưu vào bảng face_profiles
        existing_profile = db.query(FaceProfile).filter(FaceProfile.student_id == student.id).first()
        if existing_profile:
            existing_profile.encrypted_template = encrypted_bytes
            existing_profile.quality_score = quality_front["overall_score"]
            existing_profile.model_name = f"insightface/{settings.FACE_DETECTION_MODEL}"
            existing_profile.model_version = "1.0"
            existing_profile.encryption_key_version = settings.ENCRYPTION_KEY_VERSION
            existing_profile.consent_version = "gdpr_biometric_v1"
            existing_profile.is_active = True
            profile = existing_profile
        else:
            profile = FaceProfile(
                student_id=student.id,
                encrypted_template=encrypted_bytes,
                model_name=f"insightface/{settings.FACE_DETECTION_MODEL}",
                model_version="1.0",
                encryption_key_version=settings.ENCRYPTION_KEY_VERSION,
                consent_version="gdpr_biometric_v1",
                quality_score=quality_front["overall_score"],
                is_active=True
            )
            db.add(profile)

        # Ghi log kiểm toán
        db.add(AuditLog(
            user_id=user_id,
            action="FACE_PROFILE_REGISTERED_MULTI_POSE",
            entity_type="face_profiles",
            entity_id=str(student.id),
            details={
                "student_code": student.student_code,
                "poses_captured": len(embeddings_list),
                "quality_score": quality_front["overall_score"],
                "model": profile.model_name
            },
            ip_address=ip_address
        ))

        db.commit()

        return {
            "success": True,
            "message": f"Đăng ký hồ sơ sinh trắc học thành công ({len(embeddings_list)} góc mặt được trích xuất và mã hóa an toàn AES-256 GCM)!",
            "quality_score": quality_front["overall_score"],
            "model_name": profile.model_name,
            "poses_count": len(embeddings_list),
            "student_code": student.student_code
        }

    @staticmethod
    def revoke_face_profile(db: Session, student_id: int, user_id: int, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """Thu hồi sự đồng ý và hủy kích hoạt hồ sơ khuôn mặt theo chính sách sinh trắc học"""
        profile = db.query(FaceProfile).filter(FaceProfile.student_id == student_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ khuôn mặt để thu hồi.")

        profile.is_active = False
        db.add(AuditLog(
            user_id=user_id,
            action="FACE_PROFILE_REVOKED",
            entity_type="face_profiles",
            entity_id=str(student_id),
            details={"message": "Sinh viên yêu cầu thu hồi sự đồng ý sử dụng dữ liệu sinh trắc học"},
            ip_address=ip_address
        ))
        db.commit()
        return {"success": True, "message": "Hồ sơ sinh trắc học đã được thu hồi và hủy kích hoạt thành công."}

    @staticmethod
    def get_face_profile_status(db: Session, student_id: int) -> Dict[str, Any]:
        profile = db.query(FaceProfile).filter(FaceProfile.student_id == student_id, FaceProfile.is_active == True).first()
        if not profile:
            return {"registered": False, "profile": None}
        return {
            "registered": True,
            "profile": {
                "id": profile.id,
                "model_name": profile.model_name,
                "quality_score": profile.quality_score,
                "created_at": profile.created_at,
                "consent_version": profile.consent_version
            }
        }

face_service = FaceService()
