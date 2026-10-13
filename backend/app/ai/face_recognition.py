import numpy as np
from typing import Tuple, Dict, Any
from backend.app.core.config import settings

class FaceRecognizer:
    """So khớp vector đặc trưng khuôn mặt sử dụng Cosine Similarity"""

    def __init__(self, threshold: float = None):
        self.threshold = threshold or settings.RECOGNITION_SIMILARITY_THRESHOLD

    def calculate_cosine_similarity(self, embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
        """Tính Cosine Similarity giữa 2 vector đặc trưng 512 chiều"""
        norm_a = np.linalg.norm(embedding_a)
        norm_b = np.linalg.norm(embedding_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        similarity = np.dot(embedding_a, embedding_b) / (norm_a * norm_b)
        return float(np.clip(similarity, 0.0, 1.0))

    def compare_templates(self, query_embedding: np.ndarray, stored_embedding: np.ndarray) -> Dict[str, Any]:
        """So khớp và kiểm tra ngưỡng nhận diện"""
        sim_score = self.calculate_cosine_similarity(query_embedding, stored_embedding)
        is_match = bool(sim_score >= self.threshold)
        confidence = round(float(sim_score), 4)

        return {
            "is_match": is_match,
            "similarity_score": confidence,
            "threshold": self.threshold,
            "confidence_level": "HIGH" if confidence >= 0.75 else ("MEDIUM" if confidence >= self.threshold else "LOW")
        }

face_recognizer = FaceRecognizer()
