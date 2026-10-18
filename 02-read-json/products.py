import json
from pathlib import Path

PRODUCTS_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"

products = json.loads(PRODUCTS_FILE.read_text())

print(f"{len(products)} products\n")
for p in sorted(products, key=lambda p: p["unit_price"]):
    print(f"{p['sku']:<10} {p['name']:<16} {p['category']:<12} {p['unit_price']:>6.2f}")

by_category = {}
for p in products:
    by_category.setdefault(p["category"], []).append(p["name"])

print("\nby category")
for category, names in sorted(by_category.items()):
    print(f"  {category}: {', '.join(names)}")
