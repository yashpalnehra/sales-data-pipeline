import argparse
import logging
import sys

from pipeline import run
from pipeline.config import load_config


def main(argv=None):
    parser = argparse.ArgumentParser(description="clean, join and summarise sales data")
    parser.add_argument("config", nargs="?", default="config.json")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show dropped rows"
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )
    try:
        config = load_config(args.config)
        summary = run(config)
    except (ValueError, OSError) as e:
        logging.error("%s", e)
        return 1

    print(
        f"{summary['orders']} orders, {summary['total_revenue']:,.2f} in total, "
        f"{summary['dropped_rows']} rows dropped"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
