import asyncio
import itertools
from random import random

import discord
from discord.ext import commands

from modules.voice.yt import YTDLSource
from utils.command import command
from utils.errors import DiscordException

from modules.voice.music_player import MusicPlayer


class Music(commands.GroupCog, group_name='voice'):

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @command(
        name="join", description="connects to voice"
    )
    async def connect_(self, ctx, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = discord.Embed(
                    title="",
                    description="No channel to join. Please call `,join` from a voice channel.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                raise DiscordException(
                    "No channel to join. Please either specify a valid channel or join one."
                )

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise DiscordException(f"Moving to channel: <{channel}> timed out.")
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise DiscordException(
                    f"Connecting to channel: <{channel}> timed out."
                )
        await ctx.send(f"**Joined `{channel}`**")

    @command(name="play", description="streams music", long=True)
    async def play_(self, ctx, search: str, count=1):
        vc = ctx.voice_client

        if not vc:
            raise DiscordException("Need to join first")

        player = self.get_player(ctx)

        sources = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, count=count)
        for source in sources:
            await player.queue.put(source)

    @command(
        name="shuffle", description="make mess in queue"
    )
    async def random_(
        self,
        ctx,
    ):
        vc = ctx.voice_client
        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        player.queue.shuffle()

        embed = discord.Embed(
            title="Queue",
            description="There is a slight mess in the queue. 🎲",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @command(name="pause", description="pauses music")
    async def pause_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(
                title="",
                description="I am currently not playing anything",
                color=discord.Color.green(),
            )
            return await ctx.send(embed=embed)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send("Paused ⏸️")

    @command(name="resume", description="resumes music")
    async def resume_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(
                title="",
                description="I'm not connected to a voice channel",
                color=discord.Color.red(),
            )
            return await ctx.send(embed=embed)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send("Resuming ⏯️")

    @command(
        name="skip", description="skips to next song in queue"
    )
    async def skip_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            raise DiscordException("I'm not connected to a voice channel")

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        embed = discord.Embed(
            title="Skipping",
            description="Let's play something else",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

        vc.stop()

    @command(
        name="remove",
        aliases=["rm", "rem"],
        description="removes specified song from queue",
    )
    async def remove_(self, ctx, pos: int = None):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            raise DiscordException("I'm not connected to a voice channel")

        player = self.get_player(ctx)
        if pos == None:
            player.queue._queue.pop()
        else:
            try:
                s = player.queue._queue[pos - 1]
                del player.queue._queue[pos - 1]
                embed = discord.Embed(
                    title="",
                    description=f"Removed [{s['title']}]({s['webpage_url']}) [{s['requester'].mention}]",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
            except:
                raise DiscordException(f'Could not find a track for "{pos}"')

    @command(
        name="clear", description="clears entire queue"
    )
    async def clear_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            raise DiscordException("I'm not connected to a voice channel")

        player = self.get_player(ctx)
        player.queue.empty()
        await ctx.send("**Cleared**")

    @command(
        name="queue", aliases=["q", "playlist", "que"], description="shows the queue"
    )
    async def queue_info(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            raise DiscordException("I'm not connected to a voice channel")

        player = self.get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(
                title="", description="queue is empty", color=discord.Color.green()
            )
            return await ctx.send(embed=embed)

        seconds = vc.source.duration % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        # Grabs the songs in the queue...
        upcoming = list(
            itertools.islice(player.queue._queue, 0, int(len(player.queue._queue)))
        )
        fmt = "\n".join(
            f"`{(upcoming.index(_)) + 1}.` [{_['title']}]({_['webpage_url']}) | ` {duration} Requested by: {_['requester']}`\n"
            for _ in upcoming
        )
        fmt = (
            f"\n__Now Playing__:\n[{vc.source.title}]({vc.source.web_url}) | ` {duration} Requested by: {vc.source.requester}`\n\n__Up Next:__\n"
            + fmt
            + f"\n**{len(upcoming)} songs in queue**"
        )
        embed = discord.Embed(
            title=f"Queue for {ctx.guild.name}",
            description=fmt,
            color=discord.Color.green(),
        )

        await ctx.send(embed=embed)

    @command(
        name="now playing",
        description="shows the current playing song",
    )
    async def now_playing_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            raise DiscordException("I'm not connected to a voice channel")

        player = self.get_player(ctx)
        if not player.current:
            raise DiscordException("I am currently not playing anything")

        seconds = vc.source.duration % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)
        embed = discord.Embed(
            title="",
            description=f"[{vc.source.title}]({vc.source.web_url}) [{vc.source.requester.mention}] | `{duration}`",
            color=discord.Color.green(),
        )
        print(ctx)
        await ctx.send(embed=embed)

    @command(name="volume", aliases=["vol", "v"], description="Changes volume")
    async def change_volume(self, ctx, *, vol: float = None):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            raise DiscordException("I'm not connected to a voice channel")

        if not vol:
            embed = discord.Embed(
                title="",
                description=f"🔊 **{(vc.source.volume) * 100}%**",
                color=discord.Color.green(),
            )
            return await ctx.send(embed=embed)

        if not 0 < vol < 101:
            raise DiscordException("Please enter a value between 1 and 100")

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        embed = discord.Embed(
            title="",
            description=f"**`{ctx.author}`** set the volume to **{vol}%**",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @command(
        name="leave",
        description="Stops music and disconnects from voice",
    )
    async def leave_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            raise DiscordException("I'm not connected to a voice channel")

        await ctx.send("**Successfully disconnected**")

        await self.cleanup(ctx.guild)
