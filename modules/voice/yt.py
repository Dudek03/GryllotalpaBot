import asyncio
from functools import partial

from youtube_dl import YoutubeDL
import youtube_dl
import discord

from utils.errors import DiscordException

youtube_dl.utils.bug_reports_message = lambda: ""

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

ffmpegopts = {"before_options": "-nostdin", "options": "-vn"}

ytdl = YoutubeDL(ytdlopts)


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
    async def create_source(cls, ctx, search: str, *, loop, count):

        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=False)
        data = await loop.run_in_executor(None, to_run)

        if count < 0:
            raise DiscordException("Invalid count")

        if "entries" in data:
            if count == 0:
                data = data["entries"]
            else:
                data = data["entries"][:count]

        list = [f"[{d['title']}]({d['webpage_url']})" for d in data]
        list = '\n'.join(list)
        embed = discord.Embed(
            title="",
            description=f"Queued\n {list}\n[{ctx.author.mention}]",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

        return [{
            "webpage_url": d["webpage_url"],
            "requester": ctx.author,
            "title": d["title"],
        } for d in data]

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data["requester"]

        to_run = partial(ytdl.extract_info, url=data["webpage_url"], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data["url"]), data=data, requester=requester)
