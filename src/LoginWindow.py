import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from RegisterWindow import RegisterWindow
from MainWindow import MainWindow
from utils import center_window

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập")
        self.setGeometry(200, 200, 500, 600)
        self.setFixedSize(self.width(), self.height())
        center_window(self)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        title = QLabel("🌟 Link Space - Đăng nhập")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form_frame = QFrame()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên người dùng")
        self.username_input.setStyleSheet("padding: 12px; font-size: 14px; border-radius: 8px;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 12px; font-size: 14px; border-radius: 8px;")

        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)

        self.login_btn = QPushButton("Đăng nhập")
        self.login_btn.clicked.connect(self.login)
        self.login_btn.setStyleSheet("padding: 12px; background-color: #27ae60; color: white; font-weight: bold;")
        layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Bạn chưa có tài khoản? Đăng ký")
        self.register_btn.clicked.connect(self.open_register)
        self.register_btn.setStyleSheet("background-color: transparent; color: #2980b9;")
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

        self.username_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for user in users:
            if user["username"] == username and user["password"] == password:
                QMessageBox.information(self, "Đăng nhập thành công", f"Chào mừng {username}!")
                self.main_window = MainWindow(current_id=user["id"], current_user=username)
                self.main_window.show()
                self.close()
                return

        QMessageBox.warning(self, "Lỗi", "Sai tên người dùng hoặc mật khẩu!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

