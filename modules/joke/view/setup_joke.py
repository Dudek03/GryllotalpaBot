import discord
from discord import Embed
from discord.ui import View


def setup_joke(view: View, ui):
    view.clear_items()
    view.add_item(ShowAnswerButton(ui))


class ShowAnswerButton(discord.ui.Button['answer']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.blurple, label="Answer")
        self.ui = ui

    async def callback(self, interaction):
        self.ui.view.clear_items()
        await interaction.response.edit_message(content="",
                                                embed=Embed(title=self.ui.setup,
                                                            description=self.ui.answer,
                                                            color=discord.Color.blue()),
                                                view=self.view)
