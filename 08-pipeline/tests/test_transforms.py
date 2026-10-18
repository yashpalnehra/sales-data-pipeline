from datetime import date

from pipeline.transforms import filter_region, join_products, summarise, total_by

PRODUCTS = {
    "MUG": {"sku": "MUG", "name": "Mug", "category": "kitchen"},
    "TEE": {"sku": "TEE", "name": "Tee", "category": "clothing"},
}


def sale(order_id, day, sku, quantity, price, region):
    return {
        "order_id": order_id,
        "date": date.fromisoformat(day),
        "sku": sku,
        "quantity": quantity,
        "unit_price": price,
        "revenue": round(quantity * price, 2),
        "region": region,
    }


SALES = [
    sale(1, "2024-01-03", "MUG", 2, 8.0, "north"),
    sale(2, "2024-01-09", "TEE", 1, 19.0, "south"),
    sale(3, "2024-02-04", "MUG", 1, 8.0, "north"),
    sale(4, "2024-02-05", "HAT", 1, 9.0, "north"),
]


def test_join_products():
    joined, unknown = join_products(SALES, PRODUCTS)
    assert [s["category"] for s in joined] == ["kitchen", "clothing", "kitchen"]
    assert [s["order_id"] for s in unknown] == [4]


def test_filter_region():
    assert len(filter_region(SALES, "north")) == 3
    assert filter_region(SALES, "") is SALES


def test_total_by_orders_biggest_first_then_name():
    joined, _ = join_products(SALES, PRODUCTS)
    assert total_by(joined, "sku") == {"MUG": 24.0, "TEE": 19.0}
    assert total_by(joined, "region") == {"north": 24.0, "south": 19.0}


def test_summarise():
    joined, _ = join_products(SALES, PRODUCTS)
    summary = summarise(joined)
    assert summary["orders"] == 3
    assert summary["units"] == 4
    assert summary["total_revenue"] == 43.0
    assert summary["by_category"] == {"kitchen": 24.0, "clothing": 19.0}
    assert summary["by_month"] == {"2024-01": 35.0, "2024-02": 8.0}
