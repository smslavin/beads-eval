"""Weight/mass unit conversion."""

from __future__ import annotations

# Canonical unit key -> conversion factor to kilograms.
_TO_KILOGRAMS = {
    "kg": 1.0,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}

# Accepted aliases (case-insensitive) mapped to their canonical unit key.
_ALIASES = {
    "kg": "kg",
    "kilogram": "kg",
    "kilograms": "kg",
    "lb": "lb",
    "lbs": "lb",
    "pound": "lb",
    "pounds": "lb",
    "oz": "oz",
    "ounce": "oz",
    "ounces": "oz",
}


def _normalize(unit: str) -> str:
    try:
        key = unit.strip().lower()
    except AttributeError as exc:
        raise ValueError(f"Unit must be a string, got {unit!r}") from exc

    canonical = _ALIASES.get(key)
    if canonical is None:
        raise ValueError(
            f"Unknown weight unit: {unit!r}. "
            f"Supported units: kg, lb, oz (and common aliases)."
        )
    return canonical


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit``.

    Supported units (case-insensitive, with common aliases):
      - kilograms: "kg", "kilogram", "kilograms"
      - pounds: "lb", "lbs", "pound", "pounds"
      - ounces: "oz", "ounce", "ounces"

    Raises:
        ValueError: if ``value`` is negative or either unit is unrecognized.
    """
    if value < 0:
        raise ValueError(f"Weight must be non-negative, got {value!r}")

    from_key = _normalize(from_unit)
    to_key = _normalize(to_unit)

    kilograms = value * _TO_KILOGRAMS[from_key]
    return kilograms / _TO_KILOGRAMS[to_key]
