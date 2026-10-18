from collections import defaultdict


def join_products(sales, products):
    """Add name and category to each sale. Unknown skus come back separately."""
    joined = []
    unknown = []
    for sale in sales:
        product = products.get(sale["sku"])
        if product is None:
            unknown.append(sale)
        else:
            joined.append(
                {**sale, "name": product["name"], "category": product["category"]}
            )
    return joined, unknown


def filter_region(sales, region):
    if not region:
        return sales
    return [s for s in sales if s["region"] == region]


def total_by(sales, field):
    totals = defaultdict(float)
    for sale in sales:
        totals[sale[field]] += sale["revenue"]
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return {key: round(total, 2) for key, total in ranked}


def summarise(sales):
    by_month = defaultdict(float)
    for sale in sales:
        by_month[sale["date"].strftime("%Y-%m")] += sale["revenue"]
    return {
        "orders": len(sales),
        "units": sum(s["quantity"] for s in sales),
        "total_revenue": round(sum(s["revenue"] for s in sales), 2),
        "by_category": total_by(sales, "category"),
        "by_sku": total_by(sales, "sku"),
        "by_region": total_by(sales, "region"),
        "by_month": {m: round(t, 2) for m, t in sorted(by_month.items())},
    }
