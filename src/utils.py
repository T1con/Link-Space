import os
import json
from PyQt6.QtWidgets import QApplication


def center_window(window):
    screen = QApplication.primaryScreen()
    if screen:
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - window.width()) // 2
        y = (screen_geometry.height() - window.height()) // 2
        window.move(x, y)


def load_posts():
    if not os.path.exists("data/posts.json"):
        return []
    with open("data/posts.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_post(post_data):
    posts = load_posts()
    posts.append(post_data)
    with open("data/posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
