from discord.ext import commands

from modules.meme.humor_api import get_random_meme
from utils.command import command


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
