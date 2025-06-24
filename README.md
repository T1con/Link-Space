# Link Space - Ứng dụng mạng xã hội

Ứng dụng mạng xã hội được xây dựng bằng Python và PyQt6.

## Cách chạy ứng dụng

### Windows
1. **Cách 1 (Dễ nhất)**: Double-click vào file `run_app.bat`
2. **Cách 2**: Mở Command Prompt và chạy:
   ```cmd
   python run_app.py
   ```

### Linux/Mac
1. **Cách 1**: Mở Terminal và chạy:
   ```bash
   chmod +x run_app.sh
   ./run_app.sh
   ```
2. **Cách 2**: Chạy trực tiếp:
   ```bash
   python3 run_app.py
   ```

## Yêu cầu hệ thống

- **Python 3.7+**
- **PyQt6** (sẽ tự động cài đặt nếu chưa có)

## Tài khoản mẫu

- **Username**: `T1con` | **Password**: `12345654321` (Tài khoản đặc biệt)
- **Username**: `admin` | **Password**: `1`
- **Username**: `vinh` | **Password**: `1`
- **Username**: `test` | **Password**: `1`

## Tính năng chính

- ✅ Đăng nhập/Đăng ký tài khoản
- ✅ Đăng bài với hình ảnh/video
- ✅ Xem trang cá nhân
- ✅ Chỉnh sửa thông tin cá nhân
- ✅ Hệ thống điểm và level
- ✅ Huy hiệu và rank
- ✅ Pet và nhân vật đại diện
- ✅ Tin nhắn và nhóm chat
- ✅ Cộng đồng/Club
- ✅ Tìm kiếm người dùng
- ✅ Theo dõi và kết bạn
- ✅ Nickname tùy chỉnh

## Cấu trúc thư mục

```
Link Space/
├── run_app.py          # File chạy chính
├── run_app.bat         # Script chạy cho Windows
├── run_app.sh          # Script chạy cho Linux/Mac
├── src/                # Mã nguồn chính
│   ├── LoginWindow.py
│   ├── MainWindow.py
│   ├── ProfileWindow.py
│   └── ...
└── data/               # Dữ liệu ứng dụng
    ├── users/          # Thông tin người dùng
    ├── posts.json      # Bài đăng
    ├── messages/       # Tin nhắn
    └── ...
```

## Hỗ trợ

Nếu gặp lỗi, hãy kiểm tra:
1. Python đã được cài đặt chưa
2. PyQt6 đã được cài đặt chưa
3. Tất cả file trong thư mục có đầy đủ không

## Phiên bản

- **Version**: 1.0
- **Ngày cập nhật**: 2025 