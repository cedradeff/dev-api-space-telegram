import os
from urllib.parse import urlparse


def get_file_extension(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = os.path.splitext(path)[1].lower()
    return ext if ext else ".jpg"
