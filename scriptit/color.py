################################################################################
# Copyright The Script It Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
"""
Utilities for working with a terminal
"""

# Standard
from enum import Enum
from typing import Dict, Union

## Public ######################################################################


class Colors(Enum):
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


## Mapping from color name to ansi escape code for foreground color
FG_COLOR_CODES: Dict[Union[Colors, str], str] = {
    Colors.BLACK: "0;30",
    Colors.DARK_GRAY: "1;30",
    Colors.RED: "0;31",
    Colors.LIGHT_RED: "1;31",
    Colors.GREEN: "0;32",
    Colors.LIGHT_GREEN: "1;32",
    Colors.BROWN: "0;33",
    Colors.ORANGE: "0;33",
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
FG_COLOR_CODES.update(**{entry.value: FG_COLOR_CODES[entry] for entry in Colors})

## Mapping from color name to ansi escape code for background color
BG_COLOR_CODES: Dict[Union[Colors, str], str] = {
    Colors.BLACK: "0;40",
    Colors.DARK_GRAY: "1;40",
    Colors.RED: "0;41",
    Colors.LIGHT_RED: "1;41",
    Colors.GREEN: "0;42",
    Colors.LIGHT_GREEN: "1;42",
    Colors.BROWN: "0;43",
    Colors.ORANGE: "0;43",
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
BG_COLOR_CODES.update(**{entry.value: BG_COLOR_CODES[entry] for entry in Colors})

COLOR_START = "\033["
COLOR_END = "\033[0m"


def colorize(x: str, color: Union[Colors, str]) -> str:
    """Render the given text with the desired color

    Args:
        x (str): The string to render
        color (Union[Colors, str]): The name of the color

    Returns:
        x_color (str): The input string with color applied
    """
    return _apply_color(x, color, FG_COLOR_CODES)


def bg_colorize(x: str, color: Union[Colors, str]) -> str:
    """Render the given text with the desired background color

    Args:
        x (str): The string to render
        color (Union[Colors, str]): The name of the color

    Returns:
        x_color (str): The input string with color applied
    """
    return _apply_color(x, color, BG_COLOR_CODES)


def decolorize(x: str) -> str:
    """Remove all color encoding from a string

    Args:
        x (str): The string with color

    Returns:
        x_no_color (str): The input string with color removed
    """
    for color_seq in list(FG_COLOR_CODES.values()) + list(BG_COLOR_CODES.values()):
        x = x.replace(f"{color_seq}m", "")
    x = x.replace(COLOR_START, "")
    x = x.replace(COLOR_END, "")
    x = x.replace("0m", "")  # TODO: Make this not prone to removing "1.0mb"
    return x


## Impl ########################################################################


def _apply_color(
    x: str,
    color: Union[Colors, str],
    color_dict: Dict[Union[Colors, str], str],
) -> str:
    """Apply the color or raise a ValueError"""
    if color_code := color_dict.get(color):
        return f"{COLOR_START}{color_code}m{x}{COLOR_END}"
    raise ValueError(f"Invalid color: {color}")
