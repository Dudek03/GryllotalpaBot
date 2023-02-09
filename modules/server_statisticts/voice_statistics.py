import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View
from discord.utils import get

from utils.command import command
from utils.database import Database
from utils.errors import DiscordException


class VoiceStatistics(commands.GroupCog, group_name='voicestats'):
    def __init__(self, bot):
        self.bot = bot

    def get_user_name(self, id):
        user = get(self.bot.get_all_members(), id=id)
        if user is None:
            return "User not found"
        return user.name

    async def generate_top10(self, ctx, list):
        top = ""
        for record in list:
            top += self.get_user_name(record[0]) + " : " + str(round(record[1])) + " s\n"

        await ctx._send(
            content="",
            embed=Embed(title="TOP 10 VOICE USERS",
                        description=top,
                        color=discord.Color.blue()),
            view=View(timeout=None)
        )

    @command(name="general", description="Get top 10 active users on voice channels", is_hidden=False)
    async def top10_voice_channels(self, ctx):
        result = Database().top10_voice_channels(server_id=ctx.guild.id, channel_id=None)
        await self.generate_top10(ctx, result)

    @command(name="channel", description="get random meme with keyword", is_hidden=False)
    async def search_meme(self, ctx, channel: discord.VoiceChannel):
        result = Database().top10_voice_channels(server_id=ctx.guild.id, channel_id=channel.id)
        await self.generate_top10(ctx, result)
