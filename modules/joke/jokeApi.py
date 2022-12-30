import requests

from utils.errors import DiscordException

headers = {
    "content-type": "application/json",
}


def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise DiscordException("Joke not Found")
    return response.json()
