from datetime import datetime

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
    row = {k: (v or "").strip() for k, v in row.items()}
    if not row.get("order_id", "").isdigit():
        raise BadRow(f"bad order id {row.get('order_id')!r}")
    if not row.get("quantity", "").isdigit() or int(row["quantity"]) < 1:
        raise BadRow(f"bad quantity {row.get('quantity')!r}")
    try:
        price = float(row.get("unit_price", ""))
    except ValueError:
        raise BadRow(f"bad price {row.get('unit_price')!r}") from None
    if not row.get("sku") or not row.get("region"):
        raise BadRow("missing sku or region")
    quantity = int(row["quantity"])
    return {
        "order_id": int(row["order_id"]),
        "date": parse_date(row.get("date", "")),
        "sku": row["sku"].upper(),
        "quantity": quantity,
        "unit_price": round(price, 2),
        "revenue": round(quantity * price, 2),
        "region": row["region"].lower(),
    }


def clean_rows(numbered_rows):
    """(good_rows, problems). problems is a list of (line, reason)."""
    good = []
    problems = []
    seen = set()
    for line, row in numbered_rows:
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
