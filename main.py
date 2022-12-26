import asyncio
import logging
import logging.handlers
import os

from dotenv import load_dotenv
from typing import List, Optional

import discord
from discord.ext import commands
from aiohttp import ClientSession


class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        web_client: ClientSession,
        testing_guild_id: Optional[int],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.web_client = web_client
        self.initial_extensions = initial_extensions
        self.testing_guild_id = testing_guild_id

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)


async def main():
    # 0. Env
    load_dotenv()

    # 1. logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    # handler = logging.handlers.RotatingFileHandler(
    #     filename='discord.log',
    #     encoding='utf-8',
    #     maxBytes=32 * 1024 * 1024,  # 32 MiB
    #     backupCount=5,  # Rotate through 5 files
    # )
    handler = logging.StreamHandler()
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with ClientSession() as our_client:
        exts = ['test']
        intents = discord.Intents.default()
        intents.message_content = True
        async with CustomBot(commands.when_mentioned_or('$'), web_client=our_client, initial_extensions=exts,
                             intents=intents, testing_guild_id=int(os.getenv('TESTING_GUILD_ID', ''))) as bot:
            await bot.start(os.getenv('DISCORD_TOKEN', ''))


if __name__ == "__main__":
    asyncio.run(main())
