from typing import Optional

from discord.ext import commands
from discord.app_commands.commands import Command
from discord import Embed, Color
from discord.interactions import Interaction
from utils.command import command
from utils.errors import DiscordException


async def setup(bot: commands.Bot):
    @command(group=bot)
    async def create_unsave(ctx: commands.Context, name: str, code: str, description: Optional[str] = "..."):
        guild = ctx.interaction.guild

        async def callback(interaction: Interaction) -> None:
            await execute(interaction, code)

        bot.tree.add_command(
            Command(name=name, description=description, callback=callback), guild=guild)
        await ctx.interaction.response.send_message(
            embed=Embed(color=Color.green(), title=f"Created /{name}",
                        description=f"Successfully created command `{name}`"))
        await bot.tree.sync(guild=guild)

    @bot.hybrid_command()
    async def remove_command(ctx: commands.Context, name: str):
        guild = ctx.interaction.guild
        if not bot.tree.get_command(name, guild=guild):
            raise DiscordException(f"Command `{name}` not found")
        bot.tree.remove_command(name, guild=guild)
        await ctx.interaction.response.send_message(
            embed=Embed(color=Color.green(), title="Deleted", description=f"Command `{name}` deleted"))
        await bot.tree.sync(guild=guild)

    async def execute(interaction: Interaction, code: str):
        try:
            exec(
                f'async def __ex(interaction): ' +
                ''.join(f'\n {l}' for l in code.split('\n'))
            )

            return await locals()['__ex'](interaction)
        except Exception as e:
            raise DiscordException(str(e))
