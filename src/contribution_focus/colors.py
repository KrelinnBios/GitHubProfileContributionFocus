"""Fixed rainbow colors for repository rows."""


RAINBOW_COLORS = (
    "#FF6B6B",
    "#FFA94D",
    "#FFD43B",
    "#69DB7C",
    "#4DABF7",
    "#B197FC",
)


def color_for(repository: str, colors: dict[str, str], row_index: int) -> str:
    if repository in colors:
        return colors[repository]
    short_name = repository.rsplit("/", 1)[-1]
    if short_name in colors:
        return colors[short_name]
    return RAINBOW_COLORS[row_index % len(RAINBOW_COLORS)]
