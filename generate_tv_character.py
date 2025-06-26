from PIL import Image, ImageDraw, ImageFont
import os

def draw_tv_character(path):
    # Tạo ảnh 96x96 với nền trong suốt
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Nền gradient đặc biệt (xanh dương - tím)
    for y in range(96):
        for x in range(96):
            # Tạo hiệu ứng gradient
            r = int(30 + (x/96) * 100)
            g = int(50 + (y/96) * 80)
            b = int(150 + ((x+y)/192) * 100)
            d.point((x, y), fill=(r, g, b, 255))
    
    # Vẽ khung TV
    # Màn hình TV
    d.rectangle((20, 25, 76, 65), fill="#000", outline="#fff", width=2)
    
    # Chân TV
    d.rectangle((35, 65, 45, 75), fill="#333", outline="#666", width=1)
    d.rectangle((51, 65, 61, 75), fill="#333", outline="#666", width=1)
    
    # Màn hình TV với hiệu ứng
    d.rectangle((22, 27, 74, 63), fill="#1a1a2e", outline="#0f3460", width=1)
    
    # Hiệu ứng màn hình (các pixel nhỏ)
    for i in range(5):
        for j in range(3):
            x = 25 + i * 10
            y = 30 + j * 10
            color = "#4a90e2" if (i+j) % 2 == 0 else "#7b68ee"
            d.rectangle((x, y, x+6, y+6), fill=color)
    
    # Logo TV ở dưới
    d.text((48, 80), "TV", fill="#fff", anchor="mm", font=None)
    
    # Thêm hiệu ứng ánh sáng
    d.ellipse((15, 15, 25, 25), fill="#fff", outline="#fff", width=1)
    d.ellipse((71, 15, 81, 25), fill="#fff", outline="#fff", width=1)
    
    img.save(path)

if __name__ == "__main__":
    os.makedirs("data/characters", exist_ok=True)
    os.makedirs("static/characters", exist_ok=True)
    
    # Tạo ảnh cho TV character
    tv_path = "data/characters/char_tv.png"
    draw_tv_character(tv_path)
    
    # Copy sang static
    import shutil
    static_tv_path = "static/characters/char_tv.png"
    shutil.copy(tv_path, static_tv_path)
    
    print("Đã tạo nhân vật đặc biệt TV với giá vô hạn!")
    print("Ảnh đã được lưu tại:", tv_path)
    print("Và copy sang:", static_tv_path) 