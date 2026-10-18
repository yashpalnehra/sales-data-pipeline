import csv
import sys
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "data" / "sales.csv"

path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE

rows = 0
total = 0.0
with path.open(newline="") as f:
    for row in csv.DictReader(f):
        rows += 1
        total += int(row["quantity"]) * float(row["unit_price"])

print(f"{rows} orders")
print(f"total sales: {total:.2f}")
