import asyncio
from functools import partial

import discord
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from utils.errors import DiscordException


ytdlopts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # ipv6 addresses cause issues sometimes
}

ytdl = YoutubeDL(ytdlopts)


def is_url(search: str):
    return search.startswith("http://") or search.startswith("https://")


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get("title")
        self.web_url = data.get("webpage_url")
        self.duration = data.get("duration")

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, author, search: str, *, loop, count):

        loop = loop or asyncio.get_event_loop()

        if is_url(search):
            to_run = partial(ytdl.extract_info, url=search, download=False)
            data = await loop.run_in_executor(None, to_run)

            if data.get("entries") is not None:
                if count < 0:
                    raise DiscordException("Invalid count")

                if "entries" in data:
                    if count == 0:
                        data = data["entries"]
                    else:
                        data = data["entries"][:count]
            else:
                data = [data]
            return [{
                "webpage_url": d["webpage_url"],
                "requester": author,
                "title": d["title"],
            } for d in data]
        else:
            data = YoutubeSearch(search, max_results=count).to_dict()
            return [{
                "webpage_url": "https://www.youtube.com" + d["url_suffix"],
                "requester": author,
                "title": d["title"],
            } for d in data]

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data["requester"]

        to_run = partial(ytdl.extract_info, url=data["webpage_url"], download=False)
        data = await loop.run_in_executor(None, to_run)
        return cls(discord.FFmpegPCMAudio(data["url"]), data=data, requester=requester)
