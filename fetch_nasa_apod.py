import os
from dotenv import load_dotenv
from file_helpers import download_image
import argparse
from api_helpers import make_nasa_request


def extract_image_links(apods):
    img_links = [apod["url"] for apod in apods if apod.get("url")]
    if not img_links:
        print("Нет доступных изображений NASA APOD")
    return img_links


def fetch_nasa_apod(nasa_token, url, save_dir, count):
    os.makedirs(save_dir, exist_ok=True)
    apods = make_nasa_request(nasa_token, url, count)
    img_links = extract_image_links(apods)

    if not img_links:
        return

    for img_number, image_url in enumerate(img_links, start=1):
        download_image(image_url, save_dir, filename_prefix="nasa_apod", img_number=img_number)


def main():
    load_dotenv()
    nasa_token = os.environ['NASA_TOKEN']

    parser = argparse.ArgumentParser(
        description="Скачивает случайные изображения NASA APOD."
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        help="Путь к папке для сохранения изображений (по умолчанию — из .env или 'images')."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Количество изображений для скачивания (по умолчанию 5)."
    )
    args = parser.parse_args()

    # Определяем папку для сохранения
    save_dir = (
        args.images_dir
        or os.environ.get("IMAGES_DIR")
        or "images"
    )

    fetch_nasa_apod(
        nasa_token,
        "https://api.nasa.gov/planetary/apod",
        save_dir, args.count)


if __name__ == "__main__":
    main()
