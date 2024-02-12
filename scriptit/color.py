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
from typing import Union

## Public ######################################################################


class Colors(Enum):
    black = "black"
    dark_gray = "dark_gray"
    red = "red"
    light_red = "light_red"
    green = "green"
    light_green = "light_green"
    brown = "brown"
    orange = "orange"
    yellow = "yellow"
    blue = "blue"
    light_blue = "light_blue"
    purple = "purple"
    light_purple = "light_purple"
    cyan = "cyan"
    light_cyan = "light_cyan"
    light_gray = "light_gray"
    white = "white"


## Mapping from color name to ansi escape code for foreground color
FG_COLOR_CODES = {
    Colors.black: "0;30",
    Colors.dark_gray: "1;30",
    Colors.red: "0;31",
    Colors.light_red: "1;31",
    Colors.green: "0;32",
    Colors.light_green: "1;32",
    Colors.brown: "0;33",
    Colors.orange: "0;33",
    Colors.yellow: "1;33",
    Colors.blue: "0;34",
    Colors.light_blue: "1;34",
    Colors.purple: "0;35",
    Colors.light_purple: "1;35",
    Colors.cyan: "0;36",
    Colors.light_cyan: "1;36",
    Colors.light_gray: "0;37",
    Colors.white: "1;37",
}
FG_COLOR_CODES.update(**{key.value: val for key, val in FG_COLOR_CODES.items()})

## Mapping from color name to ansi escape code for background color
BG_COLOR_CODES = {
    Colors.black: "0;40",
    Colors.dark_gray: "1;40",
    Colors.red: "0;41",
    Colors.light_red: "1;41",
    Colors.green: "0;42",
    Colors.light_green: "1;42",
    Colors.brown: "0;43",
    Colors.orange: "0;43",
    Colors.yellow: "1;43",
    Colors.blue: "0;44",
    Colors.light_blue: "1;44",
    Colors.purple: "0;45",
    Colors.light_purple: "1;45",
    Colors.cyan: "0;46",
    Colors.light_cyan: "1;46",
    Colors.light_gray: "0;47",
    Colors.white: "1;47",
}
BG_COLOR_CODES.update(**{key.value: val for key, val in BG_COLOR_CODES.items()})

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
    assert color in FG_COLOR_CODES
    return f"{COLOR_START}{FG_COLOR_CODES[color]}m{x}{COLOR_END}"


def bg_colorize(x: str, color: Union[Colors, str]) -> str:
    """Render the given text with the desired background color

    Args:
        x (str): The string to render
        color (Union[Colors, str]): The name of the color

    Returns:
        x_color (str): The input string with color applied
    """
    assert color in BG_COLOR_CODES
    return f"{COLOR_START}{BG_COLOR_CODES[color]}m{x}{COLOR_END}"


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
