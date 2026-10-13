import cv2
import numpy as np
from typing import Tuple, Dict, Any

class ImageQualityAnalyzer:
    """Đánh giá chất lượng ảnh chụp khuôn mặt trước khi trích xuất đặc trưng"""

    def __init__(self, blur_threshold: float = 80.0, min_size: int = 60):
        self.blur_threshold = blur_threshold
        self.min_size = min_size

    def check_blur(self, image: np.ndarray) -> Tuple[bool, float]:
        """Tính toán độ nét dựa trên phương sai của ma trận Laplacian"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        is_clear = bool(variance >= self.blur_threshold)
        return is_clear, float(variance)

    def check_brightness(self, image: np.ndarray) -> Tuple[bool, float]:
        """Kiểm tra độ sáng trung bình (tránh quá tối < 40 hoặc cháy sáng > 220)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        mean_brightness = float(np.mean(gray))
        is_good = bool(40.0 <= mean_brightness <= 225.0)
        return is_good, mean_brightness

    def check_face_size(self, bbox: list, frame_shape: Tuple[int, int]) -> Tuple[bool, int, int]:
        """Kiểm tra kích thước khuôn mặt có đạt chuẩn tối thiểu không"""
        x1, y1, x2, y2 = bbox[:4]
        width = int(x2 - x1)
        height = int(y2 - y1)
        is_valid = bool(width >= self.min_size and height >= self.min_size)
        return is_valid, width, height

    def estimate_head_pose(self, kps: list = None, bbox: list = None, image_shape: Tuple[int, int] = (480, 640)) -> Dict[str, Any]:
        """
        Ước lượng góc xoay đầu (Yaw, Pitch, Roll) dựa trên 5 điểm mốc (landmarks) hoặc hình học khuôn mặt:
        - kps: [left_eye, right_eye, nose, left_mouth, right_mouth]
        - Yaw: âm = quay trái, dương = quay phải, gần 0 = trực diện
        """
        if kps is not None and len(kps) >= 5:
            left_eye, right_eye, nose, left_mouth, right_mouth = kps[:5]
            eye_dx = right_eye[0] - left_eye[0]
            eye_dy = right_eye[1] - left_eye[1]
            eye_dist = np.sqrt(eye_dx**2 + eye_dy**2) + 1e-6

            # Tỷ lệ khoảng cách từ mũi tới 2 mắt
            dist_left_eye_nose = nose[0] - left_eye[0]
            dist_right_eye_nose = right_eye[0] - nose[0]
            
            # Yaw ratio: nếu nhìn thẳng, mũi ở chính giữa 2 mắt (~ 1.0)
            yaw_ratio = dist_left_eye_nose / (dist_right_eye_nose + 1e-6)
            
            # Chuyển đổi sang ước tính độ (Degree)
            # yaw_ratio > 1.4: quay phải; yaw_ratio < 0.7: quay trái; 0.7 - 1.4: trực diện
            if yaw_ratio < 0.75:
                pose_type = "LEFT"
                yaw_angle = float(-25.0 * (1.0 - yaw_ratio))
            elif yaw_ratio > 1.35:
                pose_type = "RIGHT"
                yaw_angle = float(25.0 * (yaw_ratio - 1.0))
            else:
                pose_type = "FRONTAL"
                yaw_angle = float((yaw_ratio - 1.0) * 15.0)

            # Roll (độ nghiêng đầu)
            roll_angle = float(np.degrees(np.arctan2(eye_dy, eye_dx)))

            return {
                "pose_type": pose_type,
                "yaw_angle": round(yaw_angle, 1),
                "roll_angle": round(roll_angle, 1),
                "is_frontal": pose_type == "FRONTAL",
                "is_left": pose_type == "LEFT",
                "is_right": pose_type == "RIGHT",
            }

        return {
            "pose_type": "FRONTAL",
            "yaw_angle": 0.0,
            "roll_angle": 0.0,
            "is_frontal": True,
            "is_left": False,
            "is_right": False,
        }

    def evaluate(self, image: np.ndarray, bbox: list = None, kps: list = None) -> Dict[str, Any]:
        """Tổng hợp đánh giá chất lượng và tư thế mặt"""
        is_clear, blur_score = self.check_blur(image)
        is_bright, brightness_score = self.check_brightness(image)
        
        size_valid = True
        width, height = image.shape[1], image.shape[0]
        if bbox is not None:
            size_valid, width, height = self.check_face_size(bbox, image.shape[:2])

        pose = self.estimate_head_pose(kps, bbox, image.shape[:2])

        # Điểm chất lượng tổng hợp từ 0.0 đến 1.0
        normalized_blur = min(blur_score / 300.0, 1.0)
        normalized_brightness = 1.0 - abs(brightness_score - 128.0) / 128.0
        overall_score = round(float(0.6 * normalized_blur + 0.4 * normalized_brightness), 3)

        passed = is_clear and is_bright and size_valid

        error_message = None
        if not is_clear:
            error_message = f"Ảnh bị mờ nhòe (độ nét {blur_score:.1f} < {self.blur_threshold})"
        elif not is_bright:
            error_message = "Điều kiện ánh sáng không đạt (ảnh quá tối hoặc quá chói)"
        elif not size_valid:
            error_message = f"Khuôn mặt quá nhỏ ({width}x{height}px < {self.min_size}px)"

        return {
            "passed": passed,
            "overall_score": overall_score,
            "blur_score": blur_score,
            "brightness_score": brightness_score,
            "face_width": width,
            "face_height": height,
            "pose": pose,
            "error_message": error_message
        }

quality_analyzer = ImageQualityAnalyzer()
