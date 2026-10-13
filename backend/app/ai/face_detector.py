import logging
from typing import List, Dict, Any, Optional
import cv2
import numpy as np
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class FaceDetector:
    """Phát hiện khuôn mặt sử dụng InsightFace FaceAnalysis hoặc OpenCV DNN Haar/YuNet"""

    def __init__(self):
        self._app = None
        self._initialized = False

    def _lazy_init(self):
        if self._initialized:
            return
        try:
            from insightface.app import FaceAnalysis
            self._app = FaceAnalysis(name=settings.FACE_DETECTION_MODEL, providers=['CPUExecutionProvider'])
            self._app.prepare(ctx_id=-1, det_size=(640, 640))
            self._initialized = True
            logger.info("Khởi tạo InsightFace FaceAnalysis thành công.")
        except Exception as e:
            logger.warning(f"Không thể khởi tạo InsightFace trực tiếp ({e}). Sử dụng OpenCV Face Cascade làm cơ chế dự phòng an toàn.")
            self._app = None
            self._initialized = True

    def detect_faces(self, image: np.ndarray) -> List[Dict[str, Any]]:
        self._lazy_init()
        results = []

        if self._app is not None:
            try:
                faces = self._app.get(image)
                for f in faces:
                    if f.det_score >= settings.DETECTION_THRESHOLD:
                        bbox = [int(v) for v in f.bbox]
                        results.append({
                            "bbox": bbox,
                            "det_score": float(f.det_score),
                            "kps": f.kps.tolist() if hasattr(f, 'kps') and f.kps is not None else None,
                            "raw_face": f,
                        })
                return results
            except Exception as e:
                logger.error(f"Lỗi khi phát hiện mặt với InsightFace: {e}")

        # OpenCV Fallback nếu InsightFace chưa tải xong trọng số
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(settings.MIN_FACE_SIZE, settings.MIN_FACE_SIZE))
            for (x, y, w, h) in faces:
                results.append({
                    "bbox": [x, y, x + w, y + h],
                    "det_score": 0.88,
                    "kps": None,
                    "raw_face": None,
                })
        except Exception as e:
            logger.error(f"Lỗi OpenCV fallback detector: {e}")

        return results

    def crop_face(self, image: np.ndarray, bbox: list, margin: float = 0.1) -> np.ndarray:
        h, w = image.shape[:2]
        x1, y1, x2, y2 = bbox
        dx = int((x2 - x1) * margin)
        dy = int((y2 - y1) * margin)
        nx1 = max(0, x1 - dx)
        ny1 = max(0, y1 - dy)
        nx2 = min(w, x2 + dx)
        ny2 = min(h, y2 + dy)
        return image[ny1:ny2, nx1:nx2]

detector = FaceDetector()
