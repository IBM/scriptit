"""
Tests for the shape module
"""
# Standard
import re

# Third Party
import pytest

# Local
from scriptit import shape


def test_progress_bar():
    """Test various progress_bar configurations"""
    assert shape.progress_bar(0.5, 10) == "[===>----]"
    assert (
        shape.progress_bar(0.5, 10, done_char=">", undone_char=".", head_char="|")
        == "[>>>|....]"
    )
    assert shape.progress_bar(-1, 10) == "[>-------]"
    assert shape.progress_bar(2, 10) == "[=======>]"
    match = re.match(r"\[(=+)>(-)+\]", shape.progress_bar(0.75))
    assert match
    assert len(match.group(1)) > len(match.group(2))
    with pytest.raises(ValueError):
        shape.progress_bar(0.5, 10, done_char="xx")


def test_box():
    """Test various"""
