from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import time
import uuid

app = Flask(__name__)
# Cho phép mọi nguồn (CORS) để giao diện trên Netlify có thể gọi được
CORS(app)

# Render yêu cầu dùng thư mục /tmp để ghi file
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def cleanup_old_files():
    """Xóa các file cũ quá 10 phút để giải phóng bộ nhớ"""
    try:
        now = time.time()
        # Kiểm tra nếu thư mục tồn tại
        if os.path.exists(DOWNLOAD_FOLDER):
            for f in os.listdir(DOWNLOAD_FOLDER):
                f_path = os.path.join(DOWNLOAD_FOLDER, f)
                # Nếu file cũ hơn 600 giây (10 phút) thì xóa
                if os.stat(f_path).st_mtime < now - 600:
                    if os.path.isfile(f_path):
                        os.remove(f_path)
    except Exception as e:
        print(f"Lỗi dọn dẹp file: {e}")

@app.route('/')
def home():
    return "UniDownloader Backend is Running!"

@app.route('/download', methods=['POST'])
def download_video():
    # 1. Dọn dẹp file rác
    cleanup_old_files()
    
    # 2. Nhận dữ liệu
    data = request.json
    if not data:
        return jsonify({'error': 'Không có dữ liệu gửi lên'}), 400

    url = data.get('url')
    platform = data.get('platform')
    
    if not url:
        return jsonify({'error': 'Thiếu đường dẫn URL'}), 400

    # 3. Tạo tên file ngẫu nhiên
    file_id = str(uuid.uuid4())
    output_template = f'{DOWNLOAD_FOLDER}/{file_id}_%(title)s.%(ext)s'

    # 4. Cấu hình yt-dlp
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best[ext=mp4]/best', # Ưu tiên MP4
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # Giả lập trình duyệt PC
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # Cấu hình riêng cho TikTok/Douyin (Giả lập Mobile)
    if platform in ['tiktok', 'douyin']:
         ydl_opts['user_agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    
    try:
        # 5. Tải video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # 6. Trả file về cho người dùng
            return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Chạy trên port 10000 (Mặc định của Render)
    app.run(host='0.0.0.0', port=10000)