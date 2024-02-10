Args:
    do_refresh (bool): Perform line clearing before printing the next frame. Disable if output will be mixed with other sources.
    mute (bool): Silence all output.
    refresh_rate (int): Number of refreshes between writing to the output stream.
    write_stream (TextIO): The output stream.
"""

def __init__(
    self,
    do_refresh: bool = True,
    mute: bool = False,
    refresh_rate: int = 1,
    write_stream: TextIO = sys.stdout,
):
    self.do_refresh = do_refresh
    self.mute = mute
    self.refresh_rate = refresh_rate
    self.write_stream = write_stream

    self.last_report = None
    self.current_report = []
    self.refreshes = 0

def add(self, content: Any, wrap: bool = True):
    """
    Add the given content to the report.

    Args:
        content (Any): The content to add.
        wrap (bool): Whether or not to perform line wrapping.
    """
    width = shutil.get_terminal_size().columns
    for line in str(content).split("\n"):
        while wrap and len(line) > width:
            self.current_report.append(line[:width])
            line = line[width:]
        self.current_report.append(line)

def refresh(self, force: bool = False):
    """
    Cycle the report.

    Args:
        force (bool): Force the refreshed content to be written, regardless of the refresh rate.
    """
    self.refreshes += 1
    width = shutil.get_terminal_size().columns
    if force or self.refresh_rate == 1 or self.refreshes % self.refresh_rate == 1:
        if self.do_refresh and self.last_report is not None and not self.mute:
            line_clear = "\033[F" + " " * width
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
