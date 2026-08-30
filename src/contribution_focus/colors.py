"""Stable rainbow colors for repository rows."""

import hashlib


RAINBOW_COLORS = (
    "#FF6B6B",
    "#FFA94D",
    "#FFD43B",
    "#69DB7C",
    "#4DABF7",
    "#B197FC",
)


def generated_color(repository: str) -> str:
    digest = hashlib.sha256(repository.casefold().encode("utf-8")).digest()
    return RAINBOW_COLORS[int.from_bytes(digest[:2], "big") % len(RAINBOW_COLORS)]


def color_for(repository: str, colors: dict[str, str]) -> str:
    if repository in colors:
        return colors[repository]
    short_name = repository.rsplit("/", 1)[-1]
    if short_name in colors:
        return colors[short_name]
    return generated_color(repository)
