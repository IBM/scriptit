"""
Shared testing utilities
"""

# Standard
import io


class ResettableStringIO(io.StringIO):
    """TextIO that can be reset to an empty buffer for sequential outputs"""

    def reset(self):
        io.StringIO.__init__(self)
