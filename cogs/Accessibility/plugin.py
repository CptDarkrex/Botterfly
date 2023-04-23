from __future__ import annotations

from .. import Plugin
from core import Bot, Embed

from .database import Control

import discord
from discord import app_commands, Interaction

class InviteButton(discord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.link = link
        self.add_item(discord.ui.Button(label="Invite Link", url=self.link))

    @discord.ui.button(label="Invite Link", style=discord.ButtonStyle.blurple)
    async def invite_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.link, ephemeral=True)


class Accessibility(Plugin):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.bot = bot

    @app_commands.command()
    async def invite(self, interaction: Interaction):
        invitation = await interaction.channel.create_invite()
        embed = Embed(description="Select one of the buttons below to generate invite links.",
                      colour=discord.Colour.orange())
        await interaction.response.send_message(
            embed=embed,
            view=InviteButton(str(invitation))
        )


    @app_commands.command(name="member_count", description="Gets the number of members in the server.")
    async def member_count(self, interaction: Interaction):
        svr_id = interaction.guild.id
        svr_members = interaction.guild.member_count

        get_svr_id = Control.retrieve_guild_id(self=Control, svr_id=svr_id)
        get_svr_members = Control.retrieve_members_database(self=Control, svr_id=svr_id)

        if svr_members == get_svr_members:
            embed = Embed(description=f"The are **{Control.retrieve_members_database(self=Control, svr_id=svr_id)}** "
                                      f"members in this server", colour=discord.Colour.green())
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=False)
        elif svr_members != get_svr_members:
            Control.update_guild_members(self=Control, svr_id=svr_id, svr_members=svr_members)
            embed = Embed(description=f"The are **{Control.retrieve_members_database(self=Control, svr_id=svr_id)}** "
                                      f"members in this server", colour=discord.Colour.green())
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=False)
        else:
            Control.initialize_server_requirements(self=Control, svr_id=svr_id, svr_members=svr_members)
            embed = Embed(description=f"The are {Control.retrieve_members_database(self=Control, svr_id=svr_id)} "
                                      f"members in this server", colour=discord.Colour.green())
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=False)

    @app_commands.command(name="clear", description="Delete messages.")
    async def clear(self, interaction: Interaction, amount: int):
        await interaction.response.defer()
        amount = amount

        embed = Embed(description=f"deleted {amount} messages!")

        if amount > 101:
            await interaction.response.send_message(embed=Embed(description="Can't delete more than **100** messages.",
                                                                colour=discord.Colour.red()), ephemeral=True)
        else:
            await interaction.channel.purge(limit=amount)
            await interaction.channel.send(embed=embed)



async def setup(bot: Bot) -> None:
    await bot.add_cog(Accessibility(bot))


