import asyncio
from random import shuffle

import discord

from modules.voice.yt import YTDLSource


class Queue(asyncio.Queue):
    def shuffle(self):
        shuffle(self._queue)


class MusicPlayer:

    def __init__(self, ctx, ui):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        self._ui = ui

        self.queue = Queue()
        self.next = asyncio.Event()

        self.volume = 0.5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self._ui.update()
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with asyncio.timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return await self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(
                        source, loop=self.bot.loop
                    )
                except Exception as e:
                    await self._channel.send(
                        f"There was an error processing your song.\n"
                        f"```css\n[{e}]\n```"
                    )
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(
                source,
                after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set),
            )

            # TODO: Option to enable this
            if False:
                embed = discord.Embed(
                    title="Now playing",
                    description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]",
                    color=discord.Color.green(),
                )
                await self._channel.send(embed=embed)

            await self.update_ui()
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            # source.cleanup()
            self.current = None

    async def update_ui(self):
        if self._ui is not None:
            await self._ui.update()

    async def add_to_queue(self, sources):
        for source in sources:
            await self.queue.put(source)

    async def destroy(self, guild):
        """Disconnect and cleanup the player."""
        res = self.bot.loop.create_task(self._cog.cleanup(guild))
        await self.update_ui()
        return res
