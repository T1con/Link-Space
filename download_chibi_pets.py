import os
import requests

# Danh sách pet và link ảnh chibi tương ứng
pet_images = {
    'cat': 'https://cdn-icons-png.flaticon.com/512/616/616452.png',
    'dog': 'https://cdn-icons-png.flaticon.com/512/616/616448.png',
    'rabbit': 'https://cdn-icons-png.flaticon.com/512/616/616453.png',
    'hamster': 'https://cdn-icons-png.flaticon.com/512/616/616454.png',
    'parrot': 'https://cdn-icons-png.flaticon.com/512/616/616455.png',
    'turtle': 'https://cdn-icons-png.flaticon.com/512/616/616456.png',
    'penguin': 'https://cdn-icons-png.flaticon.com/512/616/616457.png',
    'unicorn': 'https://cdn-icons-png.flaticon.com/512/616/616458.png',
    'panda': 'https://cdn-icons-png.flaticon.com/512/616/616459.png',
    'fox': 'https://cdn-icons-png.flaticon.com/512/616/616460.png',
    'dolphin': 'https://cdn-icons-png.flaticon.com/512/616/616461.png',
    'owl': 'https://cdn-icons-png.flaticon.com/512/616/616462.png',
    # Pet rồng - chọn hình ngầu nhất
    'dragon': 'https://cdn-icons-png.flaticon.com/512/616/616463.png',
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