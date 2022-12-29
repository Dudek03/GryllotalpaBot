from discord.ext import commands

from modules.voice.bot import Music


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
