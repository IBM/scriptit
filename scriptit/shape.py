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
from typing import Any, List, Optional, Tuple
import shutil

# Local
from .color import decolorize

## Public ######################################################################


def progress_bar(
    complete_pct: float,
    width: Optional[int] = None,
    done_char: str = "=",
    undone_char: str = "-",
    head_char: str = ">",
) -> str:
    """Format a progress bar showing the given percent complete with the given
    total width

    Args:
        complete_pct (float): Float value in [0, 1] showing percent complete
        width (Optional[int]): The width (in characters) of the full bar.
            Defaults to the width of the current terminal
        done_char (str): The character representing completion
        undone_char (str): The character representing incomplete
        head_char (str): The character representing the head of the completion
            arrow

    Returns:
        progress_bar_str (str): String for the progress bar
    """
    if len(done_char) != 1 or len(undone_char) != 1 or len(head_char) != 1:
        raise ValueError("All char args must have length 1")
    # Flatten to [0, 1]. This is done instead of raising since this may be
    # computed and should not break
    complete_pct = max(min(1.0, complete_pct), 0.0)
    if width is None:
        width = shutil.get_terminal_size().columns
    n_done = int((width - 3) * complete_pct)
    n_undone = width - 3 - n_done
    return "[{}{}{}]".format(done_char * n_done, head_char, undone_char * n_undone)


def box(x: Any, char: str = "#", width: Optional[int] = None) -> str:
    """Render the content of the given string inside a box frame

    Args:
        x (Any): The printable value to be framed in the box
        char (str): The character to use for the box frame
        width (Optional[int]): The width of the box (defaults to terminal)

    Returns:
        boxed_text (str): The wrapped text inside the box
    """
    if width is None:
        width = shutil.get_terminal_size().columns
    x = str(x)
    raw_lines = x.split("\n")
    lines = []
    longest = 0
    max_len = width - 4
    for line in raw_lines:
        sublines, longest_subline_len = _word_wrap_to_len(line, max_len)
        lines += sublines
        longest = max(longest, longest_subline_len)
    out = "{}\n".format(char * (longest + 4))
    for line in lines:
        padding = " " * (longest - _printed_len(line))
        out += f"{char} {line}{padding} {char}\n"
    out += "{}\n".format(char * (longest + 4))
    return out


def table(
    columns: List[List[Any]],
    width: Optional[int] = None,
    max_width: Optional[int] = None,
    min_width: Optional[int] = None,
    row_dividers: bool = True,
    header: bool = True,
    hframe_char: str = "-",
    vframe_char: str = "|",
    corner_char: str = "+",
    header_char: str = "=",
) -> str:
    """Encode the given columns as an ascii table

    Args:
        columns (List[List[Any]]): List of columns, each consisting of a list of
            string entries. The first entry in each column is considered the
            column header
        width (Optional[int]): The width of the table (defaults to terminal)
        max_width (Optional[int]): If no width given, upper bound on computed
            width based on content
        min_width (Optional[int]): If no width given, the lower bound on
            computed width based on content
        row_dividers (bool): Include dividers between rows
        header (bool): Include a special divider between header and rows
        hframe_char (str): Single character for horizontal frame lines
        vframe_char (str): Single character for vertical frame lines
        corner_char (str): Single character for corners
        header_char (str): Single character for the header horizontal divider

    Returns:
        table (str): The formatted table string
    """
    # Validate arguments
    if any(
        len(char) != 1 for char in [hframe_char, vframe_char, corner_char, header_char]
    ):
        raise ValueError("*_char args must be a single character")
    if len(set([len(col) for col in columns])) > 1:
        raise ValueError("All columns must have equal length")

    if max_width is None:
        max_width = shutil.get_terminal_size().columns
    if min_width is None:
        min_width = 2 * len(columns) + 1 if width is None else width

    # Stringify all column content
    columns = [[str(val) for val in col] for col in columns]
    empty_cols = [i for i, col in enumerate(columns) if not any(col)]
    if empty_cols:
        raise ValueError(f"Found empty column(s) when stringified: {empty_cols}")

    # Determine the raw max width of each column
    max_col_width = max_width - 3 - 2 * (len(columns) - 1)
    widths = [
        min(max(_printed_len(x) for x in column), max_col_width) for column in columns
    ]

    # Determine the full width of the table
    total_width = sum([w + 3 for w in widths]) + 1
    table_width = max(min(total_width, max_width), min_width)
    usable_table_width = table_width - 1

    # For each column, determine the width as a percentage of the total width
    pcts = [float(w) / float(total_width) for w in widths]
    col_widths = [int(p * usable_table_width) + 3 for p in pcts]
    if col_widths:
        col_widths[-1] = usable_table_width - sum(col_widths[:-1])
    else:
        col_widths = [0]

    # Prepare the rows
    wrapped_cols = []
    for i, col in enumerate(columns):
        wrapped_cols.append([])
        for entry in col:
            if col_widths[i] - 2 <= 1:
                raise ValueError(f"Column width collapsed for col {i}")
            wrapped, _ = _word_wrap_to_len(entry, col_widths[i] - 2)
            wrapped_cols[-1].append(wrapped)

    # Go row-by-row and add to the output
    out = _make_hline(table_width, char=hframe_char, edge=corner_char)
    n_rows = max([len(col) for col in columns]) if columns else 0
    if not n_rows:
        if header:
            out += _make_hline(table_width, char=header_char, edge=vframe_char)
        out += _make_hline(table_width, char=hframe_char, edge=corner_char)
    for r in range(n_rows):
        entries = [col[r] if r < len(col) else [""] for col in wrapped_cols]
        most_sublines = max([len(e) for e in entries])
        for i in range(most_sublines):
            line = ""
            for c, entry in enumerate(entries):
                val = entry[i] if len(entry) > i else ""
                line += "{} {}{}".format(
                    vframe_char, val, " " * (col_widths[c] - _printed_len(val) - 2)
                )
            line += f"{vframe_char}\n"
            out += line
        if r == 0:
            if header:
                out += _make_hline(table_width, char=header_char, edge=vframe_char)
            elif row_dividers:
                out += _make_hline(table_width, char=hframe_char, edge=vframe_char)
        elif r < n_rows - 1:
            if row_dividers:
                out += _make_hline(table_width, char=hframe_char, edge=vframe_char)
        else:
            out += _make_hline(table_width, char=hframe_char, edge=corner_char)

    return out


## Impl ########################################################################


def _printed_len(x: str) -> int:
    """Get the length of the given string with non-printed characters removed"""
    return len(decolorize(x))


def _word_wrap_to_len(line: str, max_len: int) -> Tuple[List[str], int]:
    """Wrap the given line into a list of lines, each no longer than max_len
    using whitespace tokenization for word splitting.

    Args:
        line (str): The input line to be wrapped
        max_len (int): The max len for lines in the wrappe doutput

    Returns:
        sublines (List[str]): The lines wrapped to the target length
        longest (int): The length of the longest wrapped line (<= max_len)
    """
    if (printed_len := _printed_len(line)) <= max_len:
        return [line], printed_len
    else:
        longest = 0
        sublines = []
        words = line.split(" ")
        while len(words):
            subline = ""
            while len(words):
                if _printed_len(subline) + _printed_len(words[0]) <= max_len:
                    subline += words[0] + " "
                    words = words[1:]
                elif _printed_len(words[0]) > max_len:
                    cutoff = max_len - _printed_len(subline) - 1
                    if cutoff <= 0:
                        break
                    else:
                        subline += words[0][:cutoff] + "- "
                        words[0] = words[0][cutoff:]
                else:
                    # NOTE: This _is_ covered in tests, but the coverage engine
                    #   doesn't pick it up for some reason!
                    break  # pragma: no cover
            subline = subline[:-1]
            longest = max(longest, _printed_len(subline))
            sublines.append(subline)
        return sublines, longest


def _make_hline(table_width: int, char: str, edge: str) -> str:
    return "{}{}{}\n".format(edge, char * (table_width - 2), edge)
