# Chức năng Avatar và Ảnh bìa cho Cộng đồng

## Tổng quan

Đã thêm chức năng avatar và ảnh bìa cho cộng đồng trong ứng dụng Link Space. Chức năng này cho phép admin của cộng đồng tùy chỉnh giao diện bằng cách upload avatar và ảnh bìa.

## Tính năng mới

### 1. Avatar cộng đồng
- **Mô tả**: Ảnh đại diện của cộng đồng, hiển thị dạng hình tròn
- **Kích thước**: 50x50px trong danh sách, 100x100px trong trang chỉnh sửa
- **Vị trí**: Bên cạnh tên cộng đồng trong danh sách

### 2. Ảnh bìa cộng đồng
- **Mô tả**: Ảnh bìa của cộng đồng, hiển thị ở đầu card
- **Kích thước**: 150px chiều cao trong danh sách, 120px trong trang chỉnh sửa
- **Vị trí**: Phía trên card thông tin cộng đồng

### 3. Trang chỉnh sửa cộng đồng
- **Truy cập**: Chỉ admin của cộng đồng mới có quyền
- **Chức năng**: 
  - Chỉnh sửa tên và mô tả cộng đồng
  - Upload avatar mới
  - Upload ảnh bìa mới

## Cách sử dụng

### Trên Web

1. **Truy cập trang Communities**
   ```
   http://localhost:5000/communities
   ```

2. **Tạo cộng đồng mới**
   - Điền tên và mô tả cộng đồng
   - Nhấn "Tạo mới"

3. **Chỉnh sửa cộng đồng (chỉ admin)**
   - Nhấn nút "Chỉnh sửa" bên cạnh cộng đồng
   - Hoặc truy cập: `/community/{community_id}/edit`

4. **Upload avatar**
   - Chọn file ảnh từ máy tính
   - Nhấn "Upload Avatar"
   - Ảnh sẽ được hiển thị ngay lập tức

5. **Upload ảnh bìa**
   - Chọn file ảnh từ máy tính
   - Nhấn "Upload Ảnh bìa"
   - Ảnh sẽ được hiển thị ngay lập tức

### API Endpoints

#### Upload Avatar
```
POST /community/{community_id}/upload_avatar
Content-Type: multipart/form-data

Parameters:
- avatar: File ảnh

Response:
{
    "success": true/false,
    "message": "Thông báo",
    "filename": "tên_file.jpg"
}
```

#### Upload Cover
```
POST /community/{community_id}/upload_cover
Content-Type: multipart/form-data

Parameters:
- cover: File ảnh

Response:
{
    "success": true/false,
    "message": "Thông báo",
    "filename": "tên_file.jpg"
}
```

#### Chỉnh sửa thông tin
```
GET/POST /community/{community_id}/edit

Parameters (POST):
- name: Tên cộng đồng
- description: Mô tả cộng đồng
```

## Cấu trúc dữ liệu

### Cộng đồng (communities.json)
```json
{
    "id": "abc12345",
    "name": "Tên cộng đồng",
    "description": "Mô tả cộng đồng",
    "admin": "username_admin",
    "members": ["user1", "user2"],
    "avatar": "community_abc12345_avatar_20250101_120000.jpg",
    "cover": "community_abc12345_cover_20250101_120000.jpg",
    "created_at": "2025-01-01 12:00:00"
}
```

### Lưu trữ file
- **Avatar**: Lưu trong thư mục `data/covers/`
- **Ảnh bìa**: Lưu trong thư mục `data/covers/`
- **Tên file**: `community_{community_id}_{type}_{timestamp}.{extension}`

## Quyền truy cập

### Upload và chỉnh sửa
- **Chỉ admin** của cộng đồng mới có quyền upload avatar/ảnh bìa
- **Chỉ admin** mới có quyền chỉnh sửa thông tin cộng đồng

### Xem
- **Tất cả người dùng** đều có thể xem avatar và ảnh bìa của cộng đồng

## Hạn chế file

### Định dạng được hỗ trợ
- PNG, JPG, JPEG, GIF

### Kích thước tối đa
- 16MB per file

## Demo

Chạy file demo để test chức năng:

```bash
python demo_community_web.py
```

## Chạy ứng dụng

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng web
python mobile_app.py

# Truy cập
http://localhost:5000
```

## Giao diện

### Trang Communities
- Hiển thị danh sách cộng đồng với avatar và ảnh bìa
- Nút "Chỉnh sửa" cho admin
- Nút "Tham gia/Rời nhóm" cho thành viên

### Trang Edit Community
- Form chỉnh sửa thông tin cộng đồng
- Upload avatar với preview
- Upload ảnh bìa với preview
- Responsive design cho mobile

## Lưu ý

1. **Backup**: Nên backup dữ liệu trước khi test
2. **Quyền**: Chỉ admin mới có thể upload và chỉnh sửa
3. **File size**: Giới hạn 16MB per file
4. **Format**: Chỉ hỗ trợ ảnh (PNG, JPG, JPEG, GIF)
5. **Storage**: File được lưu trong thư mục `data/covers/`

## Troubleshooting

### Lỗi upload
- Kiểm tra quyền admin
- Kiểm tra định dạng file
- Kiểm tra kích thước file
- Kiểm tra quyền ghi thư mục

### Ảnh không hiển thị
- Kiểm tra đường dẫn file
- Kiểm tra quyền đọc file
- Kiểm tra route `/data/uploads/`

### Lỗi permission
- Đảm bảo đã đăng nhập
- Đảm bảo là admin của cộng đồng
- Kiểm tra session 