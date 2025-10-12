import requests
import os
import argparse


def fetch_spacex_launch(launch_id, save_dir="images"):
    os.makedirs(save_dir, exist_ok=True)
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    parsed_response = response.json()
    img_links = parsed_response.get("links", {}).get("flickr", {},).get("original", [])
    if not img_links:
        print("Нет фотографий для этого запуска")
        return

    for img_number, image_url in enumerate(img_links, start=1):
        filename = f"spacex{img_number}.jpg"
        save_path = os.path.join(save_dir, filename)
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        with open(save_path, "wb") as file:
            file.write(img_response.content)
            print(f'Файл сохранен {save_path}')


def main():
    parser = argparse.ArgumentParser(description="Скачивает фото запуска SpaceX по ID или последнего.")
    parser.add_argument(
        "--id",
        type=str,
        default="latest",
        help="ID запуска SpaceX (по умолчанию — 'latest')"
    )
    args = parser.parse_args()
    fetch_spacex_launch(args.id)


if __name__ == "__main__":
    main()
