from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import json
import os

class ChangePasswordDialog(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Đổi mật khẩu")
        self.setGeometry(400, 300, 350, 220)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Mật khẩu cũ:"))
        self.old_pw = QLineEdit()
        self.old_pw.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.old_pw)

        layout.addWidget(QLabel("Mật khẩu mới:"))
        self.new_pw = QLineEdit()
        self.new_pw.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_pw)

        layout.addWidget(QLabel("Xác nhận mật khẩu mới:"))
        self.confirm_pw = QLineEdit()
        self.confirm_pw.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_pw)

        btn = QPushButton("Đổi mật khẩu")
        btn.clicked.connect(self.change_password)
        layout.addWidget(btn)

        self.setLayout(layout)

    def change_password(self):
        old_pw = self.old_pw.text().strip()
        new_pw = self.new_pw.text().strip()
        confirm_pw = self.confirm_pw.text().strip()

        if not old_pw or not new_pw or not confirm_pw:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        if new_pw != confirm_pw:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu mới và xác nhận không khớp!")
            return
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            QMessageBox.critical(self, "Lỗi", "Không thể đọc dữ liệu người dùng!")
            return
        for user in users:
            if user["username"] == self.username:
                if user["password"] != old_pw:
                    QMessageBox.warning(self, "Lỗi", "Mật khẩu cũ không đúng!")
                    return
                user["password"] = new_pw
                break
        else:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy người dùng!")
            return
        try:
            with open("data/users.json", "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Thành công", "Đổi mật khẩu thành công!")
            self.accept()
        except Exception:
            QMessageBox.critical(self, "Lỗi", "Không thể lưu mật khẩu mới!") 