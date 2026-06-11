from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import runpy
import smtplib
from pathlib import Path


def _load_mail_config():
    # Đã đồng bộ sang "config.py" để VS Code nhận diện mã màu chính xác
    config_path = Path(__file__).with_name("config.py") 
    if not config_path.exists():
        return {}
    try:
        return runpy.run_path(str(config_path))
    except Exception:
        return {}

def _get_mail_accounts(config: dict) -> list:
    """Lấy danh sách tài khoản Gmail dự phòng để sẵn sàng xoay vòng"""
    accounts = config.get("MAIL_ACCOUNTS")
    if isinstance(accounts, list) and accounts:
        return accounts

    # Fallback nếu cấu hình dạng đơn lẻ thay vì danh sách
    sender_email = config.get("SENDER_EMAIL")
    sender_password = config.get("SENDER_PASSWORD")
    if sender_email and sender_password:
        return [{"email": sender_email, "password": sender_password}]
    return []


def _send_with_account(smtp_server: str, smtp_port: int, account: dict, to_email: str, subject: str, html_body: str) -> bool:
    """Thực hiện kết nối SMTP bảo mật TLS và gửi email"""
    sender_email = account.get("email")
    sender_password = account.get("password")
    if not sender_email or not sender_password:
        return False

    # Khởi tạo cấu trúc Email hỗ trợ HTML
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = to_email
    
    # Ép kiểu tiêu đề UTF-8 để không bị lỗi font Tiếng Việt hoặc rơi vào Spam
    message["Subject"] = Header(subject, "utf-8").encode()
    
    # Đính kèm nội dung HTML dạng UTF-8
    message.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        # Thiết lập kết nối với Timeout 20 giây tránh treo luồng ứng dụng Flask
        with smtplib.SMTP(smtp_server, smtp_port, timeout=20) as server:
            server.ehlo()
            server.starttls()  # Kích hoạt mã hóa đường truyền TLS
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [to_email], message.as_string())
        return True
    except Exception as error:
        print(f"[LỖI SMTP] Tài khoản {sender_email} thất bại: {error}")
        return False


def send_email(to_email: str, subject: str, html_body: str) -> bool:
    """Hàm tổng điều phối gửi email, tự động xoay vòng tài khoản nếu gặp lỗi"""
    config = _load_mail_config()
    smtp_server = config.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(config.get("SMTP_PORT", 587))

    accounts = _get_mail_accounts(config)
    if not accounts:
        print("[LỖI]: Hệ thống không tìm thấy bất kỳ tài khoản Gmail nào được cấu hình!")
        return False

    # Vòng lặp thông minh: Nếu tài khoản trước lỗi, tự động nhảy sang tài khoản sau
    for account in accounts:
        if _send_with_account(smtp_server, smtp_port, account, to_email, subject, html_body):
            print(f"[HỆ THỐNG]: Thư gửi thành công! [{account.get('email')} ➔ {to_email}]")
            return True

    print(f"[LỖI]: Tất cả {len(accounts)} tài khoản Gmail dự phòng đều thất bại.")
    return False