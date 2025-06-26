import os
from PIL import Image, ImageDraw, ImageFont
import json

def create_pet_image(pet_name, pet_type, size=(200, 200), bg_color=(255, 255, 255)):
    """Tạo hình ảnh Pet với thiết kế đẹp"""
    
    # Tạo canvas mới
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Màu sắc cho từng loại pet
    pet_colors = {
        'cat': {'body': (255, 182, 193), 'ears': (255, 105, 180), 'eyes': (0, 0, 0)},
        'dog': {'body': (139, 69, 19), 'ears': (160, 82, 45), 'eyes': (0, 0, 0)},
        'dragon': {'body': (50, 205, 50), 'wings': (34, 139, 34), 'eyes': (255, 215, 0)},
        'rabbit': {'body': (255, 255, 255), 'ears': (255, 182, 193), 'eyes': (0, 0, 0)},
        'hamster': {'body': (255, 218, 185), 'cheeks': (255, 182, 193), 'eyes': (0, 0, 0)},
        'parrot': {'body': (255, 215, 0), 'wings': (255, 69, 0), 'eyes': (0, 0, 0)},
        'turtle': {'body': (34, 139, 34), 'shell': (139, 69, 19), 'eyes': (0, 0, 0)},
        'penguin': {'body': (0, 0, 0), 'belly': (255, 255, 255), 'eyes': (255, 255, 255)},
        'unicorn': {'body': (255, 182, 193), 'horn': (255, 215, 0), 'eyes': (138, 43, 226)},
        'panda': {'body': (255, 255, 255), 'patches': (0, 0, 0), 'eyes': (0, 0, 0)},
        'fox': {'body': (255, 140, 0), 'ears': (255, 69, 0), 'eyes': (0, 0, 0)},
        'dolphin': {'body': (135, 206, 235), 'belly': (255, 255, 255), 'eyes': (0, 0, 0)},
        'owl': {'body': (139, 69, 19), 'wings': (160, 82, 45), 'eyes': (255, 255, 0)}
    }
    
    colors = pet_colors.get(pet_type, {'body': (128, 128, 128), 'eyes': (0, 0, 0)})
    
    # Vẽ pet dựa trên loại
    if pet_type == 'cat':
        # Vẽ mèo
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Tai
        draw.polygon([(75, 65), (85, 45), (95, 65)], fill=colors['ears'])
        draw.polygon([(105, 65), (115, 45), (125, 65)], fill=colors['ears'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(255, 105, 180))
        # Đuôi
        draw.arc([140, 100, 180, 140], 0, 180, fill=colors['body'], width=8)
        
    elif pet_type == 'dog':
        # Vẽ chó
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Tai
        draw.ellipse([65, 50, 85, 70], fill=colors['ears'])
        draw.ellipse([115, 50, 135, 70], fill=colors['ears'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(0, 0, 0))
        # Đuôi
        draw.arc([140, 100, 180, 140], 0, 180, fill=colors['body'], width=8)
        
    elif pet_type == 'dragon':
        # Vẽ rồng
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Cánh
        draw.ellipse([40, 70, 80, 110], fill=colors['wings'])
        draw.ellipse([120, 70, 160, 110], fill=colors['wings'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        # Sừng
        draw.polygon([(90, 60), (95, 40), (100, 60)], fill=(255, 215, 0))
        
    elif pet_type == 'rabbit':
        # Vẽ thỏ
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Tai dài
        draw.rectangle([75, 40, 85, 70], fill=colors['ears'])
        draw.rectangle([115, 40, 125, 70], fill=colors['ears'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(255, 182, 193))
        
    elif pet_type == 'hamster':
        # Vẽ hamster
        # Thân tròn
        draw.ellipse([50, 70, 150, 170], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Má phồng
        draw.ellipse([60, 80, 80, 100], fill=colors['cheeks'])
        draw.ellipse([120, 80, 140, 100], fill=colors['cheeks'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        
    elif pet_type == 'parrot':
        # Vẽ vẹt
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Cánh
        draw.ellipse([40, 70, 80, 110], fill=colors['wings'])
        draw.ellipse([120, 70, 160, 110], fill=colors['wings'])
        # Mỏ
        draw.polygon([(90, 85), (100, 95), (110, 85)], fill=(255, 69, 0))
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        
    elif pet_type == 'turtle':
        # Vẽ rùa
        # Mai rùa
        draw.ellipse([50, 70, 150, 170], fill=colors['shell'])
        # Thân
        draw.ellipse([70, 90, 130, 150], fill=colors['body'])
        # Đầu
        draw.ellipse([85, 80, 115, 100], fill=colors['body'])
        # Mắt
        draw.ellipse([90, 85, 100, 95], fill=colors['eyes'])
        draw.ellipse([100, 85, 110, 95], fill=colors['eyes'])
        
    elif pet_type == 'penguin':
        # Vẽ cánh cụt
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Bụng trắng
        draw.ellipse([70, 90, 130, 150], fill=colors['belly'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        # Mỏ
        draw.polygon([(95, 85), (100, 95), (105, 85)], fill=(255, 215, 0))
        
    elif pet_type == 'unicorn':
        # Vẽ kỳ lân
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Sừng
        draw.polygon([(95, 60), (100, 30), (105, 60)], fill=colors['horn'])
        # Bờm
        for i in range(5):
            draw.arc([70+i*10, 50, 90+i*10, 70], 0, 180, fill=(255, 182, 193), width=3)
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        
    elif pet_type == 'panda':
        # Vẽ gấu trúc
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Mắt đen
        draw.ellipse([75, 70, 95, 90], fill=colors['patches'])
        draw.ellipse([105, 70, 125, 90], fill=colors['patches'])
        # Tai đen
        draw.ellipse([70, 55, 90, 75], fill=colors['patches'])
        draw.ellipse([110, 55, 130, 75], fill=colors['patches'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(0, 0, 0))
        
    elif pet_type == 'fox':
        # Vẽ cáo
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Tai nhọn
        draw.polygon([(75, 65), (85, 40), (95, 65)], fill=colors['ears'])
        draw.polygon([(105, 65), (115, 40), (125, 65)], fill=colors['ears'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=colors['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=colors['eyes'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(0, 0, 0))
        # Đuôi
        draw.arc([140, 100, 180, 140], 0, 180, fill=colors['body'], width=8)
        
    elif pet_type == 'dolphin':
        # Vẽ cá heo
        # Thân
        draw.ellipse([40, 80, 160, 160], fill=colors['body'])
        # Bụng trắng
        draw.ellipse([60, 100, 140, 140], fill=colors['belly'])
        # Đầu
        draw.ellipse([70, 70, 130, 110], fill=colors['body'])
        # Mắt
        draw.ellipse([85, 85, 95, 95], fill=colors['eyes'])
        draw.ellipse([105, 85, 115, 95], fill=colors['eyes'])
        # Vây lưng
        draw.polygon([(100, 60), (110, 40), (120, 60)], fill=colors['body'])
        
    elif pet_type == 'owl':
        # Vẽ cú
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=colors['body'])
        # Đầu tròn
        draw.ellipse([70, 60, 130, 100], fill=colors['body'])
        # Mắt lớn
        draw.ellipse([75, 70, 95, 90], fill=colors['eyes'])
        draw.ellipse([105, 70, 125, 90], fill=colors['eyes'])
        # Mỏ
        draw.polygon([(95, 85), (100, 95), (105, 85)], fill=(255, 215, 0))
        # Tai
        draw.ellipse([75, 50, 85, 60], fill=colors['wings'])
        draw.ellipse([115, 50, 125, 60], fill=colors['wings'])
    
    return img

def main():
    # Tạo thư mục pets nếu chưa có
    pets_dir = 'static/pets'
    if not os.path.exists(pets_dir):
        os.makedirs(pets_dir)
    
    # Danh sách pets
    pets = [
        {"id": "cat", "name": "Mèo dễ thương"},
        {"id": "dog", "name": "Chó trung thành"},
        {"id": "dragon", "name": "Rồng huyền thoại"},
        {"id": "rabbit", "name": "Thỏ ngọc"},
        {"id": "hamster", "name": "Chuột Hamster"},
        {"id": "parrot", "name": "Vẹt thông minh"},
        {"id": "turtle", "name": "Rùa may mắn"},
        {"id": "penguin", "name": "Cánh cụt vui nhộn"},
        {"id": "unicorn", "name": "Kỳ lân mộng mơ"},
        {"id": "panda", "name": "Gấu trúc đáng yêu"},
        {"id": "fox", "name": "Cáo tinh ranh"},
        {"id": "dolphin", "name": "Cá heo thân thiện"},
        {"id": "owl", "name": "Cú thông thái"}
    ]
    
    print("Đang tạo hình ảnh Pet mới...")
    
    for pet in pets:
        pet_id = pet['id']
        pet_name = pet['name']
        
        # Tạo hình ảnh
        img = create_pet_image(pet_name, pet_id)
        
        # Lưu file
        output_path = os.path.join(pets_dir, f"{pet_id}.png")
        img.save(output_path, 'PNG')
        
        print(f"Đã tạo: {pet_name} -> {output_path}")
    
    print("\nHoàn thành! Tất cả hình ảnh Pet đã được tạo lại.")
    print("Các file được lưu trong thư mục: static/pets/")

if __name__ == "__main__":
    main() 