import os
from dotenv import load_dotenv
import random
import argparse
import sys
from telegram import Bot


load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHANNEL_ID = os.getenv("TG_CHANNEL_ID")
IMAGES_DIR = "images"


def get_random_image():
    supported_ext = (".jpg", ".jpeg", ".png", ".gif")
    images = [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.lower().endswith(supported_ext)]
    if not images:
        print("В папке 'images' нет изображений.")
        sys.exit(1)
    return random.choice(images)


def send_photo(photo_path, caption=None):
    """Отправляет фото в Telegram-канал."""
    bot_token = os.getenv("TG_BOT_TOKEN")
    channel_id = os.getenv("TG_CHANNEL_ID")

    if not bot_token or not channel_id:
        print("Ошибка: не заданы TELEGRAM_BOT_TOKEN и TELEGRAM_CHANNEL_ID.")
        sys.exit(1)

    bot = Bot(token=bot_token)

    try:
        with open(photo_path, "rb") as photo:
            print(f"Отправка фото {photo_path} в {channel_id} ...")
            bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)
        print("Фото успешно отправлено")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Отправка одной фотографии в Telegram-канал."
    )
    parser.add_argument(
        "--photo",
        type=str,
        help="Путь к фото (если не указано — выбирается случайное из папки images/)."
    )
    args = parser.parse_args()

    # Определяем, какое фото использовать
    if args.photo:
        if not os.path.exists(args.photo):
            print(f"Файл не найден: {args.photo}")
            sys.exit(1)
        photo_path = args.photo
    else:
        photo_path = get_random_image()
        print(f"Фото не указано, выбрано случайное: {photo_path}")

    # Отправляем
    send_photo(photo_path)


if __name__ == "__main__":
    main()
