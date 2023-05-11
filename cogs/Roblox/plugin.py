from __future__ import annotations

from .. import Plugin
from core import Bot, Embed

import discord
from discord import app_commands, Interaction

from typing import Optional

from .roblox import Roblox_API, session


class Roblox(Plugin):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.bot = bot
        self.rbx_api = Roblox_API()

    @app_commands.command(name="cash_out", description="payouts your money")
    async def cash_out(self, interaction: Interaction, roblox_username: str, amount: Optional[str]):
        new_recipients = []
        payload = {
            "PayoutType": "FixedAmount",
            "Recipients": []
        }

        session.cookies[".ROBLOSECURITY"] = "6C81664851810EEFD7B9B88F0CA18D7400BFE22C8E46086282AEC49FE0FE7516351" \
                                            "ECC71E2C52CE431F83F43D54D501354A07B364BE7048DBBA655DAD71E6B8C91F4F6B" \
                                            "00B77086E7FFB19F1D9376F874F2F07A9F5B9A3AA95292C2FBE46BE4386DBA76D578D" \
                                            "2E8A813C489E70AB982A2602E950C0C111B45E2C425E4EAA4A6358B929E315694F1485" \
                                            "0919D980673F307645A4CBD6A9FDE9D43E97365DCEB46C2190CF14EA9FE8AA98059C0DD" \
                                            "C9BF11313C58A8A093E762E62FB262E4555612D1DECD37D73BEE2A6DA684833ED706F0D" \
                                            "7254961AAFE3645310978E3575DFAC35716CB82F0ABBD4AF734C032D19EE1164D5D07755" \
                                            "6D5796E888EB55EC9834227672BD714F4D950788ED448DE73AC0E196C958A7734E67EB92" \
                                            "E777F4C591E4A79B871EF81D9774113FF28E6A22E32AC61D263CD9172A56C62CE820" \
                                            "48C29FBD4C79DCC45D73C4AB6A5E5C7DD46B3E40CF9D71EC14198A8C671C36E6BD09972" \
                                            "775636B708C1B3FB66992EAA3CE98045A7F334C754BDC63A0C73A8782C9AB2D04ACC" \
                                            "4E599D690"

        auth_req = self.rbx_api.roblox_request("POST", "https://auth.roblox.com/")  # authenticate roblox login with cookie
        member_req = self.rbx_api.roblox_request("GET",
                                 f"https://groups.roblox.com/v1/groups/8901078/users")  # api call for members
        print(member_req)
        member_data = member_req.json()  # turn request into json
        member_data.pop("nextPageCursor")  # remove kv pairs for clean dict comphrehension
        member_data.pop("previousPageCursor")
        member_list = {item['user']['username']: item['user']['userId'] for item in
                       member_data['data']}  # create user:id pairs

        member_names = {item['user']['username'] for item in member_data['data']}  # users
        group_req = self.rbx_api.roblox_request("GET", f"https://groups.roblox.com/v1/groups/8901078")
        group_info = group_req.json()

        try:
            new_recipients.append({'recipientId': member_list[roblox_username],
                                   # recip id is the value of the user key from the member list
                                   'recipientType': 'User',
                                   'amount': 1
                                   # reward amt is the value of the key that reps the replier disc id
                                   })  # add robux recipient to list to use to extend recipient payload

        except KeyError:
            await interaction.response.send_message("Username is spelled incorrectly. Try again.")
            await interaction.response.send_message(
                f'Alternatively, if you **are not** in the group, **"{group_info["name"]}"**'
                f' enter one of these users: \n {member_names}')

        else:
            payload["Recipients"].extend(new_recipients)  # Add winners to payload
            payout = self.rbx_api.roblox_request("POST", f"https://groups.roblox.com/v1/groups/8901078/payouts",
                                                 json=payload)  # payout robux
            new_recipients = []
            payload["Recipients"] = []
            await interaction.response.send_message("Successfully recieved username!")


async def setup(bot: Bot) -> None:
    await bot.add_cog(Roblox(bot))
