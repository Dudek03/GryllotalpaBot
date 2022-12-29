import asyncio

from discord.ext import commands
from discord.app_commands.commands import Command

from modules.meme.humorApi import get_random_meme
from utils.command import command
from utils.errors import DiscordException


async def setup(bot: commands.Bot):
    @command(group=bot)
    async def meme(ctx: commands.Context, keyword: str):
        if keyword == "":
            keyword = None

        url = get_random_meme(keyword)
        await ctx.send(url)
