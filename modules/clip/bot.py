from random import random

import discord
from discord import Color
from discord.ext import commands

from utils.command import command
from utils.errors import DiscordException


class Clip(commands.GroupCog, group_name='clip'):
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    @command(
        name="record", description="Start recording for clipping"
    )
    async def record_(self, ctx):

        ctx.voice_client.listen()
        embed = discord.Embed(title="Started the recording for clipping!",
                              description="Use /clip to clip or /stop to end recording.", color=Color.green())
        await ctx.send(embed=embed)

    @command(
        name="stop", description="Stop recording for clipping", long=True
    )
    async def stop_(self, ctx: commands.Context):
        if not ctx.voice_client.is_recording():
            return

        wav_bytes = await ctx.voice_client.stop_record()

        name = str(random.randint(000000, 999999))
        f_name = f'{name}.wav'
        with open(f_name, 'wb') as f:
            f.write(wav_bytes)

        await ctx.send(f'Stopping the Recording', file=discord.File(f_name))
