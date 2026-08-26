"""Unit tests for unitconv.temperature."""

import pytest

from unitconv.temperature import convert


def test_celsius_to_fahrenheit():
    assert convert(0, "C", "F") == pytest.approx(32.0)
    assert convert(100, "celsius", "fahrenheit") == pytest.approx(212.0)


def test_fahrenheit_to_celsius():
    assert convert(32, "F", "C") == pytest.approx(0.0)
    assert convert(212, "fahrenheit", "celsius") == pytest.approx(100.0)


def test_celsius_to_kelvin():
    assert convert(0, "C", "K") == pytest.approx(273.15)
    assert convert(-273.15, "celsius", "kelvin") == pytest.approx(0.0)


def test_kelvin_to_celsius():
    assert convert(273.15, "K", "C") == pytest.approx(0.0)
    assert convert(0, "kelvin", "celsius") == pytest.approx(-273.15)


def test_fahrenheit_to_kelvin():
    assert convert(32, "F", "K") == pytest.approx(273.15)
    assert convert(98.6, "fahrenheit", "kelvin") == pytest.approx(310.15, abs=1e-2)


def test_kelvin_to_fahrenheit():
    assert convert(273.15, "K", "F") == pytest.approx(32.0)
    assert convert(0, "kelvin", "fahrenheit") == pytest.approx(-459.67, abs=1e-2)


def test_unit_strings_are_case_insensitive():
    assert convert(0, "c", "f") == pytest.approx(32.0)
    assert convert(0, "CELSIUS", "KELVIN") == pytest.approx(273.15)


def test_same_unit_is_identity():
    assert convert(42, "C", "C") == pytest.approx(42.0)
    assert convert(42, "fahrenheit", "F") == pytest.approx(42.0)


def test_unknown_unit_raises_value_error():
    with pytest.raises(ValueError):
        convert(0, "X", "C")
    with pytest.raises(ValueError):
        convert(0, "C", "rankine")


def test_below_absolute_zero_raises_value_error():
    with pytest.raises(ValueError):
        convert(-1, "K", "C")
    with pytest.raises(ValueError):
        convert(-300, "C", "F")
