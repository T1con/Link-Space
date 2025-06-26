import os
import requests

pet_images = {
    'cat': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/cat-2022346_1280.png',
    'dog': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/dog-2022344_1280.png',
    'dragon': 'https://cdn.pixabay.com/photo/2021/01/15/15/06/dragon-5919932_1280.png',
    'rabbit': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/rabbit-2022347_1280.png',
    'hamster': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/hamster-2022345_1280.png',
    'parrot': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/parrot-2022348_1280.png',
    'turtle': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/turtle-2022350_1280.png',
    'penguin': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/penguin-2022349_1280.png',
    'unicorn': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/unicorn-2022351_1280.png',
    'panda': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/panda-2022343_1280.png',
    'fox': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/fox-2022342_1280.png',
    'dolphin': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/dolphin-2022341_1280.png',
    'owl': 'https://cdn.pixabay.com/photo/2017/01/31/13/14/owl-2022340_1280.png',
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_image(url, path):
    try:
        r = requests.get(url, headers=headers, timeout=10)
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
    print("\nHoàn thành! Hãy làm mới trang profile để xem ảnh chibi đúng cho từng pet.") 