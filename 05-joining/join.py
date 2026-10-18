import csv
import json
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load_products(path=DATA / "products.json"):
    """Products keyed by sku."""
    return {p["sku"]: p for p in json.loads(Path(path).read_text())}


def load_sales(path=DATA / "sales.csv"):
    with Path(path).open(newline="") as f:
        return [
            {
                "order_id": int(r["order_id"]),
                "sku": r["sku"],
                "quantity": int(r["quantity"]),
                "unit_price": float(r["unit_price"]),
            }
            for r in csv.DictReader(f)
        ]


def join_sales(sales, products):
    """Attach product name and category to each sale. Unknown skus come back separately."""
    joined = []
    unknown = []
    for sale in sales:
        product = products.get(sale["sku"])
        if product is None:
            unknown.append(sale)
            continue
        joined.append(
            {
                **sale,
                "name": product["name"],
                "category": product["category"],
                "revenue": round(sale["quantity"] * sale["unit_price"], 2),
            }
        )
    return joined, unknown


def revenue_by_category(joined):
    totals = defaultdict(float)
    for sale in joined:
        totals[sale["category"]] += sale["revenue"]
    return {c: round(t, 2) for c, t in sorted(totals.items(), key=lambda i: -i[1])}


def discounted_sales(joined, products):
    """Sales where the price charged was below the list price."""
    return [s for s in joined if s["unit_price"] < products[s["sku"]]["unit_price"]]


def unsold_products(joined, products):
    sold = {s["sku"] for s in joined}
    return sorted(sku for sku in products if sku not in sold)


def main():
    products = load_products()
    joined, unknown = join_sales(load_sales(), products)
    print("revenue by category")
    for category, total in revenue_by_category(joined).items():
        print(f"  {category:<12} {total:>8.2f}")
    print(f"\n{len(discounted_sales(joined, products))} sales below list price")
    print(f"never sold: {', '.join(unsold_products(joined, products)) or 'nothing'}")
    if unknown:
        print(f"{len(unknown)} sales with an unknown sku")


if __name__ == "__main__":
    main()
