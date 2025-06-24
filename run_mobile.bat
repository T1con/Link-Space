@echo off
echo ========================================
echo    Link Space Mobile - Phiên bản điện thoại
echo ========================================
echo.
echo Đang khởi động ứng dụng web...
echo.

REM Kiểm tra Python có được cài đặt không
python --version >nul 2>&1
if errorlevel 1 (
    echo Lỗi: Python chưa được cài đặt hoặc không có trong PATH
    echo Vui lòng cài đặt Python từ https://python.org
    pause
    exit /b 1
)

REM Kiểm tra Flask có được cài đặt không
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Đang cài đặt Flask và các thư viện cần thiết...
    pip install -r requirements_mobile.txt
    if errorlevel 1 (
        echo Lỗi: Không thể cài đặt Flask
        pause
        exit /b 1
    )
)

REM Tạo thư mục static nếu chưa có
if not exist "static" mkdir static
if not exist "static\avatars" mkdir static\avatars
if not exist "static\uploads" mkdir static\uploads

REM Copy dữ liệu avatar nếu có
if exist "data\avatars" (
    echo Đang copy avatar...
    xcopy "data\avatars\*" "static\avatars\" /Y /Q
)

REM Copy dữ liệu upload nếu có
if exist "data\uploads" (
    echo Đang copy uploads...
    xcopy "data\uploads\*" "static\uploads\" /Y /Q
)

echo.
echo 🌐 Link Space Mobile đang khởi động...
echo 📱 Truy cập: http://localhost:5000
echo 📱 Hoặc: http://[IP_MÁY_TÍNH]:5000 (để truy cập từ điện thoại)
echo.
echo 💡 Hướng dẫn truy cập từ điện thoại:
echo 1. Đảm bảo điện thoại và máy tính cùng mạng WiFi
echo 2. Tìm IP máy tính bằng lệnh: ipconfig
echo 3. Mở trình duyệt điện thoại và truy cập: http://[IP]:5000
echo.
echo 🔄 Nhấn Ctrl+C để dừng
echo.

REM Chạy ứng dụng
python mobile_app.py

REM Nếu có lỗi, hiển thị thông báo
if errorlevel 1 (
    echo.
    echo Có lỗi xảy ra khi chạy ứng dụng!
    echo Vui lòng kiểm tra lại cài đặt Python và Flask
    pause
) 