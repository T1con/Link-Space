# Link Space Mobile - Phiên bản điện thoại

Ứng dụng mạng xã hội Link Space được tối ưu hóa cho điện thoại, chạy qua trình duyệt web.

## 🌟 Tính năng

- ✅ **Responsive Design**: Giao diện tối ưu cho điện thoại
- ✅ **Đăng nhập/Đăng ký**: Tài khoản mẫu có sẵn
- ✅ **Đăng bài**: Văn bản, hình ảnh, video
- ✅ **Tương tác**: Like, bình luận, theo dõi
- ✅ **Trang cá nhân**: Xem và chỉnh sửa thông tin
- ✅ **Hệ thống điểm**: Level, huy hiệu, rank
- ✅ **Real-time**: Cập nhật tức thì

## 🚀 Cách chạy

### Windows
```bash
# Cách 1: Double-click
run_mobile.bat

# Cách 2: Command Prompt
python mobile_app.py
```

### Linux/Mac
```bash
# Cài đặt dependencies
pip install -r requirements_mobile.txt

# Chạy ứng dụng
python3 mobile_app.py
```

## 📱 Truy cập từ điện thoại

### Bước 1: Khởi động ứng dụng
1. Chạy `run_mobile.bat` trên máy tính
2. Đợi thông báo "Link Space Mobile đang khởi động..."

### Bước 2: Tìm IP máy tính
```cmd
ipconfig
```
Tìm dòng "IPv4 Address" (ví dụ: 192.168.1.100)

### Bước 3: Truy cập từ điện thoại
1. Đảm bảo điện thoại và máy tính cùng mạng WiFi
2. Mở trình duyệt điện thoại
3. Truy cập: `http://[IP_MÁY_TÍNH]:5000`
   - Ví dụ: `http://192.168.1.100:5000`


## 🎨 Giao diện

- **Responsive**: Tự động điều chỉnh theo kích thước màn hình
- **Mobile-first**: Thiết kế ưu tiên cho điện thoại
- **Touch-friendly**: Nút bấm lớn, dễ chạm
- **Modern UI**: Bootstrap 5 + Font Awesome

## 📁 Cấu trúc file

```
Link Space/
├── mobile_app.py           # Ứng dụng Flask chính
├── run_mobile.bat          # Script chạy Windows
├── requirements_mobile.txt # Dependencies
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   └── create_post.html
├── static/                 # Tài nguyên tĩnh
│   ├── avatars/           # Avatar users
│   └── uploads/           # File upload
└── data/                  # Dữ liệu ứng dụng
    ├── users.json
    ├── posts.json
    └── users/
```

## 🔧 Cài đặt thủ công

```bash
# 1. Cài đặt Python 3.7+
# 2. Cài đặt dependencies
pip install Flask==2.3.3
pip install Flask-SocketIO==5.3.6
pip install Werkzeug==2.3.7

# 3. Tạo thư mục static
mkdir static
mkdir static/avatars
mkdir static/uploads

# 4. Copy dữ liệu
cp data/avatars/* static/avatars/ 2>/dev/null || true

# 5. Chạy ứng dụng
python mobile_app.py
```

## 🌐 Port và Network

- **Port mặc định**: 5000
- **Host**: 0.0.0.0 (cho phép truy cập từ mạng)
- **Protocol**: HTTP
- **CORS**: Cho phép tất cả origin

## 🔒 Bảo mật

- Session-based authentication
- File upload validation
- CSRF protection (có thể thêm)
- Input sanitization

## 📊 Performance

- **Lightweight**: Chỉ sử dụng Flask cơ bản
- **Fast loading**: Bootstrap CDN
- **Optimized images**: Responsive images
- **Caching**: Browser caching

## 🐛 Troubleshooting

### Lỗi "Port 5000 đã được sử dụng"
```bash
# Tìm process sử dụng port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID [PID] /F
```

### Lỗi "Không thể kết nối"
1. Kiểm tra firewall
2. Đảm bảo cùng mạng WiFi
3. Thử IP khác (192.168.x.x)

### Lỗi "Module not found"
```bash
pip install -r requirements_mobile.txt
```

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra Python version (>= 3.7)
2. Kiểm tra network connection
3. Thử restart ứng dụng
4. Xem log lỗi trong terminal

## 🔄 Cập nhật

Để cập nhật:
1. Backup dữ liệu trong `data/`
2. Pull code mới
3. Cài đặt dependencies mới
4. Restart ứng dụng

---

**Link Space Mobile** - Kết nối mọi lúc, mọi nơi! 📱✨ 