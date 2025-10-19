import os
from dotenv import load_dotenv
from telegram import Bot
import time
import random
import argparse
from file_helpers import send_photo_via_bot
import requests


def get_image_list(images_dir):
    supported_ext = (".jpg", ".jpeg", ".png", ".gif")
    files = [
        os.path.join(images_dir, f)
        for f in os.listdir(images_dir)
        if f.lower().endswith(supported_ext)]
    return files


def get_shuffled_images(images_dir):
    images = get_image_list(images_dir)
    if not images:
        raise FileNotFoundError(f"В папке '{images_dir}' не найдено изображений")
    random.shuffle(images)
    return images


def publish_images(bot, channel_id, delay_hours, images_dir, retry_delay=30):
    while True:
        images = get_shuffled_images(images_dir)
        print("Новый цикл публикации")

        for img_path in images:
            while True:
                try:
                    send_photo_via_bot(bot, channel_id, img_path)
                    print(f"Отправлено: {os.path.basename(img_path)}")
                    break

                except (requests.exceptions.RequestException, ConnectionError) as e:
                    print(f"Ошибка соединения: {e}")
                    print(f"Повторная попытка через {retry_delay} секунд")
                    time.sleep(retry_delay)
                    continue

                except Exception as e:
                    print(f"Неожиданная ошибка при отправке {img_path}: {e}")
                    break

            print(f"Следующая публикация через {delay_hours} часов")
            time.sleep(delay_hours * 3600)


def main():
    load_dotenv()
    bot_token = os.environ["TG_BOT_TOKEN"]
    channel_id = os.environ["TG_CHANNEL_ID"]
    bot = Bot(token=bot_token)
    default_delay_hours = 4

    parser = argparse.ArgumentParser(
        description="Автоматическая публикация изображений в Telegram-канал."
    )
    parser.add_argument(
        "--delay", type=float,
        default=default_delay_hours,
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
    print(f"Старт публикаций каждые {args.delay} часов в канал {channel_id}")
    try:
        publish_images(bot, channel_id, args.delay, images_dir)
    except FileNotFoundError as e:
        print(f"Ошибка выбора файла {e}")


if __name__ == "__main__":
    main()
