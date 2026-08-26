"""Tests for unitconv.length."""

import pytest

from unitconv.length import convert


def test_meters_to_feet():
    assert convert(1, "m", "ft") == pytest.approx(3.28084, rel=1e-4)


def test_feet_to_meters():
    assert convert(1, "ft", "m") == pytest.approx(0.3048, rel=1e-6)


def test_meters_to_miles():
    assert convert(1609.344, "m", "mi") == pytest.approx(1.0, rel=1e-6)


def test_miles_to_meters():
    assert convert(1, "mi", "m") == pytest.approx(1609.344, rel=1e-6)


def test_feet_to_miles():
    assert convert(5280, "ft", "mi") == pytest.approx(1.0, rel=1e-6)


def test_miles_to_feet():
    assert convert(1, "mi", "ft") == pytest.approx(5280, rel=1e-4)


def test_case_insensitive_and_alias_units():
    assert convert(1, "Meters", "FEET") == pytest.approx(3.28084, rel=1e-4)
    assert convert(1, "mile", "meter") == pytest.approx(1609.344, rel=1e-6)


def test_zero_value():
    assert convert(0, "m", "ft") == pytest.approx(0.0)


def test_unknown_from_unit_raises():
    with pytest.raises(ValueError):
        convert(1, "banana", "m")


def test_unknown_to_unit_raises():
    with pytest.raises(ValueError):
        convert(1, "m", "banana")


def test_negative_value_raises():
    with pytest.raises(ValueError):
        convert(-1, "m", "ft")
