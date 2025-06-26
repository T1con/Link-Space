from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QMessageBox, QHBoxLayout, QTabWidget, QWidget
import os
import json
import uuid

class CommunityWindow(QDialog):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Cộng đồng/Club")
        self.setGeometry(300, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tạo tab widget để chứa các chức năng
        self.tab_widget = QTabWidget()
        
        # Tab 1: Danh sách cộng đồng
        self.community_tab = QWidget()
        self.init_community_tab()
        self.tab_widget.addTab(self.community_tab, "🏠 Cộng đồng")
        
        # Tab 2: Chủ đề thảo luận
        self.topics_tab = QWidget()
        self.init_topics_tab()
        self.tab_widget.addTab(self.topics_tab, "📝 Chủ đề")
        
        # Tab 3: Bình chọn
        self.polls_tab = QWidget()
        self.init_polls_tab()
        self.tab_widget.addTab(self.polls_tab, "📊 Bình chọn")
        
        # Tab 4: Sự kiện
        self.events_tab = QWidget()
        self.init_events_tab()
        self.tab_widget.addTab(self.events_tab, "🎉 Sự kiện")
        
        # Tab 5: Bảng xếp hạng
        self.leaderboard_tab = QWidget()
        self.init_leaderboard_tab()
        self.tab_widget.addTab(self.leaderboard_tab, "🏆 Xếp hạng")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        # Load communities sau khi đã khởi tạo tất cả tabs
        self.load_communities_for_combo()

    def init_community_tab(self):
        """Khởi tạo tab danh sách cộng đồng"""
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
        self.community_tab.setLayout(layout)

    def init_topics_tab(self):
        """Khởi tạo tab chủ đề thảo luận"""
        layout = QVBoxLayout()
        
        # Chọn cộng đồng
        layout.addWidget(QLabel("Chọn cộng đồng để xem chủ đề:"))
        self.community_combo = QListWidget()
        layout.addWidget(self.community_combo)
        
        # Nút mở chủ đề
        topics_btn = QPushButton("📝 Mở chủ đề thảo luận")
        topics_btn.clicked.connect(self.open_topics)
        layout.addWidget(topics_btn)
        
        self.topics_tab.setLayout(layout)

    def init_polls_tab(self):
        """Khởi tạo tab bình chọn"""
        layout = QVBoxLayout()
        
        # Chọn cộng đồng
        layout.addWidget(QLabel("Chọn cộng đồng để xem bình chọn:"))
        self.polls_community_combo = QListWidget()
        layout.addWidget(self.polls_community_combo)
        
        # Nút mở bình chọn
        polls_btn = QPushButton("📊 Mở bình chọn")
        polls_btn.clicked.connect(self.open_polls)
        layout.addWidget(polls_btn)
        
        self.polls_tab.setLayout(layout)

    def init_events_tab(self):
        """Khởi tạo tab sự kiện"""
        layout = QVBoxLayout()
        
        # Chọn cộng đồng
        layout.addWidget(QLabel("Chọn cộng đồng để xem sự kiện:"))
        self.events_community_combo = QListWidget()
        layout.addWidget(self.events_community_combo)
        
        # Nút mở sự kiện
        events_btn = QPushButton("🎉 Mở sự kiện")
        events_btn.clicked.connect(self.open_events)
        layout.addWidget(events_btn)
        
        self.events_tab.setLayout(layout)

    def init_leaderboard_tab(self):
        """Khởi tạo tab bảng xếp hạng"""
        layout = QVBoxLayout()
        
        # Chọn cộng đồng
        layout.addWidget(QLabel("Chọn cộng đồng để xem bảng xếp hạng:"))
        self.leaderboard_community_combo = QListWidget()
        layout.addWidget(self.leaderboard_community_combo)
        
        # Nút mở bảng xếp hạng
        leaderboard_btn = QPushButton("🏆 Mở bảng xếp hạng")
        leaderboard_btn.clicked.connect(self.open_leaderboard)
        layout.addWidget(leaderboard_btn)
        
        self.leaderboard_tab.setLayout(layout)

    def load_communities_for_combo(self):
        """Load danh sách cộng đồng cho các combo box"""
        if not os.path.exists("data/communities.json"):
            return
        with open("data/communities.json", "r", encoding="utf-8") as f:
            communities = json.load(f)
        
        # Cập nhật tất cả combo box
        combo_widgets = [
            self.community_combo,
            self.polls_community_combo,
            self.events_community_combo,
            self.leaderboard_community_combo
        ]
        
        for combo in combo_widgets:
            combo.clear()
            for c in communities:
                combo.addItem(f"{c['name']} ({c['id']})")

    def get_selected_community_id(self, combo_widget):
        """Lấy ID cộng đồng được chọn từ combo box"""
        current_item = combo_widget.currentItem()
        if not current_item:
            return None
        cid = current_item.text().split("(")[-1].replace(")", "").strip()
        return cid

    def open_topics(self):
        """Mở dialog chủ đề thảo luận"""
        community_id = self.get_selected_community_id(self.community_combo)
        if not community_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một cộng đồng!")
            return
        
        try:
            from community_dialogs import TopicDialog
            dialog = TopicDialog(community_id, self.current_user, self)
            dialog.exec()
        except ImportError:
            QMessageBox.information(self, "Thông báo", "Chức năng chủ đề thảo luận đang được phát triển!")

    def open_polls(self):
        """Mở dialog bình chọn"""
        community_id = self.get_selected_community_id(self.polls_community_combo)
        if not community_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một cộng đồng!")
            return
        
        try:
            from community_dialogs import PollDialog
            dialog = PollDialog(community_id, self.current_user, self)
            dialog.exec()
        except ImportError:
            QMessageBox.information(self, "Thông báo", "Chức năng bình chọn đang được phát triển!")

    def open_events(self):
        """Mở dialog sự kiện"""
        community_id = self.get_selected_community_id(self.events_community_combo)
        if not community_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một cộng đồng!")
            return
        
        try:
            from community_dialogs import EventDialog
            dialog = EventDialog(community_id, self.current_user, self)
            dialog.exec()
        except ImportError:
            QMessageBox.information(self, "Thông báo", "Chức năng sự kiện đang được phát triển!")

    def open_leaderboard(self):
        """Mở dialog bảng xếp hạng"""
        community_id = self.get_selected_community_id(self.leaderboard_community_combo)
        if not community_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một cộng đồng!")
            return
        
        try:
            from community_dialogs import LeaderboardDialog
            dialog = LeaderboardDialog(community_id, self.current_user, self)
            dialog.exec()
        except ImportError:
            QMessageBox.information(self, "Thông báo", "Chức năng bảng xếp hạng đang được phát triển!")

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
            self.load_communities_for_combo()
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
        self.load_communities_for_combo()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = CommunityWindow("testuser")
    win.show()
    sys.exit(app.exec()) 