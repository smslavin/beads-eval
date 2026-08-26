"""Unit tests for unitconv.weight."""

import pytest

from unitconv.weight import convert


def test_kg_to_lb():
    assert convert(1, "kg", "lb") == pytest.approx(2.20462262, rel=1e-6)


def test_lb_to_kg():
    assert convert(1, "lb", "kg") == pytest.approx(0.45359237, rel=1e-6)


def test_kg_to_oz():
    assert convert(1, "kg", "oz") == pytest.approx(35.27396195, rel=1e-6)


def test_oz_to_kg():
    assert convert(1, "oz", "kg") == pytest.approx(0.028349523125, rel=1e-6)


def test_lb_to_oz():
    assert convert(1, "lb", "oz") == pytest.approx(16.0, rel=1e-6)


def test_oz_to_lb():
    assert convert(16, "oz", "lb") == pytest.approx(1.0, rel=1e-6)


def test_same_unit_is_identity():
    assert convert(42.5, "kg", "kg") == pytest.approx(42.5)


def test_zero_is_allowed():
    assert convert(0, "kg", "lb") == pytest.approx(0.0)


@pytest.mark.parametrize(
    "unit",
    ["kg", "Kg", "KG", "kilogram", "Kilogram", "kilograms", "KILOGRAMS"],
)
def test_kilogram_aliases_case_insensitive(unit):
    assert convert(1, unit, "kg") == pytest.approx(1.0)


@pytest.mark.parametrize("unit", ["lb", "lbs", "Pound", "pounds", "POUNDS"])
def test_pound_aliases_case_insensitive(unit):
    assert convert(1, unit, "lb") == pytest.approx(1.0)


@pytest.mark.parametrize("unit", ["oz", "Ounce", "ounces", "OUNCES"])
def test_ounce_aliases_case_insensitive(unit):
    assert convert(1, unit, "oz") == pytest.approx(1.0)


def test_unknown_from_unit_raises_value_error():
    with pytest.raises(ValueError):
        convert(1, "stone", "kg")


def test_unknown_to_unit_raises_value_error():
    with pytest.raises(ValueError):
        convert(1, "kg", "stone")


def test_negative_weight_raises_value_error():
    with pytest.raises(ValueError):
        convert(-1, "kg", "lb")
