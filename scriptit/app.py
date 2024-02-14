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
This utility is used to create a terminal app that has a logging panel and an
output panel for non-log output. It also offers an embedded mode which will
simply route all logging and output lines to the standard python logger.
"""

# Standard
from functools import partial
from io import StringIO
from typing import Callable, Optional, TextIO
import logging
import shutil

# Local
from .refresh_printer import RefreshPrinter


class TerminalApp:
    __doc__ = __doc__

    CONSOLE_START = "== CONSOLE "

    ## Construction ##############################################################

    def __init__(
        self,
        log_console_size: Optional[int] = None,
        log_console_pct: float = 0.25,
        pad_log_console: bool = False,
        log_file: Optional[str] = None,
        preserve_log_handlers: bool = False,
        *args,
        **kwargs,
    ):
        """Set up the app with configuration for how to display in the terminal

        Args:
            log_console_size (Optional[int]): Explicit number of rows for the
                log panel
            log_console_pct (float): If no explicit size given, percent (0, 1]
                of the terminal to use for the log panel
            pad_log_console (bool): Pad the log console with empty lines to fit
                the desired console size
            log_file (Optional[str]): File path to send log output to for
                offline visibility
            preserve_log_handlers (bool): If true, log messages will be emitted
                by existing handlers as well as being captured by the app's
                handler wrapper
        """
        self.log_console_size = log_console_size
        self.log_console_pct = log_console_pct
        self.pad_log_console = pad_log_console
        assert log_console_pct is None or (
            log_console_pct > 0 and log_console_pct <= 1.0
        )

        # Set up the log handlers
        self.log_string_output = StringIO()
        self.log_stream = self.log_string_output
        if log_file is not None:
            # Hold the file open here for writing and close on __del__
            self.log_file_handle = open(log_file, "w")  # noqa: SIM115
            self.log_stream = TextOutputSplitter(
                self.log_string_output, self.log_file_handle
            )
        self._wrap_all_logging(preserve_log_handlers)

        # Set up a buffer to store non-log lines in
        self.previous_content_entities = []
        self.content_entries = []

        # Set up the refresh printer that will manage the output on the screen
        self.printer = RefreshPrinter(*args, **kwargs)

    def __del__(self):
        if log_file_handle := getattr(self, "log_file_handle", None):
            log_file_handle.close()

    ## Interface #################################################################

    def add(self, content):
        self.content_entries.append(content)

    def refresh(self, force=False):
        self._refresh(force=force, use_previous=False)

    ## Implementation ############################################################

    def _wrap_all_logging(self, preserve_log_handlers: bool):
        """This helper takes ownership of all logging handlers now and for the
        future (unless another framework patches the root logger). The goal is
        to funnel _all_ logging messages to the app's output stream, regardless
        of when log configuration is invoked.
        """
        # Local binding for instantiating wrapped handlers
        make_wrapped_handler: Callable[[logging.Handler], HandlerWrapper] = partial(
            HandlerWrapper,
            log_stream=self.log_stream,
            log_to_wrapped=preserve_log_handlers,
            callback=self.refresh,
        )

        # Update all existing handlers
        # NOTE: The choice here to update _all_ handlers is based on the
        #   assumption that a user will be unlikely to configure multiple
        #   handlers when running a terminal app. If they do, log lines will end
        #   up duplicated for each handler. The alternative is to attempt to
        #   decide _which_ of the multiple handlers should be wrapped, but this
        #   gets further complicated by needing to handle future handlers, so
        #   the simpler choice is to just let this be a user problem.
        for logger in [logging.root] + list(logging.root.manager.loggerDict.values()):
            if isinstance(logger, logging.PlaceHolder):
                continue
            if logger.handlers:
                for i, handler in enumerate(logger.handlers):
                    logger.handlers[i] = make_wrapped_handler(handler)

        # When new loggers are set up and have handlers directly configured,
        # intercept them and wrap the handlers
        class WrappedLogger(logging.Logger):
            def addHandler(self, handler: logging.Handler):
                super().addHandler(make_wrapped_handler(handler))

        logging.root.manager.setLoggerClass(WrappedLogger)

        # Monkey-patch the addHandler function on the root logger so that when
        # root handlers are added, they too will be wrapped
        orig_root_add_handler = logging.root.addHandler

        def addHandler(handler: logging.Handler):
            orig_root_add_handler(make_wrapped_handler(handler))

        logging.root.addHandler = addHandler

    def _refresh(self, force, use_previous):
        """
        Refresh function with full functionality for console and main panes
        """

        # Get terminal size info
        term_info = shutil.get_terminal_size()
        width = term_info.columns
        height = term_info.lines

        # Compute the heights for the panels
        log_height = self.log_console_size or int(float(height) * self.log_console_pct)
        log_height = min(height - 1, log_height)
        max_log_lines = log_height - 2  # top/bottom frame
        content_height = height - log_height

        # Add the log console
        heading = self.CONSOLE_START
        raw_log_lines = filter(
            lambda line: bool(line.strip()),
            self.log_string_output.getvalue().split("\n"),
        )
        log_lines = []
        for line in raw_log_lines:
            while len(line) > width:
                log_lines.append(line[:width])
                line = line[width:]
            log_lines.append(line)
        # DEBUG
        print(log_lines)
        self.printer.add(heading + "=" * max(0, width - len(heading)))
        for line in log_lines[-max_log_lines:]:
            self.printer.add(line)
        if self.pad_log_console:
            for _ in range(max(0, max_log_lines - len(log_lines))):
                self.printer.add("")
        self.printer.add("=" * width)

        # Add the content
        content = (
            self.content_entries if not use_previous else self.previous_content_entities
        )
        for line in content[-content_height:]:
            self.printer.add(line)

        # Refresh
        self.printer.refresh(force=force)

        # Reset the content buffer if not using the previous one
        if not use_previous:
            self.previous_content_entities = self.content_entries
            self.content_entries = []


## Impl ########################################################################


class TextOutputSplitter(TextIO):
    """Utility class for splitting a text output stream to multiple streams"""

    def __init__(self, *streams: TextIO):
        """Construct with a set of streams"""
        self.streams = streams

    def write(self, *args, **kwargs):
        """Write to all streams"""
        for s in self.streams:
            s.write(*args, **kwargs)
            s.flush()

    def flush(self):
        """Flush all streams"""
        for s in self.streams:
            s.flush()


class HandlerWrapper(logging.Handler):
    """The HandlerWrapper class is a logging handler that will wrap all existing
    logging handlers and capture their output to a TextIO stream.
    """

    def __init__(
        self,
        wrapped_handler: logging.Handler,
        log_stream: TextIO,
        log_to_wrapped: bool = False,
        callback: Optional[Callable[[], None]] = None,
    ):
        """Set up with the handler to wrap

        Args:
            wrapped_handler (logging.Handler): The handler to wrap
            log_stream (TextIO): The output text stream
            log_to_wrapped (bool): If True, the wrapped handler's emit will be
                called after the formatted record is written to the stream
        """
        self.wrapped_handler = wrapped_handler
        self.log_stream = log_stream
        self.log_to_wrapped = log_to_wrapped
        self.callback = callback
        super().__init__()

        # Forward all handler methods to the wrapped handler except those
        # that are needed to capture the output
        for method_name in [
            "createLock",
            "acquire",
            "release",
            "setLevel",
            "setFormatter",
            "addFilter",
            "removeFilter",
            "filter",
            "flush",
            "close",
            "handleError",
            "format",
        ]:
            setattr(self, method_name, getattr(self.wrapped_handler, method_name))

    def emit(self, record: logging.LogRecord):
        """Capture a record as it is emitted and write it to the stream"""
        formatted = self.wrapped_handler.format(record)
        self.log_stream.write(formatted + "\n")
        self.log_stream.flush()
        if self.log_to_wrapped:
            self.wrapped_handler.emit(record)
        if self.callback:
            self.callback()
