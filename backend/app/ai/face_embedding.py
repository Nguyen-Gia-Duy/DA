import logging
import numpy as np
import cv2
from typing import Optional

logger = logging.getLogger(__name__)

class FaceEmbeddingExtractor:
    """Trích xuất và chuẩn hóa L2 vector đặc trưng 512 chiều từ khuôn mặt"""

    def normalize_embedding(self, embedding: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return embedding
        return embedding / norm

    def extract_from_raw_face(self, raw_face) -> Optional[np.ndarray]:
        if raw_face is not None and hasattr(raw_face, 'embedding') and raw_face.embedding is not None:
            emb = np.array(raw_face.embedding, dtype=np.float32)
            return self.normalize_embedding(emb)
        return None

    def extract_deterministic_fallback(self, face_crop: np.ndarray) -> np.ndarray:
        """
        Nếu InsightFace model chưa sẵn sàng tại thời điểm chạy cục bộ,
        tạo vector đặc trưng cấu trúc HOG + spatial histogram 512 chiều có tính xác định cao.
        """
        resized = cv2.resize(face_crop, (112, 112))
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) if len(resized.shape) == 3 else resized
        
        # Trích xuất 16x32 spatial cells = 512 features
        cells = cv2.resize(gray, (16, 32)).flatten().astype(np.float32)
        # Gradient features
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=1)
        mag = np.sqrt(gx**2 + gy**2)
        mag_cells = cv2.resize(mag, (16, 32)).flatten()
        
        combined = (cells * 0.6 + mag_cells * 0.4)[:512]
        return self.normalize_embedding(combined)

embedding_extractor = FaceEmbeddingExtractor()
