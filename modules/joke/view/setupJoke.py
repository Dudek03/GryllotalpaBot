import discord
from discord.ui import View


def setup_joke(view: View, ui):
    view.clear_items()
    view.add_item(ShowAnswerButton(ui))


class ShowAnswerButton(discord.ui.Button['answer']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.blurple, label="Answer")
        self.ui = ui

    async def callback(self, interaction):
        await self.ui.show_answer()
        await interaction.response.edit_message(view=self.view)
