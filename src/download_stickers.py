import os
import zipfile
import urllib.request

STICKER_SOURCES = [
    # Emoji PNG pack (Google Noto Emoji)
    {
        "url": "https://github.com/googlefonts/noto-emoji/raw/main/png/128/emoji_u1f60a.png",
        "filename": "emoji_smile.png"
    },
    {
        "url": "https://github.com/googlefonts/noto-emoji/raw/main/png/128/emoji_u1f602.png",
        "filename": "emoji_laugh.png"
    },
    {
        "url": "https://github.com/googlefonts/noto-emoji/raw/main/png/128/emoji_u1f62d.png",
        "filename": "emoji_cry.png"
    },
    {
        "url": "https://github.com/googlefonts/noto-emoji/raw/main/png/128/emoji_u1f44d.png",
        "filename": "emoji_thumbsup.png"
    },
    # Meme PNG
    {
        "url": "https://i.imgur.com/8p0p3bA.png",
        "filename": "meme_doge.png"
    },
    {
        "url": "https://i.imgur.com/4M7IWwP.png",
        "filename": "meme_pepe.png"
    },
    {
        "url": "https://i.imgur.com/1Q9Z1Zm.png",
        "filename": "meme_trollface.png"
    },
    # Animal stickers
    {
        "url": "https://i.imgur.com/2Ro1FQm.png",
        "filename": "cat_cute.png"
    },
    {
        "url": "https://i.imgur.com/1Juc5hF.png",
        "filename": "dog_funny.png"
    },
]

DEST_DIR = os.path.join("data", "stickers")

def download_stickers():
    os.makedirs(DEST_DIR, exist_ok=True)
    for s in STICKER_SOURCES:
        dest = os.path.join(DEST_DIR, s["filename"])
        print(f"Đang tải: {s['url']} -> {dest}")
        try:
            urllib.request.urlretrieve(s["url"], dest)
            print(f"Tải xong: {s['filename']}")
        except Exception as e:
            print(f"Lỗi khi tải {s['url']}: {e}")

def main():
    download_stickers()
    print("Đã tải xong các sticker mẫu! Bạn có thể mở app và sử dụng ngay.")

if __name__ == "__main__":
    main() 