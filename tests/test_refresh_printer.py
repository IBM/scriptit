"""
Tests for RefreshPrinter
"""
# Standard
from unittest import mock

# Third Party
import pytest

from tests.conftest import ResettableStringIO

# Local
from scriptit import RefreshPrinter


def test_refresh_printer_multi_line():
    """Test that adding multiple lines refreshes correctly"""
    stream = ResettableStringIO()
    printer = RefreshPrinter(write_stream=stream)

    # Perform initial add and refresh
    printer.add("Line one")
    printer.add("Line two")
    printer.refresh()
    assert printer.refreshes == 1
    printed_lines = stream.getvalue().split("\n")
    assert len(printed_lines) == 3  # Two plus final empty line
    assert not any(line.startswith(RefreshPrinter.UP_LINE) for line in printed_lines)
    stream.reset()

    # Perform a second refresh and make sure clearing happens
    printer.add("Line three")
    printer.add("Line four")
    printer.refresh()
    assert printer.refreshes == 2
    printed_lines = stream.getvalue().split("\n")
    assert len(printed_lines) == 4  # Clear, 2 new, final \n
    assert printed_lines[0].count(RefreshPrinter.UP_LINE) == 3


def test_refresh_printer_newline_in_add():
    """Make sure that a newline in add is handled as separate lines"""
    stream = ResettableStringIO()
    printer = RefreshPrinter(write_stream=stream)

    # Perform initial add and refresh
    printer.add("Line one\nLine two")
    printer.refresh()
    assert printer.refreshes == 1
    printed_lines = stream.getvalue().split("\n")
    assert len(printed_lines) == 3  # Two plus final empty line
    assert not any(line.startswith(RefreshPrinter.UP_LINE) for line in printed_lines)


@pytest.mark.parametrize("wrap", [True, False])
def test_refresh_printer_wrap_lines(wrap):
    """Make sure long lines get wrapped if requested"""
    term_size_mock = mock.MagicMock()
    term_width = 5
    term_size_mock.columns = term_width
    with mock.patch("shutil.get_terminal_size", return_value=term_size_mock):
        stream = ResettableStringIO()
        printer = RefreshPrinter(write_stream=stream)

        # Perform initial add and refresh
        long_line = "*" * int(2.5 * term_width)
        printer.add(long_line, wrap=wrap)
        printer.refresh()
        printed_lines = stream.getvalue().split("\n")
        assert len(printed_lines) == 4 if wrap else 2


def test_clear_last_report_chars():
    """Make sure that shorter lines in an update don't retain characters from
    previous reports
    """
    stream = ResettableStringIO()
    printer = RefreshPrinter(write_stream=stream)

    # Perform initial add and refresh
    printer.add("Line one")
    printer.refresh()
    stream.reset()

    # Perform a second with a shorter line and make sure that the line does not
    # have any of the previous report in it
    printer.add("two")
    printer.refresh()
    printed_lines = stream.getvalue().split("\n")
    assert len(printed_lines) == 3  # Clear, 1 new, final \n
    assert printed_lines[0].count(RefreshPrinter.UP_LINE) == 2
    assert printed_lines[1].strip() == "two"
