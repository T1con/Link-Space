import os
import json
from ChangePasswordDialog import ChangePasswordDialog
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFileDialog
from common import backup_data, restore_data

class SettingsWindow(QDialog):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Cài đặt giao diện")
        self.setGeometry(400, 300, 350, 180)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chọn giao diện (theme):"))

        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Tối (Dark)", "dark")
        self.theme_combo.addItem("Sáng (Light)", "light")
        layout.addWidget(self.theme_combo)

        # Load current theme
        user_path = f"data/users/{self.current_user}.json"
        if os.path.exists(user_path):
            with open(user_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
            theme = user_data.get("theme", "dark")
            idx = 0 if theme == "dark" else 1
            self.theme_combo.setCurrentIndex(idx)

        save_btn = QPushButton("Lưu")
        save_btn.clicked.connect(self.save_theme)
        layout.addWidget(save_btn)

        # Thêm nút đổi mật khẩu
        change_pw_btn = QPushButton("Đổi mật khẩu")
        change_pw_btn.clicked.connect(self.open_change_password_dialog)
        layout.addWidget(change_pw_btn)

        # Thêm nút sao lưu và khôi phục dữ liệu
        backup_btn = QPushButton("Sao lưu dữ liệu")
        backup_btn.clicked.connect(self.backup_data)
        layout.addWidget(backup_btn)
        restore_btn = QPushButton("Khôi phục dữ liệu")
        restore_btn.clicked.connect(self.restore_data)
        layout.addWidget(restore_btn)

        self.setLayout(layout)

    def save_theme(self):
        theme = self.theme_combo.currentData()
        user_path = f"data/users/{self.current_user}.json"
        if os.path.exists(user_path):
            with open(user_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
        else:
            user_data = {}
        user_data["theme"] = theme
        with open(user_path, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
        QMessageBox.information(self, "Thành công", "Đã lưu giao diện! Hãy đăng nhập lại để áp dụng theme mới.")
        self.accept()

    def open_change_password_dialog(self):
        dialog = ChangePasswordDialog(self.current_user)
        dialog.exec()

    def backup_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Chọn nơi lưu file backup", "backup.zip", "Zip Files (*.zip)")
        if file_path:
            try:
                backup_data(file_path)
                QMessageBox.information(self, "Thành công", f"Đã sao lưu dữ liệu vào {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Sao lưu thất bại: {e}")

    def restore_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file backup để khôi phục", "", "Zip Files (*.zip)")
        if file_path:
            try:
                restore_data(file_path)
                QMessageBox.information(self, "Thành công", "Đã khôi phục dữ liệu thành công! Hãy đăng nhập lại để cập nhật.")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Khôi phục thất bại: {e}") 