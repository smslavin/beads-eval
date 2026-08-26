"""Length unit conversion."""

from __future__ import annotations

# Canonical unit: meters. Each entry maps a canonical unit name to how many
# meters make up one of that unit.
_METERS_PER_UNIT = {
    "m": 1.0,
    "ft": 0.3048,
    "mi": 1609.344,
}

# Maps every accepted alias (lowercased) to its canonical unit key above.
_ALIASES = {
    "m": "m",
    "meter": "m",
    "meters": "m",
    "metre": "m",
    "metres": "m",
    "ft": "ft",
    "foot": "ft",
    "feet": "ft",
    "mi": "mi",
    "mile": "mi",
    "miles": "mi",
}


def _normalize(unit: str) -> str:
    if not isinstance(unit, str):
        raise ValueError(f"Unknown length unit: {unit!r}")
    key = unit.strip().lower()
    try:
        return _ALIASES[key]
    except KeyError:
        raise ValueError(f"Unknown length unit: {unit!r}") from None


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit``.

    Supported units (case-insensitive): meters ("m", "meter", "meters",
    "metre", "metres"), feet ("ft", "foot", "feet"), and miles ("mi",
    "mile", "miles").

    Raises:
        ValueError: if either unit is unrecognized, or if ``value`` is
            negative.
    """
    if value < 0:
        raise ValueError(f"Length value cannot be negative: {value!r}")

    from_key = _normalize(from_unit)
    to_key = _normalize(to_unit)

    meters = value * _METERS_PER_UNIT[from_key]
    return meters / _METERS_PER_UNIT[to_key]
