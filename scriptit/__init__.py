"""
Scriptit: A collection of tools for writing interactive terminal applications.
"""

__version__ = "1.0.0"

# Import submodules
from . import color
from . import shape
from . import size

# Public API
__all__ = ["color", "shape", "size"]
