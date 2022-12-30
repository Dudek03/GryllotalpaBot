from discord.ext import commands

from modules.joke.jokeApi import get_random_joke
from modules.joke.ui import JokeUI
from utils.command import command


async def setup(bot: commands.Bot):
    @command(group=bot, name="joke", description="get random joke")
    async def random_joke(ctx):
        joke = get_random_joke()

        ui = JokeUI(ctx, joke['setup'], joke['punchline'])
        await ui.init()
