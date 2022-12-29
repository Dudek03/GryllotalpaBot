import discord
from discord.ui import View

from modules.voice.views.ready import AddButton, LeaveButton


def player_view(view: View, ui):
    view.clear_items()
    view.add_item(PauseButton(ui))
    view.add_item(NextButton(ui))
    view.add_item(AddButton(ui))
    view.add_item(LeaveButton(ui))


class PauseButton(discord.ui.Button['pause']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.blurple)
        self.ui = ui
        vc = self.ui.ctx.voice_client
        if vc.is_paused():
            self.emoji = "▶"
        else:
            self.emoji = "⏸️"
        self.ui = ui

    async def callback(self, interaction):
        vc = self.ui.ctx.voice_client
        if not vc.is_paused():
            self.emoji = "▶"
            vc.pause()
        else:
            self.emoji = "⏸️"
            vc.resume()
        await interaction.response.edit_message(view=self.view)


class NextButton(discord.ui.Button['next']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.blurple, emoji="⏭")
        self.ui = ui
        player = self.ui.music_cog.get_player(self.ui.ctx)
        queue_size = player.queue.qsize()
        if queue_size <= 0:
            self.disabled = True
        else:
            self.disabled = False
        self.ui = ui

    async def callback(self, interaction):
        vc = self.ui.ctx.voice_client
        player = self.ui.music_cog.get_player(self.ui.ctx)
        queue_size = player.queue.qsize()
        if queue_size <= 0:
            self.disabled = True
        else:
            self.disabled = False
        vc.stop()
        await interaction.response.edit_message(view=self.view)
