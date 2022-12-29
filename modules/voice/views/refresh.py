import discord
from discord.ui import View


def refresh_view(view: View, ui):
    view.clear_items()
    view.add_item(RefreshButton(ui))
    view.add_item(JoinButton(ui))


class RefreshButton(discord.ui.Button['refresh']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.blurple, emoji="🔁")
        self.ui = ui

    async def callback(self, interaction):
        await self.ui.update()
        await interaction.response.edit_message(view=self.view)


class JoinButton(discord.ui.Button['join']):
    def __init__(self, ui):
        super().__init__(style=discord.ButtonStyle.green, label="Join")
        self.ui = ui

    async def callback(self, interaction):
        channel = interaction.user.voice.channel
        vc = self.ui.ctx.voice_client
        try:
            await self.ui.music_cog.join(channel, vc)
        except Exception as e:
            print(e)
        await self.ui.update()
        await interaction.response.edit_message(view=self.view)
