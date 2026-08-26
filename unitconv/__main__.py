"""Allow running unitconv as `python -m unitconv`."""

from unitconv.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
