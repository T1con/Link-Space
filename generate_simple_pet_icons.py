import os
from PIL import Image, ImageDraw, ImageFont

pet_colors = {
    'cat': '#f7c59f',
    'dog': '#b2a177',
    'dragon': '#7ed957',
    'rabbit': '#f9e2ae',
    'hamster': '#e2b07a',
    'parrot': '#7fd8be',
    'turtle': '#7ec850',
    'penguin': '#b5d0e0',
    'unicorn': '#e6a6f7',
    'panda': '#e0e0e0',
    'fox': '#f7a072',
    'dolphin': '#7fc7f7',
    'owl': '#bfa77f',
}

pet_names = {
    'cat': 'Mèo',
    'dog': 'Chó',
    'dragon': 'Rồng',
    'rabbit': 'Thỏ',
    'hamster': 'Hamster',
    'parrot': 'Vẹt',
    'turtle': 'Rùa',
    'penguin': 'Cụt',
    'unicorn': 'Kỳ lân',
    'panda': 'Gấu',
    'fox': 'Cáo',
    'dolphin': 'Cá heo',
    'owl': 'Cú',
}

os.makedirs('static/pets', exist_ok=True)

for pet, color in pet_colors.items():
    img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Vẽ hình tròn
    draw.ellipse((16, 16, 240, 240), fill=color, outline='#444', width=6)
    # Thêm tên pet
    try:
        font = ImageFont.truetype('arial.ttf', 48)
    except:
        font = ImageFont.load_default()
    text = pet_names[pet]
    # Lấy kích thước chữ bằng getbbox (Pillow >=8.0)
    try:
        bbox = font.getbbox(text)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        # Nếu Pillow cũ, dùng textbbox của draw
        bbox = draw.textbbox((0,0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((256-w)/2, 180), text, fill='#222', font=font)
    # Lưu file
    img.save(f'static/pets/{pet}.png')
    print(f'✓ Đã tạo static/pets/{pet}.png')

print('\nHoàn thành! Hãy làm mới trang profile để xem icon pet đơn giản.') 