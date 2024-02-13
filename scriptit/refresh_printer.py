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
This utility is used to set up a command line output formatter which will print
content that updates in place. It is useful for printing running status during
long-running processes. For example:

p = RefreshPrinter()
for i in range(100):
    p.add("Dummy Report:")
    p.add("    iteration: " + i)
    p.refresh()
    time.sleep(1)

NOTE: the report can smoothly grow in the number of lines. Reducing the number
    of lines may result in odd behavior.
"""

# Standard
from typing import Any, TextIO
import shutil
import sys


class RefreshPrinter:
    __doc__ = __doc__

    UP_LINE = "\033[F"

    def __init__(
        self,
        do_refresh: bool = True,
        mute: bool = False,
        refresh_rate: int = 1,
        write_stream: TextIO = sys.stdout,
    ):
        """Set up the printer

        Args:
            do_refresh (bool): Perform line clearing before printing next frame.
                Disable if output will be mixed with other sources
            mute (bool): Silence all output
            refresh_rate (bool): Number of refreshes between writing to the
                output stream
            write_stream (TextIO): The output stream
        """
        self.do_refresh = do_refresh
        self.mute = mute
        self.refresh_rate = refresh_rate
        self.write_stream = write_stream

        self.last_report = None
        self.current_report = []
        self.refreshes = 0

    def add(self, content: Any, wrap: bool = True):
        """Add the given content to the report

        Args:
            content (Any): The content to add
            wrap (bool): Whether or not to perform line wrapping
        """
        width = shutil.get_terminal_size().columns
        for line in str(content).split("\n"):
            while wrap and len(line) > width:
                self.current_report.append(line[:width])
                line = line[width:]
            self.current_report.append(line)

    # When ready to cycle from the last report to the current, call refresh
    def refresh(self, force: bool = False):
        """Cycle the report

        Args:
            force (bool): Force the refreshed content to be written, regardless
                of refresh rate
        """
        self.refreshes += 1
        width = shutil.get_terminal_size().columns
        if force or self.refresh_rate == 1 or self.refreshes % self.refresh_rate == 1:
            if self.do_refresh and self.last_report is not None and not self.mute:
                line_clear = self.UP_LINE + " " * width
                self.write_stream.write(
                    line_clear * (len(self.last_report) + 1) + "\r\n"
                )
            for i, line in enumerate(self.current_report):
                if (
                    self.last_report is not None
                    and i < len(self.last_report)
                    and len(line) < len(self.last_report[i])
                ):
                    line += " " * (len(self.last_report[i]) - len(line))
                if not self.mute:
                    self.write_stream.write(line + "\n")
            self.write_stream.flush()
            self.last_report = self.current_report
        self.current_report = []
