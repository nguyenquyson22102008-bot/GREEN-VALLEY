from flask import Flask, request, jsonify, redirect, url_for, render_template, send_from_directory, session
from flask_apscheduler import APScheduler
import os
import re
from werkzeug.security import check_password_hash

# Import các module quản lý nghiệp vụ
from database import init_db, user_exists, create_user, get_user_by_email, update_user_password
from otp_service import (
    generate_otp, store_otp, get_otp, verify_otp, delete_otp, 
    can_send_otp, clean_expired_otps
)
from gmail import send_email

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static'),
)
app.secret_key = os.getenv('SECRET_KEY', 'green-valley-local-session-key')

PROTECTED_PAGE_ENDPOINTS = {
    'home_page',
    'legacy_home_page',
    'about_page',
    'features_page',
    'crops_page',
    'animals_page',
    'tools_page',
    'contact_page',
    'send_mail_page',
}


@app.before_request
def require_login_for_pages():
    if request.endpoint in PROTECTED_PAGE_ENDPOINTS and not session.get('user_email'):
        return redirect(url_for('login_page'))

# ========== CẤU HÌNH CORS VÀ SECURITY HEADERS ==========
@app.after_request
def add_local_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin == 'null' or (
        origin and (origin.startswith('http://127.0.0.1:') or origin.startswith('http://localhost:'))
    ):
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Vary'] = 'Origin'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if response.content_type and response.content_type.startswith('text/html'):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# ========== CẤU HÌNH BỘ TỰ ĐỘNG DỌN DẸP OTP ==========
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='clean_old_otps_job', seconds=60)
def scheduled_clean_expired_otps():
    """Dọn dẹp OTP hết hạn mỗi 60 giây"""
    clean_expired_otps()

# Khởi tạo database
init_db()

# ========================================================
# ĐIỀU HƯỚNG GIAO DIỆN CÁC TRANG HTML
# ========================================================

@app.route('/')
def root():
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('taikhoan/dangnhap.html')

@app.route('/logout')
def logout_page():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/register')
def register_page():
    return render_template('taikhoan/dangki.html')

@app.route('/forgot')
def forgot_page():
    return render_template('taikhoan/quenmatkhau.html')

@app.route('/reset')
def reset_page():
    return render_template('taikhoan/doimatkhau.html')

@app.route('/home')
def home_page():
    return render_template('trangchu/trangchu.html')

@app.route('/trangchu.html')
def legacy_home_page():
    return redirect(url_for('home_page'))

@app.route('/gioithieu')
@app.route('/gioithieu.html')
def about_page():
    return render_template('trangchu/gioithieu.html')

@app.route('/tinhnang')
@app.route('/tinhnang.html')
def features_page():
    return render_template('trangchu/tinhnang.html')

@app.route('/loaicay')
@app.route('/loaicay.html')
def crops_page():
    return render_template('trangchu/loaicay.html')

@app.route('/dongvat')
@app.route('/dongvat.html')
def animals_page():
    return render_template('trangchu/dongvat.html')

@app.route('/dungcu')
@app.route('/dungcu.html')
def tools_page():
    return render_template('trangchu/dungcu.html')

@app.route('/lienhe')
@app.route('/lienhe.html')
def contact_page():
    return render_template('trangchu/lienhe.html')

@app.route('/send-mail')
def send_mail_page():
    return redirect(url_for('contact_page'))

@app.route('/photo/<path:filename>')
def photo_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'photo'), filename)

@app.route('/downloads/<path:filename>')
def download_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'downloads'), filename, as_attachment=True)

# ========================================================
# HỆ THỐNG CÁC API XỬ LÝ DỮ LIỆU (DATABASE INTEGRATED)
# ========================================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    fullname = data.get('fullname')
    email = (data.get('email') or '').strip().lower()
    password = data.get('password')

    if not fullname or not email or not password:
        return jsonify({"success": False, "message": "Vui lòng điền đầy đủ thông tin!"}), 400

    try:
        if user_exists(email):
            return jsonify({"success": False, "message": "Email này đã được sử dụng!"}), 400

        if create_user(fullname, email, password):
            return jsonify({"success": True, "message": "Đăng ký tài khoản cửa hàng thành công!"}), 200
        else:
            return jsonify({"success": False, "message": "Lỗi tạo tài khoản!"}), 500
    except Exception as e:
        print(f"[LỖI ĐĂNG KÝ]: {e}")
        return jsonify({"success": False, "message": "Lỗi hệ thống cơ sở dữ liệu!"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or data.get('loginEmail') or '').strip().lower()
    password = data.get('password') or data.get('loginPassword')

    if not email or not password:
        return jsonify({"success": False, "message": "Vui lòng nhập đầy đủ Email và Mật khẩu!"}), 400

    try:
        user = get_user_by_email(email)

        if user:
            stored_fullname, stored_email, stored_hashed_password = user
            
            # Xác thực mật khẩu đã mã hóa
            if check_password_hash(stored_hashed_password, password):
                session.clear()
                session['user_email'] = stored_email
                session['user_fullname'] = stored_fullname
                return jsonify({
                    "success": True,
                    "message": "Đăng nhập thành công!",
                    "fullname": stored_fullname,
                    "email": stored_email
                }), 200

        return jsonify({"success": False, "message": "Email hoặc Mật khẩu không chính xác!"}), 401
    except Exception as e:
        print(f"[LỖI ĐĂNG NHẬP]: {e}")
        return jsonify({"success": False, "message": "Lỗi hệ thống cơ sở dữ liệu!"}), 500


@app.route('/api/send-email', methods=['POST'])
def api_send_email():
    data = request.get_json(silent=True) or {}
    to_email = (data.get('to_email') or data.get('email') or '').strip().lower()
    subject = (data.get('subject') or '').strip()
    message = (data.get('message') or data.get('body') or '').strip()

    if not to_email or not subject or not message:
        return jsonify({"success": False, "message": "Vui lòng nhập email người nhận, tiêu đề và nội dung."}), 400

    email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    if not email_pattern.match(to_email):
        return jsonify({"success": False, "message": "Địa chỉ email người nhận không hợp lệ."}), 400

    html_body = f"""
    <div style=\"font-family:Arial,Helvetica,sans-serif; max-width:700px; margin:0 auto; padding:28px; background:#ffffff; border-radius:22px; border:1px solid #e8e8e8; color:#111111;\">
        <h2 style=\"margin-bottom:10px; color:#1d2939;\">Thư gửi từ NSQ</h2>
        <p style=\"margin:0 0 20px; color:#475569; font-size:15px;\"><strong>Tiêu đề:</strong> {subject}</p>
        <div style=\"padding:22px; border-radius:18px; background:#f8fafc; color:#334155; line-height:1.8; font-size:15px;\">{message.replace('\n', '<br>')}</div>
        <p style=\"margin:24px 0 0; color:#475569; font-size:13px;\">Đây là email được gửi qua hệ thống NSQ Gmail.</p>
    </div>
    """

    try:
        if send_email(to_email, subject, html_body):
            return jsonify({"success": True, "message": "Email đã được gửi thành công!"}), 200
        return jsonify({"success": False, "message": "Gửi email thất bại. Vui lòng thử lại sau."}), 500
    except Exception as e:
        print(f"[LỖI GỬI EMAIL]: {e}")
        return jsonify({"success": False, "message": "Đã xảy ra lỗi hệ thống khi gửi email."}), 500


@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    reply_email = (data.get('email') or '').strip().lower()
    subject = (data.get('subject') or 'Liên hệ từ GREEN VALLEY').strip()
    message = (data.get('message') or '').strip()
    receiver_email = os.getenv('CONTACT_RECEIVER_EMAIL', '').strip().lower()

    if not name or not reply_email or not subject or not message:
        return jsonify({"success": False, "message": "Vui lòng nhập đầy đủ thông tin liên hệ."}), 400

    email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    if not email_pattern.match(reply_email):
        return jsonify({"success": False, "message": "Email của bạn không hợp lệ."}), 400

    if not receiver_email:
        return jsonify({
            "success": False,
            "message": "Chưa cấu hình CONTACT_RECEIVER_EMAIL trên máy chủ."
        }), 500

    html_body = f"""
    <div style="font-family:Arial,Helvetica,sans-serif; max-width:700px; margin:0 auto; padding:28px; background:#ffffff; border:1px solid #e5e7eb; color:#111827;">
        <h2>Liên hệ mới từ GREEN VALLEY</h2>
        <p><strong>Người gửi:</strong> {name}</p>
        <p><strong>Email phản hồi:</strong> {reply_email}</p>
        <p><strong>Tiêu đề:</strong> {subject}</p>
        <div style="margin-top:18px; padding:18px; background:#f8fafc; line-height:1.7;">{message.replace('\n', '<br>')}</div>
    </div>
    """

    try:
        if send_email(receiver_email, f"[GREEN VALLEY] {subject}", html_body):
            return jsonify({"success": True, "message": "Tin nhắn đã được gửi thành công!"}), 200
        return jsonify({"success": False, "message": "Không gửi được email. Vui lòng kiểm tra cấu hình SMTP."}), 500
    except Exception as e:
        print(f"[LỖI LIÊN HỆ]: {e}")
        return jsonify({"success": False, "message": "Đã xảy ra lỗi hệ thống khi gửi liên hệ."}), 500


@app.route('/api/forget', methods=['POST'])
@app.route('/api/forgot', methods=['POST'])
def forget_password():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or data.get('forgetEmail') or '').strip().lower()

    if not email:
        return jsonify({"success": False, "message": "Vui lòng nhập địa chỉ Email!"}), 400

    try:
        if not user_exists(email):
            return jsonify({"success": False, "message": "Email này không tồn tại trên hệ thống!"}), 404

        # Kiểm tra cooldown (60 giây)
        can_send, time_remaining = can_send_otp(email)
        if not can_send:
            return jsonify({
                "success": False, 
                "message": f"Thao tác quá nhanh! Vui lòng đợi thêm {time_remaining} giây để gửi lại mã mới."
            }), 429

        # Tạo OTP
        otp = generate_otp()
        store_otp(email, otp)
        
        subject = "Mã OTP khôi phục mật khẩu cửa hàng"
        html_body = f"""
        <div style="max-width:600px; margin:0 auto; background:#ffffff; border-radius:18px; padding:34px; border:1px solid #dfe8f1; font-family:sans-serif;">
            <h2 style="color:#111827;">Khôi phục mật khẩu cửa hàng</h2>
            <p style="color:#475569;">Chào bạn, mã OTP xác thực đổi mật khẩu của bạn là:</p>
            <div style="text-align:center; margin:20px 0;">
                <span style="font-size:36px; font-weight:bold; color:#1d4ed8; letter-spacing:5px; background:#f1f5f9; padding:10px 20px; border-radius:10px;">{otp}</span>
            </div>
            <p style="color:#9a3412; font-size:13px;">Mã này có hiệu lực trong 5 phút. Vui lòng tuyệt đối không chia sẻ mã này cho bất kỳ ai.</p>
        </div>
        """

        if send_email(email, subject, html_body):
            return jsonify({"success": True, "message": "Mã OTP đã được gửi thành công vào Gmail của bạn!"}), 200
        else:
            print(f"\n[MAIL FALLBACK] OTP dành cho {email}: {otp}\n")
            return jsonify({
                "success": True, 
                "message": "Hệ thống email đang bận! Mã OTP dự phòng đã được xuất thẳng ra Terminal VS Code để test."
            }), 200
    except Exception as e:
        print(f"[LỖI QUÊN MẬT KHẨU]: {e}")
        return jsonify({"success": False, "message": "Lỗi hệ thống xử lý!"}), 500


@app.route('/api/reset-password', methods=['POST'])
@app.route('/api/reset', methods=['POST'])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or data.get('resetEmail') or '').strip().lower()
    otp_input = data.get('otp')
    new_password = data.get('password') or data.get('newPassword')

    if not email or not otp_input or not new_password:
        return jsonify({"success": False, "message": "Vui lòng nhập đầy đủ thông tin!"}), 400

    try:
        # Kiểm tra OTP
        if not verify_otp(email, otp_input):
            otp_data = get_otp(email)
            if not otp_data:
                return jsonify({"success": False, "message": "Yêu cầu không hợp lệ hoặc mã OTP đã hết hạn sử dụng!"}), 400
            else:
                return jsonify({"success": False, "message": "Mã OTP nhập vào không chính xác!"}), 400

        # Cập nhật mật khẩu
        if update_user_password(email, new_password):
            delete_otp(email)
            return jsonify({"success": True, "message": "Đổi mật khẩu thành công! Vui lòng quay lại đăng nhập."}), 200
        else:
            return jsonify({"success": False, "message": "Không tìm thấy tài khoản tương ứng trên hệ thống!"}), 404
    except Exception as e:
        print(f"[LỖI ĐỔI MẬT KHẨU]: {e}")
        return jsonify({"success": False, "message": "Lỗi hệ thống cập nhật!"}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    print(f"Cửa hàng đang khởi động tại địa chỉ: http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
