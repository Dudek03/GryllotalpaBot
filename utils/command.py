import functools
import logging

from discord.ext import commands
from discord import Embed, Color
from utils.errors import DiscordException


def command(group=None, long=False, is_hidden=True, *args, **kwargs):
    if group is None:
        group = commands

    def decorator(func):
        @group.hybrid_command(*args, **kwargs)
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):

            value = None
            ctx = None
            for arg in args:
                if isinstance(arg, commands.Context):
                    ctx = arg
                    break
            if ctx is None:
                raise Exception("Missing context")

            if long:
                await ctx.interaction.response.defer(ephemeral=is_hidden)

            if long:
                async def send(*args, **kwargs):
                    await ctx.interaction.followup.send(*args, **kwargs, ephemeral=is_hidden)
            else:
                async def send(*args, **kwargs):
                    await ctx.interaction.response.send_message(*args, **kwargs, ephemeral=is_hidden)
            ctx._send = ctx.send
            ctx.send = send

            try:
                value = await func(*args, **kwargs)
            except DiscordException as e:
                if long:
                    await ctx.interaction.followup.send(
                        embed=Embed(color=Color.red(), title="Error", description=str(e)),
                        ephemeral=True)
                else:
                    await ctx.interaction.response.send_message(
                        embed=Embed(color=Color.red(), title="Error", description=str(e)),
                        ephemeral=True)
            except Exception as e:
                if long:
                    await ctx.interaction.followup.send(
                        embed=Embed(color=Color.red(),
                                    title="Error",
                                    description="Something went wrong 😥"),
                        ephemeral=True)
                else:
                    await ctx.interaction.response.send_message(
                        embed=Embed(color=Color.red(),
                                    title="Error",
                                    description="Something went wrong 😥"),
                        ephemeral=True)
                logger = logging.getLogger(f'discord.custom.command.{func.__name__}')
                logger.error(e, exc_info=True, stack_info=True)

            return value

        return wrapper

    return decorator
