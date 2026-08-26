"""Temperature conversion utilities.

Supports Celsius, Fahrenheit, and Kelvin. Unit strings are accepted
case-insensitively, using either a single-letter code ("C", "F", "K")
or the full name ("celsius", "fahrenheit", "kelvin").
"""

from __future__ import annotations

_ALIASES = {
    "c": "C",
    "celsius": "C",
    "f": "F",
    "fahrenheit": "F",
    "k": "K",
    "kelvin": "K",
}

_ABSOLUTE_ZERO_C = -273.15


def _normalize_unit(unit: str) -> str:
    try:
        key = unit.strip().lower()
    except AttributeError as exc:
        raise ValueError(f"Unknown temperature unit: {unit!r}") from exc

    normalized = _ALIASES.get(key)
    if normalized is None:
        raise ValueError(f"Unknown temperature unit: {unit!r}")
    return normalized


def _to_celsius(value: float, unit: str) -> float:
    if unit == "C":
        return value
    if unit == "F":
        return (value - 32) * 5 / 9
    if unit == "K":
        return value - 273.15
    raise AssertionError(f"unreachable unit: {unit!r}")


def _from_celsius(value_c: float, unit: str) -> float:
    if unit == "C":
        return value_c
    if unit == "F":
        return value_c * 9 / 5 + 32
    if unit == "K":
        return value_c + 273.15
    raise AssertionError(f"unreachable unit: {unit!r}")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit``.

    Units may be given case-insensitively as a single letter ("C", "F", "K")
    or a full name ("celsius", "fahrenheit", "kelvin").

    Raises:
        ValueError: if either unit is unrecognized, or if ``value`` is
            physically invalid (below absolute zero) for ``from_unit``.
    """
    normalized_from = _normalize_unit(from_unit)
    normalized_to = _normalize_unit(to_unit)

    value_c = _to_celsius(value, normalized_from)
    if value_c < _ABSOLUTE_ZERO_C - 1e-9:
        raise ValueError(
            f"Value {value} {from_unit!r} is below absolute zero"
        )

    return _from_celsius(value_c, normalized_to)
