#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Space - Ứng dụng mạng xã hội
File chạy chính của ứng dụng
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

# Thêm thư mục src vào path để import các module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.LoginWindow import LoginWindow

def main():
    """Hàm chính để khởi chạy ứng dụng"""
    
    # Tạo ứng dụng Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Link Space")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Link Space Team")
    
    # Thiết lập style và font mặc định
    app.setStyle('Fusion')
    
    # Tải file style nếu có
    style_file = os.path.join('src', 'style.qss')
    if os.path.exists(style_file):
        try:
            with open(style_file, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Không thể tải file style: {e}")
    
    # Tạo và hiển thị cửa sổ đăng nhập
    login_window = LoginWindow()
    login_window.show()
    
    # Chạy ứng dụng
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 