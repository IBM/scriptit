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
This collection of tools helps making working with file sizes easy and human
readable.
"""

# Standard
from typing import List, Optional
import re

## Constants ###################################################################

## Default list of units
DEFAULT_UNITS = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
OVERFLOW_UNIT = "YB"

## Functions ###################################################################


def to_hr(num_bytes: int, units: Optional[List[str]] = None) -> str:
    """Get the human readable version of a size in bytes

    Args:
        num_bytes (int): The number of bytes
        units (Optional[List[str]]): The sequence of unit suffixes

    Returns:
        hr_size (str): Human readable size
    """
    assert isinstance(
        num_bytes, int
    ), "Can only convert from int bytes to human readable"
    if units is None:
        units = DEFAULT_UNITS
    fmt_num = float(num_bytes)
    for unit in units[:-1]:
        if abs(fmt_num) < 1024.0:
            return "{:3.1f}{}".format(fmt_num, unit)
        fmt_num /= 1024.0
    return "{:.1f}{}".format(fmt_num, units[-1])


def from_hr(hr_size: str, units: Optional[List[str]] = None) -> int:
    """Parse from the human readable version of a size back into bytes

    Args:
        hr_size (str): The human readable size string
        units (Optional[List[str]]): The sequence of unit suffixes

    Returns:
        num_bytes ()
    """
    assert isinstance(
        hr_size, str
    ), "Can only convert from string human readable to bytes"
    units = units or DEFAULT_UNITS
    for i, unit in enumerate(units):
        m = re.match("(\d*\.?\d*)" + unit, hr_size)
        if m:
            rawval = float(m.group(1))
            return int((1024.0**i) * rawval)
    raise ValueError(f"Unable to convert {hr_size} to number of bytes")
