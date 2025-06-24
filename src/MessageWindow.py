import os
import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton,
    QListWidget, QListWidgetItem, QHBoxLayout,
    QFileDialog, QLabel, QScrollArea, QWidget, QGridLayout, QMessageBox, QLineEdit, QComboBox
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QDateTime
from PyQt6 import QtCore
import tempfile
import threading
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import emoji


class MessageWindow(QDialog):
    def __init__(self, current_id, current_user, receiver=None):
        super().__init__()
        self.current_id = current_id
        self.current_user = current_user
        self.receiver = receiver
        self.setWindowTitle(f"Nhắn tin với @{self.receiver}" if receiver else "Tin nhắn")
        self.setGeometry(150, 150, 500, 600)
        self.messages_file = f"data/messages/{self.current_user}_to_{self.receiver}.json"
        self.init_ui()
        self.load_messages()

    def init_ui(self):
        layout = QVBoxLayout()

        self.chat_list = QListWidget()
        layout.addWidget(self.chat_list)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Nhập tin nhắn, emoji, sticker...")
        self.message_input.setFixedHeight(80)

        send_btn = QPushButton("➤")
        send_btn.setToolTip("Gửi tin nhắn")
        send_btn.clicked.connect(self.send_message)

        emoji_btn = QPushButton("😊")
        emoji_btn.setToolTip("Chèn emoji")
        emoji_btn.clicked.connect(self.insert_emoji)

        sticker_btn = QPushButton("🧩")
        sticker_btn.setToolTip("Gửi sticker")
        sticker_btn.clicked.connect(self.choose_sticker)

        image_btn = QPushButton("🖼")
        image_btn.setToolTip("Gửi ảnh")
        image_btn.clicked.connect(self.send_image)

        video_btn = QPushButton("🎥")
        video_btn.setToolTip("Gửi video")
        video_btn.clicked.connect(self.send_video)

        audio_btn = QPushButton("🎤")
        audio_btn.setToolTip("Ghi âm và gửi giọng nói")
        audio_btn.clicked.connect(self.record_audio)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(emoji_btn)
        btn_layout.addWidget(sticker_btn)
        btn_layout.addWidget(image_btn)
        btn_layout.addWidget(video_btn)
        btn_layout.addWidget(audio_btn)
        btn_layout.addWidget(send_btn)

        layout.addWidget(self.message_input)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.message_input.textChanged.connect(self.emoji_autoreplace)

    def insert_emoji(self):
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QComboBox
        import emoji
        dialog = QDialog(self)
        dialog.setWindowTitle("Chọn emoji nâng cao")
        dialog.setGeometry(400, 300, 400, 500)
        layout = QVBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Tìm emoji theo tên...")
        layout.addWidget(search_input)
        group_combo = QComboBox()
        group_combo.addItem("Tất cả", None)
        # Lấy danh sách emoji và nhóm
        all_emojis = []
        emoji_groups = {}
        for shortcode in emoji.EMOJI_DATA:
            em = emoji.emojize(shortcode, language='alias')
            group = emoji.EMOJI_DATA[shortcode].get("group", "Other")
            emoji_groups.setdefault(group, []).append((em, shortcode))
            all_emojis.append((em, shortcode, group))
        for group in emoji_groups:
            group_combo.addItem(group, group)
        layout.addWidget(group_combo)
        emoji_list = QListWidget()
        def update_emoji_list():
            text = search_input.text().lower().strip()
            group = group_combo.currentData()
            emoji_list.clear()
            for em, shortcode, g in all_emojis:
                if (not group or g == group) and (text in shortcode.lower() or text in g.lower()):
                    item = QListWidgetItem(f"{em}  {shortcode}")
                    emoji_list.addItem(item)
        search_input.textChanged.connect(update_emoji_list)
        group_combo.currentIndexChanged.connect(update_emoji_list)
        update_emoji_list()
        layout.addWidget(emoji_list)
        def insert_selected():
            selected = emoji_list.selectedItems()
            if selected:
                for item in selected:
                    em = item.text().split()[0]
                    self.message_input.insertPlainText(em)
        emoji_list.itemDoubleClicked.connect(lambda item: (self.message_input.insertPlainText(item.text().split()[0]), dialog.accept()))
        insert_btn = QPushButton("Chèn emoji đã chọn")
        insert_btn.clicked.connect(insert_selected)
        layout.addWidget(insert_btn)
        dialog.setLayout(layout)
        dialog.exec()

    def choose_sticker(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Chọn sticker")
        dialog.setGeometry(400, 300, 400, 300)
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        sticker_dir = "data/stickers"
        if not os.path.exists(sticker_dir):
            os.makedirs(sticker_dir)
        stickers = [f for f in os.listdir(sticker_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
        if not stickers:
            layout.addWidget(QLabel("Chưa có sticker nào. Hãy thêm file vào data/stickers!"))
        else:
            for idx, sticker in enumerate(stickers):
                btn = QPushButton()
                btn.setIcon(QIcon(os.path.join(sticker_dir, sticker)))
                btn.setIconSize(QtCore.QSize(64, 64))
                btn.setFixedSize(72, 72)
                btn.setToolTip(sticker)
                btn.clicked.connect(lambda checked, s=sticker: self.choose_sticker_file(dialog, os.path.join(sticker_dir, s)))
                grid.addWidget(btn, idx // 5, idx % 5)
            scroll.setWidget(container)
            layout.addWidget(scroll)
        dialog.setLayout(layout)
        dialog.exec()

    def choose_sticker_file(self, dialog, file_path):
        self.display_message(file_path, msg_type="sticker")
        self.save_message(file_path, msg_type="sticker")
        dialog.accept()

    def send_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.display_message(file_path, msg_type="image")
            self.save_message(file_path, msg_type="image")

    def send_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn video", "", "Videos (*.mp4 *.avi *.mov)")
        if file_path:
            self.display_message(file_path, msg_type="video")
            self.save_message(file_path, msg_type="video")

    def send_message(self):
        content = self.message_input.toPlainText().strip()
        if content:
            self.display_message(content, msg_type="text")
            self.save_message(content, msg_type="text")
            self.message_input.clear()
            # Chatbot AI trả lời nếu receiver là 'gptbot'
            if self.receiver == "gptbot":
                reply = self.get_bot_reply(content)
                self.display_message(reply, msg_type="text", sender="gptbot")
                self.save_message(reply, msg_type="text")

    def get_bot_reply(self, user_message):
        # Nếu có OpenAI API key thì dùng GPT, nếu không thì hardcode logic
        import os
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_message}]
                )
                content = response.choices[0].message.content
                if content:
                    return content.strip()
                return "[GPT lỗi]: Không nhận được phản hồi từ API."
            except Exception as e:
                return f"[GPT lỗi]: {e}"
        # Hardcode logic đơn giản
        msg = user_message.lower()
        if "hello" in msg or "hi" in msg or "chào" in msg:
            return "Xin chào! Tôi là chatbot AI. Bạn cần hỏi gì?"
        if "tên" in msg:
            return "Tôi là gptbot, trợ lý AI của bạn!"
        if "cảm ơn" in msg:
            return "Không có gì, tôi luôn sẵn sàng giúp bạn!"
        if "mấy giờ" in msg or "giờ" in msg:
            from datetime import datetime
            return f"Bây giờ là {datetime.now().strftime('%H:%M:%S')}"
        if "ai tạo ra bạn" in msg:
            return "Tôi được tạo bởi OpenAI và được tích hợp vào Link Space bởi admin."
        return "Tôi chưa hiểu ý bạn lắm, bạn có thể hỏi lại không?"

    def display_message(self, content, msg_type="text", msg_index=None, sender=None, timestamp=None):
        item = QListWidgetItem()
        is_own = sender == self.current_user if sender else False
        can_recall = False
        if is_own and timestamp:
            from datetime import datetime, timedelta
            try:
                t = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if datetime.now() - t <= timedelta(minutes=2):
                    can_recall = True
            except Exception:
                pass
        
        # Load user data to get nickname
        sender_username = sender or self.current_user
        user_data = self.load_user_data(sender_username)
        nickname = user_data.get("nickname", "")
        
        # Format sender display with nickname
        if nickname:
            sender_display = f"{sender_username} ({nickname})"
        else:
            sender_display = sender_username
            
        # Lấy reaction nếu có
        reaction = self.get_reaction(msg_index)
        reaction_str = f"  {reaction}" if reaction else ""
        
        if msg_type == "text":
            item.setText(f"{sender_display}: {content}{reaction_str}")
        elif msg_type == "image":
            label = QLabel()
            pixmap = QPixmap(content).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.setText(f"{sender_display} gửi: {os.path.basename(content)}{reaction_str}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(label.sizeHint())
            self.chat_list.addItem(item)
            self.chat_list.setItemWidget(item, label)
            if can_recall:
                self.add_recall_button(msg_index)
            self.add_reaction_button(msg_index)
            return
        elif msg_type == "sticker":
            label = QLabel()
            pixmap = QPixmap(content).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(label.sizeHint())
            self.chat_list.addItem(item)
            self.chat_list.setItemWidget(item, label)
            if can_recall:
                self.add_recall_button(msg_index)
            self.add_reaction_button(msg_index)
            return
        elif msg_type == "video":
            item.setText(f"{sender_display} gửi video: {os.path.basename(content)}{reaction_str}")
        elif msg_type == "audio":
            label = QLabel(f"{sender_display} gửi ghi âm: {os.path.basename(content)}{reaction_str}")
            play_btn = QPushButton("Phát")
            def play_audio():
                import sys, subprocess
                if sys.platform.startswith('win'):
                    os.startfile(content)
                elif sys.platform.startswith('darwin'):
                    subprocess.call(['open', content])
                else:
                    subprocess.call(['xdg-open', content])
            play_btn.clicked.connect(play_audio)
            w = QWidget()
            l = QVBoxLayout(w)
            l.addWidget(label)
            l.addWidget(play_btn)
            item.setSizeHint(w.sizeHint())
            self.chat_list.addItem(item)
            self.chat_list.setItemWidget(item, w)
            if can_recall:
                self.add_recall_button(msg_index)
            self.add_reaction_button(msg_index)
            return
        self.chat_list.addItem(item)
        if can_recall:
            self.add_recall_button(msg_index)
        self.add_reaction_button(msg_index)

    def add_recall_button(self, msg_index):
        btn = QPushButton("Thu hồi")
        btn.setToolTip("Xóa/thu hồi tin nhắn này")
        def recall():
            self.recall_message(msg_index)
        btn.clicked.connect(recall)
        item = QListWidgetItem()
        w = QWidget()
        l = QHBoxLayout(w)
        l.addStretch()
        l.addWidget(btn)
        item.setSizeHint(w.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, w)

    def recall_message(self, msg_index):
        if not os.path.exists(self.messages_file):
            return
        with open(self.messages_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
        if 0 <= msg_index < len(messages):
            messages[msg_index]["content"] = "Tin nhắn đã được thu hồi"
            messages[msg_index]["type"] = "text"
        with open(self.messages_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)
        self.chat_list.clear()
        self.load_messages()

    def save_message(self, content, msg_type):
        os.makedirs(os.path.dirname(self.messages_file), exist_ok=True)
        messages = []
        if os.path.exists(self.messages_file):
            with open(self.messages_file, "r", encoding="utf-8") as f:
                messages = json.load(f)
        # Kiểm tra chặn
        if self.receiver:
            path = f"data/users/{self.receiver}.json"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                if "blocked" in user_data and self.current_user in user_data["blocked"]:
                    from PyQt6.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Bị chặn", f"Bạn đã bị @{self.receiver} chặn. Không thể gửi tin nhắn.")
                    return
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        messages.append({
            "sender": self.current_user,
            "receiver": self.receiver,
            "type": msg_type,
            "content": content,
            "timestamp": timestamp,
            "seen": False
        })
        with open(self.messages_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)

    def load_messages(self):
        if os.path.exists(self.messages_file):
            with open(self.messages_file, "r", encoding="utf-8") as f:
                messages = json.load(f)
                # Ẩn tin nhắn nếu mình đã chặn người gửi
                path = f"data/users/{self.current_user}.json"
                blocked = []
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f2:
                        user_data = json.load(f2)
                        blocked = user_data.get("blocked", [])
                # Đánh dấu đã xem nếu là người nhận
                updated = False
                for msg in messages:
                    if msg["receiver"] == self.current_user and not msg.get("seen", False):
                        msg["seen"] = True
                        updated = True
                if updated:
                    with open(self.messages_file, "w", encoding="utf-8") as fw:
                        json.dump(messages, fw, indent=4, ensure_ascii=False)
                self._last_seen_index = -1
                for i, msg in enumerate(messages):
                    if msg.get("seen") and msg["receiver"] == self.current_user:
                        self._last_seen_index = i
                for i, msg in enumerate(messages):
                    if msg["sender"] in blocked:
                        continue
                    self.display_message(msg["content"], msg_type=msg["type"], msg_index=i, sender=msg["sender"], timestamp=msg["timestamp"])
                    # Hiển thị "Đã xem" cho tin nhắn cuối cùng đã xem
                    if i == self._last_seen_index:
                        item = QListWidgetItem("Đã xem")
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                        self.chat_list.addItem(item)

    def record_audio(self):
        duration, fs = 10, 44100
        msg = QMessageBox(self)
        msg.setWindowTitle("Ghi âm")
        msg.setText("Đang ghi âm... Nhấn OK để dừng và gửi.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        audio_data = []
        def callback(indata, frames, time, status):
            audio_data.append(indata.copy())
        stream = sd.InputStream(samplerate=fs, channels=1, callback=callback)
        stream.start()
        msg.exec()
        stream.stop()
        stream.close()
        audio_np = np.concatenate(audio_data, axis=0)
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        write(tmpfile.name, fs, audio_np)
        self.display_message(tmpfile.name, msg_type="audio")
        self.save_message(tmpfile.name, msg_type="audio")

    @staticmethod
    def create_group_dialog(current_user):
        dialog = QDialog()
        dialog.setWindowTitle("Tạo nhóm chat mới")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tên nhóm:"))
        name_input = QLineEdit()
        layout.addWidget(name_input)
        layout.addWidget(QLabel("Chọn thành viên:"))
        user_list = QListWidget()
        # Load user list
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = [u["username"] for u in json.load(f) if u["username"] != current_user]
        for u in users:
            user_list.addItem(u)
        user_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(user_list)
        btn = QPushButton("Tạo nhóm")
        def create_group():
            name = name_input.text().strip()
            members = [current_user] + [item.text() for item in user_list.selectedItems()]
            if not name or len(members) < 2:
                QMessageBox.warning(dialog, "Lỗi", "Nhóm phải có tên và ít nhất 2 thành viên!")
                return
            import uuid
            group_id = str(uuid.uuid4())[:8]
            group = {"id": group_id, "name": name, "members": members}
            groups = []
            if os.path.exists("data/groups.json"):
                with open("data/groups.json", "r", encoding="utf-8") as f:
                    groups = json.load(f)
            groups.append(group)
            with open("data/groups.json", "w", encoding="utf-8") as f:
                json.dump(groups, f, indent=4, ensure_ascii=False)
            QMessageBox.information(dialog, "Thành công", f"Đã tạo nhóm '{name}'!")
            dialog.accept()
        btn.clicked.connect(create_group)
        layout.addWidget(btn)
        dialog.setLayout(layout)
        dialog.exec()

    @staticmethod
    def open_group_list(current_user):
        dialog = QDialog()
        dialog.setWindowTitle("Danh sách nhóm chat")
        layout = QVBoxLayout()
        group_list = QListWidget()
        groups = []
        if os.path.exists("data/groups.json"):
            with open("data/groups.json", "r", encoding="utf-8") as f:
                groups = json.load(f)
        for g in groups:
            if current_user in g["members"]:
                group_list.addItem(f"{g['name']} ({g['id']})")
        layout.addWidget(group_list)
        def open_group():
            sel = group_list.currentItem()
            if sel:
                group_id = sel.text().split("(")[-1].replace(")", "").strip()
                win = GroupChatWindow(group_id, current_user)
                win.exec()
        open_btn = QPushButton("Mở nhóm")
        open_btn.clicked.connect(open_group)
        layout.addWidget(open_btn)
        dialog.setLayout(layout)
        dialog.exec()

    def emoji_autoreplace(self):
        # Tự động thay :smile: thành emoji khi gõ
        import re
        text = self.message_input.toPlainText()
        def repl(m):
            code = m.group(1)
            return emoji.emojize(f':{code}:', language='alias')
        new_text = re.sub(r':([\w_\-+]+):', repl, text)
        if new_text != text:
            cursor = self.message_input.textCursor()
            pos = cursor.position()
            self.message_input.blockSignals(True)
            self.message_input.setPlainText(new_text)
            self.message_input.blockSignals(False)
            cursor.setPosition(pos)
            self.message_input.setTextCursor(cursor)

    def add_reaction_button(self, msg_index):
        btn = QPushButton("😊")
        btn.setToolTip("Thêm reaction cho tin nhắn này")
        def choose_reaction():
            from PyQt6.QtWidgets import QDialog, QHBoxLayout, QPushButton
            dialog = QDialog(self)
            dialog.setWindowTitle("Chọn reaction")
            layout = QHBoxLayout()
            reactions = ["❤", "😆", "😢", "👍", "👎"]
            for r in reactions:
                rbtn = QPushButton(r)
                rbtn.setFixedSize(36, 36)
                rbtn.clicked.connect(lambda checked, rx=r: self.set_reaction(msg_index, rx, dialog))
                layout.addWidget(rbtn)
            dialog.setLayout(layout)
            dialog.exec()
        btn.clicked.connect(choose_reaction)
        item = QListWidgetItem()
        w = QWidget()
        l = QHBoxLayout(w)
        l.addStretch()
        l.addWidget(btn)
        item.setSizeHint(w.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, w)

    def set_reaction(self, msg_index, reaction, dialog):
        if msg_index is None:
            return
        if not os.path.exists(self.messages_file):
            return
        with open(self.messages_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
        if 0 <= msg_index < len(messages):
            messages[msg_index]["reaction"] = reaction
            with open(self.messages_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=4, ensure_ascii=False)
        dialog.accept()
        self.chat_list.clear()
        self.load_messages()

    def get_reaction(self, msg_index):
        if msg_index is None:
            return ""
        if not os.path.exists(self.messages_file):
            return ""
        with open(self.messages_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
        if 0 <= msg_index < len(messages):
            return messages[msg_index].get("reaction", "")
        return ""

    def load_user_data(self, username):
        """Load user data from JSON file"""
        path = f"data/users/{username}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}


class GroupChatWindow(QDialog):
    def __init__(self, group_id, current_user):
        super().__init__()
        self.group_id = group_id
        self.current_user = current_user
        self.setWindowTitle(f"Nhóm: {self.get_group_name()}")
        self.setGeometry(200, 200, 600, 600)
        self.messages_file = f"data/messages/group_{group_id}.json"
        self.init_ui()
        self.load_messages()

    def get_group_name(self):
        if not os.path.exists("data/groups.json"):
            return self.group_id
        with open("data/groups.json", "r", encoding="utf-8") as f:
            groups = json.load(f)
        for g in groups:
            if g["id"] == self.group_id:
                return g["name"]
        return self.group_id

    def get_members(self):
        if not os.path.exists("data/groups.json"):
            return []
        with open("data/groups.json", "r", encoding="utf-8") as f:
            groups = json.load(f)
        for g in groups:
            if g["id"] == self.group_id:
                return g["members"]
        return []

    def init_ui(self):
        layout = QVBoxLayout()
        self.chat_list = QListWidget()
        layout.addWidget(self.chat_list)
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Nhập tin nhắn...")
        self.message_input.setFixedHeight(80)
        send_btn = QPushButton("Gửi")
        send_btn.clicked.connect(self.send_message)
        layout.addWidget(self.message_input)
        layout.addWidget(send_btn)
        # Hiển thị thành viên
        members = ", ".join(self.get_members())
        layout.addWidget(QLabel(f"Thành viên: {members}"))
        self.setLayout(layout)

    def load_messages(self):
        self.chat_list.clear()
        if os.path.exists(self.messages_file):
            with open(self.messages_file, "r", encoding="utf-8") as f:
                messages = json.load(f)
                for msg in messages:
                    item = QListWidgetItem(f"{msg['sender']}: {msg['content']}")
                    self.chat_list.addItem(item)

    def send_message(self):
        content = self.message_input.toPlainText().strip()
        if not content:
            return
        messages = []
        if os.path.exists(self.messages_file):
            with open(self.messages_file, "r", encoding="utf-8") as f:
                messages = json.load(f)
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        messages.append({
            "sender": self.current_user,
            "content": content,
            "timestamp": timestamp
        })
        with open(self.messages_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)
        self.message_input.clear()
        self.load_messages()
