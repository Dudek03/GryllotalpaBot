from typing import Optional

from discord.ext.commands import HybridGroup


def create_group(name: str, description: Optional[str]):
    return HybridGroup(name, description)
