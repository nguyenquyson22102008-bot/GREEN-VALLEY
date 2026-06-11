"""
otp_service.py - Quản lý tất cả hoạt động OTP (One-Time Password)
"""
import secrets
from datetime import datetime, timedelta

# In-memory store cho OTP
OTP_STORE = {}


def generate_otp() -> str:
    """Sinh mã OTP 6 chữ số"""
    return f"{secrets.randbelow(900000) + 100000}"


def store_otp(email: str, otp: str) -> None:
    """Lưu OTP vào bộ nhớ đệm"""
    OTP_STORE[email] = {
        "otp": otp,
        "created_at": datetime.now()
    }


def get_otp(email: str) -> dict:
    """Lấy dữ liệu OTP"""
    return OTP_STORE.get(email)


def is_otp_expired(email: str) -> bool:
    """Kiểm tra OTP đã hết hạn chưa (5 phút)"""
    if email not in OTP_STORE:
        return True
    
    otp_data = OTP_STORE[email]
    return datetime.now() - otp_data['created_at'] > timedelta(minutes=5)


def verify_otp(email: str, otp_input: str) -> bool:
    """Xác minh OTP nhập vào"""
    if email not in OTP_STORE:
        return False
    
    if is_otp_expired(email):
        delete_otp(email)
        return False
    
    otp_data = OTP_STORE[email]
    return otp_data['otp'] == str(otp_input).strip()


def delete_otp(email: str) -> None:
    """Xóa OTP khỏi bộ nhớ đệm"""
    if email in OTP_STORE:
        del OTP_STORE[email]


def can_send_otp(email: str, cooldown_seconds: int = 60) -> tuple:
    """
    Kiểm tra có thể gửi OTP không (cooldown 60 giây)
    Trả về: (True/False, số giây còn lại nếu False)
    """
    if email not in OTP_STORE:
        return True, 0
    
    otp_data = OTP_STORE[email]
    time_passed = datetime.now() - otp_data['created_at']
    
    if time_passed < timedelta(seconds=cooldown_seconds):
        time_remaining = cooldown_seconds - int(time_passed.total_seconds())
        return False, time_remaining
    
    return True, 0


def clean_expired_otps() -> None:
    """Dọn dẹp tất cả OTP hết hạn"""
    expired_emails = [email for email in list(OTP_STORE.keys()) if is_otp_expired(email)]
    for email in expired_emails:
        delete_otp(email)
        print(f"[HỆ THỐNG]: Đã tự động xóa OTP hết hạn của: {email}")
