# Hướng dẫn cài đặt Python và khởi động Link Space Web

## Bước 1: Cài đặt Python

### Cách 1: Tải từ trang chủ Python
1. Truy cập: https://www.python.org/downloads/
2. Tải phiên bản Python mới nhất (Python 3.11 hoặc 3.12)
3. Chạy file cài đặt
4. **QUAN TRỌNG**: Đánh dấu vào ô "Add Python to PATH" trong quá trình cài đặt
5. Chọn "Install Now"

### Cách 2: Cài đặt từ Microsoft Store (Windows 10/11)
1. Mở Microsoft Store
2. Tìm kiếm "Python"
3. Cài đặt "Python 3.11" hoặc "Python 3.12"

## Bước 2: Kiểm tra cài đặt

Sau khi cài đặt, mở PowerShell và chạy:
```powershell
python --version
```

Nếu hiển thị phiên bản Python, cài đặt thành công!

## Bước 3: Cài đặt thư viện cần thiết

Trong thư mục dự án, chạy:
```powershell
pip install -r requirements_mobile.txt
```

## Bước 4: Khởi động ứng dụng web

### Cách 1: Sử dụng file batch
Double-click vào file `run_mobile.bat`

### Cách 2: Chạy thủ công
```powershell
python mobile_app.py
```

## Bước 5: Truy cập ứng dụng

🌐 Link Space Mobile đang khởi động...
📱 Truy cập: http://localhost:5000
Hoặc: http://[IP_MÁY_TÍNH]:5000 (để truy cập từ điện thoại)

### Tìm IP máy tính:
```powershell
ipconfig
```
Tìm dòng "IPv4 Address" trong phần WiFi hoặc Ethernet.

## Tài khoản mặc định:
- **Username**: T1con
- **Password**: (để trống)

## Lỗi thường gặp:

### Lỗi "python không được nhận diện"
- Cài đặt lại Python và đảm bảo đánh dấu "Add Python to PATH"
- Hoặc khởi động lại máy tính

### Lỗi "ModuleNotFoundError"
- Chạy: `pip install -r requirements_mobile.txt`

### Lỗi "Port 5000 đã được sử dụng"
- Đóng các ứng dụng khác đang sử dụng port 5000
- Hoặc thay đổi port trong file `mobile_app.py`

## Hỗ trợ:
Nếu gặp vấn đề, hãy kiểm tra:
1. Python đã được cài đặt chưa
2. Các thư viện đã được cài đặt chưa
3. Port 5000 có bị chiếm không
4. Firewall có chặn không 