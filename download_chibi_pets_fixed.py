import os
import requests

pet_images = {
    'cat': 'https://cdn-icons-png.flaticon.com/512/616/616408.png',      # Mèo
    'dog': 'https://cdn-icons-png.flaticon.com/512/616/616408.png',      # Chó
    'dragon': 'https://cdn-icons-png.flaticon.com/512/616/616430.png',   # Rồng (ngầu)
    'rabbit': 'https://cdn-icons-png.flaticon.com/512/616/616418.png',   # Thỏ
    'hamster': 'https://cdn-icons-png.flaticon.com/512/616/616419.png',  # Hamster
    'parrot': 'https://cdn-icons-png.flaticon.com/512/616/616420.png',   # Vẹt
    'turtle': 'https://cdn-icons-png.flaticon.com/512/616/616421.png',   # Rùa
    'penguin': 'https://cdn-icons-png.flaticon.com/512/616/616422.png',  # Cánh cụt
    'unicorn': 'https://cdn-icons-png.flaticon.com/512/616/616423.png',  # Kỳ lân
    'panda': 'https://cdn-icons-png.flaticon.com/512/616/616424.png',    # Gấu trúc
    'fox': 'https://cdn-icons-png.flaticon.com/512/616/616425.png',      # Cáo
    'dolphin': 'https://cdn-icons-png.flaticon.com/512/616/616426.png',  # Cá heo
    'owl': 'https://cdn-icons-png.flaticon.com/512/616/616427.png',      # Cú
}

def download_image(url, path):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(path, 'wb') as f:
            f.write(r.content)
        print(f"✓ Đã tải: {path}")
    except Exception as e:
        print(f"✗ Lỗi tải {url}: {e}")

if __name__ == "__main__":
    os.makedirs('static/pets', exist_ok=True)
    for pet, url in pet_images.items():
        filename = f'static/pets/{pet}.png'
        download_image(url, filename)
    print("\nHoàn thành! Hãy làm mới trang profile để xem ảnh chibi mới cho các pet.") 