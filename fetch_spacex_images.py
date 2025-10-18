import os
import argparse
from file_helpers import download_images
from api_helpers import make_spacex_request


def extract_spacex_image_links(parsed_response):
    img_links = parsed_response.get("links", {}).get("flickr", {}).get("original", [])
    if not img_links:
        print("Нет фотографий для этого запуска")
    return img_links


def fetch_spacex_launch(launch_id, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    parsed_response = make_spacex_request(launch_id)
    img_links = extract_spacex_image_links(parsed_response)
    if not img_links:
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
