# Command line

The summary from the earlier folders, with options.

    python3 sales_report.py
    python3 sales_report.py --from 2024-02-01 --to 2024-02-29
    python3 sales_report.py --region north --format csv
    python3 sales_report.py --format json --out summary.json

`--format` is text, csv or json. Dates are inclusive and must be YYYY-MM-DD, argparse rejects anything else. A missing input file exits with 1, a range where `--from` is after `--to` exits with 2, and both print a one-line error.

Tests call `main()` with argument lists, so nothing is spawned: `python3 -m pytest`.
