import requests
import os
from dotenv import load_dotenv
from file_helpers import get_file_extension


def fetch_nasa_apod(url, save_dir="images"):
    token = os.environ["NASA_TOKEN"]
    os.makedirs(save_dir, exist_ok=True)
    payload = {"api_key": token, "count": 5}
    response = requests.get(url, params=payload)
    response.raise_for_status()

    apods = response.json()

    for i, apod in enumerate(apods, start=1):
        image_url = apod.get("url")
        if not image_url:
            continue

        ext = get_file_extension(image_url)
        filename = f"nasa_apod_{i}{ext}"
        save_path = os.path.join(save_dir, filename)

        # Загружаем и сохраняем картинку
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        with open(save_path, "wb") as file:
            file.write(img_response.content)
            print(f"✅ Файл сохранён: {save_path}")


def main():
    load_dotenv()
    fetch_nasa_apod("https://api.nasa.gov/planetary/apod")


if __name__ == "__main__":
    main()
