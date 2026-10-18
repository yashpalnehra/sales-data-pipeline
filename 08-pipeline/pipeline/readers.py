import csv
import json
from pathlib import Path

from pipeline.cleaning import clean_rows

REQUIRED_COLUMNS = {"order_id", "date", "sku", "quantity", "unit_price", "region"}


def read_sales(path):
    """Cleaned sales rows plus the list of dropped lines."""
    with Path(path).open(newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing columns: {', '.join(sorted(missing))}")
        return clean_rows((reader.line_num, row) for row in reader)


def read_products(path):
    products = json.loads(Path(path).read_text())
    if not isinstance(products, list):
        raise ValueError(f"{path} should contain a list of products")
    return {p["sku"]: p for p in products}
