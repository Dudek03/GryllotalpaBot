import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View

from modules.joke.view.setupJoke import setup_joke


class JokeUI:
    def __init__(self, ctx: commands.Context, setup: str, answer: str):
        super().__init__()
        self.ctx = ctx
        self.setup = setup
        self.answer = answer
        self.interaction = None
        self.message = None
        self.view = View(timeout=None)

    async def init(self):
        setup_joke(self.view, self)
        self.message = await self.ctx._send(
            content="",
            embed=Embed(title=self.setup,
                        description="",
                        color=discord.Color.blue()),
            view=self.view
        )
        self.interaction = self.ctx.interaction

    async def show_answer(self):
        self.view.clear_items()
        await self.message.edit(
            content="",
            embed=Embed(title=self.setup,
                        description=self.answer,
                        color=discord.Color.blue()),
            view=self.view
        )
