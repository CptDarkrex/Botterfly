from __future__ import annotations

import asyncio

from .. import Plugin
from core import Bot, Embed

from discord import Interaction, app_commands

from transformers import AutoTokenizer, AutoModelForCausalLM

# Setup of the bot
pygmalion = "PygmalionAI/pygmalion-6b"
# pygmalion = "anon8231489123/gpt4-x-alpaca-13b-native-4bit-128g"
tokenizer = AutoTokenizer.from_pretrained(pygmalion)
model = AutoModelForCausalLM.from_pretrained(pygmalion)


class Botterfly(Plugin):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.bot = bot

    @app_commands.command(name="roleplay", description="Roleplay with Botterfly")
    async def roleplay(self, interaction: Interaction, prompt: str):
        await interaction.response.defer(ephemeral=False, thinking=True)
        await asyncio.sleep(15)
        # Setting up the input
        inputs = tokenizer([prompt], return_tensors="pt")

        # Implementation of the above setup
        reply_ids = model.generate(**inputs, max_new_tokens=100)  # return_dict_in_generate=True, output_scores=True
        outputs = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
        embed = Embed(description=f"{outputs}")
        await interaction.followup.send(embed=embed)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Botterfly(bot))
