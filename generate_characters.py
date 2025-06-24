from PIL import Image, ImageDraw, ImageFont
import os

# Danh sách nhân vật (id, name, gender, color)
characters = [
    ("char_m_01", "Minh Quân", "male", "#3498db"),
    ("char_m_02", "Anh Dũng", "male", "#2980b9"),
    ("char_m_03", "Bảo Long", "male", "#1abc9c"),
    ("char_m_04", "Hữu Phúc", "male", "#16a085"),
    ("char_m_05", "Quốc Huy", "male", "#2ecc71"),
    ("char_m_06", "Gia Bảo", "male", "#27ae60"),
    ("char_m_07", "Tuấn Kiệt", "male", "#f1c40f"),
    ("char_m_08", "Đức Anh", "male", "#f39c12"),
    ("char_m_09", "Khánh Duy", "male", "#e67e22"),
    ("char_m_10", "Phúc Thịnh", "male", "#d35400"),
    ("char_m_11", "Hoàng Nam", "male", "#e74c3c"),
    ("char_m_12", "Duy Khang", "male", "#c0392b"),
    ("char_m_13", "Văn Khôi", "male", "#8e44ad"),
    ("char_m_14", "Hải Đăng", "male", "#9b59b6"),
    ("char_m_15", "Trọng Nghĩa", "male", "#34495e"),
    ("char_f_01", "Bảo Ngọc", "female", "#fd79a8"),
    ("char_f_02", "Khánh Linh", "female", "#e17055"),
    ("char_f_03", "Minh Châu", "female", "#fab1a0"),
    ("char_f_04", "Thu Trang", "female", "#f8c291"),
    ("char_f_05", "Phương Thảo", "female", "#f6e58d"),
    ("char_f_06", "Ngọc Hân", "female", "#f9ca24"),
    ("char_f_07", "Quỳnh Anh", "female", "#7ed6df"),
    ("char_f_08", "Hà My", "female", "#22a6b3"),
    ("char_f_09", "Tú Anh", "female", "#6ab04c"),
    ("char_f_10", "Thanh Vân", "female", "#badc58"),
    ("char_f_11", "Kim Ngân", "female", "#e056fd"),
    ("char_f_12", "Diễm Quỳnh", "female", "#be2edd"),
    ("char_f_13", "Hồng Nhung", "female", "#686de0"),
    ("char_f_14", "Mai Phương", "female", "#30336b"),
    ("char_f_15", "Trúc Lam", "female", "#95afc0"),
    ("char_pm", "Phương Minh", "female", "#ff69b4") # Đặc biệt: màu hồng nổi bật
]

def draw_character(path, name, gender, color, special=False):
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Nền tròn màu riêng
    d.ellipse((8, 8, 120, 120), fill=color, outline="#333", width=3)
    # Gương mặt đơn giản
    face_color = "#ffe0b2" if gender == "male" else "#fff0f6"
    d.ellipse((32, 32, 104, 104), fill=face_color, outline="#333", width=2)
    # Mắt
    d.ellipse((52, 60, 60, 72), fill="#333")
    d.ellipse((68, 60, 76, 72), fill="#333")
    # Miệng
    d.arc((60, 80, 68, 96), 0, 180, fill="#333", width=2)
    # Tên nhân vật
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = None
    d.text((64, 110), name[:8], fill="#222", anchor="mm", font=font)
    # Hiệu ứng đặc biệt cho Phương Minh
    if special:
        d.ellipse((90, 20, 120, 50), fill="#ffb6c1", outline="#ff69b4", width=2)
        d.text((105, 35), "❤", fill="#e84393", anchor="mm", font=font)
    img.save(path)

if __name__ == "__main__":
    os.makedirs("data/characters", exist_ok=True)
    for cid, name, gender, color in characters:
        special = (cid == "char_pm")
        draw_character(f"data/characters/{cid}.png", name, gender, color, special)
    print("Đã tạo xong icon cho tất cả nhân vật!") 