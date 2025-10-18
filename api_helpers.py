import requests


def make_nasa_request(nasa_token, url, count):
    payload = {"api_key": nasa_token, "count": count}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def make_spacex_request(launch_id):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
