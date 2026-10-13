import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Xử lý gửi email OTP và thông báo qua Google SMTP App Password"""

    @staticmethod
    def send_email(to_email: str, subject: str, html_body: str) -> bool:
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.warning(
                f"[SMTP Simulation] Chưa cấu hình SMTP_PASSWORD trong .env. "
                f"Nội dung email gửi tới '{to_email}' với tiêu đề '{subject}'."
            )
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg["To"] = to_email

            part = MIMEText(html_body, "html", "utf-8")
            msg.attach(part)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, msg.as_string())
            
            logger.info(f"Đã gửi email thành công tới {to_email}")
            return True
        except Exception as e:
            logger.error(f"Lỗi khi gửi email tới {to_email}: {e}")
            return False

    @classmethod
    def send_otp_email(cls, to_email: str, recipient_name: str, otp_code: str, purpose_text: str = "kích hoạt tài khoản") -> bool:
        subject = f"[{settings.PROJECT_NAME}] Mã xác thực OTP ({otp_code})"
        html_body = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px; background-color: #ffffff;">
            <div style="text-align: center; margin-bottom: 24px;">
                <h2 style="color: #1e3a8a; margin: 0;">FACEATTEND ENTERPRISE</h2>
                <p style="color: #64748b; font-size: 14px; margin-top: 4px;">Hệ thống Quản lý Sinh viên & Điểm danh Nhận diện Khuôn mặt AI</p>
            </div>
            <div style="border-top: 2px solid #3b82f6; padding-top: 16px;">
                <p style="font-size: 16px; color: #1e293b;">Xin chào <strong>{recipient_name}</strong>,</p>
                <p style="color: #475569; line-height: 1.6;">
                    Bạn vừa thực hiện yêu cầu <strong>{purpose_text}</strong> trên hệ thống FaceAttend Enterprise.
                    Vui lòng sử dụng mã OTP gồm 6 chữ số dưới đây để hoàn tất xác thực:
                </p>
                <div style="margin: 28px 0; text-align: center;">
                    <span style="display: inline-block; font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #1d4ed8; background-color: #eff6ff; padding: 12px 28px; border-radius: 8px; border: 1px dashed #3b82f6;">
                        {otp_code}
                    </span>
                </div>
                <p style="color: #dc2626; font-size: 13px;">
                    * Lưu ý: Mã xác thực có hiệu lực trong vòng <strong>{settings.OTP_EXPIRE_MINUTES} phút</strong>. Không chia sẻ mã này cho bất kỳ ai.
                </p>
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;" />
                <p style="font-size: 12px; color: #94a3b8; text-align: center;">
                    Đây là email tự động từ hệ thống. Nếu bạn không yêu cầu hành động này, vui lòng bỏ qua email.
                </p>
            </div>
        </div>
        """
        return cls.send_email(to_email, subject, html_body)

    @classmethod
    def send_activation_success_email(cls, to_email: str, recipient_name: str) -> bool:
        subject = f"[{settings.PROJECT_NAME}] Kích hoạt tài khoản thành công"
        html_body = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px; background-color: #ffffff;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #10b981; margin: 0;">XÁC THỰC THÀNH CÔNG</h2>
            </div>
            <p style="font-size: 16px; color: #1e293b;">Xin chào <strong>{recipient_name}</strong>,</p>
            <p style="color: #475569; line-height: 1.6;">
                Tài khoản sinh viên của bạn tại <strong>{settings.PROJECT_NAME}</strong> đã được kích hoạt thành công.
                Bây giờ bạn có thể đăng nhập vào hệ thống, xem thời khóa biểu và đăng ký khuôn mặt để tham gia điểm danh AI.
            </p>
            <p style="color: #64748b; font-size: 13px; margin-top: 20px;">Trân trọng,<br>Ban Đào tạo & Quản lý Sinh viên</p>
        </div>
        """
        return cls.send_email(to_email, subject, html_body)

email_service = EmailService()
