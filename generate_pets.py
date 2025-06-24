from PIL import Image, ImageDraw, ImageFont
import os

# Danh sách pet mới
pets = [
    ("rabbit", "Thỏ", "#f8e1e7"),
    ("hamster", "Hamster", "#ffeaa7"),
    ("parrot", "Vẹt", "#81ecec"),
    ("turtle", "Rùa", "#55efc4"),
    ("penguin", "Cánh cụt", "#dfe6e9"),
    ("unicorn", "Kỳ lân", "#fd79a8"),
    ("panda", "Gấu trúc", "#dff9fb"),
    ("fox", "Cáo", "#fab1a0"),
    ("dolphin", "Cá heo", "#74b9ff"),
    ("owl", "Cú", "#636e72"),
]

def draw_pet(path, name, color):
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Nền tròn
    d.ellipse((8, 8, 88, 88), fill=color, outline="#333", width=3)
    # Mặt pet đơn giản
    face_color = "#fff" if color != "#636e72" else "#b2bec3"
    d.ellipse((28, 28, 76, 76), fill=face_color, outline="#333", width=2)
    # Mắt
    d.ellipse((44, 48, 50, 56), fill="#222")
    d.ellipse((58, 48, 64, 56), fill="#222")
    # Miệng
    d.arc((50, 60, 62, 72), 0, 180, fill="#222", width=2)
    # Tên pet
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = None
    d.text((48, 80), name, fill="#222", anchor="mm", font=font)
    img.save(path)

if __name__ == "__main__":
    os.makedirs("data/pets", exist_ok=True)
    for pid, name, color in pets:
        out_path = f"data/pets/{pid}.png"
        if not os.path.exists(out_path):
            draw_pet(out_path, name, color)
    print("Đã sinh ảnh cho 10 pet mới!") 