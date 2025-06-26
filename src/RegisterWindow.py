import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFrame, QApplication, QComboBox
from PyQt6.QtCore import Qt
import json
import uuid
from utils import center_window
import os
import werkzeug.security

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng ký Tài khoản")
        # Đặt kích thước tương tự như LoginWindow để có giao diện nhất quán
        self.setGeometry(200, 200, 500, 600) 
        self.setFixedSize(self.width(), self.height()) # Không cho resize
        center_window(self)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Title Label
        title_label = QLabel("ĐĂNG KÝ TÀI KHOẢN MỚI")
        title_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #FF1493;
            margin-bottom: 10px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # ---
        input_frame = QFrame(self)
        input_frame_layout = QVBoxLayout()
        input_frame_layout.setContentsMargins(30, 30, 30, 30)
        input_frame_layout.setSpacing(15)

        self.label_user = QLabel("Tên người dùng:")
        self.label_user.setStyleSheet("font-size: 16px; color: #34495e; border: none; font-family: 'Segoe UI', Arial, sans-serif;")
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Nhập tên người dùng bạn muốn")
        self.input_user.setStyleSheet("""
            padding: 12px; 
            border: 1px solid #bdc3c7;
            color: #CD5C5C; 
            border-radius: 8px;
            font-size: 15px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        self.label_pass = QLabel("Mật khẩu:")
        self.label_pass.setStyleSheet("font-size: 16px; color: #34495e; border: none; font-family: 'Segoe UI', Arial, sans-serif;")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setPlaceholderText("Nhập mật khẩu của bạn")
        self.input_pass.setStyleSheet("""
            padding: 12px; 
            border: 1px solid #bdc3c7;
            color: #CD5C5C;
            border-radius: 8px; 
            font-size: 15px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        # Thêm trường ngày sinh
        self.label_birthday = QLabel("Ngày sinh (YYYY-MM-DD):")
        self.label_birthday.setStyleSheet("font-size: 16px; color: #34495e; border: none; font-family: 'Segoe UI', Arial, sans-serif;")
        self.input_birthday = QLineEdit()
        self.input_birthday.setPlaceholderText("VD: 2000-01-01")
        self.input_birthday.setStyleSheet("""
            padding: 12px; 
            border: 1px solid #bdc3c7;
            color: #34495e; 
            border-radius: 8px;
            font-size: 15px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)

        # Thêm trường chọn giới tính
        self.label_gender = QLabel("Giới tính:")
        self.label_gender.setStyleSheet("font-size: 16px; color: #34495e; border: none; font-family: 'Segoe UI', Arial, sans-serif;")
        self.combo_gender = QComboBox()
        self.combo_gender.addItems(["Nam", "Nữ", "Khác"])
        self.combo_gender.setStyleSheet("padding: 10px; font-size: 15px; border-radius: 8px;")

        input_frame_layout.addWidget(self.label_user)
        input_frame_layout.addWidget(self.input_user)
        input_frame_layout.addWidget(self.label_pass)
        input_frame_layout.addWidget(self.input_pass)
        input_frame_layout.addWidget(self.label_birthday)
        input_frame_layout.addWidget(self.input_birthday)
        input_frame_layout.addWidget(self.label_gender)
        input_frame_layout.addWidget(self.combo_gender)

        input_frame.setLayout(input_frame_layout)
        input_frame.setStyleSheet("""
            background-color: #ecf0f1;
            border: 1px solid #dfe6e9;
            border-radius: 15px;
        """)
        main_layout.addWidget(input_frame)

        # ---
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)

        self.btn_register = QPushButton("Đăng ký")
        self.btn_register.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 0.5px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #219d54;
            }
        """)
        self.btn_register.clicked.connect(self.register)

        # Nút quay lại màn hình đăng nhập
        self.btn_back_to_login = QPushButton("Quay lại Đăng nhập")
        self.btn_back_to_login.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 0.5px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
            QPushButton:pressed {
                background-color: #616f70;
            }
        """)
        self.btn_back_to_login.clicked.connect(self.go_to_login)

        buttons_layout.addWidget(self.btn_register)
        buttons_layout.addWidget(self.btn_back_to_login)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.input_user.returnPressed.connect(self.register)
        self.input_pass.returnPressed.connect(self.register)

    def register(self):
        id = str(uuid.uuid4())
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        birthday = self.input_birthday.text().strip()
        gender = self.combo_gender.currentText()

        if not username or not password or not birthday:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ tên người dùng, mật khẩu và ngày sinh!")
            return

        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for user_data in users:
            if user_data["username"].lower() == username.lower():
                QMessageBox.warning(self, "Lỗi", "Tên người dùng đã tồn tại. Vui lòng chọn tên khác.")
                return

        password_hash = werkzeug.security.generate_password_hash(password)
        users.append({"id": id, "username": username, "password_hash": password_hash, "birthday": birthday, "gender": gender})

        try:
            with open("data/users.json", "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            os.makedirs("data/users", exist_ok=True)
            with open(f"data/users/{username}.json", "w", encoding="utf-8") as f:
                json.dump({"bio": "", "following": [], "birthday": birthday, "gender": gender}, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.")
            self.go_to_login()
        except IOError as e:
            QMessageBox.critical(self, "Lỗi Ghi File", f"Không thể ghi dữ liệu người dùng: {e}")

    def go_to_login(self):
        # Quay lại màn hình đăng nhập
        from LoginWindow import LoginWindow 
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close() # Đóng cửa sổ đăng ký hiện tại