# 🌐 Tính Năng Cộng Đồng Mới - Link Space Web

## 📋 Tổng Quan

Đã thêm 4 tính năng cộng đồng mới vào Link Space Web App:

1. **💬 Chủ đề thảo luận** - Tạo và thảo luận các chủ đề trong cộng đồng
2. **📊 Bình chọn** - Tạo cuộc bình chọn và thăm dò ý kiến
3. **📅 Sự kiện** - Tổ chức và tham gia các sự kiện cộng đồng
4. **🏆 Bảng xếp hạng** - Theo dõi hoạt động và xếp hạng thành viên

## 🚀 Cài Đặt và Chạy

### 1. Cài đặt dependencies
```bash
pip install flask flask-socketio
```

### 2. Chạy demo để tạo dữ liệu mẫu
```bash
python demo_community_web.py
```

### 3. Khởi động web app
```bash
python mobile_app.py
```

### 4. Truy cập ứng dụng
- Mở trình duyệt: `http://localhost:5000`
- Đăng nhập với tài khoản có sẵn hoặc tạo mới

## 🎯 Hướng Dẫn Sử Dụng

### 📍 Truy Cập Tính Năng Cộng Đồng

1. Đăng nhập vào Link Space
2. Click vào menu **"👥 Cộng đồng"** trong sidebar
3. Tham gia một cộng đồng hoặc tạo cộng đồng mới
4. Sử dụng các tab để truy cập tính năng:

### 💬 Chủ Đề Thảo Luận

**Tạo chủ đề mới:**
1. Chọn tab **"Chủ đề thảo luận"**
2. Chọn cộng đồng từ dropdown
3. Click **"Tạo chủ đề mới"**
4. Điền tiêu đề và nội dung
5. Click **"Tạo chủ đề"**

**Tính năng:**
- ✅ Tạo chủ đề với tiêu đề và nội dung
- ✅ Thêm bình luận vào chủ đề
- ✅ Like/unlike chủ đề
- ✅ Xem danh sách chủ đề theo cộng đồng
- ✅ Hiển thị số bình luận và like

### 📊 Bình Chọn

**Tạo bình chọn mới:**
1. Chọn tab **"Bình chọn"**
2. Chọn cộng đồng từ dropdown
3. Click **"Tạo bình chọn mới"**
4. Điền câu hỏi và các lựa chọn
5. Đặt thời hạn bình chọn
6. Click **"Tạo bình chọn"**

**Bình chọn:**
1. Chọn một lựa chọn
2. Click **"Bình chọn"**

**Tính năng:**
- ✅ Tạo bình chọn với nhiều lựa chọn
- ✅ Đặt thời hạn bình chọn
- ✅ Mỗi người chỉ được bình chọn 1 lần
- ✅ Hiển thị kết quả theo thời gian thực
- ✅ Tính phần trăm phiếu bầu

### 📅 Sự Kiện

**Tạo sự kiện mới:**
1. Chọn tab **"Sự kiện"**
2. Chọn cộng đồng từ dropdown
3. Click **"Tạo sự kiện mới"**
4. Điền thông tin sự kiện:
   - Tên sự kiện
   - Mô tả
   - Địa điểm
   - Thời gian
   - Số người tham gia tối đa (tùy chọn)
5. Click **"Tạo sự kiện"**

**Tham gia sự kiện:**
1. Xem danh sách sự kiện
2. Click **"Tham gia"** bên cạnh sự kiện muốn tham gia

**Tính năng:**
- ✅ Tạo sự kiện với đầy đủ thông tin
- ✅ Giới hạn số người tham gia
- ✅ Tham gia/rời khỏi sự kiện
- ✅ Hiển thị danh sách người tham gia
- ✅ Theo dõi trạng thái sự kiện

### 🏆 Bảng Xếp Hạng

**Xem bảng xếp hạng:**
1. Chọn tab **"Bảng xếp hạng"**
2. Chọn cộng đồng từ dropdown
3. Xem danh sách thành viên được sắp xếp theo điểm

**Hệ thống điểm:**
- 🎯 Tạo chủ đề: +10 điểm
- 💬 Bình luận: +2 điểm
- ❤️ Nhận like: +1 điểm
- 📊 Tạo bình chọn: +5 điểm
- 🗳️ Bình chọn: +1 điểm
- 📅 Tạo sự kiện: +15 điểm
- 👥 Tham gia sự kiện: +3 điểm

**Cấp độ:**
- Mỗi 100 điểm = 1 level
- Level càng cao = hoạt động càng tích cực

## 🔧 Cấu Trúc Dữ Liệu

### File dữ liệu được tạo tự động:
- `data/community_topics.json` - Chủ đề thảo luận
- `data/community_polls.json` - Bình chọn
- `data/community_events.json` - Sự kiện
- `data/community_leaderboard.json` - Bảng xếp hạng

### API Endpoints:
```
POST /api/community/create_topic
GET  /api/community/topics/<community_id>
POST /api/community/create_poll
GET  /api/community/polls/<community_id>
POST /api/community/vote_poll
POST /api/community/create_event
GET  /api/community/events/<community_id>
POST /api/community/join_event
GET  /api/community/leaderboard/<community_id>
GET  /api/community/user_stats
```

## 🎨 Giao Diện

### Responsive Design:
- ✅ Tương thích mobile và desktop
- ✅ Bootstrap 5 UI framework
- ✅ Modal dialogs cho tạo mới
- ✅ Tab navigation cho các tính năng
- ✅ Real-time updates với JavaScript

### Tính năng UI:
- 🎯 Dropdown chọn cộng đồng
- 📝 Form validation
- 🔄 Auto-refresh sau khi tạo
- 📊 Progress bars cho bình chọn
- 🏆 Medal icons cho top 3
- 📱 Mobile-friendly layout

## 🚀 Tính Năng Nâng Cao

### Gamification:
- 🎮 Hệ thống điểm và level
- 🏆 Bảng xếp hạng cạnh tranh
- 📈 Thống kê hoạt động cá nhân
- 🎯 Mục tiêu và thành tích

### Tương Tác:
- 💬 Bình luận real-time
- ❤️ Like/unlike
- 📊 Bình chọn an toàn
- 👥 Quản lý tham gia sự kiện

### Quản Lý:
- 🔒 Kiểm tra quyền thành viên
- ⏰ Thời hạn bình chọn
- 👥 Giới hạn tham gia sự kiện
- 📊 Thống kê chi tiết

## 🔮 Phát Triển Tương Lai

### Tính năng có thể thêm:
- 📧 Thông báo email cho sự kiện
- 📱 Push notifications
- 🖼️ Upload ảnh cho chủ đề
- 🎥 Video call cho sự kiện online
- 📊 Biểu đồ thống kê nâng cao
- 🏅 Huy hiệu và thành tích
- 🤖 Bot tự động quản lý
- 🌍 Đa ngôn ngữ

### Tối ưu hóa:
- ⚡ Caching cho performance
- 🔍 Tìm kiếm và lọc nâng cao
- 📱 PWA (Progressive Web App)
- 🔐 Bảo mật nâng cao

## 🐛 Xử Lý Lỗi

### Lỗi thường gặp:
1. **"Bạn không phải thành viên cộng đồng này"**
   - Giải pháp: Tham gia cộng đồng trước

2. **"Bạn đã bình chọn rồi!"**
   - Giải pháp: Mỗi người chỉ được bình chọn 1 lần

3. **"Sự kiện đã đầy người tham gia!"**
   - Giải pháp: Chờ người khác rời khỏi hoặc tạo sự kiện mới

4. **"Cuộc bình chọn đã kết thúc!"**
   - Giải pháp: Tạo bình chọn mới

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra console browser (F12)
2. Xem log server trong terminal
3. Kiểm tra file dữ liệu JSON
4. Restart server nếu cần

---

**🎉 Chúc bạn sử dụng các tính năng cộng đồng mới vui vẻ!** 