import functools
import logging

from discord.ext import commands
from discord import Embed, Color
from utils.errors import DiscordException


def command(group, *args, **kwargs):
    def decorator(func):
        @group.hybrid_command(*args, **kwargs)
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            value = None

            async def send(*args, **kwargs):
                await ctx.interaction.response.send_message(*args, **kwargs, ephemeral=False)

            ctx.send = send

            try:
                value = await func(ctx, *args, **kwargs)
            except DiscordException as e:
                await ctx.interaction.response.send_message(
                    embed=Embed(color=Color.red(), title="Error", description=str(e)),
                    ephemeral=True)
            except Exception as e:
                await ctx.interaction.response.send_message(
                    embed=Embed(color=Color.red(),
                                title="Error",
                                description="Something went wrong 😥"),
                    ephemeral=True)
                logger = logging.getLogger(f'discord.custom.command.{func.__name__}')
                logger.error(e)

            return value

        return wrapper

    return decorator


def command(group, *args, **kwargs):
    def decorator(func):
        @group.hybrid_command(*args, **kwargs)
        @functools.wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            value = None

            async def send(*args, **kwargs):
                await ctx.interaction.response.send_message(*args, **kwargs, ephemeral=True)

            ctx.send = send

            try:
                value = await func(ctx, *args, **kwargs)
            except DiscordException as e:
                await ctx.interaction.response.send_message(
                    embed=Embed(color=Color.red(), title="Error", description=str(e)),
                    ephemeral=True)
            except Exception as e:
                await ctx.interaction.response.send_message(
                    embed=Embed(color=Color.red(),
                                title="Error",
                                description="Something went wrong 😥"),
                    ephemeral=True)
                logger = logging.getLogger(f'discord.custom.command.{func.__name__}')
                logger.error(e)

            return value

        return wrapper

    return decorator
