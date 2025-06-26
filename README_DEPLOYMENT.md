# 🚀 Hướng dẫn Deploy Link Space lên Render

## 📋 Yêu cầu hệ thống

- Python 3.11+
- Git
- Tài khoản Render (miễn phí)

## 🔧 Các bước deploy

### 1. Chuẩn bị code

Đảm bảo các file sau đã có trong project:
- `requirements.txt` - Dependencies
- `Procfile` - Cấu hình process
- `mobile_app.py` - File chính
- `render.yaml` - Cấu hình Render (tùy chọn)

### 2. Push code lên GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/link-space.git
git push -u origin main
```

### 3. Deploy lên Render

1. **Đăng nhập Render**: https://render.com
2. **Tạo Web Service mới**
3. **Connect GitHub repository**
4. **Cấu hình:**
   - **Name**: link-space
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT mobile_app:app`
   - **Plan**: Free

### 4. Environment Variables (tùy chọn)

Thêm các biến môi trường trong Render:
- `SECRET_KEY`: Secret key cho Flask
- `FLASK_ENV`: production

## 🌐 Truy cập

Sau khi deploy thành công, bạn sẽ có URL dạng:
```
https://link-space.onrender.com
```

## 🔧 Troubleshooting

### Lỗi thường gặp:

1. **Port binding error**: Đảm bảo sử dụng `$PORT` trong start command
2. **Import error**: Kiểm tra `requirements.txt` có đầy đủ dependencies
3. **File not found**: Đảm bảo các file static và data được include

### Debug:

- Xem logs trong Render Dashboard
- Kiểm tra build logs
- Test locally trước khi deploy

## 📱 Tính năng

✅ Đăng ký/Đăng nhập  
✅ Đăng bài với media  
✅ Like/Comment  
✅ Chat real-time  
✅ Profile management  
✅ PWA support  
✅ Mobile responsive  

## 🔒 Bảo mật

- Mật khẩu được hash
- Session management
- Input validation
- File upload restrictions

## 📈 Performance

- Gunicorn worker
- Eventlet async
- Static file serving
- Caching support 