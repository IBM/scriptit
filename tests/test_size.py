"""
Tests for the size tools
"""

# Third Party
import pytest

# Local
from scriptit import size


@pytest.mark.parametrize(
    ["num_bytes", "hr_val", "round_trip_bytes", "units"],
    [
        # Bytes
        (5, "5.0B", 5, None),
        # KB
        (int(12.34 * 1024), "12.3KB", int(12.3 * 1024), None),
        # MB
        (int(4.2 * (1024**2)), "4.2MB", int(4.2 * (1024**2)), None),
        # YB (overflow)
        (
            2000 * (1024 ** (len(size.DEFAULT_UNITS) - 1)),
            "2000.0YB",
            2000 * (1024 ** (len(size.DEFAULT_UNITS) - 1)),
            None,
        ),
        # GB w/ non-default units
        (
            37 * (1024**3),
            "37.0gb",
            37 * (1024**3),
            [unit.lower() for unit in size.DEFAULT_UNITS],
        ),
    ],
)
def test_size_to_from_hr(num_bytes, hr_val, round_trip_bytes, units):
    """Test round tripping bytes through human readable form"""
    hr = size.to_hr(num_bytes, units)
    assert hr == hr_val
    round_trip = size.from_hr(hr, units)
    assert round_trip == round_trip_bytes


def test_unparsable_hr():
    """Make sure that a ValueError is raised if the value can't be parsed"""
    with pytest.raises(ValueError):
        size.from_hr("not valid")
