from PyQt6.QtWidgets import QWidget, QLineEdit, QListWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
import json

class UserSearchWidget(QWidget):
    user_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm người dùng...")
        self.result_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.result_list)
        self.setLayout(layout)

        self.search_input.textChanged.connect(self.search_users)
        self.result_list.itemClicked.connect(self.emit_user_selected)

    def search_users(self, text):
        self.result_list.clear()
        if not text.strip():
            return

        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
                for user in users:
                    if text.lower() in user["username"].lower():
                        self.result_list.addItem(user["username"])
        except:
            pass

    def emit_user_selected(self, item):
        self.user_selected.emit(item.text())