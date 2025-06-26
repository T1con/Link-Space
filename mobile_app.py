#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Space Mobile - Ứng dụng mạng xã hội cho điện thoại
Phiên bản web sử dụng Flask
"""

# import eventlet
# Monkey patch phải đặt trước mọi import khác
# eventlet.monkey_patch()

import os
import json
import base64
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
import zipfile
from io import BytesIO

# Import CommunityFeatures
from community_features import CommunityFeatures

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'link_space_mobile_secret_key_2025')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Khởi tạo CommunityFeatures
community_features = CommunityFeatures()

# Cấu hình upload file
UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
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

def load_messages():
    """Load tin nhắn từ JSON"""
    try:
        with open('data/messages.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_messages(messages):
    """Lưu tin nhắn vào JSON"""
    with open('data/messages.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

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
            if user['username'] == username:
                # Kiểm tra mật khẩu đã hash
                if 'password_hash' in user:
                    if check_password_hash(user['password_hash'], password):
                        session['username'] = username
                        session['user_id'] = user['id']
                        return redirect(url_for('home'))
                else:
                    # Backward compatibility với mật khẩu plain text
                    if user['password'] == password:
                        # Cập nhật thành hash
                        user['password_hash'] = generate_password_hash(password)
                        del user['password']
                        save_users(users)
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
        
        if len(username) < 3:
            flash('Tên đăng nhập phải có ít nhất 3 ký tự!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'error')
            return render_template('register.html')
        
        users = load_users()
        for user in users:
            if user['username'] == username:
                flash('Tên đăng nhập đã tồn tại!', 'error')
                return render_template('register.html')
        
        # Tạo user mới với mật khẩu đã hash
        new_user = {
            'id': str(uuid.uuid4()),
            'username': username,
            'password_hash': generate_password_hash(password)
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
            'friend_requests': [],
            'nickname': username,
            'bio': '',
            'birthday': '',
            'hobbies': '',
            'location': '',
            'idol': '',
            'gender': ''
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
    users = {u['username']: load_user_data(u['username']) for u in load_users()}
    
    return render_template('home.html', 
                         username=username, 
                         user_data=user_data, 
                         posts=posts,
                         users=users)

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    """Trang cá nhân"""
    if 'username' not in session:
        return redirect(url_for('login'))
    current_user = session['username']
    user_data = load_user_data(username)
    current_user_data = load_user_data(current_user)
    # Load pets dict
    with open('data/pets.json', 'r', encoding='utf-8') as f:
        pets = json.load(f)
    pets_dict = {p['id']: p for p in pets}
    # Load characters dict
    with open('data/characters.json', 'r', encoding='utf-8') as f:
        characters = json.load(f)
    characters_dict = {c['id']: c for c in characters}
    # Xử lý chọn nhân vật đại diện
    if request.method == 'POST' and current_user == username:
        char_id = request.form.get('set_main_character')
        if char_id and char_id in user_data.get('characters', []):
            user_data['main_character'] = char_id
            save_user_data(username, user_data)
            flash('Đã chọn nhân vật đại diện!', 'success')
            return redirect(url_for('profile', username=username))
    return render_template('profile.html', 
                         target_user=username,
                         user_data=user_data,
                         current_user=current_user,
                         current_user_data=current_user_data,
                         pets_dict=pets_dict,
                         characters_dict=characters_dict)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """Chỉnh sửa hồ sơ"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = load_user_data(username)
    
    if request.method == 'POST':
        # Cập nhật thông tin cơ bản
        user_data['nickname'] = request.form.get('nickname', '').strip()
        user_data['bio'] = request.form.get('bio', '').strip()
        user_data['birthday'] = request.form.get('birthday', '').strip()
        user_data['hobbies'] = request.form.get('hobbies', '').strip()
        user_data['location'] = request.form.get('location', '').strip()
        user_data['idol'] = request.form.get('idol', '').strip()
        user_data['gender'] = request.form.get('gender', '').strip()
        
        # Xử lý upload avatar
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and avatar_file.filename and allowed_file(avatar_file.filename):
                # Chỉ cho phép ảnh
                if avatar_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    filename = secure_filename(f"{username}_avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{avatar_file.filename}")
                    filepath = os.path.join('static/avatars', filename)
                    avatar_file.save(filepath)
                    user_data['avatar'] = f"avatars/{filename}"
        
        # Xử lý upload cover
        if 'cover' in request.files:
            cover_file = request.files['cover']
            if cover_file and cover_file.filename and allowed_file(cover_file.filename):
                # Chỉ cho phép ảnh
                if cover_file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    filename = secure_filename(f"{username}_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{cover_file.filename}")
                    filepath = os.path.join('static/covers', filename)
                    cover_file.save(filepath)
                    user_data['cover'] = f"covers/{filename}"
        
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
            if file and file.filename and allowed_file(file.filename):
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

@app.route('/messages')
def messages():
    """Trang tin nhắn"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    messages_data = load_messages()
    user_conversations = {}
    
    # Lọc conversations của user hiện tại
    for conversation_key, messages_list in messages_data.items():
        if username in conversation_key:
            user_conversations[conversation_key] = messages_list
    
    return render_template('messages.html', 
                         username=username,
                         conversations=user_conversations)

@app.route('/chat/<username>')
def chat(username):
    """Trang chat với user cụ thể"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    current_user = session['username']
    if current_user == username:
        return redirect(url_for('messages'))
    
    conversation_key = f"{current_user}_{username}" if current_user < username else f"{username}_{current_user}"
    
    return render_template('chat_window.html',
                         current_user=current_user,
                         target_user=username,
                         conversation_key=conversation_key)

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
        # Kiểm tra cả 2 trường hợp: posts có id và posts cũ không có id
        post_identifier = post.get('id') or f"{post.get('username')}_{post.get('timestamp')}"
        
        if post_identifier == post_id:
            if username in post.get('likes', []):
                post['likes'].remove(username)
                liked = False
            else:
                if 'likes' not in post:
                    post['likes'] = []
                post['likes'].append(username)
                liked = True
            save_posts(posts)
            return jsonify({'liked': liked, 'likes_count': len(post.get('likes', []))})
    
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

@app.route('/api/messages/<conversation_key>')
def get_messages(conversation_key):
    """API lấy tin nhắn của conversation"""
    if 'username' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    messages_data = load_messages()
    messages = messages_data.get(conversation_key, [])
    
    return jsonify({'messages': messages})

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """API gửi tin nhắn"""
    if 'username' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    data = request.get_json()
    target_user = data.get('target_user')
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Tin nhắn không được để trống'}), 400
    
    current_user = session['username']
    messages_data = load_messages()
    
    # Tạo key cho conversation
    conversation_key = f"{current_user}_{target_user}" if current_user < target_user else f"{target_user}_{current_user}"
    
    if conversation_key not in messages_data:
        messages_data[conversation_key] = []
    
    new_message = {
        'id': str(uuid.uuid4()),
        'sender': current_user,
        'content': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    messages_data[conversation_key].append(new_message)
    save_messages(messages_data)
    
    # Emit qua Socket.IO
    socketio.emit('new_message', {
        'conversation_key': conversation_key,
        'message': new_message
    })
    
    return jsonify({'success': True, 'message': new_message})

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/data/uploads/<path:filename>')
def uploaded_files(filename):
    """Serve uploaded files"""
    return send_from_directory('data/uploads', filename)

@app.route('/sw.js')
def service_worker():
    """Serve Service Worker"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def manifest():
    """Serve Web App Manifest"""
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

# API lấy comment của post
@app.route('/api/comment_post/<post_id>', methods=['GET'])
def get_comments(post_id):
    posts = load_posts()
    for post in posts:
        # Kiểm tra cả 2 trường hợp: posts có id và posts cũ không có id
        post_identifier = post.get('id') or f"{post.get('username')}_{post.get('timestamp')}"
        
        if post_identifier == post_id:
            return jsonify({'comments': post.get('comments', [])})
    return jsonify({'error': 'Không tìm thấy bài đăng'}), 404

# API thêm comment vào post
@app.route('/api/comment_post/<post_id>', methods=['POST'])
def add_comment(post_id):
    if 'username' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    data = request.get_json()
    comment = data.get('comment', '').strip()
    if not comment:
        return jsonify({'error': 'Bình luận không được để trống'}), 400
    posts = load_posts()
    for post in posts:
        # Kiểm tra cả 2 trường hợp: posts có id và posts cũ không có id
        post_identifier = post.get('id') or f"{post.get('username')}_{post.get('timestamp')}"
        
        if post_identifier == post_id:
            if 'comments' not in post:
                post['comments'] = []
            post['comments'].append({
                'username': session['username'],
                'content': comment,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            save_posts(posts)
            return jsonify({'success': True, 'comment': post['comments'][-1]})
    return jsonify({'error': 'Không tìm thấy bài đăng'}), 404

# Socket.IO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    join_room(room)
    print(f'Client joined room: {room}')

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data.get('room')
    leave_room(room)
    print(f'Client left room: {room}')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = None
    success = None
    if request.method == 'POST':
        old_pw = request.form.get('old_password', '').strip()
        new_pw = request.form.get('new_password', '').strip()
        confirm_pw = request.form.get('confirm_password', '').strip()
        if not old_pw or not new_pw or not confirm_pw:
            error = 'Vui lòng nhập đầy đủ thông tin!'
        elif new_pw != confirm_pw:
            error = 'Mật khẩu mới và xác nhận không khớp!'
        elif len(new_pw) < 6:
            error = 'Mật khẩu mới phải có ít nhất 6 ký tự!'
        else:
            users = load_users()
            for user in users:
                if user['username'] == session['username']:
                    if 'password_hash' not in user or not check_password_hash(user['password_hash'], old_pw):
                        error = 'Mật khẩu cũ không đúng!'
                        break
                    user['password_hash'] = generate_password_hash(new_pw)
                    save_users(users)
                    success = 'Đổi mật khẩu thành công!'
                    break
            else:
                error = 'Không tìm thấy người dùng!'
    return render_template('change_password.html', error=error, success=success)

@app.route('/communities', methods=['GET', 'POST'])
def communities():
    """Trang cộng đồng"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        if name:
            # Tạo cộng đồng mới sử dụng CommunityFeatures
            community_id = community_features.create_community(name, description, session['username'])
            flash('Tạo cộng đồng thành công!', 'success')
            return redirect(url_for('communities'))
    
    # Xử lý join/leave community
    join_id = request.args.get('join')
    leave_id = request.args.get('leave')
    
    if join_id:
        communities = community_features.load_communities()
        for community in communities:
            if community['id'] == join_id and session['username'] not in community['members']:
                community['members'].append(session['username'])
                with open('data/communities.json', 'w', encoding='utf-8') as f:
                    json.dump(communities, f, indent=4, ensure_ascii=False)
                flash('Đã tham gia cộng đồng!', 'success')
                break
    
    if leave_id:
        communities = community_features.load_communities()
        for community in communities:
            if community['id'] == leave_id and session['username'] in community['members']:
                community['members'].remove(session['username'])
                with open('data/communities.json', 'w', encoding='utf-8') as f:
                    json.dump(communities, f, indent=4, ensure_ascii=False)
                flash('Đã rời khỏi cộng đồng!', 'success')
                break
    
    communities = community_features.load_communities()
    return render_template('communities.html', communities=communities)

@app.route('/community/<community_id>/upload_avatar', methods=['POST'])
def upload_community_avatar(community_id):
    """Upload avatar cho cộng đồng"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'})
    
    # Kiểm tra quyền admin
    if not community_features.is_community_admin(community_id, session['username']):
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'})
    
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'message': 'Không có file được chọn'})
    
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Không có file được chọn'})
    
    if file and allowed_file(file.filename):
        # Tạo tên file mới
        filename = f"community_{community_id}_avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower() if file.filename else 'jpg'}"
        
        # Lưu file vào thư mục covers (dùng chung với ảnh bìa)
        filepath = os.path.join('data/covers', filename)
        file.save(filepath)
        
        # Cập nhật avatar trong community sử dụng CommunityFeatures
        if community_features.update_community_avatar(community_id, filename):
            return jsonify({'success': True, 'message': 'Upload avatar thành công', 'filename': filename})
        else:
            return jsonify({'success': False, 'message': 'Không thể cập nhật avatar'})
    
    return jsonify({'success': False, 'message': 'File không hợp lệ'})

@app.route('/community/<community_id>/upload_cover', methods=['POST'])
def upload_community_cover(community_id):
    """Upload ảnh bìa cho cộng đồng"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'})
    
    # Kiểm tra quyền admin
    if not community_features.is_community_admin(community_id, session['username']):
        return jsonify({'success': False, 'message': 'Không có quyền thực hiện'})
    
    if 'cover' not in request.files:
        return jsonify({'success': False, 'message': 'Không có file được chọn'})
    
    file = request.files['cover']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Không có file được chọn'})
    
    if file and allowed_file(file.filename):
        # Tạo tên file mới
        filename = f"community_{community_id}_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower() if file.filename else 'jpg'}"
        
        # Lưu file vào thư mục covers
        filepath = os.path.join('data/covers', filename)
        file.save(filepath)
        
        # Cập nhật cover trong community sử dụng CommunityFeatures
        if community_features.update_community_cover(community_id, filename):
            return jsonify({'success': True, 'message': 'Upload ảnh bìa thành công', 'filename': filename})
        else:
            return jsonify({'success': False, 'message': 'Không thể cập nhật ảnh bìa'})
    
    return jsonify({'success': False, 'message': 'File không hợp lệ'})

@app.route('/community/<community_id>/edit', methods=['GET', 'POST'])
def edit_community(community_id):
    """Trang chỉnh sửa thông tin cộng đồng"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    community = community_features.get_community_by_id(community_id)
    if not community:
        flash('Không tìm thấy cộng đồng!', 'error')
        return redirect(url_for('communities'))
    
    if not community_features.is_community_admin(community_id, session['username']):
        flash('Bạn không có quyền chỉnh sửa cộng đồng này!', 'error')
        return redirect(url_for('communities'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        if name:
            if community_features.update_community_info(community_id, name, description):
                flash('Cập nhật thông tin thành công!', 'success')
                return redirect(url_for('communities'))
            else:
                flash('Có lỗi xảy ra khi cập nhật!', 'error')
    
    return render_template('edit_community.html', community=community)

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if 'username' not in session:
        return redirect(url_for('login'))
    groups = []
    if os.path.exists('data/groups.json'):
        with open('data/groups.json', 'r', encoding='utf-8') as f:
            groups = json.load(f)
    error = None
    success = None
    # Tạo nhóm mới
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        members = request.form.getlist('members')
        if not name or len(members) < 2:
            error = 'Nhóm phải có tên và ít nhất 2 thành viên!'
        else:
            gid = str(uuid.uuid4())[:8]
            group = {
                'id': gid,
                'name': name,
                'members': [session['username']] + members
            }
            groups.append(group)
            with open('data/groups.json', 'w', encoding='utf-8') as f:
                json.dump(groups, f, indent=4, ensure_ascii=False)
            success = 'Đã tạo nhóm mới!'
    # Join/leave nhóm (nếu cần)
    join_id = request.args.get('join')
    leave_id = request.args.get('leave')
    if join_id or leave_id:
        for g in groups:
            if g['id'] == (join_id or leave_id):
                members = g.get('members', [])
                if join_id and session['username'] not in members:
                    members.append(session['username'])
                    success = 'Đã tham gia nhóm!'
                if leave_id and session['username'] in members:
                    members.remove(session['username'])
                    success = 'Đã rời nhóm!'
                g['members'] = members
                with open('data/groups.json', 'w', encoding='utf-8') as f:
                    json.dump(groups, f, indent=4, ensure_ascii=False)
                break
        return redirect(url_for('groups'))
    # Lấy danh sách user để chọn thành viên
    users = []
    if os.path.exists('data/users.json'):
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users = [u['username'] for u in json.load(f) if u['username'] != session['username']]
    return render_template('groups.html', groups=groups, users=users, error=error, success=success)

@app.route('/group_chat/<group_id>', methods=['GET', 'POST'])
def group_chat(group_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    # Lấy thông tin nhóm
    group = None
    if os.path.exists('data/groups.json'):
        with open('data/groups.json', 'r', encoding='utf-8') as f:
            groups = json.load(f)
            for g in groups:
                if g['id'] == group_id:
                    group = g
                    break
    if not group or session['username'] not in group['members']:
        return redirect(url_for('groups'))
    # Đọc tin nhắn nhóm
    msg_path = f'data/messages/group_{group_id}.json'
    messages = []
    if os.path.exists(msg_path):
        with open(msg_path, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    error = None
    # Gửi tin nhắn mới
    if request.method == 'POST':
        content = request.form.get('message', '').strip()
        if not content:
            error = 'Tin nhắn không được để trống!'
        else:
            from datetime import datetime
            messages.append({
                'sender': session['username'],
                'content': content,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            with open(msg_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=4, ensure_ascii=False)
            return redirect(url_for('group_chat', group_id=group_id))
    return render_template('group_chat.html', group=group, messages=messages, error=error)

@app.route('/pet_shop', methods=['GET', 'POST'])
def pet_shop():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_path = f"data/users/{session['username']}.json"
    user_data = {}
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    pets = []
    if os.path.exists('data/pets.json'):
        with open('data/pets.json', 'r', encoding='utf-8') as f:
            pets = json.load(f)
    error = None
    success = None
    # Mua pet
    buy_id = request.args.get('buy')
    if buy_id:
        for pet in pets:
            if pet['id'] == buy_id:
                if buy_id in user_data.get('pets', []):
                    error = 'Bạn đã sở hữu pet này!'
                elif user_data.get('points', 0) < pet['price']:
                    error = 'Bạn không đủ điểm để mua pet này!'
                else:
                    user_data.setdefault('pets', []).append(buy_id)
                    user_data['points'] = user_data.get('points', 0) - pet['price']
                    success = f'Đã mua pet {pet["name"]}!'
                break
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
        return redirect(url_for('pet_shop'))
    # Chọn pet chính
    main_id = request.args.get('main')
    if main_id and main_id in user_data.get('pets', []):
        user_data['main_pet'] = main_id
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
        success = 'Đã chọn pet chính!'
        return redirect(url_for('pet_shop'))
    return render_template('pet_shop.html', pets=pets, user_data=user_data, error=error, success=success)

@app.route('/character_shop', methods=['GET', 'POST'])
def character_shop():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_path = f"data/users/{session['username']}.json"
    user_data = {}
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    chars = []
    if os.path.exists('data/characters.json'):
        with open('data/characters.json', 'r', encoding='utf-8') as f:
            chars = json.load(f)
    error = None
    success = None
    # Mua character
    buy_id = request.args.get('buy')
    if buy_id:
        for char in chars:
            if char['id'] == buy_id:
                if buy_id in user_data.get('characters', []):
                    error = 'Bạn đã sở hữu nhân vật này!'
                elif user_data.get('points', 0) < char['price']:
                    error = 'Bạn không đủ điểm để mua nhân vật này!'
                else:
                    user_data.setdefault('characters', []).append(buy_id)
                    user_data['points'] = user_data.get('points', 0) - char['price']
                    success = f'Đã mua nhân vật {char["name"]}!'
                break
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
        return redirect(url_for('character_shop'))
    # Chọn character chính
    main_id = request.args.get('main')
    if main_id and main_id in user_data.get('characters', []):
        user_data['main_character'] = main_id
        with open(user_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
        success = 'Đã chọn nhân vật đại diện!'
        return redirect(url_for('character_shop'))
    return render_template('character_shop.html', chars=chars, user_data=user_data, error=error, success=success)

@app.route('/rank')
def rank():
    """Trang bảng xếp hạng người dùng theo điểm"""
    if 'username' not in session:
        return redirect(url_for('login'))
    users = load_users()
    user_data_list = []
    for u in users:
        data = load_user_data(u['username'])
        data['username'] = u['username']
        user_data_list.append(data)
    # Sắp xếp theo điểm, giảm dần
    user_data_list.sort(key=lambda x: x.get('points', 0), reverse=True)
    return render_template('rank.html', users=user_data_list)

# --- TÍNH NĂNG BẠN BÈ ---
@app.route('/add_friend/<username>', methods=['POST'])
def add_friend(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    current_user = session['username']
    if current_user == username:
        flash('Không thể kết bạn với chính mình!', 'error')
        return redirect(url_for('profile', username=username))
    user_data = load_user_data(username)
    current_user_data = load_user_data(current_user)
    # Nếu đã là bạn bè
    if username in current_user_data.get('friends', []):
        flash('Đã là bạn bè!', 'info')
        return redirect(url_for('profile', username=username))
    # Nếu đã gửi lời mời
    if username in current_user_data.get('sent_requests', []):
        flash('Đã gửi lời mời kết bạn!', 'info')
        return redirect(url_for('profile', username=username))
    # Thêm vào danh sách chờ xác nhận
    current_user_data.setdefault('sent_requests', []).append(username)
    user_data.setdefault('friend_requests', []).append(current_user)
    save_user_data(current_user, current_user_data)
    save_user_data(username, user_data)
    flash('Đã gửi lời mời kết bạn!', 'success')
    return redirect(url_for('profile', username=username))

@app.route('/accept_friend/<username>', methods=['POST'])
def accept_friend(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    current_user = session['username']
    user_data = load_user_data(username)
    current_user_data = load_user_data(current_user)
    # Xóa khỏi danh sách chờ xác nhận
    if username in current_user_data.get('friend_requests', []):
        current_user_data['friend_requests'].remove(username)
    if current_user in user_data.get('sent_requests', []):
        user_data['sent_requests'].remove(current_user)
    # Thêm vào danh sách bạn bè
    current_user_data.setdefault('friends', []).append(username)
    user_data.setdefault('friends', []).append(current_user)
    save_user_data(current_user, current_user_data)
    save_user_data(username, user_data)
    flash('Đã chấp nhận kết bạn!', 'success')
    return redirect(url_for('profile', username=username))

@app.route('/decline_friend/<username>', methods=['POST'])
def decline_friend(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    current_user = session['username']
    user_data = load_user_data(username)
    current_user_data = load_user_data(current_user)
    # Xóa khỏi danh sách chờ xác nhận
    if username in current_user_data.get('friend_requests', []):
        current_user_data['friend_requests'].remove(username)
    if current_user in user_data.get('sent_requests', []):
        user_data['sent_requests'].remove(current_user)
    save_user_data(current_user, current_user_data)
    save_user_data(username, user_data)
    flash('Đã từ chối lời mời kết bạn!', 'info')
    return redirect(url_for('profile', username=username))

@app.route('/remove_friend/<username>', methods=['POST'])
def remove_friend(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    current_user = session['username']
    user_data = load_user_data(username)
    current_user_data = load_user_data(current_user)
    # Xóa khỏi danh sách bạn bè
    if username in current_user_data.get('friends', []):
        current_user_data['friends'].remove(username)
    if current_user in user_data.get('friends', []):
        user_data['friends'].remove(current_user)
    save_user_data(current_user, current_user_data)
    save_user_data(username, user_data)
    flash('Đã hủy kết bạn!', 'info')
    return redirect(url_for('profile', username=username))

# ==================== API CỘNG ĐỒNG MỚI ====================

@app.route('/api/community/create_topic', methods=['POST'])
def api_create_topic():
    """API tạo chủ đề thảo luận mới"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    data = request.get_json()
    community_id = data.get('community_id')
    title = data.get('title')
    content = data.get('content')
    
    if not all([community_id, title, content]):
        return jsonify({'success': False, 'error': 'Thiếu thông tin'})
    
    # Kiểm tra quyền thành viên
    if not community_features.is_community_member(community_id, session['username']):
        return jsonify({'success': False, 'error': 'Bạn không phải thành viên cộng đồng này'})
    
    try:
        topic_id = community_features.create_topic(community_id, title, content, session['username'])
        return jsonify({'success': True, 'topic_id': topic_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/topics/<community_id>')
def api_get_topics(community_id):
    """API lấy danh sách chủ đề của cộng đồng"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    try:
        topics = community_features.get_community_topics(community_id)
        return jsonify({'success': True, 'topics': topics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/create_poll', methods=['POST'])
def api_create_poll():
    """API tạo bình chọn mới"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    data = request.get_json()
    community_id = data.get('community_id')
    question = data.get('question')
    options = data.get('options')
    duration_days = data.get('duration_days', 7)
    
    if not all([community_id, question, options]) or len(options) < 2:
        return jsonify({'success': False, 'error': 'Thiếu thông tin hoặc ít nhất 2 lựa chọn'})
    
    # Kiểm tra quyền thành viên
    if not community_features.is_community_member(community_id, session['username']):
        return jsonify({'success': False, 'error': 'Bạn không phải thành viên cộng đồng này'})
    
    try:
        poll_id = community_features.create_poll(community_id, question, options, session['username'], duration_days)
        return jsonify({'success': True, 'poll_id': poll_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/polls/<community_id>')
def api_get_polls(community_id):
    """API lấy danh sách bình chọn của cộng đồng"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    try:
        polls = community_features.get_community_polls(community_id)
        return jsonify({'success': True, 'polls': polls})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/vote_poll', methods=['POST'])
def api_vote_poll():
    """API bình chọn"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    data = request.get_json()
    poll_id = data.get('poll_id')
    option_index = data.get('option_index')
    
    if poll_id is None or option_index is None:
        return jsonify({'success': False, 'error': 'Thiếu thông tin'})
    
    try:
        success, message = community_features.vote_poll(poll_id, option_index, session['username'])
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/create_event', methods=['POST'])
def api_create_event():
    """API tạo sự kiện mới"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    data = request.get_json()
    community_id = data.get('community_id')
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    event_date = data.get('event_date')
    max_participants = data.get('max_participants')
    
    if not all([community_id, title, description, location, event_date]):
        return jsonify({'success': False, 'error': 'Thiếu thông tin'})
    
    # Kiểm tra quyền thành viên
    if not community_features.is_community_member(community_id, session['username']):
        return jsonify({'success': False, 'error': 'Bạn không phải thành viên cộng đồng này'})
    
    try:
        event_id = community_features.create_event(community_id, title, description, location, event_date, session['username'], max_participants)
        return jsonify({'success': True, 'event_id': event_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/events/<community_id>')
def api_get_events(community_id):
    """API lấy danh sách sự kiện của cộng đồng"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    try:
        events = community_features.get_community_events(community_id)
        return jsonify({'success': True, 'events': events})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/join_event', methods=['POST'])
def api_join_event():
    """API tham gia sự kiện"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    data = request.get_json()
    event_id = data.get('event_id')
    
    if not event_id:
        return jsonify({'success': False, 'error': 'Thiếu thông tin'})
    
    try:
        success, message = community_features.join_event(event_id, session['username'])
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/leaderboard/<community_id>')
def api_get_leaderboard(community_id):
    """API lấy bảng xếp hạng của cộng đồng"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    try:
        leaderboard = community_features.get_community_leaderboard(community_id)
        return jsonify({'success': True, 'leaderboard': leaderboard})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/community/user_stats')
def api_get_user_stats():
    """API lấy thống kê của người dùng"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Chưa đăng nhập'})
    
    try:
        stats = community_features.get_user_stats(session['username'])
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🌐 Link Space Mobile đang khởi động...")
    print(f"📱 Truy cập: http://localhost:{port}")
    print("🔄 Nhấn Ctrl+C để dừng")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug) 