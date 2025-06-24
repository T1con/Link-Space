@echo off
echo ========================================
echo    Link Space - Ứng dụng mạng xã hội
echo ========================================
echo.
echo Đang khởi động ứng dụng...
echo.

REM Kiểm tra Python có được cài đặt không
python --version >nul 2>&1
if errorlevel 1 (
    echo Lỗi: Python chưa được cài đặt hoặc không có trong PATH
    echo Vui lòng cài đặt Python từ https://python.org
    pause
    exit /b 1
)

REM Kiểm tra PyQt6 có được cài đặt không
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo Đang cài đặt PyQt6...
    pip install PyQt6
    if errorlevel 1 (
        echo Lỗi: Không thể cài đặt PyQt6
        pause
        exit /b 1
    )
)

REM Chạy ứng dụng
python run_app.py

REM Nếu có lỗi, hiển thị thông báo
if errorlevel 1 (
    echo.
    echo Có lỗi xảy ra khi chạy ứng dụng!
    echo Vui lòng kiểm tra lại cài đặt Python và PyQt6
    pause
) 