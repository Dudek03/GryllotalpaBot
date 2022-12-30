import os
import urllib.parse
from typing import Union
import requests

from utils.errors import DiscordException

headers = {
    "content-type": "application/json",
    "x-api-key": os.getenv("HUMOR_API_KEY")
}


def get_random_meme(keyword: Union[str, None]):
    url = "https://api.humorapi.com/memes/random"
    if keyword is not None:
        url = f"https://api.humorapi.com/memes/random?keywords={urllib.parse.quote(keyword)}"
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise DiscordException("Meme not Found")
    return response.json()['url']
