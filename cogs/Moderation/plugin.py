from __future__ import annotations
from .. import Plugin
from core import Bot
from discord import app_commands, Interaction, Member, User
from typing import Optional


def can_moderate():
    async def predicate(interaction: Interaction):
        target: Member = interaction.namespace.member or interaction.namespace.target
        if not target: return True
        assert interaction.guild is not None and isinstance(interaction.user, Member)

        if (
            target.top_role.position > interaction.user.top_role.position
            or target.guild_permissions.kick_members
            or target.guild_permissions.ban_members
            or target.guild_permissions.administrator
            or target.guild_permissions.manage_guild
        ):
            raise app_commands.CheckFailure(f" You can't moderate **{target}**")
        return True
    return app_commands.check(predicate)


class Moderation(Plugin):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.default_permissions(kick_members=True)
    @app_commands.describe(member="Select a member to kick.", reason="Reason for kicking.")
    @app_commands.guild_only()
    async def kick_command(self, interaction: Interaction, member: Member, reason: Optional[str]):
        if not reason: reason = "No reason."
        try:
            await member.kick(reason=reason)
        except:
            await self.bot.error(f"I'm sorry, but I'm not able to kick **{member}** from the server.", interaction)
        else:
            await self.bot.success(
                f"Kicked {member} from the server.",
                interaction
            )

    @app_commands.command(name="ban", description="Ban a member.")
    @app_commands.default_permissions(ban_members=True)
    @can_moderate()
    @app_commands.describe(member="Select a member to ban.", reason="Reason for banning.")
    @app_commands.guild_only()
    async def ban_command(self, interaction: Interaction, member: Member, reason: Optional[str]):
        if not reason: reason = "No reason."
        try:
            await member.ban(reason=reason)
        except:
            await self.bot.error(f"I'm sorry but I'm not able to ban {member} from the server.", interaction)
        else:
            await self.bot.success(f"Successfully banned **{member}** from the server.", interaction)

    @app_commands.command(name="unban", description="Unban a user")
    @app_commands.default_permissions(ban_members=True)
    @app_commands.describe(user="Provide a user or user id to unban", reason="Reason to unban")
    @app_commands.guild_only()
    async def unban_command(self, interaction: Interaction, user: User, reason: Optional[str]):
        if not reason: reason = "No reason."
        assert interaction.guild is not None
        try:
            await interaction.guild.fetch_ban(user)
        except:
            await self.bot.error(f"**{user}** is not banned.", interaction)
        else:
            try:
                await interaction.guild.unban(user, reason=reason)
            except:
                await self.bot.error(
                    f"I'm sorry, but I'm not able to unban **{user}** from the server.",
                    interaction
                )
            else:
                await self.bot.success(
                    f"Successfully unbanned **{user}** from the server.",
                    interaction
                )


async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))
