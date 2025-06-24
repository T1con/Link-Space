#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Space Mobile - Ứng dụng mạng xã hội cho điện thoại
Phiên bản web sử dụng Flask
"""

import os
import json
import base64
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'link_space_mobile_secret_key_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Cấu hình upload file
UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Tạo thư mục static nếu chưa có
os.makedirs('static', exist_ok=True)
os.makedirs('static/avatars', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_users():
    """Load danh sách users từ JSON"""
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    """Lưu danh sách users vào JSON"""
    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def load_user_data(username):
    """Load dữ liệu user từ file riêng"""
    try:
        with open(f'data/users/{username}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_user_data(username, data):
    """Lưu dữ liệu user vào file riêng"""
    os.makedirs('data/users', exist_ok=True)
    with open(f'data/users/{username}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_posts():
    """Load bài đăng từ JSON"""
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_posts(posts):
    """Lưu bài đăng vào JSON"""
    with open('data/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    """Trang chủ - chuyển hướng đến login nếu chưa đăng nhập"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Trang đăng nhập"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                session['user_id'] = user['id']
                return redirect(url_for('home'))
        
        flash('Sai tên đăng nhập hoặc mật khẩu!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Trang đăng ký"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'error')
            return render_template('register.html')
        
        users = load_users()
        for user in users:
            if user['username'] == username:
                flash('Tên đăng nhập đã tồn tại!', 'error')
                return render_template('register.html')
        
        # Tạo user mới
        new_user = {
            'id': str(uuid.uuid4()),
            'username': username,
            'password': password
        }
        users.append(new_user)
        save_users(users)
        
        # Tạo file dữ liệu user
        user_data = {
            'points': 0,
            'level': 1,
            'badges': ['Người mới'],
            'friends': [],
            'following': [],
            'followers': [],
            'friend_requests': []
        }
        save_user_data(username, user_data)
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/home')
def home():
    """Trang chính sau khi đăng nhập"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = load_user_data(username)
    posts = load_posts()
    
    return render_template('home.html', 
                         username=username, 
                         user_data=user_data, 
                         posts=posts)

@app.route('/profile/<username>')
def profile(username):
    """Trang cá nhân"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    current_user = session['username']
    user_data = load_user_data(username)
    current_user_data = load_user_data(current_user)
    
    return render_template('profile.html', 
                         target_user=username,
                         user_data=user_data,
                         current_user=current_user,
                         current_user_data=current_user_data)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """Chỉnh sửa hồ sơ"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = load_user_data(username)
    
    if request.method == 'POST':
        user_data['nickname'] = request.form.get('nickname', '').strip()
        user_data['bio'] = request.form.get('bio', '').strip()
        user_data['birthday'] = request.form.get('birthday', '').strip()
        user_data['hobbies'] = request.form.get('hobbies', '').strip()
        user_data['location'] = request.form.get('location', '').strip()
        user_data['idol'] = request.form.get('idol', '').strip()
        user_data['gender'] = request.form.get('gender', '').strip()
        
        save_user_data(username, user_data)
        flash('Cập nhật hồ sơ thành công!', 'success')
        return redirect(url_for('profile', username=username))
    
    return render_template('edit_profile.html', user_data=user_data)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    """Tạo bài đăng mới"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if not content:
            flash('Nội dung bài đăng không được để trống!', 'error')
            return render_template('create_post.html')
        
        # Xử lý upload file
        media_path = None
        if 'media' in request.files:
            file = request.files['media']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{session['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                media_path = f"uploads/{filename}"
        
        # Tạo bài đăng mới
        new_post = {
            'id': str(uuid.uuid4()),
            'username': session['username'],
            'content': content,
            'media': media_path,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'likes': [],
            'comments': []
        }
        
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        
        # Cộng điểm cho user
        user_data = load_user_data(session['username'])
        user_data['points'] = user_data.get('points', 0) + 10
        save_user_data(session['username'], user_data)
        
        flash('Đăng bài thành công! +10 điểm', 'success')
        return redirect(url_for('home'))
    
    return render_template('create_post.html')

@app.route('/logout')
def logout():
    """Đăng xuất"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/like_post/<post_id>', methods=['POST'])
def like_post(post_id):
    """API like bài đăng"""
    if 'username' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    username = session['username']
    posts = load_posts()
    
    for post in posts:
        if post['id'] == post_id:
            if username in post['likes']:
                post['likes'].remove(username)
                liked = False
            else:
                post['likes'].append(username)
                liked = True
            save_posts(posts)
            return jsonify({'liked': liked, 'likes_count': len(post['likes'])})
    
    return jsonify({'error': 'Không tìm thấy bài đăng'}), 404

@app.route('/api/follow/<username>', methods=['POST'])
def follow_user(username):
    """API theo dõi user"""
    if 'username' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    current_user = session['username']
    if current_user == username:
        return jsonify({'error': 'Không thể theo dõi chính mình'}), 400
    
    current_user_data = load_user_data(current_user)
    target_user_data = load_user_data(username)
    
    if username in current_user_data.get('following', []):
        # Bỏ theo dõi
        current_user_data['following'].remove(username)
        target_user_data['followers'].remove(current_user)
        following = False
    else:
        # Theo dõi
        current_user_data.setdefault('following', []).append(username)
        target_user_data.setdefault('followers', []).append(current_user)
        following = True
    
    save_user_data(current_user, current_user_data)
    save_user_data(username, target_user_data)
    
    return jsonify({'following': following})

@app.route('/sw.js')
def service_worker():
    """Serve Service Worker"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def manifest():
    """Serve Web App Manifest"""
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

if __name__ == '__main__':
    print("🌐 Link Space Mobile đang khởi động...")
    print("📱 Truy cập: http://localhost:5000")
    print("📱 Hoặc: http://[IP_MÁY_TÍNH]:5000 (để truy cập từ điện thoại)")
    print("🔄 Nhấn Ctrl+C để dừng")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 