import os
import json
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QTextEdit, QDialog, QScrollArea
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal
from src.common import add_points_and_update_level_badge

class PostWidget(QWidget):
    delete_post_signal = pyqtSignal(dict)
    view_profile_signal = pyqtSignal(str)
    post_updated_signal = pyqtSignal()

    def __init__(self, username, content, image_path, likes, comments, timestamp, video_path=None, current_logged_in_user=""):
        super().__init__()
        self.username = username
        self.content = content
        self.image_path = image_path
        
        # --- Data migration for likes ---
        if isinstance(likes, int):
            # Handle old data format where likes was an integer count
            self.likers = [] 
        else:
            # New format is a list of usernames
            self.likers = likes
        # --------------------------------

        self.comments = comments
        self.timestamp = timestamp
        self.video_path = video_path
        self.current_logged_in_user = current_logged_in_user
        
        self.is_liked_by_user = self.current_logged_in_user in self.likers

        # --- Thêm viewed_by ---
        self.viewed_by = self.load_viewed_by()
        self.mark_as_viewed()

        self.init_ui()
        self.setObjectName("PostWidget")

    def init_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        
        # Load user data to get nickname
        user_data = self.load_user_data()
        nickname = user_data.get("nickname", "")
        
        if nickname:
            user_label = QLabel(f"@{self.username} ({nickname})")
        else:
            user_label = QLabel(f"@{self.username}")
        
        user_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        user_label.setCursor(Qt.CursorShape.PointingHandCursor)
        user_label.mousePressEvent = self.open_profile
        top_layout.addWidget(user_label)

        # Add 'Xem hồ sơ' button
        view_btn = QPushButton("👁️")
        view_btn.setToolTip("Xem hồ sơ người dùng này")
        view_btn.setFixedSize(28, 28)
        view_btn.clicked.connect(lambda: self.view_profile_signal.emit(self.username))
        top_layout.addWidget(view_btn)

        top_layout.addStretch()

        time_label = QLabel(self.timestamp)
        time_label.setFont(QFont("Arial", 8))
        top_layout.addWidget(time_label)

        layout.addLayout(top_layout)

        content_label = QLabel(self.content)
        content_label.setWordWrap(True)
        layout.addWidget(content_label)

        if self.image_path and os.path.exists(self.image_path):
            image_label = QLabel()
            pixmap = QPixmap(self.image_path).scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)

        # Hiển thị video nếu có
        if self.video_path and os.path.exists(self.video_path):
            video_label = QLabel(f"🎥 Video: {os.path.basename(self.video_path)}")
            layout.addWidget(video_label)
            play_btn = QPushButton("Phát video")
            play_btn.clicked.connect(self.play_video)
            layout.addWidget(play_btn)

        layout.addWidget(self.create_action_bar())
        # Nút yêu thích
        fav_btn = QPushButton()
        fav_btn.setText("⭐" if self.is_favorited() else "☆")
        fav_btn.setToolTip("Đánh dấu yêu thích bài viết này")
        fav_btn.clicked.connect(self.toggle_favorite)
        layout.addWidget(fav_btn)
        self.fav_btn = fav_btn
        self.setLayout(layout)

    def create_action_bar(self):
        bar = QHBoxLayout()

        self.like_btn = QPushButton()
        self.update_like_button()
        self.like_btn.clicked.connect(self.toggle_like)

        self.comment_btn = QPushButton(f"✉ {len(self.comments)}")
        self.comment_btn.clicked.connect(self.comment_popup)

        # --- Nút xem ai đã xem ---
        view_btn = QPushButton(f"👁️ Ai đã xem ({len(self.viewed_by)})")
        view_btn.setToolTip("Xem danh sách người đã xem bài viết này")
        view_btn.clicked.connect(self.show_viewed_by)
        bar.addWidget(view_btn)
        # ------------------------

        bar.addStretch()

        if self.username == self.current_logged_in_user:
            del_btn = QPushButton("❌")
            del_btn.setToolTip("Xóa bài viết")
            del_btn.clicked.connect(self.confirm_delete)
            bar.addWidget(del_btn)

        container = QWidget()
        container.setLayout(bar)
        return container

    def toggle_like(self):
        if self.is_liked_by_user:
            self.likers.remove(self.current_logged_in_user)
            self.is_liked_by_user = False
        else:
            self.likers.append(self.current_logged_in_user)
            self.is_liked_by_user = True
        
        self.update_like_button()
        self.save_likes()

    def update_like_button(self):
        likes_count = len(self.likers)
        if self.is_liked_by_user:
            self.like_btn.setText(f"❤️ {likes_count}")
            self.like_btn.setToolTip("Bạn đã thích bài viết này. Nhấn để bỏ thích.")
        else:
            self.like_btn.setText(f"🤍 {likes_count}")
            self.like_btn.setToolTip("Thích bài viết này.")

    def save_likes(self):
        posts_file = "data/posts.json"
        try:
            with open(posts_file, "r+", encoding="utf-8") as f:
                posts = json.load(f)
                for p in posts:
                    if p["username"] == self.username and p["timestamp"] == self.timestamp:
                        p["likes"] = self.likers
                        break
                f.seek(0)
                json.dump(posts, f, indent=4, ensure_ascii=False)
                f.truncate()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu lượt thích: {e}")

    def comment_popup(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bình luận")
        dialog.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(dialog)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        comments_widget = QWidget()
        comments_layout = QVBoxLayout(comments_widget)

        for comment in self.comments:
            lbl = QLabel(comment)
            lbl.setWordWrap(True)
            comments_layout.addWidget(lbl)

        scroll.setWidget(comments_widget)
        layout.addWidget(scroll)

        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText("Nhập bình luận...")
        layout.addWidget(self.comment_input)

        post_btn = QPushButton("Đăng bình luận")
        post_btn.clicked.connect(lambda: self.add_comment(dialog))
        layout.addWidget(post_btn)

        dialog.exec()

    def add_comment(self, dialog):
        comment = self.comment_input.toPlainText().strip()
        if comment:
            self.comments.append(comment)
            self.comment_btn.setText(f"✉ {len(self.comments)}")
            self.save_comments()
            if self.current_logged_in_user:
                add_points_and_update_level_badge(self.current_logged_in_user, "comment")
            dialog.accept()
            QMessageBox.information(self, "Thành công", "Đã thêm bình luận!")

    def save_comments(self):
        posts_file = "data/posts.json"
        try:
            with open(posts_file, "r+", encoding="utf-8") as f:
                posts = json.load(f)
                for p in posts:
                    if p["username"] == self.username and p["timestamp"] == self.timestamp:
                        p["comments"] = self.comments
                        break
                f.seek(0)
                json.dump(posts, f, indent=4, ensure_ascii=False)
                f.truncate()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu bình luận: {e}")

    def confirm_delete(self):
        result = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa bài viết này không?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            self.delete_post_signal.emit({"username": self.username, "timestamp": self.timestamp})

    def open_profile(self, ev):
        self.view_profile_signal.emit(self.username)

    def play_video(self):
        import subprocess
        import sys
        if not self.video_path:
            return
        video_path = str(self.video_path)
        if sys.platform.startswith('win'):
            os.startfile(video_path)
        elif sys.platform.startswith('darwin'):
            subprocess.call(['open', video_path])
        else:
            subprocess.call(['xdg-open', video_path])

    def is_favorited(self):
        import os, json
        if not self.current_logged_in_user:
            return False
        path = f"data/users/{self.current_logged_in_user}.json"
        if not os.path.exists(path):
            return False
        with open(path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
        favs = user_data.get("favorites", [])
        return any(p.get("username") == self.username and p.get("timestamp") == self.timestamp for p in favs)

    def toggle_favorite(self):
        import os, json
        if not self.current_logged_in_user:
            return
        path = f"data/users/{self.current_logged_in_user}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
        else:
            user_data = {}
        favs = user_data.get("favorites", [])
        key = {"username": self.username, "timestamp": self.timestamp}
        if self.is_favorited():
            favs = [p for p in favs if not (p["username"] == self.username and p["timestamp"] == self.timestamp)]
        else:
            favs.append(key)
        user_data["favorites"] = favs
        with open(path, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
        self.fav_btn.setText("⭐" if self.is_favorited() else "☆")

    def load_viewed_by(self):
        posts_file = "data/posts.json"
        try:
            with open(posts_file, "r", encoding="utf-8") as f:
                posts = json.load(f)
                for p in posts:
                    if p["username"] == self.username and p["timestamp"] == self.timestamp:
                        return p.get("viewed_by", [])
        except Exception:
            pass
        return []

    def mark_as_viewed(self):
        if not self.current_logged_in_user or self.current_logged_in_user in self.viewed_by:
            return
        self.viewed_by.append(self.current_logged_in_user)
        posts_file = "data/posts.json"
        try:
            with open(posts_file, "r+", encoding="utf-8") as f:
                posts = json.load(f)
                for p in posts:
                    if p["username"] == self.username and p["timestamp"] == self.timestamp:
                        p["viewed_by"] = self.viewed_by
                        break
                f.seek(0)
                json.dump(posts, f, indent=4, ensure_ascii=False)
                f.truncate()
        except Exception:
            pass

    def show_viewed_by(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ai đã xem bài viết này")
        dialog.setGeometry(400, 300, 300, 400)
        layout = QVBoxLayout(dialog)
        if not self.viewed_by:
            layout.addWidget(QLabel("Chưa ai xem bài viết này."))
        else:
            for user in self.viewed_by:
                layout.addWidget(QLabel(f"@{user}"))
        dialog.setLayout(layout)
        dialog.exec()

    def load_user_data(self):
        """Load user data from JSON file"""
        path = f"data/users/{self.username}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}