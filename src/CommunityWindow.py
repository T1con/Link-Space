from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QMessageBox, QHBoxLayout
import os
import json
import uuid

class CommunityWindow(QDialog):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Cộng đồng/Club")
        self.setGeometry(300, 200, 500, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.load_communities()
        layout.addWidget(QLabel("Danh sách cộng đồng:"))
        layout.addWidget(self.list_widget)
        btn_layout = QHBoxLayout()
        join_btn = QPushButton("Tham gia/Rời nhóm")
        join_btn.clicked.connect(self.toggle_join)
        btn_layout.addWidget(join_btn)
        open_btn = QPushButton("Xem nhóm")
        open_btn.clicked.connect(self.open_community)
        btn_layout.addWidget(open_btn)
        create_btn = QPushButton("Tạo cộng đồng mới")
        create_btn.clicked.connect(self.create_community)
        btn_layout.addWidget(create_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_communities(self):
        self.list_widget.clear()
        if not os.path.exists("data/communities.json"):
            return
        with open("data/communities.json", "r", encoding="utf-8") as f:
            communities = json.load(f)
        for c in communities:
            self.list_widget.addItem(f"{c['name']} ({c['id']})")

    def get_selected_community(self):
        sel = self.list_widget.currentItem()
        if not sel:
            return None
        cid = sel.text().split("(")[-1].replace(")", "").strip()
        with open("data/communities.json", "r", encoding="utf-8") as f:
            communities = json.load(f)
        for c in communities:
            if c["id"] == cid:
                return c
        return None

    def toggle_join(self):
        c = self.get_selected_community()
        if not c:
            QMessageBox.warning(self, "Lỗi", "Chọn một cộng đồng!")
            return
        members = c.get("members", [])
        if self.current_user in members:
            members.remove(self.current_user)
        else:
            members.append(self.current_user)
        c["members"] = members
        self.save_community(c)
        QMessageBox.information(self, "Thành công", "Đã cập nhật thành viên!")

    def open_community(self):
        c = self.get_selected_community()
        if not c:
            QMessageBox.warning(self, "Lỗi", "Chọn một cộng đồng!")
            return
        QMessageBox.information(self, c["name"], f"Mô tả: {c.get('description','') or 'Không có'}\nThành viên: {', '.join(c.get('members', []))}")

    def create_community(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Tạo cộng đồng mới")
        layout = QVBoxLayout()
        name_input = QLineEdit()
        name_input.setPlaceholderText("Tên cộng đồng")
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("Mô tả")
        layout.addWidget(QLabel("Tên cộng đồng:"))
        layout.addWidget(name_input)
        layout.addWidget(QLabel("Mô tả:"))
        layout.addWidget(desc_input)
        create_btn = QPushButton("Tạo")
        def do_create():
            name = name_input.text().strip()
            desc = desc_input.text().strip()
            if not name:
                QMessageBox.warning(dialog, "Lỗi", "Tên cộng đồng không được để trống!")
                return
            cid = str(uuid.uuid4())[:8]
            community = {"id": cid, "name": name, "description": desc, "admin": self.current_user, "members": [self.current_user]}
            if os.path.exists("data/communities.json"):
                with open("data/communities.json", "r", encoding="utf-8") as f:
                    communities = json.load(f)
            else:
                communities = []
            communities.append(community)
            with open("data/communities.json", "w", encoding="utf-8") as f:
                json.dump(communities, f, indent=4, ensure_ascii=False)
            QMessageBox.information(dialog, "Thành công", "Đã tạo cộng đồng mới!")
            dialog.accept()
            self.load_communities()
        create_btn.clicked.connect(do_create)
        layout.addWidget(create_btn)
        dialog.setLayout(layout)
        dialog.exec()

    def save_community(self, updated_community):
        if not os.path.exists("data/communities.json"):
            return
        with open("data/communities.json", "r", encoding="utf-8") as f:
            communities = json.load(f)
        for i, c in enumerate(communities):
            if c["id"] == updated_community["id"]:
                communities[i] = updated_community
                break
        with open("data/communities.json", "w", encoding="utf-8") as f:
            json.dump(communities, f, indent=4, ensure_ascii=False)
        self.load_communities()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = CommunityWindow("testuser")
    win.show()
    sys.exit(app.exec()) 