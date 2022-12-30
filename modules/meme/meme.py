import asyncio
from typing import Optional

from discord.ext import commands
from discord.app_commands.commands import Command
from discord.ui import View

from modules.meme.humorApi import get_random_meme
from utils.command import command
from utils.errors import DiscordException


class Meme(commands.GroupCog, group_name='meme'):
    def __init__(self, bot):
        self.bot = bot

    @command(name="random", description="get random meme", is_hidden=False)
    async def random_meme(self, ctx):
        url = get_random_meme(None)
        await ctx.send(url)

    @command(name="search", description="get random meme with keyword", is_hidden=False)
    async def search_meme(self, ctx, keywords: str):
        url = get_random_meme(keywords)
        await ctx.send(url)
