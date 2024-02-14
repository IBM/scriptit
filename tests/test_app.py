"""
Tests for TerminalApp
"""

# Standard
from contextlib import contextmanager
from unittest import mock
import logging
import os
import tempfile

from tests.conftest import ResettableStringIO

# Local
from scriptit import RefreshPrinter, TerminalApp


@contextmanager
def reset_logging():
    """Fixture to reset global changes to the logging module

    NOTE: This uses a contextmanager instead of a fixture because the pytest log
        capture system takes place _after_ a fixture runs and therefore the
        tests end up with multiple handlers.
    """
    new_root = logging.RootLogger(logging.root.level)
    new_manager = logging.Manager(new_root)
    new_root.manager = new_manager
    with mock.patch("logging.root", new_root):
        with mock.patch.object(logging.Logger, "manager", new_manager):
            with mock.patch.object(logging.Logger, "root", new_root):
                logging.basicConfig()
                log = new_root.getChild("TEST")
                yield log


def test_app_basic():
    """Test that the basic execution of the app works as expected"""
    with reset_logging() as log:
        # Set up the app that will capture the logging
        stream = ResettableStringIO()
        app = TerminalApp(write_stream=stream)

        # Log and make sure the content went to the stream
        log.warning("hello")
        lines = stream.getvalue().split("\n")
        assert len(lines) == 4
        assert lines[0].startswith(TerminalApp.CONSOLE_START)
        assert "hello" in lines[1]
        assert set([ch for ch in lines[2].strip()]) == {"="}
        assert not lines[3].strip()
        stream.reset()

        # Add some content and refresh. This will include the logs and the added
        # content lines
        app.add("Line one")
        app.add("Line two")
        app.refresh()
        lines = stream.getvalue().split("\n")
        assert len(lines) == 7
        assert lines[0].count(RefreshPrinter.UP_LINE) == 4
        assert lines[1].startswith(TerminalApp.CONSOLE_START)
        assert "hello" in lines[2]
        assert set([ch for ch in lines[3].strip()]) == {"="}
        assert lines[4].strip() == "Line one"
        assert lines[5].strip() == "Line two"
        assert not lines[6].strip()


def test_app_log_file():
    """Test that logging to a file works alongside the app"""
    with tempfile.TemporaryDirectory() as workdir, reset_logging() as log:
        log_file = os.path.join(workdir, "test.log")
        stream = ResettableStringIO()
        TerminalApp(write_stream=stream, log_file=log_file)

        # Log and make sure the content went to the stream and the file
        log.warning("hello")
        lines = stream.getvalue().split("\n")
        assert len(lines) == 4
        with open(log_file, "r") as handle:
            log_file_lines = list(handle.readlines())
        assert len(log_file_lines) == 1
        stream.reset()

        # Log again and make sure there are now two log lines in the file
        log.warning("world")
        lines = stream.getvalue().split("\n")
        assert len(lines) == 6  # Clear + extra log line
        with open(log_file, "r") as handle:
            log_file_lines = list(handle.readlines())
        assert len(log_file_lines) == 2


def test_app_preserve_logs():
    """Test that preserving existing loggers works as expected"""
    with reset_logging() as log:
        stream = ResettableStringIO()
        logger_stream = ResettableStringIO()
        logging.root.addHandler(logging.StreamHandler(logger_stream))
        TerminalApp(write_stream=stream, preserve_log_handlers=True)
        log.warning("hello")
        logged_lines = logger_stream.getvalue().split("\n")
        assert len(logged_lines) == 2
        assert "hello" in logged_lines[0]
        assert not logged_lines[1].strip()


def test_app_pad_log_console():
    """Test that the log console can be padded to a fixed size"""
    with reset_logging():
        stream = ResettableStringIO()
        TerminalApp(
            write_stream=stream,
            pad_log_console=True,
            log_console_size=5,
        )
        log = logging.getLogger("NEW")
        log.warning("watch out")
        lines = stream.getvalue().split("\n")
        assert len(lines) == 6  # Padded to 5 plus last newline


def test_app_logging_post_config():
    """Test that logging can be configured after the app initializes and log
    placeholders don't cause any problems
    """
    with reset_logging():
        stream = ResettableStringIO()
        TerminalApp(write_stream=stream)
        logging.basicConfig(level=logging.INFO, force=True)
        log = logging.getLogger("foo.bar.baz")
        log.info("hello there")
        lines = stream.getvalue().split("\n")
        assert len(lines) == 4  # Header, line, footer, newline


def test_app_logging_direct_add_handler():
    """Make sure that addHandler called on a logger will get wrapped"""
    with reset_logging():
        stream = ResettableStringIO()
        TerminalApp(write_stream=stream)
        log = logging.getLogger("test")
        log.addHandler(logging.StreamHandler())
        log.setLevel(logging.DEBUG)
        log.propagate = False
        log.debug("watch out")
        lines = stream.getvalue().split("\n")
        assert len(lines) == 4  # Header, line, footer, newline


def test_app_logging_placeholder():
    """Make sure that logging placeholders can be safely reconfigured"""
    with reset_logging():
        log = logging.getLogger("foo.bar.baz")
        stream = ResettableStringIO()
        TerminalApp(write_stream=stream)
        log.warning("test")
        lines = stream.getvalue().split("\n")
        assert len(lines) == 4  # Header, line, footer, newline


def test_app_wrap_long_log_lines():
    """Make sure long lines get wrapped if they exceed the term width"""
    term_size_mock = mock.MagicMock()
    term_width = 20
    term_size_mock.columns = term_width
    term_size_mock.lines = 150
    with reset_logging() as log, mock.patch(
        "shutil.get_terminal_size", return_value=term_size_mock
    ):
        stream = ResettableStringIO()
        TerminalApp(write_stream=stream)
        msg = "*" * int(term_width * 2.1)
        log.warning(msg)
        lines = stream.getvalue().split("\n")
        assert len(lines) == 6
