import csv
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "data" / "sales.csv"


def load_sales(path=DEFAULT_FILE):
    """Rows of the clean sales file with proper types and a revenue field."""
    rows = []
    with Path(path).open(newline="") as f:
        for row in csv.DictReader(f):
            quantity = int(row["quantity"])
            price = float(row["unit_price"])
            rows.append(
                {
                    "order_id": int(row["order_id"]),
                    "date": date.fromisoformat(row["date"]),
                    "sku": row["sku"],
                    "region": row["region"],
                    "quantity": quantity,
                    "revenue": round(quantity * price, 2),
                }
            )
    return rows


def revenue_by(rows, field):
    """Total revenue per value of a field, biggest first."""
    totals = defaultdict(float)
    for row in rows:
        totals[row[field]] += row["revenue"]
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return [(key, round(total, 2)) for key, total in ranked]


def revenue_by_month(rows):
    totals = defaultdict(float)
    for row in rows:
        totals[row["date"].strftime("%Y-%m")] += row["revenue"]
    return {month: round(total, 2) for month, total in sorted(totals.items())}


def units_by_sku(rows):
    counts = Counter()
    for row in rows:
        counts[row["sku"]] += row["quantity"]
    return dict(counts.most_common())


def average_order_value(rows):
    if not rows:
        return 0.0
    return round(sum(r["revenue"] for r in rows) / len(rows), 2)


def busiest_day(rows):
    """The date with the most orders. Ties go to the earlier date."""
    if not rows:
        return None
    counts = Counter(r["date"] for r in rows)
    return min(counts, key=lambda d: (-counts[d], d))


def main():
    rows = load_sales()
    print(f"{len(rows)} orders, average {average_order_value(rows):.2f} per order")
    print(f"busiest day: {busiest_day(rows)}\n")
    print("revenue by month")
    for month, total in revenue_by_month(rows).items():
        print(f"  {month}  {total:>8.2f}")
    print("\nrevenue by product")
    for sku, total in revenue_by(rows, "sku"):
        print(f"  {sku:<10} {total:>8.2f}")
    print("\nrevenue by region")
    for region, total in revenue_by(rows, "region"):
        print(f"  {region:<10} {total:>8.2f}")


if __name__ == "__main__":
    main()
