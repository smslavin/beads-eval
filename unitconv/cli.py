"""Command-line entrypoint for unitconv."""

import argparse
import sys

from unitconv import __version__, length, temperature, weight

_CONVERTERS = {
    "temperature": temperature.convert,
    "length": length.convert,
    "weight": weight.convert,
}


def _add_convert_subparser(subparsers, name: str, help_text: str) -> None:
    sub = subparsers.add_parser(name, help=help_text)
    sub.add_argument("value", type=float, help="numeric value to convert")
    sub.add_argument("from_unit", help="unit to convert from")
    sub.add_argument("to_unit", help="unit to convert to")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="unitconv",
        description="Convert values between units.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")
    _add_convert_subparser(subparsers, "temperature", "Convert a temperature value")
    _add_convert_subparser(subparsers, "length", "Convert a length value")
    _add_convert_subparser(subparsers, "weight", "Convert a weight value")

    return parser


def main(argv=None) -> int:
    """Parse arguments and dispatch. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    convert = _CONVERTERS[args.command]
    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
