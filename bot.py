import os
from dotenv import load_dotenv
from telegram import Bot
import time
import random
import argparse
from file_helpers import send_photo_via_bot


def get_image_list(images_dir):
    supported_ext = (".jpg", ".jpeg", ".png", ".gif")
    files = [
        os.path.join(images_dir, f)
        for f in os.listdir(images_dir)
        if f.lower().endswith(supported_ext)]
    return files


def shuffle_images(images_dir):
    """Получает и перемешивает список изображений из папки."""
    images = get_image_list(images_dir)
    if not images:
        raise FileNotFoundError(f"В папке '{images_dir}' не найдено изображений")
    random.shuffle(images)
    return images


def publish_single_image(bot, channel_id, img_path):
    """Отправляет одно изображение через бота."""
    send_photo_via_bot(bot, channel_id, img_path)
    print(f"Отправлено: {os.path.basename(img_path)}")


def wait_for_next_publication(delay_hours):
    """Задержка перед следующей публикацией."""
    print(f"Следующая публикация через {delay_hours} часов...")
    time.sleep(delay_hours * 3600)


def publish_images(bot, channel_id, delay_hours, images_dir):
    """Основной цикл публикации изображений."""
    images = shuffle_images(images_dir)
    published = []

    while True:
        if len(published) == len(images):
            print("Все фото опубликованы. Цикл начинается заново.")
            published.clear()
            random.shuffle(images)

        for img_path in images:
            if img_path in published:
                continue

            publish_single_image(bot, channel_id, img_path)
            published.append(img_path)
            wait_for_next_publication(delay_hours)


def main():
    load_dotenv()
    bot_token = os.environ["TG_BOT_TOKEN"]
    channel_id = os.environ["TG_CHANNEL_ID"]
    bot = Bot(token=bot_token)
    DEFAULT_DELAY_HOURS = 4

    parser = argparse.ArgumentParser(
        description="Автоматическая публикация изображений в Telegram-канал."
    )
    parser.add_argument(
        "--delay", type=float,
        default=DEFAULT_DELAY_HOURS,
        help="Задержка между публикациями (в часах). По умолчанию 4."
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        help="Путь к папке с изображениями (по умолчанию — из .env или 'images')"
    )
    args = parser.parse_args()

    images_dir = (
        args.images_dir
        or os.environ.get("IMAGES_DIR")
        or "images"
    )

    if not bot_token or not channel_id:
        print("Ошибка: не задан TG_BOT_TOKEN или TG_CHANNEL_ID.")
        return
    bot = Bot(token=bot_token)
    print(f"Старт публикаций каждые {args.delay} часов в канал {channel_id}")
    try:
        publish_images(bot, channel_id, args.delay, images_dir)
    except FileNotFoundError as e:
        print(f"Ошибка выбора файла {e}")


if __name__ == "__main__":
    main()
