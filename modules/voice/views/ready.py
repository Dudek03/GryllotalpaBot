import discord
from discord.ui import View

from modules.voice.views.add_modal import AddModal


def ready_view(view: View, ui):
    view.clear_items()
    view.add_item(AddButton(ui))
    view.add_item(LeaveButton(ui))


class AddButton(discord.ui.Button['add']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.blurple, emoji="➕")
        self.ui = ui

    async def callback(self, interaction):
        await interaction.response.send_modal(AddModal(self.ui))


class LeaveButton(discord.ui.Button['leave']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.red, label="Leave")
        self.ui = ui

    async def callback(self, interaction):
        await self.ui.music_cog.cleanup(self.ui.ctx.guild)
        await interaction.response.edit_message(view=self.view)
        await self.ui.update()
