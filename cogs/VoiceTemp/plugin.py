from __future__ import annotations

from .. import Plugin
from core import Bot, Embed

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Member, User


class TemporaryVoice(Plugin):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.bot = bot
        self.temp_channels = []
        self.temp_categories = []

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: discord.VoiceState, after: discord.VoiceState):
        possible_channel_name = f"{member.name}'s area"
        temp_channel_name = "temp"
        temp_teams_channel_name = "teams"

        if not after.channel:
            if before.channel:
                if before.channel.id in self.temp_channels:
                    if len(before.channel.members) == 0:
                        await before.channel.delete()

                if before.channel.id in self.temp_categories:
                    if len(before.channel.members) == 0:
                        for channel in before.channel.category.channels:
                            await channel.delete()
                        await before.channel.category.delete()

        if after.channel.name == temp_channel_name:
            temporary_channel = await after.channel.clone(name=possible_channel_name)
            await member.move_to(temporary_channel)
            self.temp_channels.append(temporary_channel.id)

        if after.channel.name == temp_teams_channel_name:
            temp_category = await after.channel.guild.create_category(name=possible_channel_name)
            await temp_category.create_text_channel(name="text")
            temporary_channel = await temp_category.create_voice_channel(name="voice")
            await member.move_to(temporary_channel)
            self.temp_categories.append(temporary_channel.id)

        if before.channel:
            if before.channel.id in self.temp_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()

            if before.channel.id in self.temp_categories:
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                    await before.channel.category.delete()


async def setup(bot: Bot) -> None:
    await bot.add_cog(TemporaryVoice(bot))
