import os
import json
import shutil
import zipfile
import math

POSTS_FILE = "data/posts.json"


def load_posts():
    if not os.path.exists(POSTS_FILE):
        return []
    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_post(new_post):
    posts = load_posts()
    posts.append(new_post)
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


def delete_post(username, timestamp):
    posts = load_posts()
    # Xóa bài đăng có đúng username và timestamp
    posts = [p for p in posts if not (p["username"] == username and p["timestamp"] == timestamp)]
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


def add_notification(username, message):
    import os, json
    notif_path = f"data/users/{username}_notifications.json"
    notifications = []
    if os.path.exists(notif_path):
        with open(notif_path, "r", encoding="utf-8") as f:
            try:
                notifications = json.load(f)
            except Exception:
                notifications = []
    from datetime import datetime
    notifications.append({
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(notif_path, "w", encoding="utf-8") as f:
        json.dump(notifications, f, indent=4, ensure_ascii=False)


def load_notifications(username):
    import os, json
    notif_path = f"data/users/{username}_notifications.json"
    if os.path.exists(notif_path):
        with open(notif_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []


def backup_data(backup_path="backup.zip"):
    """Nén toàn bộ thư mục data thành file zip."""
    if os.path.exists(backup_path):
        os.remove(backup_path)
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for foldername, subfolders, filenames in os.walk("data"):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                backup_zip.write(file_path, os.path.relpath(file_path, "data"))
    return backup_path


def restore_data(backup_path="backup.zip"):
    """Giải nén file zip vào thư mục data (ghi đè dữ liệu cũ)."""
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Không tìm thấy file backup: {backup_path}")
    # Xoá toàn bộ data cũ
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.makedirs("data", exist_ok=True)
    with zipfile.ZipFile(backup_path, 'r') as backup_zip:
        backup_zip.extractall("data")


def add_points_and_update_level_badge(username, action):
    import os, json
    user_path = f"data/users/{username}.json"
    if not os.path.exists(user_path):
        return
    with open(user_path, "r", encoding="utf-8") as f:
        user = json.load(f)
    # Điểm cho từng hành động
    action_points = {"post": 10, "comment": 2, "friend": 5}
    points = user.get("points", 0) + action_points.get(action, 0)
    user["points"] = points
    # Level
    user["level"] = math.floor(points / 100) + 1
    # Badge
    badges = user.get("badges", [])
    badge_map = [
        (5000, "Thách Đấu"),
        (2000, "Đại Cao Thủ"),
        (1000, "Huyền thoại"),
        (500, "Cao thủ"),
        (100, "Người mới")
    ]  # mốc điểm, tên badge
    for m, name in badge_map:
        if points >= m and name not in badges:
            badges.append(name)
    user["badges"] = badges
    with open(user_path, "w", encoding="utf-8") as f:
        json.dump(user, f, indent=4, ensure_ascii=False)
