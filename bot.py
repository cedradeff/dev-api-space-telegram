import os
from dotenv import load_dotenv
from telegram import Bot
import time
import random
import argparse


load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHANNEL_ID = os.getenv("TG_CHANNEL_ID")
bot = Bot(token=BOT_TOKEN)
DEFAULT_DELAY_HOURS = 4


def get_image_list():
    IMAGES_DIR = "images"
    supported_ext = (".jpg", ".jpeg", ".png", ".gif")
    files = [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.lower().endswith(supported_ext)]
    return files


def publish_images(bot: Bot, delay_hours: int):
    images = get_image_list()
    if not images:
        print("В папке 'images' нет изображений.")
        return

    published = []

    while True:
        if len(published) == len(images):
            print("Все фото опубликованы. Цикл начинается заново")
            published.clear()
            random.shuffle(images)

        for img_path in images:
            if img_path in published:
                continue

            try:
                print(f"Отправка: {img_path}")
                with open(img_path, "rb") as photo:
                    bot.send_photo(chat_id=CHANNEL_ID, photo=photo)
                published.append(img_path)
            except Exception as e:
                print(f"Ошибка при отправке {img_path}: {e}")

            print(f"Следующая публикация через {delay_hours} часов...")
            time.sleep(delay_hours * 3600)


def main():
    parser = argparse.ArgumentParser(description="Автоматическая публикация изображений в Telegram-канал.")
    parser.add_argument("--delay", type=float, default=float(os.getenv("PUBLISH_DELAY_HOURS", DEFAULT_DELAY_HOURS)),
                        help="Задержка между публикациями (в часах). По умолчанию 4.")
    args = parser.parse_args()
    if not BOT_TOKEN or not CHANNEL_ID:
        print("Ошибка: не задан TG_BOT_TOKEN или TG_CHANNEL_ID.")
        return
    bot = Bot(token=BOT_TOKEN)
    print(f"Старт публикаций каждые {args.delay} часов в канал {CHANNEL_ID}")
    publish_images(bot, args.delay)


if __name__ == "__main__":
    main()
