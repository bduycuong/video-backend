from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import time
import uuid
import re

app = Flask(__name__)
# Cho phép kết nối từ mọi nguồn (quan trọng cho Netlify)
CORS(app)

# Cấu hình thư mục lưu file (Render bắt buộc dùng /tmp)
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def cleanup_old_files():
    """Xóa file cũ quá 10 phút để giải phóng bộ nhớ"""
    try:
        now = time.time()
        if os.path.exists(DOWNLOAD_FOLDER):
            for f in os.listdir(DOWNLOAD_FOLDER):
                f_path = os.path.join(DOWNLOAD_FOLDER, f)
                # Nếu file cũ hơn 600 giây (10 phút)
                if os.stat(f_path).st_mtime < now - 600:
                    if os.path.isfile(f_path):
                        os.remove(f_path)
    except Exception as e:
        print(f"Cleanup error: {e}")

def fix_douyin_url(url):
    """
    Hàm sửa lỗi link Douyin dạng cửa sổ nổi (modal_id)
    Chuyển từ: .../jingxuan?modal_id=7577611630494682420
    Sang: https://www.douyin.com/video/7577611630494682420
    """
    if "douyin.com" in url and "modal_id=" in url:
        try:
            # Tìm dãy số ID sau chữ modal_id=
            video_id = re.search(r'modal_id=(\d+)', url).group(1)
            fixed_url = f"https://www.douyin.com/video/{video_id}"
            print(f"Fixed Douyin URL: {fixed_url}")
            return fixed_url
        except Exception as e:
            print(f"Error fixing Douyin URL: {e}")
            return url
    return url

@app.route('/')
def home():
    return "UniDownloader Backend (Fix FB + Douyin + YT) is Running!"

@app.route('/download', methods=['POST'])
def download_video():
    # 1. Dọn dẹp file rác
    cleanup_old_files()
    
    data = request.json
    if not data or not data.get('url'):
        return jsonify({'error': 'Thiếu đường dẫn URL'}), 400

    raw_url = data.get('url')
    platform = data.get('platform')
    
    # 2. FIX LỖI DOUYIN: Tự động sửa link trước khi tải
    url = fix_douyin_url(raw_url)

    # 3. Tạo tên file
    file_id = str(uuid.uuid4())
    
    # === FIX LỖI FACEBOOK: Cắt tên video tối đa 100 ký tự ===
    # %(title).100s nghĩa là lấy 100 ký tự đầu của tiêu đề
    output_template = f'{DOWNLOAD_FOLDER}/{file_id}_%(title).100s.%(ext)s'

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best[ext=mp4]/best', # Ưu tiên MP4
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True, # Loại bỏ ký tự đặc biệt trong tên file
        # Giả lập trình duyệt máy tính
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # === FIX LỖI YOUTUBE: Nạp Cookies nếu có ===
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    # Cấu hình riêng cho TikTok/Douyin (Giả lập điện thoại để dễ tải hơn)
    if platform in ['tiktok', 'douyin']:
         ydl_opts['user_agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    
    try:
        print(f"Downloading: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Gửi file về cho người dùng
            return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))

    except Exception as e:
        error_message = str(e)
        print(f"Error: {error_message}")
        
        # Trả về thông báo lỗi thân thiện hơn
        if "Sign in" in error_message:
            return jsonify({'error': 'YouTube chặn IP (Cần file cookies.txt trên Server).'}), 500
        if "Unsupported URL" in error_message:
            return jsonify({'error': 'Link không được hỗ trợ hoặc sai định dạng.'}), 500
            
        return jsonify({'error': f'Lỗi hệ thống: {error_message}'}), 500

if __name__ == '__main__':
    # Chạy server trên port 10000
    app.run(host='0.0.0.0', port=10000)