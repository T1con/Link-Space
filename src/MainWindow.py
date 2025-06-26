import os
import json
import shutil
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFileDialog,
    QMessageBox, QFrame
)
from PyQt6.QtGui import QPixmap, QFont, QPainter, QBrush
from PyQt6.QtCore import Qt, QDateTime

from src.PostWidget import PostWidget
from src.ProfileWindow import ProfileWindow
from src.MessageWindow import MessageWindow, GroupChatWindow
from src.common import load_posts, save_post, delete_post, add_notification, load_notifications, add_points_and_update_level_badge
from src.SettingsWindow import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self, current_id, current_user):
        super().__init__()
        self.current_id = current_id
        self.current_user = current_user
        self.setWindowTitle("Link Space - Home")
        self.setGeometry(100, 100, 1000, 700)
        self.image_path = None
        self.video_path = None
        self.init_ui()
        self.load_posts()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        self.create_story_bar()
        self.create_header()
        self.create_post_input()
        self.create_post_list()

    def create_story_bar(self):
        # Story bar layout
        self.story_layout = QHBoxLayout()
        self.story_layout.setSpacing(16)
        self.story_layout.setContentsMargins(8, 8, 8, 8)
        # Load stories
        stories = []
        if os.path.exists('data/stories.json'):
            with open('data/stories.json', 'r', encoding='utf-8') as f:
                try:
                    stories = json.load(f)
                except Exception:
                    stories = []
        # Lọc story còn hạn 24h
        from datetime import datetime, timedelta
        now = datetime.now()
        valid_stories = [s for s in stories if (now - datetime.strptime(s['timestamp'], '%Y-%m-%d %H:%M:%S')) < timedelta(hours=24)]
        # Lấy danh sách user có story
        users_with_story = list({s['username'] for s in valid_stories})
        # Thêm avatar story cho từng user
        for username in users_with_story:
            avatar_path = f"data/avatars/{username}.png"
            avatar = QLabel()
            if os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path).scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                rounded = QPixmap(pixmap.size())
                rounded.fill(Qt.GlobalColor.transparent)
                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setBrush(QBrush(pixmap))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(rounded.rect())
                painter.end()
                avatar.setPixmap(rounded)
            else:
                from PyQt6.QtGui import QColor
                pixmap = QPixmap(56, 56)
                pixmap.fill(QColor("gray"))
                avatar.setPixmap(pixmap)
            avatar.setFixedSize(56, 56)
            avatar.setCursor(Qt.CursorShape.PointingHandCursor)
            avatar.setToolTip(f"Xem story của @{username}")
            # TODO: avatar.mousePressEvent = lambda ev, u=username: self.open_story_popup(u)
            self.story_layout.addWidget(avatar)
        # Thêm avatar + nút + cho user hiện tại
        my_avatar = QWidget()
        my_layout = QVBoxLayout(my_avatar)
        my_layout.setContentsMargins(0, 0, 0, 0)
        my_layout.setSpacing(2)
        avatar_label = QLabel()
        avatar_path = f"data/avatars/{self.current_user}.png"
        if os.path.exists(avatar_path):
            pixmap = QPixmap(avatar_path).scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            rounded = QPixmap(pixmap.size())
            rounded.fill(Qt.GlobalColor.transparent)
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QBrush(pixmap))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(rounded.rect())
            painter.end()
            avatar_label.setPixmap(rounded)
        else:
            from PyQt6.QtGui import QColor
            pixmap = QPixmap(56, 56)
            pixmap.fill(QColor("gray"))
            avatar_label.setPixmap(pixmap)
        avatar_label.setFixedSize(56, 56)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        my_layout.addWidget(avatar_label)
        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(24, 24)
        plus_btn.setToolTip("Đăng story mới")
        # TODO: plus_btn.clicked.connect(self.add_story)
        my_layout.addWidget(plus_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.story_layout.addWidget(my_avatar)
        # Thêm story_layout vào main_layout
        self.main_layout.addLayout(self.story_layout)

    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(12)

        self.avatar_label = QLabel()
        avatar_path = f"data/avatars/{self.current_user}.png"
        if os.path.exists(avatar_path):
            pixmap = QPixmap(avatar_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            # --- Make avatar rounded ---
            rounded = QPixmap(pixmap.size())
            rounded.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QBrush(pixmap))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(rounded.rect())
            painter.end()

            self.avatar_label.setPixmap(rounded)
            # -------------------------
        else:
            # Fallback for missing avatar
            from PyQt6.QtGui import QColor
            pixmap = QPixmap(40, 40)
            pixmap.fill(QColor("gray"))
            self.avatar_label.setPixmap(pixmap)

        self.avatar_label.setFixedSize(40, 40)
        self.avatar_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.avatar_label.mousePressEvent = self.open_own_profile

        # Load user data to get nickname
        user_data = self.load_user_data()
        nickname = user_data.get("nickname", "")
        
        if nickname:
            username_label = QLabel(f"@{self.current_user} ({nickname})")
        else:
            username_label = QLabel(f"@{self.current_user}")
        username_label.setFont(QFont("Arial", 11))

        # Add 'Trang cá nhân' button
        profile_btn = QPushButton("👤")
        profile_btn.setToolTip("Xem trang cá nhân của bạn")
        profile_btn.setFixedSize(32, 32)
        profile_btn.clicked.connect(lambda: self.open_user_profile(self.current_user))

        # Nút cộng đồng
        community_btn = QPushButton("🌐")
        community_btn.setToolTip("Cộng đồng/Club")
        community_btn.setFixedSize(32, 32)
        community_btn.clicked.connect(self.open_community_list)

        # Nút nhóm chat
        group_btn = QPushButton("👥")
        group_btn.setToolTip("Nhóm chat")
        group_btn.setFixedSize(32, 32)
        group_btn.clicked.connect(self.open_group_list)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm người dùng...")
        self.search_input.returnPressed.connect(self.try_open_user_profile)

        msg_btn = QPushButton("💬")
        msg_btn.setFixedWidth(40)
        msg_btn.setToolTip("Tin nhắn")
        msg_btn.clicked.connect(self.open_message_window)

        # Nút cài đặt
        settings_btn = QPushButton("⚙️")
        settings_btn.setToolTip("Cài đặt giao diện")
        settings_btn.setFixedSize(32, 32)
        settings_btn.clicked.connect(self.open_settings)

        # Nút thông báo
        notif_btn = QPushButton("🔔")
        notif_btn.setToolTip("Thông báo hoạt động")
        notif_btn.setFixedSize(32, 32)
        notif_btn.clicked.connect(self.show_notifications)

        logout_btn = QPushButton("🚪")
        logout_btn.setToolTip("Đăng xuất")
        logout_btn.clicked.connect(self.logout)

        header.addWidget(self.avatar_label)
        header.addWidget(username_label)
        header.addWidget(profile_btn)
        header.addWidget(community_btn)
        header.addWidget(group_btn)
        header.addStretch()
        header.addWidget(self.search_input)
        header.addWidget(msg_btn)
        header.addWidget(settings_btn)
        header.addWidget(notif_btn)
        header.addWidget(logout_btn)

        self.main_layout.addLayout(header)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(line)

    def create_post_input(self):
        layout = QHBoxLayout()

        self.post_input = QLineEdit()
        self.post_input.setPlaceholderText("Bạn đang nghĩ gì?")

        img_btn = QPushButton("🖼")
        img_btn.setToolTip("Thêm ảnh")
        img_btn.clicked.connect(self.choose_image)
        video_btn = QPushButton("🎥")
        video_btn.setToolTip("Thêm video")
        video_btn.clicked.connect(self.choose_video)
        post_btn = QPushButton("➕")
        post_btn.setToolTip("Đăng bài")
        post_btn.clicked.connect(self.create_post)

        layout.addWidget(self.post_input)
        layout.addWidget(img_btn)
        layout.addWidget(video_btn)
        layout.addWidget(post_btn)

        self.main_layout.addLayout(layout)

    def create_post_list(self):
        self.posts_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container.setLayout(self.posts_layout)
        scroll_area.setWidget(container)

        self.main_layout.addWidget(scroll_area)

    def load_posts(self):
        # Clear existing posts
        while self.posts_layout.count():
            item = self.posts_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        all_posts = load_posts()
        # Hiển thị tất cả bài Post cho mọi user
        for post in reversed(all_posts):
            widget = PostWidget(
                post.get("username"),
                post.get("content"),
                post.get("image_path"),
                post.get("likes", []),
                post.get("comments", []),
                post.get("timestamp"),
                post.get("video_path"),
                current_logged_in_user=self.current_user
            )
            widget.delete_post_signal.connect(lambda data=post: self.remove_post(data))
            widget.view_profile_signal.connect(self.open_user_profile)
            self.posts_layout.addWidget(widget)

    def remove_post(self, post_data):
        delete_post(post_data["username"], post_data["timestamp"])
        self.load_posts()

    def create_post(self):
        content = self.post_input.text().strip()
        if not content:
            QMessageBox.warning(self, "Lỗi", "Nội dung không được để trống.")
            return
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        image_path = ""
        video_path = ""
        if self.image_path:
            dest = os.path.join("data/images", os.path.basename(self.image_path))
            os.makedirs("data/images", exist_ok=True)
            shutil.copy(self.image_path, dest)
            image_path = dest
        if self.video_path:
            dest = os.path.join("data/videos", os.path.basename(self.video_path))
            os.makedirs("data/videos", exist_ok=True)
            shutil.copy(self.video_path, dest)
            video_path = dest
        post = {
            "username": self.current_user,
            "content": content,
            "image_path": image_path,
            "video_path": video_path,
            "likes": [],
            "comments": [],
            "timestamp": timestamp
        }
        save_post(post)
        add_points_and_update_level_badge(self.current_user, "post")
        self.post_input.clear()
        self.image_path = None
        self.video_path = None
        self.load_posts()
        # Gửi thông báo cho follower
        user_data_path = f"data/users/{self.current_user}.json"
        if os.path.exists(user_data_path):
            with open(user_data_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
                followers = user_data.get("followers", [])
                for follower in followers:
                    add_notification(follower, f"@{self.current_user} vừa đăng một bài viết mới.")

    def choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path

    def choose_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn video", "", "Videos (*.mp4 *.avi *.mov)")
        if file_path:
            self.video_path = file_path

    def open_own_profile(self, ev):
        self.open_user_profile(self.current_user)

    def open_user_profile(self, username):
        profile = ProfileWindow(self.current_id, self.current_user, username)
        profile.exec()

    def logout(self):
        self.close()

    def try_open_user_profile(self):
        username = self.search_input.text().strip().lstrip("@")
        if username:
            self.open_user_profile(username)

    def open_message_window(self):
        window = MessageWindow(self.current_id, self.current_user, None)
        window.exec()

    def open_settings(self):
        settings = SettingsWindow(self.current_user)
        settings.exec()

    def show_notifications(self):
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget
        dialog = QDialog(self)
        dialog.setWindowTitle("Thông báo hoạt động")
        dialog.setGeometry(500, 200, 400, 500)
        layout = QVBoxLayout()
        notifications = load_notifications(self.current_user)
        if not notifications:
            layout.addWidget(QLabel("Không có thông báo nào."))
        else:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            container = QWidget()
            vbox = QVBoxLayout(container)
            for notif in reversed(notifications[-50:]):
                lbl = QLabel(f"{notif['message']}<br><span style='color:gray;font-size:10px'>{notif['timestamp']}</span>")
                lbl.setTextFormat(Qt.TextFormat.RichText)
                vbox.addWidget(lbl)
            scroll.setWidget(container)
            layout.addWidget(scroll)
        dialog.setLayout(layout)
        dialog.exec()

    def open_group_list(self):
        MessageWindow.open_group_list(self.current_user)

    def open_community_list(self):
        from CommunityWindow import CommunityWindow
        dialog = CommunityWindow(self.current_user)
        dialog.exec()

    def load_user_data(self):
        """Load current user data from JSON file"""
        path = f"data/users/{self.current_user}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}