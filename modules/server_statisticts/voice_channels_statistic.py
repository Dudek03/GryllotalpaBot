import time

from sqlalchemy.orm import Session

from models.connection_time import ConnectionTime
from utils.database import Database


class VoiceChannelStatistic:
    def __init__(self):
        self.active_members = {}
        pass

    def register_new_connection_time(self, server_id: int, channel_id: int, user_id: int, timeChannel: int):
        with Session(Database().engine) as session:
            record = ConnectionTime(
                server_id=server_id,
                channel_id=channel_id,
                user_id=user_id,
                time=timeChannel,
                timestamp=int(time.time())
            )
            session.add(record)
            session.commit()

    def find_member_in_tab(self, member, members):
        for m in members:
            if m.id == member:
                return True
        return False

    async def on_voice_state_update(self, member, before, after):
        server_id = member.guild.id
        if before.channel is not None:
            channel_id = before.channel.id
        else:
            channel_id = after.channel.id
        marker = str(server_id) + "x" + str(channel_id)
        after_members = []
        if after.channel is not None:
            channel = after.channel
            after_members = channel.members
        disconnected_members = []
        active_member = self.active_members.get(marker, [])
        for m in self.active_members.get(marker, []):
            if not self.find_member_in_tab(m[0].id, after_members):
                disconnected_members.append(m)
                active_member.remove(m)
        self.active_members[marker] = active_member

        def map2members(l: list):
            result = []
            for e in l:
                result.append(e[0])
            return result

        for m in after_members:
            if not self.find_member_in_tab(m.id, map2members(self.active_members.get(marker, []))):
                l = self.active_members.get(marker, None)
                obj = [m, time.time()]
                if l is None:
                    self.active_members[marker] = [obj]
                else:
                    l.append(obj)
        for user in disconnected_members:
            self.register_new_connection_time(server_id, channel_id, user[0].id, time.time() - user[1])
