import os
from dotenv import load_dotenv
import random
import argparse
import sys
from telegram import Bot
from file_helpers import send_photo_via_bot


def get_random_image(images_dir):
    supported_ext = (".jpg", ".jpeg", ".png", ".gif")
    images = [
        os.path.join(images_dir, f)
        for f in os.listdir(images_dir)
        if f.lower().endswith(supported_ext)]
    if not images:
        print(f"В папке {images_dir} нет изображений.")
        sys.exit(1)
    return random.choice(images)


def send_photo(bot_token, channel_id, photo_path, caption=None):
    """Отправляет фото в Telegram-канал."""

    if not bot_token or not channel_id:
        raise ValueError("Не заданы TG_BOT_TOKEN и TG_CHANNEL_ID")
    bot = Bot(token=bot_token)
    send_photo_via_bot(bot, channel_id, photo_path, caption)


def main():
    load_dotenv()
    bot_token = os.environ["TG_BOT_TOKEN"]
    channel_id = os.environ["TG_CHANNEL_ID"]
    parser = argparse.ArgumentParser(
        description="Отправка одной фотографии в Telegram-канал."
    )
    parser.add_argument(
        "--photo",
        type=str,
        help="Путь к изображению"
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        help="Путь к папке с изображениями (по умолчанию — из .env или 'images')."
    )
    args = parser.parse_args()

    images_dir = (
        args.images_dir
        or os.environ("IMAGES_DIR")
        or "images"
    )

    # Определяем, какое фото использовать
    if args.photo:
        if not os.path.exists(args.photo):
            print(f"Файл не найден: {args.photo}")
            sys.exit(1)
        photo_path = args.photo
    else:
        photo_path = get_random_image(images_dir)
        print(f"Фото не указано, выбрано случайное: {photo_path}")

    # Отправляем
    try:
        send_photo(bot_token, channel_id, photo_path)
    except ValueError as e:
        print(f"Ошибка при отправке фото: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
