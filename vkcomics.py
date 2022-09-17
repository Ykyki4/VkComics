import random
import requests
import os

from pathlib import Path, PurePath
from environs import Env


def download_comics_image(image_url, comics_name):
    response = requests.get(image_url)
    response.raise_for_status()
    filename = f"{comics_name}.png"
    Path("images/").mkdir(parents=True, exist_ok=True)
    path = PurePath("images", filename)
    with open(path, 'wb') as file:
        file.write(response.content)
        return path

def post_image_to_server(image_url, comics_name, upload_url):
    try:
        path = download_comics_image(image_url, comics_name)
        with open(path, 'rb') as file:
            files = {"photo": file}
            response = requests.post(upload_url, files=files)
            response.raise_for_status()
    finally:
        os.remove(path)
    return response.json()


def post_image_to_album(server_post_response, access_token, api_version):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "server": server_post_response["server"],
        "photo": server_post_response["photo"],
        "hash": server_post_response["hash"],
        "access_token": access_token,
        "v": api_version
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def post_image_to_wall(album_post_response, api_version, commics_message):
    owner_id = album_post_response["response"][0]["owner_id"]
    media_id = album_post_response["response"][0]["id"]
    url = "https://api.vk.com/method/wall.post"
    params = {"access_token": access_token,
              "v": api_version,
              "attachments": f"photo{owner_id}_{media_id}",
              "owner_id": -215997139,
              "from_group": 1,
              "message": commics_message
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.text


def request_upload_url(access_token, api_version):
    url = f"https://api.vk.com/method/photos.getWallUploadServer"
    params = {"access_token": access_token,
              "v": api_version}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    client_id = env("CLIENT_ID")
    access_token = env("VK_ACCESS_TOKEN")
    api_version = 5.131

    comics_url = f"https://xkcd.com/{random.randrange(1, 999)}/info.0.json"

    response = requests.get(comics_url)
    response.raise_for_status()
    comics_response = response.json()

    upload_url = request_upload_url(
        access_token, api_version)["response"]["upload_url"]
    image_url = comics_response["img"]

    comics_name = comics_response["safe_title"]
    server_post_response = post_image_to_server(
        image_url, comics_name, upload_url)
    album_post_response = post_image_to_album(
        server_post_response, access_token, api_version)
    commics_message = comics_response["alt"]


    print(post_image_to_wall(
        album_post_response, api_version, commics_message))
