import csv
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "data" / "sales_messy.csv"
DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y")


class BadRow(ValueError):
    pass


def parse_date(text):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            pass
    raise BadRow(f"bad date {text!r}")


def clean_row(row):
    """Turn one raw CSV row into typed values. Raises BadRow if it cannot."""
    row = {k: (v or "").strip() for k, v in row.items()}
    if not row["order_id"].isdigit():
        raise BadRow(f"bad order id {row['order_id']!r}")
    if not row["quantity"].isdigit() or int(row["quantity"]) < 1:
        raise BadRow(f"bad quantity {row['quantity']!r}")
    try:
        price = float(row["unit_price"])
    except ValueError:
        raise BadRow(f"bad price {row['unit_price']!r}") from None
    if not row["sku"] or not row["region"]:
        raise BadRow("missing sku or region")
    return {
        "order_id": int(row["order_id"]),
        "date": parse_date(row["date"]),
        "sku": row["sku"].upper(),
        "quantity": int(row["quantity"]),
        "unit_price": round(price, 2),
        "region": row["region"].lower(),
    }


def clean_rows(numbered_rows):
    """Clean (line, row) pairs. Returns (good_rows, problems) with problems as (line, reason)."""
    good = []
    problems = []
    seen = set()
    for line, row in numbered_rows:
        # a line of only commas gives a row of empty strings
        if not any(row.values()):
            continue
        try:
            cleaned = clean_row(row)
        except BadRow as e:
            problems.append((line, str(e)))
            continue
        if cleaned["order_id"] in seen:
            problems.append((line, f"duplicate order {cleaned['order_id']}"))
            continue
        seen.add(cleaned["order_id"])
        good.append(cleaned)
    return good, problems


def numbered(reader):
    """Pair each row with its real line number. The reader skips blank lines."""
    for row in reader:
        yield reader.line_num, row


def read_clean(path):
    with Path(path).open(newline="") as f:
        return clean_rows(numbered(csv.DictReader(f)))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE
    good, problems = read_clean(path)
    print(f"{len(good)} good rows, {len(problems)} dropped")
    for line, reason in problems:
        print(f"  line {line}: {reason}")


if __name__ == "__main__":
    main()
