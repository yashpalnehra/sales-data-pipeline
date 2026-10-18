import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load_sales(path=DATA / "sales.csv"):
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


def summarise(rows):
    """One summary dict with the numbers every report needs."""
    by_sku = defaultdict(lambda: {"units": 0, "revenue": 0.0})
    by_month = defaultdict(float)
    for row in rows:
        by_sku[row["sku"]]["units"] += row["quantity"]
        by_sku[row["sku"]]["revenue"] += row["revenue"]
        by_month[row["date"].strftime("%Y-%m")] += row["revenue"]
    return {
        "orders": len(rows),
        "total_revenue": round(sum(r["revenue"] for r in rows), 2),
        "by_sku": {
            sku: {"units": v["units"], "revenue": round(v["revenue"], 2)}
            for sku, v in sorted(by_sku.items(), key=lambda i: -i[1]["revenue"])
        },
        "by_month": {m: round(t, 2) for m, t in sorted(by_month.items())},
    }


def money(amount):
    """8.5 becomes '8.50', 1234.5 becomes '1,234.50'."""
    return f"{amount:,.2f}"


def write_json(summary, path):
    Path(path).write_text(json.dumps(summary, indent=2) + "\n")


def write_csv(summary, path):
    """One row per sku. Easy to open in a spreadsheet."""
    with Path(path).open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sku", "units", "revenue"])
        for sku, v in summary["by_sku"].items():
            writer.writerow([sku, v["units"], f"{v['revenue']:.2f}"])


def write_text(summary, path):
    lines = [
        f"{summary['orders']} orders, {money(summary['total_revenue'])} in total",
        "",
        "by product",
    ]
    for sku, v in summary["by_sku"].items():
        lines.append(f"  {sku:<10} {v['units']:>4} units  {money(v['revenue']):>10}")
    lines += ["", "by month"]
    for month, total in summary["by_month"].items():
        lines.append(f"  {month}  {money(total):>10}")
    Path(path).write_text("\n".join(lines) + "\n")


def main():
    out = Path(__file__).resolve().parent / "out"
    out.mkdir(exist_ok=True)
    summary = summarise(load_sales())
    write_json(summary, out / "summary.json")
    write_csv(summary, out / "by_sku.csv")
    write_text(summary, out / "summary.txt")
    print((out / "summary.txt").read_text())
    print(f"written to {out}")


if __name__ == "__main__":
    main()
