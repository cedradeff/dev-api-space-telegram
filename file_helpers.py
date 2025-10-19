import os
import requests
from urllib.parse import urlparse


def get_file_extension(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = os.path.splitext(path)[1].lower()
    return ext if ext else ".jpg"


def save_image_to_disk(image_content, save_path):
    with open(save_path, "wb") as file:
        file.write(image_content)
    print(f"Файл сохранен {save_path}")


def download_images(img_links, save_dir, filename_prefix):
    for img_number, image_url in enumerate(img_links, start=1):
        ext = get_file_extension(image_url)
        filename = f"{filename_prefix}_{img_number}{ext}"
        save_path = os.path.join(save_dir, filename)
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        save_image_to_disk(img_response.content, save_path)


def send_photo_via_bot(bot, chat_id, photo_path, caption=None):
    with open(photo_path, "rb") as photo:
        print(f"Отправка фото {photo_path} в {chat_id} ...")
        bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
    print(f"Фото успешно отправлено: {photo_path}")
