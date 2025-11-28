<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UniDownloader - Tải Video Đa Nền Tảng</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Inter', sans-serif; }
        .tab-btn { transition: all 0.2s ease; }
        .tab-btn.active {
            background-color: #EFF6FF; color: #2563EB;
            border: 1px solid #BFDBFE; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .tab-btn:hover:not(.active) { background-color: #F8FAFC; }
        .loader {
            border: 3px solid #f3f3f3; border-radius: 50%;
            border-top: 3px solid #ffffff; width: 20px; height: 20px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="bg-slate-100 min-h-screen flex flex-col items-center justify-center p-4">

    <div class="bg-white w-full max-w-2xl rounded-2xl shadow-xl overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-center text-white">
            <h1 class="text-3xl font-bold mb-2"><i class="fa-solid fa-cloud-arrow-down mr-3"></i>UniDownloader</h1>
            <p class="text-blue-100 opacity-90 text-lg">Tải video YouTube, TikTok, FB, Insta, Douyin, Xiaohongshu</p>
        </div>

        <!-- Tabs Navigation -->
        <div class="bg-white border-b border-gray-100 p-4">
            <div class="grid grid-cols-3 sm:grid-cols-6 gap-2">
                <button onclick="switchTab('youtube')" id="tab-youtube" class="tab-btn active flex flex-col items-center justify-center py-3 px-2 rounded-xl border border-transparent text-gray-500 hover:text-gray-700">
                    <i class="fa-brands fa-youtube text-2xl mb-1 text-red-600"></i><span class="text-xs font-semibold">YouTube</span>
                </button>
                <button onclick="switchTab('tiktok')" id="tab-tiktok" class="tab-btn flex flex-col items-center justify-center py-3 px-2 rounded-xl border border-transparent text-gray-500 hover:text-gray-700">
                    <i class="fa-brands fa-tiktok text-2xl mb-1 text-black"></i><span class="text-xs font-semibold">TikTok</span>
                </button>
                <button onclick="switchTab('facebook')" id="tab-facebook" class="tab-btn flex flex-col items-center justify-center py-3 px-2 rounded-xl border border-transparent text-gray-500 hover:text-gray-700">
                    <i class="fa-brands fa-facebook text-2xl mb-1 text-blue-700"></i><span class="text-xs font-semibold">Facebook</span>
                </button>
                <button onclick="switchTab('instagram')" id="tab-instagram" class="tab-btn flex flex-col items-center justify-center py-3 px-2 rounded-xl border border-transparent text-gray-500 hover:text-gray-700">
                    <i class="fa-brands fa-instagram text-2xl mb-1 text-pink-600"></i><span class="text-xs font-semibold">Instagram</span>
                </button>
                <button onclick="switchTab('douyin')" id="tab-douyin" class="tab-btn flex flex-col items-center justify-center py-3 px-2 rounded-xl border border-transparent text-gray-500 hover:text-gray-700">
                    <i class="fa-solid fa-music text-2xl mb-1 text-black"></i><span class="text-xs font-semibold">Douyin</span>
                </button>
                <button onclick="switchTab('xiaohongshu')" id="tab-xiaohongshu" class="tab-btn flex flex-col items-center justify-center py-3 px-2 rounded-xl border border-transparent text-gray-500 hover:text-gray-700">
                    <i class="fa-solid fa-book-open text-2xl mb-1 text-red-500"></i><span class="text-xs font-semibold">XiaoHongShu</span>
                </button>
            </div>
        </div>

        <!-- Content Area -->
        <div class="p-8">
            <div id="notification" class="hidden mb-6 p-4 rounded-xl text-sm flex items-center shadow-sm"></div>

            <div id="forms-container">
                <!-- FORM CHÍNH -->
                <form id="download-form" onsubmit="handleDownload(event)">
                    <div class="mb-6">
                        <label class="block text-gray-700 text-sm font-bold mb-3" id="input-label">
                            <i class="fa-brands fa-youtube mr-2 text-red-600"></i>Dán Link Video YouTube
                        </label>
                        <div class="relative group">
                            <input type="text" id="video-url" class="w-full pl-12 pr-24 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-gray-800" placeholder="https://youtube.com/watch?v=..." required>
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <i class="fa-solid fa-link text-gray-400"></i>
                            </div>
                            <button type="button" onclick="pasteFromClipboard()" class="absolute right-2 top-2 bottom-2 px-4 bg-white border border-gray-200 hover:bg-gray-50 text-gray-600 text-xs font-bold rounded-lg shadow-sm">DÁN LINK</button>
                        </div>
                    </div>
                    <input type="hidden" id="platform-input" value="youtube">
                    
                    <button type="submit" id="submit-btn" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-xl shadow-lg transition-all flex justify-center items-center gap-3 text-lg">
                        <span>Bắt Đầu Tải Xuống</span><i class="fa-solid fa-download"></i>
                    </button>
                </form>
            </div>
            
            <div class="mt-8 text-center text-xs text-gray-400">
                <p>Mẹo: Đảm bảo link video ở chế độ Công khai (Public)</p>
            </div>
        </div>
    </div>

    <!-- CODE KẾT NỐI VỚI RENDER -->
    <script>
        const tabConfig = {
            'youtube': { label: 'Dán Link Video YouTube', icon: 'fa-youtube', color: 'text-red-600', placeholder: 'https://youtube.com/watch?v=...' },
            'tiktok': { label: 'Dán Link Video TikTok', icon: 'fa-tiktok', color: 'text-black', placeholder: 'https://vt.tiktok.com/...' },
            'facebook': { label: 'Dán Link Video Facebook', icon: 'fa-facebook', color: 'text-blue-700', placeholder: 'https://www.facebook.com/watch/...' },
            'instagram': { label: 'Dán Link Video Instagram', icon: 'fa-instagram', color: 'text-pink-600', placeholder: 'https://www.instagram.com/reel/...' },
            'douyin': { label: 'Dán Link Video Douyin', icon: 'fa-music', color: 'text-black', placeholder: 'Copy link từ Douyin App...' },
            'xiaohongshu': { label: 'Dán Link XiaoHongShu', icon: 'fa-book-open', color: 'text-red-500', placeholder: 'Copy link từ Tiểu Hồng Thư...' }
        };

        function switchTab(platform) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`tab-${platform}`).classList.add('active');
            
            const config = tabConfig[platform];
            const label = document.getElementById('input-label');
            const input = document.getElementById('video-url');
            
            label.innerHTML = `<i class="fa-brands ${config.icon} mr-2 ${config.color}"></i>${config.label}`;
            input.placeholder = config.placeholder;
            document.getElementById('platform-input').value = platform;
        }

        async function pasteFromClipboard() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('video-url').value = text;
            } catch (err) { alert('Vui lòng dán thủ công (Ctrl+V)'); }
        }

        async function handleDownload(e) {
            e.preventDefault();
            const btn = document.getElementById('submit-btn');
            const originalContent = btn.innerHTML;
            const inputVal = document.getElementById('video-url').value;
            const platformName = document.getElementById('platform-input').value;

            // =========================================================================
            // CHỈ CẦN SỬA ĐÚNG DÒNG DƯỚI ĐÂY LÀ CHẠY
            // Thay link ví dụ bằng link thật của bạn, nhớ giữ nguyên đuôi /download
            // Ví dụ: const API_URL = "https://ten-app-cua-ban.onrender.com/download";
            
            const API_URL = "HÃY_DÁN_LINK_RENDER_CỦA_BẠN_VÀO_ĐÂY/download";
            
            // =========================================================================

            if (API_URL.includes("HÃY_DÁN_LINK")) {
                showNotification("Lỗi: Bạn chưa dán link Server Render vào code!", "error");
                return;
            }

            btn.disabled = true;
            btn.innerHTML = `<div class="loader mr-3"></div> Đang xử lý...`;
            btn.classList.add('bg-gray-400', 'cursor-not-allowed');

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: inputVal, platform: platformName })
                });

                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.error || 'Lỗi từ server');
                }

                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = `video_${platformName}_${Date.now()}.mp4`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                
                showNotification("Tải xuống thành công!", "success");
            } catch (error) {
                showNotification(error.message, "error");
            } finally {
                btn.disabled = false;
                btn.innerHTML = originalContent;
                btn.classList.remove('bg-gray-400', 'cursor-not-allowed');
            }
        }

        function showNotification(msg, type) {
            const notif = document.getElementById('notification');
            notif.className = `mb-6 p-4 rounded-xl text-sm flex items-center shadow-sm ${type === 'error' ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-700'}`;
            notif.innerHTML = msg;
            notif.classList.remove('hidden');
            setTimeout(() => notif.classList.add('hidden'), 5000);
        }
    </script>
</body>
</html>