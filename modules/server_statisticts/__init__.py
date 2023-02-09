from discord.ext import commands

from modules.server_statisticts.voice_statistics import VoiceStatistics


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceStatistics(bot))
