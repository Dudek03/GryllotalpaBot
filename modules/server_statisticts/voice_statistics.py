import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View
from discord.utils import get

from utils.command import command
from utils.database import Database
from utils.errors import DiscordException
import os
import time
from typing import Union

from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import Session

from models.base import Base
from models.connection_time import ConnectionTime


class VoiceStatistics(commands.GroupCog, group_name='voicestats'):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_top10_voice_users_by_channel(server_id: int, channel_id: Union[int, None]):
        with Session(Database().engine) as session:
            if channel_id is None:
                result = session.query(ConnectionTime.user_id, func.sum(ConnectionTime.time).label("sumTime")) \
                    .where(ConnectionTime.server_id.is_(server_id)) \
                    .group_by(ConnectionTime.user_id) \
                    .order_by(desc("sumTime")) \
                    .limit(10) \
                    .all()
            else:
                result = session.query(ConnectionTime.user_id, func.sum(ConnectionTime.time).label("sumTime")) \
                    .where(ConnectionTime.server_id == server_id) \
                    .where(ConnectionTime.channel_id == channel_id) \
                    .group_by(ConnectionTime.user_id) \
                    .order_by(desc("sumTime")) \
                    .limit(10) \
                    .all()
        return result

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
    async def top10_active_users_on_voice_channels(self, ctx):
        result = self.get_top10_voice_users_by_channel(server_id=ctx.guild.id, channel_id=None)
        await self.generate_top10(ctx, result)

    @command(name="channel", description="get random meme with keyword", is_hidden=False)
    async def top10_active_users_on_voice_channel(self, ctx, channel: discord.VoiceChannel):
        result = self.get_top10_voice_users_by_channel(server_id=ctx.guild.id, channel_id=channel.id)
        await self.generate_top10(ctx, result)
