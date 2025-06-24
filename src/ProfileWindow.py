import os
import json
import shutil
from ChangePasswordDialog import ChangePasswordDialog
from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QTextEdit, QMessageBox, QScrollArea, QWidget, QInputDialog, QLineEdit, QComboBox, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QFont, QBitmap, QPainter, QBrush, QColor, QCursor, QPolygon, QPainterPath, QImage
from PyQt6.QtCore import Qt, QSize, QTimer, QPoint
from PostWidget import PostWidget
from common import add_notification, add_points_and_update_level_badge
import math

class ProfileWindow(QDialog):
    def __init__(self, current_id, current_user, target_user):
        super().__init__()
        self.current_id = current_id
        self.current_user = current_user
        self.target_user = target_user
        self.setWindowTitle(f"Hồ sơ của @{target_user}")
        self.setGeometry(300, 150, 600, 800)

        self.user_data = self.load_user_data()
        self.current_user_data = self.load_current_user_data()
        self.setup_ui()

    def load_user_data(self):
        path = f"data/users/{self.target_user}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def load_current_user_data(self):
        path = f"data/users/{self.current_user}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def setup_ui(self):
        # Tạo layout chính cho nội dung profile
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # Ảnh bìa
        cover_label = QLabel()
        cover_path = f"data/covers/{self.target_user}.jpg"
        if os.path.exists(cover_path):
            cover_pixmap = QPixmap(cover_path).scaled(600, 180, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            cover_label.setPixmap(cover_pixmap)
        else:
            cover_label.setFixedHeight(180)
            cover_label.setStyleSheet("background-color: #dfe6e9;")
        layout.addWidget(cover_label)

        # Nếu là user hiện tại, thêm nút đổi ảnh bìa
        if self.target_user == self.current_user:
            change_cover_btn = QPushButton("Đổi ảnh bìa")
            change_cover_btn.setToolTip("Đổi ảnh bìa cá nhân")
            change_cover_btn.clicked.connect(self.change_cover)
            layout.addWidget(change_cover_btn)

        avatar = QLabel()
        avatar_path = f"data/avatars/{self.target_user}.png"
        badges = self.user_data.get("badges", [])
        points = self.user_data.get("points", 0)
        self._avatar_pixmap = None
        self._avatar_timer = None
        # --- Rank mới ---
        # Hiệu ứng đặc biệt cho T1con - CHỦ NHÂN
        if self.target_user == "T1con" and "Chủ Nhân" in badges:
            # Avatar đứng im, thêm vương miện phía trên, hiệu ứng lửa động xung quanh (không che avatar)
            if os.path.exists(avatar_path):
                pixmap_raw = QPixmap(avatar_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                # Chuyển sang QImage để tạo alpha mask hình tròn
                image = pixmap_raw.toImage().convertToFormat(QImage.Format.Format_ARGB32)
                size = image.size()
                mask = QImage(size, QImage.Format.Format_ARGB32)
                mask.fill(Qt.GlobalColor.transparent)
                mask_painter = QPainter(mask)
                mask_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                mask_painter.setBrush(Qt.GlobalColor.white)
                mask_painter.setPen(Qt.PenStyle.NoPen)
                mask_painter.drawEllipse(0, 0, size.width(), size.height())
                mask_painter.end()
                for y in range(size.height()):
                    for x in range(size.width()):
                        if mask.pixelColor(x, y).alpha() == 0:
                            image.setPixelColor(x, y, QColor(0, 0, 0, 0))
                pixmap = QPixmap.fromImage(image)
                # Tạo canvas lớn hơn để vẽ vương miện và hiệu ứng động
                canvas = QPixmap(140, 160)
                canvas.fill(Qt.GlobalColor.transparent)
                self._avatar_effect_angle = 0
                def update_effect():
                    temp_canvas = QPixmap(canvas)
                    temp_canvas.fill(Qt.GlobalColor.transparent)
                    painter = QPainter(temp_canvas)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    # Vẽ avatar tròn
                    painter.drawPixmap(20, 40, pixmap)
                    # Vẽ vương miện phía trên avatar
                    crown_color = QColor(255, 215, 0)
                    painter.setBrush(QBrush(crown_color))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(50, 30, 40, 18)
                    painter.drawPolygon(QPolygon([QPoint(55, 38), QPoint(60, 20), QPoint(65, 38)]))
                    painter.drawPolygon(QPolygon([QPoint(70, 38), QPoint(70, 23), QPoint(75, 38)]))
                    painter.drawPolygon(QPolygon([QPoint(80, 38), QPoint(85, 20), QPoint(90, 38)]))
                    painter.setPen(QColor(255, 180, 0))
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    painter.drawEllipse(50, 30, 40, 18)
                    # Hiệu ứng lửa động xung quanh avatar (chỉ di chuyển vòng lửa lên trên)
                    import random
                    center_x, center_y = 70, 70  # center_y nhỏ hơn để vòng lửa lên trên
                    avatar_radius = 50  # bán kính avatar (gần đúng)
                    flame_radius = 62   # bán kính vòng lửa lớn hơn avatar
                    flame_count = 18
                    for i in range(flame_count):
                        base_angle = self._avatar_effect_angle + i * (360 // flame_count)
                        flame_rad = base_angle * math.pi / 180
                        flame_offset = 8 * math.sin((self._avatar_effect_angle + i*20) * math.pi / 180)
                        # Vị trí ngọn lửa: chỉ ngoài rìa avatar
                        x = int(center_x + (flame_radius + flame_offset) * math.cos(flame_rad) - 8)
                        y = int(center_y + (flame_radius + flame_offset) * math.sin(flame_rad) - 12)
                        # Màu lửa động: cam-đỏ-vàng, alpha nhấp nháy
                        hue = 25 + int(10 * math.sin((self._avatar_effect_angle + i*30) * math.pi / 180))
                        sat = 255
                        val = 255
                        alpha = 180 + int(60 * math.sin((self._avatar_effect_angle + i*40) * math.pi / 180))
                        color = QColor()
                        color.setHsv(hue, sat, val, max(80, min(255, alpha)))
                        painter.setBrush(QBrush(color))
                        painter.setPen(Qt.PenStyle.NoPen)
                        flame_w = 16 + int(6 * math.sin((self._avatar_effect_angle + i*15) * math.pi / 180))
                        flame_h = 22 + int(8 * math.cos((self._avatar_effect_angle + i*25) * math.pi / 180))
                        painter.drawEllipse(x, y, flame_w, flame_h)
                    painter.end()
                    avatar.setPixmap(temp_canvas)
                    self._avatar_effect_angle = (self._avatar_effect_angle + 4) % 360
                self._avatar_timer = QTimer(self)
                self._avatar_timer.timeout.connect(update_effect)
                self._avatar_timer.start(40)
                update_effect()
            else:
                pixmap = QPixmap(140, 160)
                pixmap.fill(QColor("gray"))
                avatar.setPixmap(pixmap)
        elif "Đại Cao Thủ" in badges or points >= 2000:
            # Viền tím tĩnh
            border_color = "#a259f7"
            if os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                size = pixmap.size()
                border_width = 8
                total_size = size + QSize(border_width*2, border_width*2)
                rounded = QPixmap(total_size)
                rounded.fill(Qt.GlobalColor.transparent)
                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setBrush(QBrush(QColor(border_color)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(0, 0, total_size.width(), total_size.height())
                painter.setBrush(QBrush(pixmap))
                painter.drawEllipse(border_width, border_width, size.width(), size.height())
                painter.end()
                avatar.setPixmap(rounded)
            else:
                pixmap = QPixmap(100, 100)
                pixmap.fill(QColor("gray"))
                avatar.setPixmap(pixmap)
        elif "Huyền thoại" in badges or points >= 1000:
            # Hiệu ứng phát sáng động cầu vồng
            if os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self._avatar_pixmap = pixmap
                self._avatar_hue = 0
                def update_glow():
                    border_width = 8
                    size = pixmap.size()
                    total_size = size + QSize(border_width*2, border_width*2)
                    rounded = QPixmap(total_size)
                    rounded.fill(Qt.GlobalColor.transparent)
                    painter = QPainter(rounded)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    color = QColor()
                    color.setHsv(self._avatar_hue, 255, 255)
                    painter.setBrush(QBrush(color))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(0, 0, total_size.width(), total_size.height())
                    painter.setBrush(QBrush(pixmap))
                    painter.drawEllipse(border_width, border_width, size.width(), size.height())
                    painter.end()
                    avatar.setPixmap(rounded)
                    self._avatar_hue = (self._avatar_hue + 8) % 360
                self._avatar_timer = QTimer(self)
                self._avatar_timer.timeout.connect(update_glow)
                self._avatar_timer.start(60)
                update_glow()
            else:
                pixmap = QPixmap(100, 100)
                pixmap.fill(QColor("gray"))
                avatar.setPixmap(pixmap)
        else:
            # Các rank khác: viền tĩnh như cũ
            if "Cao thủ" in badges or points >= 500:
                border_color = "#0984e3"
            elif "Người mới" in badges or points >= 100:
                border_color = "#b2bec3"
            else:
                border_color = "#dfe6e9"
            if os.path.exists(avatar_path):
                pixmap = QPixmap(avatar_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                size = pixmap.size()
                border_width = 6
                total_size = size + QSize(border_width*2, border_width*2)
                rounded = QPixmap(total_size)
                rounded.fill(Qt.GlobalColor.transparent)
                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setBrush(QBrush(QColor(border_color)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(0, 0, total_size.width(), total_size.height())
                painter.setBrush(QBrush(pixmap))
                painter.drawEllipse(border_width, border_width, size.width(), size.height())
                painter.end()
                avatar.setPixmap(rounded)
            else:
                pixmap = QPixmap(100, 100)
                pixmap.fill(QColor("gray"))
                avatar.setPixmap(pixmap)
        # Đặt avatar vào widget căn giữa tuyệt đối
        avatar_center_widget = QWidget()
        avatar_center_layout = QHBoxLayout(avatar_center_widget)
        avatar_center_layout.addStretch()
        avatar_center_layout.addWidget(avatar)
        avatar_center_layout.addStretch()
        avatar_center_layout.setContentsMargins(0, 10, 0, 10)
        layout.addWidget(avatar_center_widget)

        name_label = QLabel(f"@{self.target_user}")
        name_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Hiển thị nickname nếu có
        nickname = self.user_data.get("nickname", "")
        if nickname:
            nickname_label = QLabel(f"📝 {nickname}")
            nickname_label.setFont(QFont("Arial", 12, QFont.Weight.Normal))
            nickname_label.setStyleSheet("color: #636e72;")
            layout.addWidget(nickname_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # --- Add follower counts ---
        stats_layout = QHBoxLayout()
        followers_count = len(self.user_data.get("followers", []))
        following_count = len(self.user_data.get("following", []))
        
        followers_label = QLabel(f"{followers_count} người theo dõi")
        following_label = QLabel(f"{following_count} đang theo dõi")

        stats_layout.addWidget(followers_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        stats_layout.addStretch()
        stats_layout.addWidget(following_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(stats_layout)
        # -------------------------

        # Hiển thị bio với định dạng
        bio_label = QLabel()
        bio_label.setTextFormat(Qt.TextFormat.RichText)
        bio_label.setOpenExternalLinks(True)
        bio_html = self.format_bio(self.user_data.get("bio", "Chưa có giới thiệu."))
        bio_label.setText(bio_html)
        bio_label.setWordWrap(True)
        layout.addWidget(bio_label)

        # --- Birthday ---
        birthday = self.user_data.get("birthday", "Chưa cập nhật ngày sinh")
        birthday_label = QLabel(f"🎂 Ngày sinh: {birthday}")
        layout.addWidget(birthday_label)
        # -------------------------

        # --- Sở thích, nơi sống, idol ---
        hobbies = self.user_data.get("hobbies", "Chưa cập nhật")
        location = self.user_data.get("location", "Chưa cập nhật")
        idol = self.user_data.get("idol", "Chưa cập nhật")
        hobbies_label = QLabel(f"💡 Sở thích: {hobbies}")
        location_label = QLabel(f"🏡 Sống ở: {location}")
        idol_label = QLabel(f"⭐ Idol: {idol}")
        layout.addWidget(hobbies_label)
        layout.addWidget(location_label)
        layout.addWidget(idol_label)
        # --- Điểm, level, badge ---
        points = self.user_data.get("points", 0)
        level = self.user_data.get("level", 1)
        badges = self.user_data.get("badges", [])
        points_label = QLabel(f"🏆 Điểm: {points}")
        level_label = QLabel(f"🎯 Level: {level}")
        badges_label = QLabel(f"🎖️ Huy hiệu: {', '.join(badges) if badges else 'Chưa có'}")
        layout.addWidget(points_label)
        layout.addWidget(level_label)
        layout.addWidget(badges_label)
        # Ghi chú mức rank
        rank_note = QLabel(
            "<b>Giải thích cấp bậc:</b><br>"
            "<span style='color:#FFD700; font-weight: bold;'>👑 CHỦ NHÂN</span>: Tài khoản đặc biệt<br>"
            "<span style='color:#b2bec3'>Người mới</span>: &ge; 100 điểm<br>"
            "<span style='color:#0984e3'>Cao thủ</span>: &ge; 500 điểm<br>"
            "<span style='color:#686de0'>Huyền thoại</span>: &ge; 1000 điểm<br>"
            "<span style='color:#a259f7'>Đại Cao Thủ</span>: &ge; 2000 điểm<br>"
            "<span style='color:#e84393'>Thách Đấu</span>: &ge; 5000 điểm<br>"
        )
        rank_note.setTextFormat(Qt.TextFormat.RichText)
        rank_note.setWordWrap(True)
        layout.addWidget(rank_note)
        # -----------------------------

        # Hiển thị giới tính
        gender = self.user_data.get("gender", "Chưa cập nhật")
        gender_label = QLabel(f"👤 Giới tính: {gender}")
        layout.addWidget(gender_label)

        # Xác định rank hiện tại
        def get_rank(points, badges):
            # Rank đặc biệt cho T1con
            if self.target_user == "T1con" and "Chủ Nhân" in badges:
                return "CHỦ NHÂN"
            elif "Thách Đấu" in badges or points >= 5000:
                return "Thách Đấu"
            elif "Đại Cao Thủ" in badges or points >= 2000:
                return "Đại Cao Thủ"
            elif "Huyền thoại" in badges or points >= 1000:
                return "Huyền thoại"
            elif "Cao thủ" in badges or points >= 500:
                return "Cao thủ"
            elif "Người mới" in badges or points >= 100:
                return "Người mới"
            else:
                return "Chưa có rank"
        current_rank = get_rank(points, badges)
        
        # Hiển thị rank với màu sắc đặc biệt cho T1con
        if current_rank == "CHỦ NHÂN":
            rank_display = QLabel(f"<b>Rank hiện tại:</b> <span style='color:#FFD700; font-size: 16px; font-weight: bold;'>👑 {current_rank} 👑</span>")
        else:
            rank_display = QLabel(f"<b>Rank hiện tại:</b> <span style='color:#e84393'>{current_rank}</span>")
        rank_display.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(rank_display)

        if self.target_user == self.current_user:
            btn_layout = QHBoxLayout()

            edit_btn = QPushButton("✏️")
            edit_btn.setToolTip("Sửa hồ sơ")
            edit_btn.clicked.connect(self.edit_profile)
            btn_layout.addWidget(edit_btn)

            change_avatar_btn = QPushButton("👤")
            change_avatar_btn.setToolTip("Đổi ảnh đại diện")
            change_avatar_btn.clicked.connect(self.change_avatar)
            btn_layout.addWidget(change_avatar_btn)

            # Thêm nút đổi mật khẩu
            change_pw_btn = QPushButton("Đổi mật khẩu")
            change_pw_btn.setToolTip("Đổi mật khẩu tài khoản")
            change_pw_btn.clicked.connect(self.open_change_password_dialog)
            btn_layout.addWidget(change_pw_btn)

            # Thêm nút cửa hàng pet nếu là user hiện tại
            petshop_btn = QPushButton("🦄 Cửa hàng Pet")
            petshop_btn.setToolTip("Mua và chọn pet bằng điểm thưởng")
            petshop_btn.clicked.connect(self.open_pet_shop)
            btn_layout.addWidget(petshop_btn)

            # Thêm nút cửa hàng nhân vật nếu là user hiện tại
            charshop_btn = QPushButton("🧑‍🎤 Cửa hàng Nhân vật")
            charshop_btn.setToolTip("Mua và chọn nhân vật đại diện bằng điểm thưởng")
            charshop_btn.clicked.connect(self.open_character_shop)
            btn_layout.addWidget(charshop_btn)

            layout.addLayout(btn_layout)
        else:
            follow_btn = QPushButton()
            if self.is_following():
                follow_btn.setText("➖ Bỏ theo dõi")
                follow_btn.setToolTip("Nhấn để bỏ theo dõi người dùng này")
            else:
                follow_btn.setText("➕ Theo dõi")
                follow_btn.setToolTip("Nhấn để theo dõi người dùng này")
            follow_btn.clicked.connect(lambda: self.toggle_follow(follow_btn))
            layout.addWidget(follow_btn)

            message_btn = QPushButton("💬")
            message_btn.setToolTip(f"Nhắn tin cho @{self.target_user}")
            message_btn.clicked.connect(self.send_message)
            layout.addWidget(message_btn)

            # Nút chặn
            block_btn = QPushButton("🚫 Chặn")
            block_btn.setToolTip("Chặn người dùng này")
            block_btn.clicked.connect(self.block_user)
            layout.addWidget(block_btn)

            # Nút báo cáo
            report_btn = QPushButton("⚠️ Báo cáo")
            report_btn.setToolTip("Báo cáo người dùng này")
            report_btn.clicked.connect(self.report_user)
            layout.addWidget(report_btn)

            # --- Friend Button ---
            friend_btn = QPushButton()
            self.friend_status = self.get_friendship_status()
            
            if self.friend_status == "friends":
                friend_btn.setText("💔 Hủy kết bạn")
                friend_btn.setToolTip("Hủy kết bạn với người dùng này")
                friend_btn.clicked.connect(lambda: self.handle_friend_action("unfriend"))
            elif self.friend_status == "request_sent":
                friend_btn.setText("🚫 Hủy lời mời")
                friend_btn.setToolTip("Hủy lời mời kết bạn đã gửi")
                friend_btn.clicked.connect(lambda: self.handle_friend_action("cancel_request"))
            elif self.friend_status == "request_received":
                friend_btn.setText("❓ Phản hồi lời mời")
                friend_btn.setToolTip("Phản hồi lời mời kết bạn")
                friend_btn.clicked.connect(lambda: self.handle_friend_action("respond_request"))
            else: # "not_friends"
                friend_btn.setText("🤝 Kết bạn")
                friend_btn.setToolTip("Gửi lời mời kết bạn")
                friend_btn.clicked.connect(lambda: self.handle_friend_action("add_friend"))

            layout.addWidget(friend_btn)
            # --------------------

        # Gợi ý kết bạn thông minh (chỉ cho user hiện tại)
        if self.target_user == self.current_user:
            suggest_label = QLabel("\n🤝 Gợi ý kết bạn thông minh:")
            layout.addWidget(suggest_label)
            suggestions = self.recommend_friends()
            if suggestions:
                for username in suggestions:
                    btn = QPushButton(f"@{username}")
                    btn.setToolTip("Xem hồ sơ và gửi lời mời kết bạn")
                    btn.clicked.connect(lambda checked, u=username: self.open_user_profile(u))
                    layout.addWidget(btn)
            else:
                layout.addWidget(QLabel("Không có gợi ý nào phù hợp."))

        # Hiển thị pet chính nếu có
        main_pet = self.user_data.get("main_pet", None)
        pets = self.user_data.get("pets", [])
        if main_pet:
            pet_info = self.get_pet_info(main_pet)
            if pet_info:
                pet_img = QLabel()
                if os.path.exists(pet_info["image"]):
                    pix = QPixmap(pet_info["image"]).scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    pet_img.setPixmap(pix)
                pet_img.setToolTip(f"Pet: {pet_info['name']}")
                layout.addWidget(pet_img, alignment=Qt.AlignmentFlag.AlignHCenter)
                # Ghi chú pet
                pet_note = QLabel(f"<b>Pet chính:</b> {pet_info['name']}<br><i>Pet giúp trang cá nhân của bạn thêm sinh động!</i>")
                pet_note.setTextFormat(Qt.TextFormat.RichText)
                pet_note.setWordWrap(True)
                layout.addWidget(pet_note)
        else:
            pet_note = QLabel("<b>Pet chính:</b> Chưa chọn")
            pet_note.setTextFormat(Qt.TextFormat.RichText)
            layout.addWidget(pet_note)

        # Hiển thị nhân vật đại diện nếu có
        main_char = self.user_data.get("main_character", None)
        characters = self.user_data.get("characters", [])
        if main_char:
            char_info = self.get_character_info(main_char)
            if char_info:
                char_img = QLabel()
                if os.path.exists(char_info["image"]):
                    pix = QPixmap(char_info["image"]).scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    char_img.setPixmap(pix)
                char_img.setToolTip(f"Nhân vật: {char_info['name']}")
                layout.addWidget(char_img, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(QLabel("\nBài viết:"))

        scroll = QScrollArea()
        container = QWidget()
        self.posts_layout = QVBoxLayout()

        container.setLayout(self.posts_layout)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        layout.addWidget(scroll)

        # Cuối cùng, bọc content_widget trong QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.load_posts()

    def load_posts(self):
        self.posts_layout.setSpacing(10)
        try:
            with open("data/posts.json", "r", encoding="utf-8") as f:
                posts = json.load(f)
            for post in reversed(posts):
                if post.get("username") == self.target_user:
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
                    self.posts_layout.addWidget(widget)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải bài viết: {e}")

    def edit_profile(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Sửa hồ sơ")
        dialog.setGeometry(400, 300, 400, 450)
        layout = QVBoxLayout()
        
        # Thêm trường Nick Name
        nickname_input = QLineEdit()
        nickname_input.setPlaceholderText("Nhập nickname của bạn...")
        nickname_input.setText(self.user_data.get("nickname", ""))
        layout.addWidget(QLabel("Nick Name:"))
        layout.addWidget(nickname_input)
        
        bio_input = QTextEdit()
        bio_input.setText(self.user_data.get("bio", ""))
        layout.addWidget(QLabel("Giới thiệu:"))
        layout.addWidget(bio_input)

        birthday_input = QLineEdit()
        birthday_input.setPlaceholderText("YYYY-MM-DD")
        birthday_input.setText(self.user_data.get("birthday", ""))
        layout.addWidget(QLabel("Ngày sinh (YYYY-MM-DD):"))
        layout.addWidget(birthday_input)

        # --- Thêm trường sở thích, nơi sống (chỉ chọn), idol ---
        hobbies_input = QLineEdit()
        hobbies_input.setPlaceholderText("Ví dụ: Đọc sách, đá bóng...")
        hobbies_input.setText(self.user_data.get("hobbies", ""))
        layout.addWidget(QLabel("Sở thích:"))
        layout.addWidget(hobbies_input)

        # Danh sách tỉnh/thành phố Việt Nam
        vietnam_cities = [
            "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cần Thơ", "Cao Bằng", "Đà Nẵng", "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP Hồ Chí Minh", "Trà Vinh", "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
        ]
        location_combo = QComboBox()
        location_combo.addItem("Chọn nơi sống...")
        location_combo.addItems(vietnam_cities)
        # Nếu user đã có nơi sống, chọn sẵn
        current_location = self.user_data.get("location", "")
        if current_location in vietnam_cities:
            location_combo.setCurrentText(current_location)
        layout.addWidget(QLabel("Sống ở đâu:"))
        layout.addWidget(location_combo)

        idol_input = QLineEdit()
        idol_input.setPlaceholderText("Ví dụ: Sơn Tùng, Taylor Swift...")
        idol_input.setText(self.user_data.get("idol", ""))
        layout.addWidget(QLabel("Idol của bạn là ai:"))
        layout.addWidget(idol_input)

        # Thêm trường chọn giới tính
        gender_combo = QComboBox()
        gender_combo.addItems(["Nam", "Nữ", "Khác"])
        current_gender = self.user_data.get("gender", "")
        if current_gender in ["Nam", "Nữ", "Khác"]:
            gender_combo.setCurrentText(current_gender)
        layout.addWidget(QLabel("Giới tính:"))
        layout.addWidget(gender_combo)

        save_btn = QPushButton("Lưu")
        save_btn.clicked.connect(lambda: self.save_profile(
            nickname_input.text(), bio_input.toPlainText(), birthday_input.text(),
            hobbies_input.text(), location_combo.currentText(), idol_input.text(), gender_combo.currentText(), dialog))
        layout.addWidget(save_btn)

        dialog.setLayout(layout)
        dialog.exec()

    def save_profile(self, nickname, bio_text, birthday_text, hobbies_text, location_text, idol_text, gender_text, dialog):
        self.user_data["nickname"] = nickname.strip()
        self.user_data["bio"] = bio_text.strip()
        self.user_data["birthday"] = birthday_text.strip()
        self.user_data["hobbies"] = hobbies_text.strip()
        self.user_data["location"] = location_text.strip()
        self.user_data["idol"] = idol_text.strip()
        self.user_data["gender"] = gender_text.strip()
        os.makedirs("data/users", exist_ok=True)
        with open(f"data/users/{self.current_user}.json", "w", encoding="utf-8") as f:
            json.dump(self.user_data, f, indent=4, ensure_ascii=False)
        dialog.accept()
        self.close()
        self.__init__(self.current_id, self.current_user, self.target_user)
        self.exec()

    def change_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh đại diện", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            dest_path = f"data/avatars/{self.current_user}.png"
            shutil.copy(file_path, dest_path)
            QMessageBox.information(self, "Thành công", "Ảnh đại diện đã được cập nhật!")
            self.close()
            self.__init__(self.current_id, self.current_user, self.target_user)
            self.exec()

    def is_following(self):
        # Load current user's data to check who they are following
        path = f"data/users/{self.current_user}.json"
        if not os.path.exists(path):
            return False
        with open(path, "r", encoding="utf-8") as f:
            current_user_data = json.load(f)
        following = current_user_data.get("following", [])
        return self.target_user in following

    def toggle_follow(self, button):
        # Update current user's following list
        current_user_path = f"data/users/{self.current_user}.json"
        os.makedirs(os.path.dirname(current_user_path), exist_ok=True)
        
        current_user_data = {}
        if os.path.exists(current_user_path):
            with open(current_user_path, "r", encoding="utf-8") as f:
                current_user_data = json.load(f)
        
        following_list = current_user_data.get("following", [])

        # Update target user's followers list
        target_user_path = f"data/users/{self.target_user}.json"
        target_user_data = self.user_data # Already loaded
        followers_list = target_user_data.get("followers", [])

        if self.target_user in following_list:
            # --- Unfollow ---
            following_list.remove(self.target_user)
            if self.current_user in followers_list:
                followers_list.remove(self.current_user)
            button.setText("➕ Theo dõi")
        else:
            # --- Follow ---
            following_list.append(self.target_user)
            if self.current_user not in followers_list:
                followers_list.append(self.current_user)
            button.setText("➖ Bỏ theo dõi")
            # Gửi thông báo cho user được theo dõi
            add_notification(self.target_user, f"@{self.current_user} đã theo dõi bạn.")

        # Save current user's data
        current_user_data["following"] = following_list
        with open(current_user_path, "w", encoding="utf-8") as f:
            json.dump(current_user_data, f, indent=4, ensure_ascii=False)

        # Save target user's data
        target_user_data["followers"] = followers_list
        with open(target_user_path, "w", encoding="utf-8") as f:
            json.dump(target_user_data, f, indent=4, ensure_ascii=False)
        
        # Refresh the profile window to show updated follower count
        self.close()
        self.__init__(self.current_id, self.current_user, self.target_user)
        self.exec()

    def send_message(self):
        from MessageWindow import MessageWindow
        window = MessageWindow(self.current_id, self.current_user, self.target_user)
        window.exec()

    def get_friendship_status(self):
        # Default to empty lists if keys don't exist
        current_user_friends = self.current_user_data.get("friends", [])
        target_user_requests = self.user_data.get("friend_requests", [])
        current_user_requests = self.current_user_data.get("friend_requests", [])

        if self.target_user in current_user_friends:
            return "friends"
        elif self.current_user in target_user_requests:
            return "request_sent"
        elif self.target_user in current_user_requests:
            return "request_received"
        else:
            return "not_friends"

    def handle_friend_action(self, action):
        # Ensure lists exist before modification
        self.current_user_data.setdefault("friends", [])
        self.current_user_data.setdefault("friend_requests", [])
        self.user_data.setdefault("friends", [])
        self.user_data.setdefault("friend_requests", [])

        if action == "add_friend":
            self.user_data["friend_requests"].append(self.current_user)
            # Cộng điểm cho cả 2 user
            add_points_and_update_level_badge(self.current_user, "friend")
            add_points_and_update_level_badge(self.target_user, "friend")
        
        elif action == "cancel_request":
            if self.current_user in self.user_data["friend_requests"]:
                self.user_data["friend_requests"].remove(self.current_user)

        elif action == "unfriend":
            if self.target_user in self.current_user_data["friends"]:
                self.current_user_data["friends"].remove(self.target_user)
            if self.current_user in self.user_data["friends"]:
                self.user_data["friends"].remove(self.current_user)
        
        elif action == "respond_request":
            reply = QMessageBox.question(self, "Phản hồi lời mời", 
                                         f"Bạn có muốn chấp nhận lời mời kết bạn từ @{self.target_user} không?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                                         QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Yes:
                # Add to each other's friends lists
                self.current_user_data["friends"].append(self.target_user)
                self.user_data["friends"].append(self.current_user)
                # Remove the request from the current user's request list
                if self.target_user in self.current_user_data["friend_requests"]:
                    self.current_user_data["friend_requests"].remove(self.target_user)
            elif reply == QMessageBox.StandardButton.No:
                # Just remove the request
                if self.target_user in self.current_user_data["friend_requests"]:
                    self.current_user_data["friend_requests"].remove(self.target_user)
            else: # Cancel
                return # Do nothing

        self.save_all_user_data()
        self.refresh_window()

    def save_all_user_data(self):
        # Save current user's data
        current_user_path = f"data/users/{self.current_user}.json"
        with open(current_user_path, "w", encoding="utf-8") as f:
            json.dump(self.current_user_data, f, indent=4, ensure_ascii=False)

        # Save target user's data
        target_user_path = f"data/users/{self.target_user}.json"
        with open(target_user_path, "w", encoding="utf-8") as f:
            json.dump(self.user_data, f, indent=4, ensure_ascii=False)
            
    def refresh_window(self):
        self.close()
        self.__init__(self.current_id, self.current_user, self.target_user)
        self.exec()

    def open_change_password_dialog(self):
        dialog = ChangePasswordDialog(self.current_user)
        dialog.exec()

    def change_cover(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh bìa", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            os.makedirs("data/covers", exist_ok=True)
            dest_path = f"data/covers/{self.current_user}.jpg"
            shutil.copy(file_path, dest_path)
            QMessageBox.information(self, "Thành công", "Ảnh bìa đã được cập nhật!")
            self.close()
            self.__init__(self.current_id, self.current_user, self.target_user)
            self.exec()

    def format_bio(self, bio):
        import re
        # Đậm **text** hoặc __text__
        bio = re.sub(r"\*\*(.*?)\*\*", r"<b>\\1</b>", bio)
        bio = re.sub(r"__(.*?)__", r"<b>\\1</b>", bio)
        # Nghiêng *text* hoặc _text_
        bio = re.sub(r"\*(.*?)\*", r"<i>\\1</i>", bio)
        bio = re.sub(r"_(.*?)_", r"<i>\\1</i>", bio)
        # Liên kết [text](url)
        bio = re.sub(r"\[(.*?)\]\((https?://[^\s]+)\)", r'<a href="\\2">\\1</a>', bio)
        # Hashtag #tag
        bio = re.sub(r"#(\w+)", r'<span style="color:#2980b9">#\\1</span>', bio)
        # Tag user @username
        bio = re.sub(r"@(\w+)", r'<span style="color:#27ae60">@\\1</span>', bio)
        return bio

    def block_user(self):
        path = f"data/users/{self.current_user}.json"
        import json, os
        user_data = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
        blocked = user_data.get("blocked", [])
        if self.target_user not in blocked:
            blocked.append(self.target_user)
            user_data["blocked"] = blocked
            with open(path, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Đã chặn", f"Bạn đã chặn @{self.target_user}. Họ sẽ không thể nhắn tin cho bạn.")

    def report_user(self):
        import json, os
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        reason, ok = QInputDialog.getText(self, "Báo cáo người dùng", "Lý do báo cáo:")
        if ok and reason.strip():
            report = {
                "reporter": self.current_user,
                "target": self.target_user,
                "reason": reason.strip()
            }
            reports = []
            if os.path.exists("data/reports.json"):
                with open("data/reports.json", "r", encoding="utf-8") as f:
                    reports = json.load(f)
            reports.append(report)
            with open("data/reports.json", "w", encoding="utf-8") as f:
                json.dump(reports, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Đã báo cáo", "Cảm ơn bạn đã báo cáo. Chúng tôi sẽ xem xét trường hợp này.")

    def recommend_friends(self):
        # Gợi ý bạn bè dựa vào bạn chung, sở thích, tương tác nhắn tin
        import os
        import json
        from collections import Counter
        # Lấy danh sách user
        users = []
        if os.path.exists("data/users.json"):
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        my_data = self.current_user_data
        my_friends = set(my_data.get("friends", []))
        my_hobbies = set([h.strip().lower() for h in my_data.get("hobbies", "").split(",") if h.strip()])
        # 1. Bạn chung
        friend_scores = Counter()
        for user in users:
            uname = user["username"]
            if uname == self.current_user or uname in my_friends:
                continue
            u_friends = set(user.get("friends", []))
            chung = len(my_friends & u_friends)
            if chung > 0:
                friend_scores[uname] += chung * 3
        # 2. Sở thích giống nhau
            u_hobbies = set([h.strip().lower() for h in user.get("hobbies", "").split(",") if h.strip()])
            same_hobby = len(my_hobbies & u_hobbies)
            if same_hobby > 0:
                friend_scores[uname] += same_hobby * 2
        # 3. Tương tác nhắn tin
        msg_dir = "data/messages"
        if os.path.exists(msg_dir):
            for fname in os.listdir(msg_dir):
                if not fname.endswith(".json"): continue
                if self.current_user in fname:
                    other = fname.replace(self.current_user, "").replace("_to_", "").replace(".json", "").replace("_", "").strip()
                    if other and other != self.current_user and other not in my_friends:
                        friend_scores[other] += 1
        # Loại bỏ bạn đã là bạn bè
        for f in my_friends:
            if f in friend_scores:
                del friend_scores[f]
        # Trả về top 5 gợi ý
        return [u for u, _ in friend_scores.most_common(5)]

    def open_user_profile(self, username):
        profile = ProfileWindow(self.current_id, self.current_user, username)
        profile.exec()

    def open_pet_shop(self):
        import json
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QScrollArea, QWidget
        dialog = QDialog(self)
        dialog.setWindowTitle("Cửa hàng Pet")
        dialog.setGeometry(400, 200, 500, 600)
        vbox = QVBoxLayout(dialog)
        # Load pet list
        pets = []
        if os.path.exists("data/pets.json"):
            with open("data/pets.json", "r", encoding="utf-8") as f:
                pets = json.load(f)
        user_pets = self.user_data.get("pets", [])
        main_pet = self.user_data.get("main_pet", None)
        points = self.user_data.get("points", 0)
        # Widget chứa danh sách pet để scroll
        pet_widget = QWidget()
        pet_layout = QVBoxLayout(pet_widget)
        for pet in pets:
            hbox = QHBoxLayout()
            img = QLabel()
            img.setFixedSize(56, 56)
            img.setStyleSheet("border: 2px solid #dfe6e9; border-radius: 12px; background: #fff;")
            if os.path.exists(pet["image"]):
                pix = QPixmap(pet["image"]).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                img.setPixmap(pix)
                img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                img.setText("Không có ảnh")
                img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            hbox.addWidget(img)
            hbox.addWidget(QLabel(f"{pet['name']} ({pet['price']} điểm)"))
            if pet["id"] in user_pets:
                select_btn = QPushButton("Chọn làm pet chính" if main_pet != pet["id"] else "Đang dùng")
                select_btn.setEnabled(main_pet != pet["id"])
                select_btn.clicked.connect(lambda checked, pid=pet["id"]: self.set_main_pet(pid, dialog))
                hbox.addWidget(select_btn)
            else:
                buy_btn = QPushButton(f"Mua ({pet['price']} điểm)")
                buy_btn.setEnabled(points >= pet["price"])
                buy_btn.clicked.connect(lambda checked, pid=pet["id"], price=pet["price"]: self.buy_pet(pid, price, dialog))
                hbox.addWidget(buy_btn)
            pet_layout.addLayout(hbox)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(pet_widget)
        vbox.addWidget(scroll)
        dialog.setLayout(vbox)
        dialog.exec()

    def buy_pet(self, pet_id, price, dialog):
        if self.user_data.get("points", 0) < price:
            QMessageBox.warning(self, "Thiếu điểm", "Bạn không đủ điểm để mua pet này!")
            return
        self.user_data.setdefault("pets", []).append(pet_id)
        self.user_data["points"] -= price
        self.save_all_user_data()
        QMessageBox.information(self, "Thành công", "Đã mua pet thành công!")
        dialog.accept()
        self.refresh_window()

    def set_main_pet(self, pet_id, dialog):
        self.user_data["main_pet"] = pet_id
        self.save_all_user_data()
        QMessageBox.information(self, "Thành công", "Đã chọn pet chính!")
        dialog.accept()
        self.refresh_window()

    def get_pet_info(self, pet_id):
        if os.path.exists("data/pets.json"):
            with open("data/pets.json", "r", encoding="utf-8") as f:
                pets = json.load(f)
                for pet in pets:
                    if pet["id"] == pet_id:
                        return pet
        return None

    def open_character_shop(self):
        import json
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QSizePolicy, QScrollArea, QWidget
        from PyQt6.QtGui import QPixmap, QCursor
        from PyQt6.QtCore import Qt
        dialog = QDialog(self)
        dialog.setWindowTitle("Cửa hàng Nhân vật")
        dialog.setGeometry(400, 200, 600, 600)
        vbox = QVBoxLayout(dialog)
        # Hiển thị điểm hiện tại
        points = self.user_data.get("points", 0)
        points_label = QLabel(f"Điểm hiện tại: <b>{points}</b>")
        points_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(points_label)
        # Load character list
        chars = []
        if os.path.exists("data/characters.json"):
            with open("data/characters.json", "r", encoding="utf-8") as f:
                chars = json.load(f)
        user_chars = self.user_data.get("characters", [])
        main_char = self.user_data.get("main_character", None)
        # Lưới nhân vật trong widget riêng để scroll
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(18)
        col_count = 3
        # --- Thêm lựa chọn không trang bị nhân vật ---
        none_box = QVBoxLayout()
        none_img = QLabel()
        none_img.setFixedSize(80, 80)
        none_img.setStyleSheet("border: 4px dashed #b2bec3; border-radius: 18px; background: #f5f6fa;")
        none_img.setText("Không\ntrang bị")
        none_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        none_box.addWidget(none_img, alignment=Qt.AlignmentFlag.AlignCenter)
        none_label = QLabel("Không trang bị")
        none_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        none_box.addWidget(none_label)
        btn_none = QPushButton("Bỏ trang bị" if main_char else "Đang không dùng")
        btn_none.setEnabled(bool(main_char))
        btn_none.clicked.connect(lambda checked: self.unset_main_character(dialog))
        btn_none.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        none_box.addWidget(btn_none)
        grid.addLayout(none_box, 0, 0)
        # --- Hiển thị các nhân vật còn lại ---
        for idx, char in enumerate(chars):
            row, col = divmod(idx + 1, col_count)  # +1 vì slot 0 là 'không trang bị'
            char_box = QVBoxLayout()
            img = QLabel()
            img.setFixedSize(80, 80)
            border = "#dfe6e9"
            if char["id"] == main_char:
                border = "#00b894"
            elif char["id"] in user_chars:
                border = "#0984e3"
            if char["id"] == "char_pm":
                border = "#e84393"
                img.setStyleSheet(f"border: 4px solid {border}; border-radius: 18px; background: #fff; box-shadow: 0 0 16px #ffb6c1;")
            else:
                img.setStyleSheet(f"border: 4px solid {border}; border-radius: 18px; background: #fff;")
            if os.path.exists(char["image"]):
                pix = QPixmap(char["image"]).scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                img.setPixmap(pix)
                img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                img.setText("Không có ảnh")
                img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tooltip = f"<b>{char['name']}</b><br>Giới tính: {char.get('gender','')}<br>Giá: {char['price']} điểm"
            if char["id"] == "char_pm":
                tooltip += "<br><span style='color:#e84393'>Nhân vật đặc biệt!</span>"
            img.setToolTip(tooltip)
            char_box.addWidget(img, alignment=Qt.AlignmentFlag.AlignCenter)
            name_label = QLabel(char["name"])
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            char_box.addWidget(name_label)
            price_label = QLabel(f"{char['price']} điểm")
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            char_box.addWidget(price_label)
            if char["id"] in user_chars:
                btn = QPushButton("Chọn làm đại diện" if main_char != char["id"] else "Đang dùng")
                btn.setEnabled(main_char != char["id"])
                btn.clicked.connect(lambda checked, cid=char["id"]: self.set_main_character(cid, dialog))
            else:
                btn = QPushButton(f"Mua ({char['price']} điểm)")
                btn.setEnabled(points >= char["price"])
                btn.clicked.connect(lambda checked, cid=char["id"], price=char["price"]: self.buy_character(cid, price, dialog))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            char_box.addWidget(btn)
            grid.addLayout(char_box, row, col)
        # Bọc lưới trong QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(grid_widget)
        vbox.addWidget(scroll)
        dialog.setLayout(vbox)
        dialog.exec()

    def buy_character(self, char_id, price, dialog):
        if self.user_data.get("points", 0) < price:
            QMessageBox.warning(self, "Thiếu điểm", "Bạn không đủ điểm để mua nhân vật này!")
            return
        self.user_data.setdefault("characters", []).append(char_id)
        self.user_data["points"] -= price
        self.save_all_user_data()
        QMessageBox.information(self, "Thành công", "Đã mua nhân vật thành công!")
        dialog.accept()
        self.refresh_window()

    def set_main_character(self, char_id, dialog):
        self.user_data["main_character"] = char_id
        self.save_all_user_data()
        QMessageBox.information(self, "Thành công", "Đã chọn nhân vật đại diện!")
        dialog.accept()
        self.refresh_window()

    def get_character_info(self, char_id):
        if os.path.exists("data/characters.json"):
            with open("data/characters.json", "r", encoding="utf-8") as f:
                chars = json.load(f)
                for char in chars:
                    if char["id"] == char_id:
                        return char
        return None

    def unset_main_character(self, dialog):
        if "main_character" in self.user_data:
            del self.user_data["main_character"]
            self.save_all_user_data()
            QMessageBox.information(self, "Thành công", "Đã bỏ trang bị nhân vật!")
            dialog.accept()
            self.refresh_window()