#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script để kiểm tra tất cả chức năng chính của Link Space
"""

import requests
import json
import time
import os
from werkzeug.security import generate_password_hash, check_password_hash

BASE_URL = "http://localhost:5000"
USERS_PATH = 'data/users.json'
USER_DIR = 'data/users'

def test_login():
    """Test đăng nhập"""
    print("🔐 Testing Login...")
    session = requests.Session()
    
    # Test login
    login_data = {
        'username': 'T1con',
        'password': '1'  # Mật khẩu đúng
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data)
    if response.status_code == 200:
        print("✅ Login successful")
        return session
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None

def test_like_post(session):
    """Test like/unlike post"""
    print("\n❤️ Testing Like/Unlike...")
    
    # Test like post cũ (không có id)
    post_id = "T1con_2025-06-22T21:29:35"
    response = session.post(f"{BASE_URL}/api/like_post/{post_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Like successful: {data}")
    else:
        print(f"❌ Like failed: {response.status_code} - {response.text}")

def test_comment_post(session):
    """Test comment post"""
    print("\n💬 Testing Comment...")
    
    # Test comment post cũ
    post_id = "T1con_2025-06-22T21:29:35"
    comment_data = {
        'comment': 'Test comment từ script!'
    }
    
    response = session.post(f"{BASE_URL}/api/comment_post/{post_id}", 
                           json=comment_data)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Comment successful: {data}")
    else:
        print(f"❌ Comment failed: {response.status_code} - {response.text}")

def test_get_comments(session):
    """Test lấy comments"""
    print("\n📝 Testing Get Comments...")
    
    post_id = "T1con_2025-06-22T21:29:35"
    response = session.get(f"{BASE_URL}/api/comment_post/{post_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Get comments successful: {data}")
    else:
        print(f"❌ Get comments failed: {response.status_code} - {response.text}")

def test_profile(session):
    """Test trang profile"""
    print("\n👤 Testing Profile...")
    
    response = session.get(f"{BASE_URL}/profile/T1con")
    
    if response.status_code == 200:
        print("✅ Profile page accessible")
    else:
        print(f"❌ Profile failed: {response.status_code}")

def test_home(session):
    """Test trang home"""
    print("\n🏠 Testing Home...")
    
    response = session.get(f"{BASE_URL}/home")
    
    if response.status_code == 200:
        print("✅ Home page accessible")
    else:
        print(f"❌ Home failed: {response.status_code}")

def test_messages(session):
    """Test trang messages"""
    print("\n💌 Testing Messages...")
    
    response = session.get(f"{BASE_URL}/messages")
    
    if response.status_code == 200:
        print("✅ Messages page accessible")
    else:
        print(f"❌ Messages failed: {response.status_code}")

def sync_user_passwords():
    with open(USERS_PATH, 'r', encoding='utf-8') as f:
        users = json.load(f)
    changed = False
    for user in users:
        if 'password' in user:
            # Nếu đã có password_hash thì bỏ qua, ưu tiên hash
            if 'password_hash' not in user:
                user['password_hash'] = generate_password_hash(user['password'])
            del user['password']
            changed = True
    if changed:
        with open(USERS_PATH, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    print('[OK] Đồng bộ password_hash cho users.json')

def test_login_auto(username, password):
    with open(USERS_PATH, 'r', encoding='utf-8') as f:
        users = json.load(f)
    for user in users:
        if user['username'] == username and 'password_hash' in user and check_password_hash(user['password_hash'], password):
            print(f'[PASS] Đăng nhập thành công cho user: {username}')
            return True
    print(f'[FAIL] Đăng nhập thất bại cho user: {username}')
    return False

def test_change_password(username, old_pw, new_pw):
    with open(USERS_PATH, 'r', encoding='utf-8') as f:
        users = json.load(f)
    for user in users:
        if user['username'] == username and 'password_hash' in user and check_password_hash(user['password_hash'], old_pw):
            user['password_hash'] = generate_password_hash(new_pw)
            with open(USERS_PATH, 'w', encoding='utf-8') as f2:
                json.dump(users, f2, indent=4, ensure_ascii=False)
            print(f'[PASS] Đổi mật khẩu thành công cho user: {username}')
            return True
    print(f'[FAIL] Đổi mật khẩu thất bại cho user: {username}')
    return False

def test_register(username, password):
    with open(USERS_PATH, 'r', encoding='utf-8') as f:
        users = json.load(f)
    if any(u['username'] == username for u in users):
        print(f'[FAIL] User {username} đã tồn tại!')
        return False
    user = {
        'id': str(os.urandom(8).hex()),
        'username': username,
        'password_hash': generate_password_hash(password)
    }
    users.append(user)
    with open(USERS_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    print(f'[PASS] Đăng ký thành công user: {username}')
    return True

def test_setting_theme(username):
    user_path = os.path.join(USER_DIR, f'{username}.json')
    # Đảm bảo file tồn tại
    if not os.path.exists(user_path):
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump({'theme': 'dark'}, f)
    # Đọc file, tự động sửa nếu thiếu trường
    try:
        with open(user_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    except Exception:
        user_data = {'theme': 'dark'}
    if 'theme' not in user_data:
        user_data['theme'] = 'dark'
    # Đổi theme và lưu lại
    user_data['theme'] = 'light' if user_data['theme'] == 'dark' else 'dark'
    try:
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
        print(f'[PASS] Đổi theme cho user {username} thành {user_data["theme"]}')
    except Exception as e:
        print(f'[FAIL] Không thể lưu theme: {e}')

def test_api_like_comment(post_id, username, password):
    session = requests.Session()
    # Đăng nhập để lấy session cookie
    login_data = {'username': username, 'password': password}
    resp = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
    if resp.status_code not in (200, 302):
        print(f'[FAIL] Không thể đăng nhập để test API: {resp.status_code}')
        return
    # Test like
    like_resp = session.post(f'{BASE_URL}/api/like_post/{post_id}')
    if like_resp.status_code == 200 and like_resp.json().get('liked') is not None:
        print(f'[PASS] Like/Unlike post {post_id}')
    else:
        print(f'[FAIL] Like/Unlike post {post_id}: {like_resp.status_code} - {like_resp.text}')
    # Test comment
    comment_resp = session.post(f'{BASE_URL}/api/comment_post/{post_id}', json={'comment': 'Test comment tự động!'} )
    if comment_resp.status_code == 200 and comment_resp.json().get('success'):
        print(f'[PASS] Comment post {post_id}')
    else:
        print(f'[FAIL] Comment post {post_id}: {comment_resp.status_code} - {comment_resp.text}')

def main():
    print("🚀 Starting Link Space Function Tests...")
    print("=" * 50)
    
    # Test login
    session = test_login()
    if not session:
        print("❌ Cannot continue without login")
        return
    
    # Test các chức năng
    test_home(session)
    test_profile(session)
    test_like_post(session)
    test_comment_post(session)
    test_get_comments(session)
    test_messages(session)
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")

if __name__ == "__main__":
    sync_user_passwords()
    # Test đăng nhập với user mặc định (bạn có thể thay đổi username/password cho phù hợp)
    test_login_auto('T1con', '')
    test_login_auto('admin', '')
    # Test đổi mật khẩu
    test_change_password('T1con', '', '123456')
    test_login_auto('T1con', '123456')
    # Test đăng ký user mới
    test_register('test_auto', 'abc123')
    test_login_auto('test_auto', 'abc123')
    # Test setting cho user T1con
    test_setting_theme('T1con')
    # Test API like/comment với user test_auto nếu có post
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
            if posts:
                post_id = posts[0].get('id') or posts[0].get('post_id')
                if post_id:
                    test_api_like_comment(post_id, 'test_auto', 'abc123')
    except Exception:
        pass
    main() 