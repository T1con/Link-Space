import requests
import sys
import random
import string
import json
import os
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

BASE_URL = 'http://localhost:5000'

def random_username():
    return 'test_api_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# Test đăng ký
# Gửi đúng trường: username, password, confirm_password
# Không gửi birthday/gender vì backend không yêu cầu

def test_register(username, password):
    data = {
        'username': username,
        'password': password,
        'confirm_password': password
    }
    resp = requests.post(f'{BASE_URL}/register', data=data, allow_redirects=False)
    if resp.status_code in (200, 302):
        print(f'[PASS] Đăng ký user {username}')
        return True
    print(f'[FAIL] Đăng ký user {username}: {resp.status_code}')
    return False

# Test đăng nhập
session = requests.Session()
def test_login(session, username, password):
    data = {
        'username': username,
        'password': password
    }
    resp = session.post(f'{BASE_URL}/login', data=data, allow_redirects=False)
    if resp.status_code in (200, 302):
        print(f'[PASS] Đăng nhập user {username}')
        return True
    print(f'[FAIL] Đăng nhập user {username}: {resp.status_code}')
    return False

# Test like bài viết (giả sử có post id)
def test_like(post_id):
    # Ưu tiên API /api/like_post/<post_id>
    resp = session.post(f'{BASE_URL}/api/like_post/{post_id}')
    if resp.status_code == 200 and resp.json().get('liked') is not None:
        print(f'[PASS] Like/Unlike post {post_id}')
        return True
    print(f'[FAIL] Like/Unlike post {post_id}: {resp.text}')
    return False

# Test comment bài viết
def test_comment(post_id, content):
    # Ưu tiên API /api/comment_post/<post_id>
    resp = session.post(f'{BASE_URL}/api/comment_post/{post_id}', json={'comment': content})
    if resp.status_code == 200 and resp.json().get('success'):
        print(f'[PASS] Comment post {post_id}')
        return True
    print(f'[FAIL] Comment post {post_id}: {resp.text}')
    return False

def get_first_post_id():
    # Thử các endpoint phổ biến
    endpoints = [
        '/api/posts', '/api/get_posts', '/home'
    ]
    for ep in endpoints:
        try:
            resp = session.get(BASE_URL + ep)
            if resp.status_code == 200:
                # Nếu là JSON
                try:
                    data = resp.json()
                    if isinstance(data, list) and data:
                        post = data[0]
                        return post.get('id') or post.get('post_id')
                except Exception:
                    # Nếu là HTML, thử parse id từ file posts.json
                    pass
        except Exception:
            continue
    # Nếu không có API, đọc trực tiếp file posts.json
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
            if posts:
                post = posts[0]
                return post.get('id') or post.get('post_id')
    except Exception:
        pass
    return None

def test_chat(session, user1, user2):
    # Gửi tin nhắn từ user1 -> user2
    msg = 'Hello from ' + user1
    data = {'target_user': user2, 'message': msg}
    resp = session.post(f'{BASE_URL}/api/send_message', json=data)
    if resp.status_code == 200 and resp.json().get('success'):
        print(f'[PASS] Nhắn tin từ {user1} tới {user2}')
    else:
        print(f'[FAIL] Nhắn tin từ {user1} tới {user2}')
    # Lấy tin nhắn
    key = f'{min(user1,user2)}_{max(user1,user2)}'
    resp = session.get(f'{BASE_URL}/api/messages/{key}')
    if resp.status_code == 200 and any(msg in m['content'] for m in resp.json().get('messages', [])):
        print(f'[PASS] Lấy tin nhắn giữa {user1} và {user2}')
    else:
        print(f'[FAIL] Lấy tin nhắn giữa {user1} và {user2}')

def test_pet(session):
    resp = session.get(f'{BASE_URL}/pet_shop', allow_redirects=True)
    if 'Đăng nhập' in resp.text or resp.url.endswith('/login'):
        print('[FAIL] Truy cập cửa hàng Pet: Chưa đăng nhập')
    elif resp.status_code == 200 and 'Cửa hàng Pet' in resp.text:
        print('[PASS] Truy cập cửa hàng Pet')
    else:
        print('[FAIL] Truy cập cửa hàng Pet')

def test_character(session):
    resp = session.get(f'{BASE_URL}/character_shop', allow_redirects=True)
    if 'Đăng nhập' in resp.text or resp.url.endswith('/login'):
        print('[FAIL] Truy cập cửa hàng Nhân vật: Chưa đăng nhập')
    elif resp.status_code == 200 and 'Cửa hàng Nhân vật' in resp.text:
        print('[PASS] Truy cập cửa hàng Nhân vật')
    else:
        print('[FAIL] Truy cập cửa hàng Nhân vật')

def test_community(session):
    resp = session.get(f'{BASE_URL}/communities', allow_redirects=True)
    if 'Đăng nhập' in resp.text or resp.url.endswith('/login'):
        print('[FAIL] Truy cập cộng đồng: Chưa đăng nhập')
    elif resp.status_code == 200 and 'Cộng đồng' in resp.text:
        print('[PASS] Truy cập cộng đồng')
    else:
        print('[FAIL] Truy cập cộng đồng')

def test_group(session):
    resp = session.get(f'{BASE_URL}/groups', allow_redirects=True)
    if 'Đăng nhập' in resp.text or resp.url.endswith('/login'):
        print('[FAIL] Truy cập nhóm chat: Chưa đăng nhập')
    elif resp.status_code == 200 and 'Nhóm chat' in resp.text:
        print('[PASS] Truy cập nhóm chat')
    else:
        print('[FAIL] Truy cập nhóm chat')

def test_backup(session):
    resp = session.get(f'{BASE_URL}/backup', allow_redirects=True)
    if 'Đăng nhập' in resp.text or resp.url.endswith('/login'):
        print('[FAIL] Tải backup dữ liệu: Chưa đăng nhập')
    elif resp.status_code == 200 and resp.headers.get('Content-Type','').startswith('application/zip'):
        print('[PASS] Tải backup dữ liệu')
    else:
        print('[FAIL] Tải backup dữ liệu')

def add_sample_data(username):
    user_path = f'data/users/{username}.json'
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf-8') as f:
            user = json.load(f)
        user['points'] = 5000
        user['pets'] = ["cat", "dog", "dragon"]
        user['main_pet'] = "cat"
        user['characters'] = ["char_m_01", "char_f_01"]
        user['main_character'] = "char_m_01"
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user, f, indent=4, ensure_ascii=False)

def test_add_friend(session, from_user, to_user):
    resp = session.post(f'{BASE_URL}/add_friend/{to_user}', allow_redirects=False)
    if resp.status_code in (200, 302):
        print(f'[PASS] {from_user} gửi lời mời kết bạn tới {to_user}')
        return True
    print(f'[FAIL] {from_user} gửi lời mời kết bạn tới {to_user}: {resp.status_code}')
    return False

def test_accept_friend(session, from_user, to_user):
    resp = session.post(f'{BASE_URL}/accept_friend/{from_user}', allow_redirects=False)
    if resp.status_code in (200, 302):
        print(f'[PASS] {to_user} chấp nhận kết bạn với {from_user}')
        return True
    print(f'[FAIL] {to_user} chấp nhận kết bạn với {from_user}: {resp.status_code}')
    return False

def test_decline_friend(session, from_user, to_user):
    resp = session.post(f'{BASE_URL}/decline_friend/{from_user}', allow_redirects=False)
    if resp.status_code in (200, 302):
        print(f'[PASS] {to_user} từ chối kết bạn với {from_user}')
        return True
    print(f'[FAIL] {to_user} từ chối kết bạn với {from_user}: {resp.status_code}')
    return False

def test_remove_friend(session, from_user, to_user):
    resp = session.post(f'{BASE_URL}/remove_friend/{to_user}', allow_redirects=False)
    if resp.status_code in (200, 302):
        print(f'[PASS] {from_user} hủy kết bạn với {to_user}')
        return True
    print(f'[FAIL] {from_user} hủy kết bạn với {to_user}: {resp.status_code}')
    return False

def get_user_data(username):
    path = f'data/users/{username}.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def test_friendship_flow():
    username1 = random_username()
    username2 = random_username()
    password = 'test123456'
    test_register(username1, password)
    test_register(username2, password)
    session1 = requests.Session()
    session2 = requests.Session()
    test_login(session1, username1, password)
    test_login(session2, username2, password)
    # 1. Gửi lời mời kết bạn
    test_add_friend(session1, username1, username2)
    # 2. Kiểm tra trạng thái: username2 có friend_requests từ username1
    data2 = get_user_data(username2)
    if 'friend_requests' in data2 and username1 in data2['friend_requests']:
        print(f'[PASS] {username2} nhận được lời mời kết bạn từ {username1}')
    else:
        print(f'[FAIL] {username2} không nhận được lời mời kết bạn từ {username1}')
    # 3. Chấp nhận kết bạn
    test_accept_friend(session2, username1, username2)
    # 4. Kiểm tra trạng thái bạn bè
    data1 = get_user_data(username1)
    data2 = get_user_data(username2)
    if 'friends' in data1 and username2 in data1['friends'] and 'friends' in data2 and username1 in data2['friends']:
        print(f'[PASS] {username1} và {username2} đã là bạn bè')
    else:
        print(f'[FAIL] {username1} và {username2} chưa là bạn bè')
    # 5. Hủy kết bạn
    test_remove_friend(session1, username1, username2)
    data1 = get_user_data(username1)
    data2 = get_user_data(username2)
    if (not data1.get('friends') or username2 not in data1['friends']) and (not data2.get('friends') or username1 not in data2['friends']):
        print(f'[PASS] {username1} và {username2} đã hủy kết bạn')
    else:
        print(f'[FAIL] {username1} và {username2} vẫn còn là bạn bè')

def main():
    username1 = random_username()
    username2 = random_username()
    password = 'test123456'
    # Đăng ký 2 user
    test_register(username1, password)
    test_register(username2, password)
    # Đăng nhập user1
    session1 = requests.Session()
    test_login(session1, username1, password)
    # Đăng nhập user2
    session2 = requests.Session()
    test_login(session2, username2, password)
    # Bổ sung dữ liệu mẫu cho user1
    add_sample_data(username1)
    # Test chat
    test_chat(session1, username1, username2)
    # Test pet
    test_pet(session1)
    # Test character
    test_character(session1)
    # Test cộng đồng
    test_community(session1)
    # Test nhóm chat
    test_group(session1)
    # Test backup
    test_backup(session1)
    print('\n--- TEST CHỨC NĂNG BẠN BÈ ---')
    test_friendship_flow()

if __name__ == '__main__':
    main() 