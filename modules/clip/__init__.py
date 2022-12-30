from discord.ext import commands

from modules.clip.bot import Clip


async def setup(bot: commands.Bot):
    await bot.add_cog(Clip(bot))
