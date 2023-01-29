# TEMPORARY DATABASE IT WILL BE CHANGE AFTER IMPLEMENT DATABASE
import datetime

import discord

rows = dict()


class VoiceChannelStatistic:
    def __init__(self):
        self.active_members = []
        pass

    def find_member_in_tab(self, member, members):
        for m in members:
            if m.id == member:
                return True
        return False

    async def on_voice_state_update(self, member, before, after):
        print("EVENT")
        after_members = []
        if after.channel is not None:
            print("after")
            channel = after.channel
            after_members = channel.members
        print(self.active_members, after_members)
        disconnected_members = []
        for m in self.active_members:
            if not self.find_member_in_tab(m.id, after_members):
                disconnected_members.append(m)

        for m in after_members:
            if not self.find_member_in_tab(m.id, self.active_members):
                self.active_members.append(m)
        print("DISCORNECTED", disconnected_members)
