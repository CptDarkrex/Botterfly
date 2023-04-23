from __future__ import annotations

from discord import Colour
from discord import Embed as OriginalEmbed

from typing import Optional
from typing import Union
from typing_extensions import Self


__all__ = [
    "Embed",
]


class Embed(OriginalEmbed):
    def __init__(self, color: Optional[Union[int, Colour]] = Colour.blurple(), **kwargs):
        super().__init__(color=color, **kwargs)

    def credits(self) -> Self:
        super().set_footer(text="Made with ❤️ by Kralos#1442")
        return self
