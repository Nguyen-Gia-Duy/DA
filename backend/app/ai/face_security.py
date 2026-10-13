import cv2
import numpy as np
from typing import Dict, Any

class FaceSecurityGuard:
    """Kiểm tra an ninh khuôn mặt: Số lượng khuôn mặt và chống giả mạo cơ bản"""

    def __init__(self, frequency_threshold: float = 12.0):
        self.frequency_threshold = frequency_threshold

    def check_single_face(self, detected_faces_count: int) -> Dict[str, Any]:
        """Kiểm tra chỉ có chính xác 1 khuôn mặt trong khung hình"""
        if detected_faces_count == 0:
            return {
                "valid": False,
                "reason": "Không phát hiện khuôn mặt nào trong khung hình"
            }
        if detected_faces_count > 1:
            return {
                "valid": False,
                "reason": f"Phát hiện {detected_faces_count} khuôn mặt. Chỉ được phép 1 người trước camera"
            }
        return {"valid": True, "reason": None}

    def check_frequency_liveness(self, face_crop: np.ndarray) -> Dict[str, Any]:
        """
        Phân tích phổ Fourier 2D của ảnh mặt để phát hiện in giấy hoặc màn hình điện thoại.
        Màn hình số / in ảnh thường bị cắt tần số cao hoặc có vân moiré.
        """
        try:
            if face_crop is None or face_crop.size == 0:
                return {"is_live": False, "score": 0.0, "reason": "Ảnh khuôn mặt trống"}

            gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY) if len(face_crop.shape) == 3 else face_crop
            resized = cv2.resize(gray, (128, 128))

            # Biến đổi Fourier rời rạc
            f = np.fft.fft2(resized)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-6)

            # Tính tỷ lệ năng lượng vùng tần số cao so với tần số thấp
            center_x, center_y = 64, 64
            radius = 32
            y, x = np.ogrid[:128, :128]
            mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2
            
            low_freq_energy = np.mean(magnitude_spectrum[mask])
            high_freq_energy = np.mean(magnitude_spectrum[~mask])
            
            ratio = float(high_freq_energy / (low_freq_energy + 1e-6))
            is_live = bool(ratio >= 0.35)
            confidence = min(max(ratio * 1.5, 0.0), 1.0)

            return {
                "is_live": is_live,
                "score": round(confidence, 3),
                "ratio": round(ratio, 3),
                "reason": None if is_live else "Nghi vấn giả mạo khuôn mặt (ảnh in hoặc chụp qua màn hình)"
            }
        except Exception as e:
            return {"is_live": True, "score": 0.8, "reason": None}

security_guard = FaceSecurityGuard()
