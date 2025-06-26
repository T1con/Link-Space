import os
from PIL import Image, ImageDraw, ImageFilter
import json

def create_enhanced_pet_image(pet_name, pet_type, size=(200, 200)):
    """Tạo hình ảnh Pet với thiết kế đẹp và hiệu ứng"""
    
    # Tạo canvas mới với background gradient
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Tạo background gradient
    for y in range(size[1]):
        alpha = int(255 * (1 - y / size[1]) * 0.1)  # Gradient từ trên xuống
        draw.line([(0, y), (size[0], y)], fill=(255, 255, 255, alpha))
    
    # Màu sắc và thiết kế cho từng loại pet
    pet_designs = {
        'cat': {
            'body': (255, 182, 193), 'ears': (255, 105, 180), 'eyes': (0, 0, 0),
            'pattern': [(255, 182, 193), (255, 105, 180)], 'accessory': 'bow'
        },
        'dog': {
            'body': (139, 69, 19), 'ears': (160, 82, 45), 'eyes': (0, 0, 0),
            'pattern': [(139, 69, 19), (160, 82, 45)], 'accessory': 'collar'
        },
        'dragon': {
            'body': (50, 205, 50), 'wings': (34, 139, 34), 'eyes': (255, 215, 0),
            'pattern': [(50, 205, 50), (34, 139, 34)], 'accessory': 'fire', 'horn': (255, 215, 0)
        },
        'rabbit': {
            'body': (255, 255, 255), 'ears': (255, 182, 193), 'eyes': (0, 0, 0),
            'pattern': [(255, 255, 255), (255, 182, 193)], 'accessory': 'carrot'
        },
        'hamster': {
            'body': (255, 218, 185), 'cheeks': (255, 182, 193), 'eyes': (0, 0, 0),
            'pattern': [(255, 218, 185), (255, 182, 193)], 'accessory': 'seed'
        },
        'parrot': {
            'body': (255, 215, 0), 'wings': (255, 69, 0), 'eyes': (0, 0, 0),
            'pattern': [(255, 215, 0), (255, 69, 0)], 'accessory': 'feather'
        },
        'turtle': {
            'body': (34, 139, 34), 'shell': (139, 69, 19), 'eyes': (0, 0, 0),
            'pattern': [(34, 139, 34), (139, 69, 19)], 'accessory': 'leaf'
        },
        'penguin': {
            'body': (0, 0, 0), 'belly': (255, 255, 255), 'eyes': (255, 255, 255),
            'pattern': [(0, 0, 0), (255, 255, 255)], 'accessory': 'fish'
        },
        'unicorn': {
            'body': (255, 182, 193), 'horn': (255, 215, 0), 'eyes': (138, 43, 226),
            'pattern': [(255, 182, 193), (255, 215, 0)], 'accessory': 'rainbow'
        },
        'panda': {
            'body': (255, 255, 255), 'patches': (0, 0, 0), 'eyes': (0, 0, 0),
            'pattern': [(255, 255, 255), (0, 0, 0)], 'accessory': 'bamboo'
        },
        'fox': {
            'body': (255, 140, 0), 'ears': (255, 69, 0), 'eyes': (0, 0, 0),
            'pattern': [(255, 140, 0), (255, 69, 0)], 'accessory': 'star'
        },
        'dolphin': {
            'body': (135, 206, 235), 'belly': (255, 255, 255), 'eyes': (0, 0, 0),
            'pattern': [(135, 206, 235), (255, 255, 255)], 'accessory': 'wave'
        },
        'owl': {
            'body': (139, 69, 19), 'wings': (160, 82, 45), 'eyes': (255, 255, 0),
            'pattern': [(139, 69, 19), (160, 82, 45)], 'accessory': 'book'
        }
    }
    
    design = pet_designs.get(pet_type, {
        'body': (128, 128, 128), 'eyes': (0, 0, 0),
        'pattern': [(128, 128, 128), (64, 64, 64)], 'accessory': None
    })
    
    # Vẽ pet với thiết kế nâng cao
    if pet_type == 'cat':
        # Thân với hiệu ứng
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Tai nhọn
        draw.polygon([(75, 65), (85, 45), (95, 65)], fill=design['ears'])
        draw.polygon([(105, 65), (115, 45), (125, 65)], fill=design['ears'])
        # Mắt với highlight
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        draw.ellipse([82, 77, 86, 81], fill=(255, 255, 255))  # Highlight
        draw.ellipse([112, 77, 116, 81], fill=(255, 255, 255))  # Highlight
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(255, 105, 180))
        # Đuôi cong
        draw.arc([140, 100, 180, 140], 0, 180, fill=design['body'], width=8)
        # Nơ
        draw.ellipse([85, 70, 95, 80], fill=(255, 105, 180))
        draw.ellipse([105, 70, 115, 80], fill=(255, 105, 180))
        
    elif pet_type == 'dog':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Tai tròn
        draw.ellipse([65, 50, 85, 70], fill=design['ears'])
        draw.ellipse([115, 50, 135, 70], fill=design['ears'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        draw.ellipse([82, 77, 86, 81], fill=(255, 255, 255))  # Highlight
        draw.ellipse([112, 77, 116, 81], fill=(255, 255, 255))  # Highlight
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(0, 0, 0))
        # Đuôi
        draw.arc([140, 100, 180, 140], 0, 180, fill=design['body'], width=8)
        # Vòng cổ
        draw.ellipse([75, 90, 125, 110], fill=(255, 215, 0), width=3)
        
    elif pet_type == 'dragon':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Cánh với hiệu ứng
        draw.ellipse([40, 70, 80, 110], fill=design['wings'])
        draw.ellipse([120, 70, 160, 110], fill=design['wings'])
        # Mắt phát sáng
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        # Sừng
        if 'horn' in design:
            draw.polygon([(90, 60), (95, 40), (100, 60)], fill=design['horn'])
        # Lửa
        for i in range(3):
            draw.polygon([(85+i*5, 50), (90+i*5, 30), (95+i*5, 50)], fill=(255, 69, 0))
        
    elif pet_type == 'rabbit':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Tai dài
        draw.rectangle([75, 40, 85, 70], fill=design['ears'])
        draw.rectangle([115, 40, 125, 70], fill=design['ears'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(255, 182, 193))
        # Cà rốt
        draw.rectangle([170, 100, 180, 120], fill=(255, 69, 0))
        draw.ellipse([165, 95, 185, 105], fill=(34, 139, 34))
        
    elif pet_type == 'hamster':
        # Thân tròn
        draw.ellipse([50, 70, 150, 170], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Má phồng
        draw.ellipse([60, 80, 80, 100], fill=design['cheeks'])
        draw.ellipse([120, 80, 140, 100], fill=design['cheeks'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        # Hạt
        draw.ellipse([170, 120, 180, 130], fill=(139, 69, 19))
        
    elif pet_type == 'parrot':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Cánh
        draw.ellipse([40, 70, 80, 110], fill=design['wings'])
        draw.ellipse([120, 70, 160, 110], fill=design['wings'])
        # Mỏ
        draw.polygon([(90, 85), (100, 95), (110, 85)], fill=(255, 69, 0))
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        # Lông
        for i in range(5):
            draw.line([(160, 80+i*5), (180, 70+i*5)], fill=(255, 215, 0), width=2)
        
    elif pet_type == 'turtle':
        # Mai rùa với hoa văn
        draw.ellipse([50, 70, 150, 170], fill=design['shell'])
        # Hoạ tiết mai
        for i in range(3):
            for j in range(3):
                draw.ellipse([70+i*20, 90+j*20, 80+i*20, 100+j*20], fill=(160, 82, 45))
        # Thân
        draw.ellipse([70, 90, 130, 150], fill=design['body'])
        # Đầu
        draw.ellipse([85, 80, 115, 100], fill=design['body'])
        # Mắt
        draw.ellipse([90, 85, 100, 95], fill=design['eyes'])
        draw.ellipse([100, 85, 110, 95], fill=design['eyes'])
        # Lá
        draw.ellipse([170, 100, 190, 120], fill=(34, 139, 34))
        
    elif pet_type == 'penguin':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Bụng trắng
        draw.ellipse([70, 90, 130, 150], fill=design['belly'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        # Mỏ
        draw.polygon([(95, 85), (100, 95), (105, 85)], fill=(255, 215, 0))
        # Cá
        draw.ellipse([170, 120, 190, 140], fill=(135, 206, 235))
        
    elif pet_type == 'unicorn':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Sừng
        if 'horn' in design:
            draw.polygon([(95, 60), (100, 30), (105, 60)], fill=design['horn'])
        # Bờm cầu vồng
        colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (138, 43, 226)]
        for i, color in enumerate(colors):
            draw.arc([70+i*8, 50, 90+i*8, 70], 0, 180, fill=color, width=3)
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        
    elif pet_type == 'panda':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Mắt đen
        draw.ellipse([75, 70, 95, 90], fill=design['patches'])
        draw.ellipse([105, 70, 125, 90], fill=design['patches'])
        # Tai đen
        draw.ellipse([70, 55, 90, 75], fill=design['patches'])
        draw.ellipse([110, 55, 130, 75], fill=design['patches'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(0, 0, 0))
        # Tre
        draw.rectangle([170, 100, 180, 140], fill=(34, 139, 34))
        
    elif pet_type == 'fox':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Tai nhọn
        draw.polygon([(75, 65), (85, 40), (95, 65)], fill=design['ears'])
        draw.polygon([(105, 65), (115, 40), (125, 65)], fill=design['ears'])
        # Mắt
        draw.ellipse([80, 75, 90, 85], fill=design['eyes'])
        draw.ellipse([110, 75, 120, 85], fill=design['eyes'])
        # Mũi
        draw.ellipse([95, 85, 105, 95], fill=(0, 0, 0))
        # Đuôi
        draw.arc([140, 100, 180, 140], 0, 180, fill=design['body'], width=8)
        # Ngôi sao
        points = [(175, 80), (177, 85), (182, 85), (178, 88), (180, 93), (175, 90), (170, 93), (172, 88), (168, 85), (173, 85)]
        draw.polygon(points, fill=(255, 215, 0))
        
    elif pet_type == 'dolphin':
        # Thân
        draw.ellipse([40, 80, 160, 160], fill=design['body'])
        # Bụng trắng
        draw.ellipse([60, 100, 140, 140], fill=design['belly'])
        # Đầu
        draw.ellipse([70, 70, 130, 110], fill=design['body'])
        # Mắt
        draw.ellipse([85, 85, 95, 95], fill=design['eyes'])
        draw.ellipse([105, 85, 115, 95], fill=design['eyes'])
        # Vây lưng
        draw.polygon([(100, 60), (110, 40), (120, 60)], fill=design['body'])
        # Sóng
        for i in range(3):
            draw.arc([160, 100+i*10, 180, 120+i*10], 0, 180, fill=(135, 206, 235), width=2)
        
    elif pet_type == 'owl':
        # Thân
        draw.ellipse([60, 80, 140, 160], fill=design['body'])
        # Đầu tròn
        draw.ellipse([70, 60, 130, 100], fill=design['body'])
        # Mắt lớn
        draw.ellipse([75, 70, 95, 90], fill=design['eyes'])
        draw.ellipse([105, 70, 125, 90], fill=design['eyes'])
        # Mỏ
        draw.polygon([(95, 85), (100, 95), (105, 85)], fill=(255, 215, 0))
        # Tai
        draw.ellipse([75, 50, 85, 60], fill=design['wings'])
        draw.ellipse([115, 50, 125, 60], fill=design['wings'])
        # Sách
        draw.rectangle([170, 100, 190, 140], fill=(255, 255, 255))
        draw.line([(170, 110), (190, 110)], fill=(0, 0, 0), width=1)
        draw.line([(170, 120), (190, 120)], fill=(0, 0, 0), width=1)
        draw.line([(170, 130), (190, 130)], fill=(0, 0, 0), width=1)
    
    # Thêm hiệu ứng shadow
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse([65, 175, 135, 185], fill=(0, 0, 0, 50))
    
    # Kết hợp shadow với hình chính
    result = Image.alpha_composite(shadow, img)
    
    return result

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
    
    print("Đang tạo hình ảnh Pet nâng cao...")
    
    for pet in pets:
        pet_id = pet['id']
        pet_name = pet['name']
        
        # Tạo hình ảnh
        img = create_enhanced_pet_image(pet_name, pet_id)
        
        # Lưu file
        output_path = os.path.join(pets_dir, f"{pet_id}_enhanced.png")
        img.save(output_path, 'PNG')
        
        print(f"Đã tạo: {pet_name} -> {output_path}")
    
    print("\nHoàn thành! Tất cả hình ảnh Pet nâng cao đã được tạo.")
    print("Các file được lưu trong thư mục: static/pets/")

if __name__ == "__main__":
    main() 