import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

DEFAULT_SALES = Path(__file__).resolve().parent.parent / "data" / "sales.csv"


def load_sales(path):
    with Path(path).open(newline="") as f:
        return [
            {
                "date": date.fromisoformat(r["date"]),
                "sku": r["sku"],
                "region": r["region"],
                "quantity": int(r["quantity"]),
                "revenue": round(int(r["quantity"]) * float(r["unit_price"]), 2),
            }
            for r in csv.DictReader(f)
        ]


def filter_rows(rows, start=None, end=None, region=None):
    """Keep rows inside the date range (inclusive) and region, when given."""
    kept = []
    for row in rows:
        if start and row["date"] < start:
            continue
        if end and row["date"] > end:
            continue
        if region and row["region"] != region:
            continue
        kept.append(row)
    return kept


def summarise(rows):
    by_sku = defaultdict(float)
    for row in rows:
        by_sku[row["sku"]] += row["revenue"]
    return {
        "orders": len(rows),
        "total_revenue": round(sum(r["revenue"] for r in rows), 2),
        "by_sku": {
            k: round(v, 2) for k, v in sorted(by_sku.items(), key=lambda i: -i[1])
        },
    }


def as_text(summary):
    lines = [f"{summary['orders']} orders, {summary['total_revenue']:.2f} in total"]
    for sku, total in summary["by_sku"].items():
        lines.append(f"  {sku:<10} {total:>10.2f}")
    return "\n".join(lines) + "\n"


def as_csv(summary):
    lines = ["sku,revenue"]
    lines += [f"{sku},{total:.2f}" for sku, total in summary["by_sku"].items()]
    return "\n".join(lines) + "\n"


def as_json(summary):
    return json.dumps(summary, indent=2) + "\n"


FORMATS = {"text": as_text, "csv": as_csv, "json": as_json}


def build_parser():
    p = argparse.ArgumentParser(description="sales summary with optional filters")
    p.add_argument("--sales", default=DEFAULT_SALES, help="sales csv file")
    p.add_argument(
        "--from", dest="start", type=date.fromisoformat, help="first day, YYYY-MM-DD"
    )
    p.add_argument(
        "--to", dest="end", type=date.fromisoformat, help="last day, YYYY-MM-DD"
    )
    p.add_argument("--region", help="only this region")
    p.add_argument("--format", choices=FORMATS, default="text")
    p.add_argument("--out", help="write here instead of printing")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.start and args.end and args.start > args.end:
        print("error: --from is after --to", file=sys.stderr)
        return 2
    try:
        rows = load_sales(args.sales)
    except FileNotFoundError:
        print(f"error: no such file: {args.sales}", file=sys.stderr)
        return 1

    rows = filter_rows(rows, args.start, args.end, args.region)
    output = FORMATS[args.format](summarise(rows))
    if args.out:
        Path(args.out).write_text(output)
        print(f"wrote {args.out}")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
