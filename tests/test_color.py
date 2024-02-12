"""
Tests for the color tools
"""

# Third Party
import pytest

# Local
from scriptit import color


@pytest.mark.parametrize("color_fn", [color.colorize, color.bg_colorize])
def test_color_round_trip(color_fn):
    """Make sure that the colorize functions round trip with decolorize"""
    text = "Hello there world!"
    colorized = color_fn(text, "red")
    assert colorized != text
    assert colorized.startswith(color.COLOR_START)
    assert colorized.endswith(color.COLOR_END)
    round_trip = color.decolorize(colorized)
    assert round_trip == text


@pytest.mark.parametrize("enum_val", color.Colors)
def test_colorize_enum_or_name(enum_val):
    """Make sure that the enum value and the string name can both be used"""
    txt = "Lorum ipsum"
    assert color.colorize(txt, enum_val) == color.colorize(txt, enum_val.value)
    assert color.bg_colorize(txt, enum_val) == color.bg_colorize(txt, enum_val.value)


def test_invalid_color():
    """Make sure that a ValueError is raised on an invalid color"""
    with pytest.raises(ValueError):
        color.colorize("hey there", "not valid")
