"""
This collection of tools helps make working with file sizes easy and human-readable.
"""

from typing import List, Optional
import re

DEFAULT_UNITS = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]

def to_hr(num_bytes: int, units: Optional[List[str]] = None) -> str:
    """Get the human-readable version of a size in bytes

    Args:
        num_bytes (int): The number of bytes
        units (Optional[List[str]]): The sequence of unit suffixes

    Returns:
        hr_size (str): Human-readable size
    """
    assert isinstance(num_bytes, int), "Input must be an integer representing bytes"
    if units is None:
        units = DEFAULT_UNITS
    fmt_num = float(num_bytes)
    for unit in units:
        if abs(fmt_num) < 1024.0:
            return "{:3.1f}{}".format(fmt_num, unit)
        fmt_num /= 1024.0
    return "{:.1f}{}".format(fmt_num, "YB")


def from_hr(hr_size: str, units: Optional[List[str]] = None) -> int:
    """Parse from the human-readable version of a size back into bytes

    Args:
        hr_size (str): The human-readable size string
        units (Optional[List[str]]): The sequence of unit suffixes

    Returns:
        num_bytes (int): Number of bytes
    """
    assert isinstance(hr_size, str), "Input must be a string representing a human-readable size"
    if units is None:
        units = DEFAULT_UNITS
    for i, unit in enumerate(units):
        m = re.match(r"(\d*\.?\d*)" + unit, hr_size)
        if m:
            rawval = float(m.group(1))
            return int((1024.0 ** i) * rawval)
    raise ValueError(f"Unable to convert '{hr_size}' to number of bytes")
