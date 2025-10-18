import requests
import os
import argparse
from file_helpers import download_images


def fetch_spacex_launch(launch_id, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    parsed_response = response.json()
    img_links = parsed_response.get("links", {}).get("flickr", {},).get("original", [])
    if not img_links:
        print("Нет фотографий для этого запуска")
        return
    download_images(img_links, save_dir, filename_prefix="spacex_apod")


def main():
    parser = argparse.ArgumentParser(
        description="Скачивает фото запуска SpaceX по ID или последнего."
    )
    parser.add_argument(
        "--id",
        type=str,
        default="latest",
        help="ID запуска SpaceX (по умолчанию — 'latest')"
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        help="Путь к папке для сохранения изображений (по умолчанию — из .env или 'images')."
    )

    args = parser.parse_args()
    save_dir = (
        args.images_dir
        or os.environ.get("IMAGES_DIR")
        or "images"
    )

    fetch_spacex_launch(args.id, save_dir)


if __name__ == "__main__":
    main()
