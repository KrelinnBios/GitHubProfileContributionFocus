"""Fixed rainbow colors for repository rows."""


RAINBOW_COLORS = (
    "#FF1744",
    "#FF9100",
    "#FFEA00",
    "#00E676",
    "#2979FF",
    "#AA00FF",
)


def color_for(repository: str, colors: dict[str, str], row_index: int) -> str:
    if repository in colors:
        return colors[repository]
    short_name = repository.rsplit("/", 1)[-1]
    if short_name in colors:
        return colors[short_name]
    return RAINBOW_COLORS[row_index % len(RAINBOW_COLORS)]
