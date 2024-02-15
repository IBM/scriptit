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


@pytest.mark.parametrize(
    ["x", "kwargs", "exp_text_lines"],
    [
        ("Hello World", {}, 1),
        ("Hello World", {"char": "*"}, 1),
        ("Hello World", {"width": 9}, 2),
    ],
)
def test_box(x, kwargs, exp_text_lines):
    """Test various configs for boxes"""
    box = shape.box(x, **kwargs)
    box_lines = box.strip().split("\n")
    assert len(box_lines) == exp_text_lines + 2
    assert box_lines[0]
    frame_char = box_lines[0][0]
    assert all(
        set([ch for ch in line]) == {frame_char}
        for line in [box_lines[0], box_lines[-1]]
    )
    assert all(
        line[0] == frame_char and line[-1] == frame_char for line in box_lines[1:-1]
    )


@pytest.mark.parametrize(
    ["columns", "kwargs"],
    [
        # Simple 2x3
        ([["First", "Gabe", "Me"], ["Last", "Goodhart", "You"]], {}),
        # Empty element
        ([["First", "Gabe", "Me"], ["Last", "", "You"]], {}),
        # Empty header
        ([["", "Gabe", "Me"], ["Last", "", "You"]], {}),
        # No header
        ([["First", "Gabe", "Me"], ["Last", "Goodhart", "You"]], {"header": False}),
        # No row div
        (
            [["First", "Gabe", "Me"], ["Last", "Goodhart", "You"]],
            {"row_dividers": False},
        ),
        # No row div or header
        (
            [["First", "Gabe", "Me"], ["Last", "Goodhart", "You"]],
            {"row_dividers": False, "header": False},
        ),
        # Custom chars
        (
            [["First", "Gabe", "Me"], ["Last", "Goodhart", "You"]],
            {
                "hframe_char": "H",
                "vframe_char": "V",
                "corner_char": "*",
                "header_char": "$",
            },
        ),
        # Empty table
        ([], {}),
        # Word wrapping
        ([["Name", "My name is Gabe Goodhart"], ["Foo Bar", "Y"]], {"max_width": 15}),
    ],
)
def test_table_valid(columns, kwargs):
    """Test various valid configs for tables"""
    table = shape.table(columns, **kwargs)
    table_lines = table.strip().split("\n")
    assert len(table_lines) >= 2
    top_frame = table_lines[0]
    bottom_frame = table_lines[-1]
    assert len(top_frame) > 1
    assert len(bottom_frame) > 1
    corner = top_frame[0]
    assert kwargs.get("corner_char", corner) == corner
    assert {top_frame[-1], bottom_frame[0], bottom_frame[-1]} == {corner}
    if columns:
        assert len(top_frame) > 2
        hline_char = top_frame[1]
        assert kwargs.get("hframe_char", hline_char) == hline_char
        assert set([ch for ch in top_frame[1:-1]]) == {hline_char}
        assert set([ch for ch in bottom_frame[1:-1]]) == {hline_char}
        assert len(table_lines) > 2
        vline_char = table_lines[1][0]
        assert kwargs.get("vframe_char", vline_char) == vline_char

        # Test the horizontal dividers
        do_row_divs = kwargs.get("row_dividers", True)
        do_header = kwargs.get("header", True)
        hlines = [
            line for line in table_lines[1:-1] if len(line) >= 2 and line[1] != " "
        ]
        if not do_row_divs and not do_header:
            assert not hlines
        else:
            exp_hlines = len(columns[0]) - 1 if do_row_divs else 1
            assert len(hlines) == exp_hlines
            assert all(set([hline[0], hline[-1]]) == {vline_char} for hline in hlines)
            if do_header:
                header_hline = hlines[0]
                row_divs = hlines[1:]
                header_char = header_hline[2]
                assert kwargs.get("header_char", header_char) == header_char
                assert set([ch for ch in header_hline[1:-1]]) == {header_char}
            else:
                row_divs = hlines
            if row_divs:
                assert len(set(row_divs)) == 1
                row_div = row_divs[0]
                assert set([ch for ch in row_div[1:-1]]) == {hline_char}

        # Test the vertical dividers
        body_lines = [
            line for line in table_lines[1:-1] if len(line) >= 2 and line[1] == " "
        ]
        exp_vlines = len(columns) + 1
        assert all(
            line.count(vline_char) == exp_vlines and line[0] == line[-1] == vline_char
            for line in body_lines
        )


@pytest.mark.parametrize(
    ["columns", "kwargs"],
    [
        # No valid columns
        ([[]], {}),
        # Some invalid columns
        ([["Hi", "there"], ["", ""]], {}),
        # Uneven columns
        ([["Hi", "there"], ["Hey"]], {}),
        # Invalid char overrides
        ([["Hi"]], {"hframe_char": "--"}),
        # Column collapse
        ([["Hi", "This is a test to see how long"], ["X", "X"]], {"max_width": 5}),
    ],
)
def test_table_invalid(columns, kwargs):
    """Make sure all invalid kwarg options raise ValueError"""
    with pytest.raises(ValueError):
        shape.table(columns, **kwargs)
