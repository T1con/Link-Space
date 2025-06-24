#!/bin/bash

echo "========================================"
echo "   Link Space - Ứng dụng mạng xã hội"
echo "========================================"
echo ""
echo "Đang khởi động ứng dụng..."
echo ""

# Kiểm tra Python có được cài đặt không
if ! command -v python3 &> /dev/null; then
    echo "Lỗi: Python3 chưa được cài đặt"
    echo "Vui lòng cài đặt Python từ https://python.org"
    exit 1
fi

# Kiểm tra PyQt6 có được cài đặt không
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo "Đang cài đặt PyQt6..."
    pip3 install PyQt6
    if [ $? -ne 0 ]; then
        echo "Lỗi: Không thể cài đặt PyQt6"
        exit 1
    fi
fi

# Cấp quyền thực thi cho file
chmod +x run_app.py

# Chạy ứng dụng
python3 run_app.py

# Kiểm tra lỗi
if [ $? -ne 0 ]; then
    echo ""
    echo "Có lỗi xảy ra khi chạy ứng dụng!"
    echo "Vui lòng kiểm tra lại cài đặt Python và PyQt6"
fi 