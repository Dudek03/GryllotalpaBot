from discord.ext import commands

from modules.meme.meme import Meme


async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))
