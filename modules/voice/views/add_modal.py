import logging

import discord


class AddModal(discord.ui.Modal, title='Play'):

    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    search = discord.ui.TextInput(
        label='What should i play for you?',
        placeholder='Enter title or url...',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        res = await self.ui.music_cog.search_and_play(self.ui.ctx, self.search.value, 1)
        await interaction.response.send_message(**res, ephemeral=True)
        await self.ui.update()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logging.getLogger("discord").error(error, exc_info=True)
        await self.ui.update()
