import asyncio

from discord.ext import commands
from discord.app_commands.commands import Command


async def setup(bot: commands.Bot):
    @bot.hybrid_command()
    async def ask(ctx: commands.Context):
        await ctx.send('Do you want to continue?')

    @bot.hybrid_group(fallback="get")
    async def tag(ctx, name):
        await ctx.send(f"Showing tag: {name}")

    @tag.command()
    async def create(ctx, name):
        await ctx.send(f"Created tag: {name}")

    @bot.hybrid_command()
    async def com(ctx: commands.Context):
        guild = ctx.interaction.guild
        bot.tree.add_command(Command(name="xd", description="eeee", callback=xd), guild=guild)
        await ctx.send(f"ok")
        await bot.tree.sync(guild=guild)

    @bot.hybrid_command()
    async def rem(ctx: commands.Context):
        guild = ctx.interaction.guild
        bot.tree.remove_command("xd", guild=guild)
        await ctx.send(f"ok")
        await bot.tree.sync(guild=guild)

    async def xd(ctx):
        print(ctx)
