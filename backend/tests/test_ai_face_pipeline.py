import numpy as np
import pytest
from backend.app.core.security import encrypt_face_embedding, decrypt_face_embedding
from backend.app.ai.face_recognition import face_recognizer
from backend.app.ai.image_quality import quality_analyzer
from backend.app.ai.face_security import security_guard

def test_embedding_aes_encryption_and_decryption():
    """Kiểm tra mã hóa AES-256 GCM và giải mã toàn vẹn vector 512 chiều"""
    original_vector = np.random.randn(512).astype(np.float32)
    original_vector = original_vector / np.linalg.norm(original_vector)

    encrypted = encrypt_face_embedding(original_vector)
    assert isinstance(encrypted, bytes)
    assert len(encrypted) > 512 * 4 # IV + Tag + Ciphertext

    decrypted = decrypt_face_embedding(encrypted)
    assert decrypted.shape == (512,)
    assert np.allclose(original_vector, decrypted, atol=1e-5)

def test_cosine_similarity_calculation():
    """Kiểm tra độ chính xác của hàm Cosine Similarity"""
    v1 = np.random.randn(512).astype(np.float32)
    v1 = v1 / np.linalg.norm(v1)

    # Cùng 1 vector -> similarity phải bằng 1.0
    res_self = face_recognizer.compare_templates(v1, v1)
    assert pytest.approx(res_self["similarity_score"], 0.001) == 1.0
    assert res_self["is_match"] is True

    # Vector trực giao -> similarity xấp xỉ 0.0
    v2 = np.random.randn(512).astype(np.float32)
    v2 = v2 - np.dot(v2, v1) * v1
    v2 = v2 / np.linalg.norm(v2)
    res_ortho = face_recognizer.compare_templates(v1, v2)
    assert res_ortho["similarity_score"] < 0.1
    assert res_ortho["is_match"] is False

def test_image_quality_blur_and_brightness():
    """Kiểm tra phát hiện ảnh mờ và điều kiện sáng"""
    # Ảnh đen hoàn toàn (quá tối)
    black_img = np.zeros((200, 200, 3), dtype=np.uint8)
    eval_black = quality_analyzer.evaluate(black_img)
    assert eval_black["passed"] is False

    # Ảnh mờ đơn sắc
    blur_img = np.full((200, 200, 3), 128, dtype=np.uint8)
    eval_blur = quality_analyzer.evaluate(blur_img)
    assert eval_blur["passed"] is False

def test_face_security_single_face_rule():
    """Kiểm tra quy tắc nghiêm ngặt: chỉ duy nhất 1 khuôn mặt"""
    assert security_guard.check_single_face(0)["valid"] is False
    assert security_guard.check_single_face(2)["valid"] is False
    assert security_guard.check_single_face(1)["valid"] is True
