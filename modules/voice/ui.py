import itertools

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View

from modules.voice.utils import get_duration
from modules.voice.views.player import player_view
from modules.voice.views.ready import ready_view
from modules.voice.views.refresh import refresh_view


class UI:
    def __init__(self, ctx: commands.Context, music_cog):
        super().__init__()
        self.ctx = ctx
        self.music_cog = music_cog
        self.interaction = None
        self.message = None
        self.view = View(timeout=None)

    async def init(self):
        refresh_view(self.view, self)
        self.message = await self.ctx._send(
            content="",
            embed=Embed(title="Player",
                        description="Waiting for interaction",
                        color=discord.Color.blue()),
            view=self.view
        )
        self.interaction = self.ctx.interaction

    async def update(self):
        vc = self.ctx.voice_client
        refresh_view(self.view, self)
        if not vc or not vc.is_connected():
            await self.message.edit(
                view=self.view,
                content="",
                embed=Embed(title="Player",
                            description="Not connected",
                            color=discord.Color.red())
            )
            return

        player = self.music_cog.get_player(self.ctx)
        ready_view(self.view, self)
        title = f"Player on {vc.channel}"
        if not player.current:
            await self.message.edit(
                view=self.view,
                content="",
                embed=Embed(title=title,
                            description="Nothing playing",
                            color=discord.Color.green())
            )
            return

        queue_size = player.queue.qsize()
        upcoming = list(
            itertools.islice(player.queue._queue, 0, int(len(player.queue._queue)))
        )
        description = f"NOW PLAYING:\n[{vc.source.title}]({vc.source.web_url}) [{vc.source.requester.mention}] | `{get_duration(self.ctx)}`\n"
        if queue_size > 0:
            ele = upcoming[0]
            description += f"Next: [{ele['title']}]({ele['webpage_url']})\n"
        description += f"Left in queue: {queue_size}"
        player_view(self.view, self)

        embed = Embed(
            title=title,
            description=description,
            color=discord.Color.green(),
        )
        await self.message.edit(
            content="",
            embed=embed,
            view=self.view,
        )
