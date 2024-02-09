"""
Utilities for working with terminal colors
"""

from enum import Enum
from typing import Union

class Colors(Enum):
    """Enumeration of terminal colors"""
    BLACK = "black"
    DARK_GRAY = "dark_gray"
    RED = "red"
    LIGHT_RED = "light_red"
    GREEN = "green"
    LIGHT_GREEN = "light_green"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    BLUE = "blue"
    LIGHT_BLUE = "light_blue"
    PURPLE = "purple"
    LIGHT_PURPLE = "light_purple"
    CYAN = "cyan"
    LIGHT_CYAN = "light_cyan"
    LIGHT_GRAY = "light_gray"
    WHITE = "white"

COLOR_START = "\033["
COLOR_END = "\033[0m"

FG_COLOR_CODES = {
    Colors.BLACK: "0;30",
    Colors.DARK_GRAY: "1;30",
    Colors.RED: "0;31",
    Colors.LIGHT_RED: "1;31",
    Colors.GREEN: "0;32",
    Colors.LIGHT_GREEN: "1;32",
    Colors.BROWN: "0;33",
    Colors.ORANGE: "0;33",  # Alias for brown
    Colors.YELLOW: "1;33",
    Colors.BLUE: "0;34",
    Colors.LIGHT_BLUE: "1;34",
    Colors.PURPLE: "0;35",
    Colors.LIGHT_PURPLE: "1;35",
    Colors.CYAN: "0;36",
    Colors.LIGHT_CYAN: "1;36",
    Colors.LIGHT_GRAY: "0;37",
    Colors.WHITE: "1;37",
}

BG_COLOR_CODES = {
    Colors.BLACK: "0;40",
    Colors.DARK_GRAY: "1;40",
    Colors.RED: "0;41",
    Colors.LIGHT_RED: "1;41",
    Colors.GREEN: "0;42",
    Colors.LIGHT_GREEN: "1;42",
    Colors.BROWN: "0;43",
    Colors.ORANGE: "0;43",  # Alias for brown
    Colors.YELLOW: "1;43",
    Colors.BLUE: "0;44",
    Colors.LIGHT_BLUE: "1;44",
    Colors.PURPLE: "0;45",
    Colors.LIGHT_PURPLE: "1;45",
    Colors.CYAN: "0;46",
    Colors.LIGHT_CYAN: "1;46",
    Colors.LIGHT_GRAY: "0;47",
    Colors.WHITE: "1;47",
}

def _apply_color(x: str, color_code: str) -> str:
    """Apply the given color code to the text"""
    return f"{COLOR_START}{color_code}m{x}{COLOR_END}"

def colorize(text: str, color: Union[Colors, str]) -> str:
    """Render the given text with the specified color"""
    assert color in FG_COLOR_CODES, f"Invalid color: {color}"
    return _apply_color(text, FG_COLOR_CODES[color])

def bg_colorize(text: str, color: Union[Colors, str]) -> str:
    """Render the given text with the specified background color"""
    assert color in BG_COLOR_CODES, f"Invalid color: {color}"
    return _apply_color(text, BG_COLOR_CODES[color])

def decolorize(text: str) -> str:
    """Remove color encoding from the text"""
    for color_code in list(FG_COLOR_CODES.values()) + list(BG_COLOR_CODES.values()):
        text = text.replace(f"{color_code}m", "")
    text = text.replace(COLOR_START, "")
    text = text.replace(COLOR_END, "")
    return text
