# unitconv

A toy command-line unit converter. It supports temperature, length, and
weight conversions between a small set of common units.

## Install

```bash
pip install -e .
```

This installs the `unitconv` console script (and makes `python -m unitconv`
available too).

## Usage

Each subcommand takes the same three arguments: `<value> <from_unit> <to_unit>`.

```bash
unitconv <command> <value> <from_unit> <to_unit>
```

(All examples below also work as `python -m unitconv <command> <value> <from_unit> <to_unit>`.)

### `temperature`

```console
$ python -m unitconv temperature 100 C F
212.0

$ python -m unitconv temperature 0 celsius fahrenheit
32.0

$ python -m unitconv temperature 300 K C
26.850000000000023
```

Supported units (case-insensitive):

| Unit        | Accepted names           |
|-------------|---------------------------|
| Celsius     | `C`, `celsius`             |
| Fahrenheit  | `F`, `fahrenheit`          |
| Kelvin      | `K`, `kelvin`               |

Values below absolute zero (for the given `from_unit`) are rejected with an error.

### `length`

```console
$ python -m unitconv length 1 mi ft
5280.0

$ python -m unitconv length 10 m ft
32.808398950131235

$ python -m unitconv length 1 mile meters
1609.344
```

Supported units (case-insensitive):

| Unit   | Accepted names                          |
|--------|------------------------------------------|
| Meters | `m`, `meter`, `meters`, `metre`, `metres` |
| Feet   | `ft`, `foot`, `feet`                      |
| Miles  | `mi`, `mile`, `miles`                     |

Negative values are rejected with an error.

### `weight`

```console
$ python -m unitconv weight 1 kg lb
2.2046226218487757

$ python -m unitconv weight 16 oz lb
1.0

$ python -m unitconv weight 5 pounds kilograms
2.2679618500000003
```

Supported units (case-insensitive):

| Unit      | Accepted names                          |
|-----------|-------------------------------------------|
| Kilograms | `kg`, `kilogram`, `kilograms`              |
| Pounds    | `lb`, `lbs`, `pound`, `pounds`             |
| Ounces    | `oz`, `ounce`, `ounces`                    |

Negative values are rejected with an error.

## Errors

An unrecognized unit or an invalid value (negative length/weight, or a
temperature below absolute zero) prints an `Error: ...` message to stderr
and exits with status `1`. For example:

```console
$ python -m unitconv length 5 mi km
Error: Unknown length unit: 'km'
```
