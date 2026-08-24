"""Configuration loading for contribution focus charts."""

import json
from pathlib import Path

DEFAULT_THEME = {
    "light_text": "#24292f",
    "light_muted": "#57606a",
    "light_empty": "#d0d7de",
    "dark_text": "#f0f6fc",
    "dark_muted": "#8b949e",
    "dark_empty": "#30363d",
}

DEFAULT_COLORS = {"Other": "#8B949E"}


def _object_section(raw: dict, name: str) -> dict:
    value = raw.get(name, {})
    if not isinstance(value, dict):
        raise RuntimeError(f"configuration field '{name}' must be a JSON object")
    return value


def load_config(config_path: Path) -> dict:
    raw = {}
    if config_path.exists():
        raw = json.loads(config_path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, dict):
        raise RuntimeError("configuration root must be a JSON object")

    theme = DEFAULT_THEME.copy()
    theme.update(_object_section(raw, "theme"))
    colors = DEFAULT_COLORS.copy()
    colors.update(_object_section(raw, "colors"))

    excluded_repositories = raw.get("excluded_repositories", [])
    if not isinstance(excluded_repositories, list):
        raise RuntimeError(
            "configuration field 'excluded_repositories' must be a JSON array"
        )

    excluded = {
        str(repository).strip().casefold()
        for repository in excluded_repositories
        if str(repository).strip()
    }
    return {
        "owner": str(raw.get("owner", "")).strip(),
        "excluded_repositories": excluded,
        "theme": theme,
        "colors": colors,
    }
