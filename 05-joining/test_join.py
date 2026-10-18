from join import (
    discounted_sales,
    join_sales,
    load_products,
    load_sales,
    revenue_by_category,
    unsold_products,
)

PRODUCTS = {
    "MUG": {"sku": "MUG", "name": "Mug", "category": "kitchen", "unit_price": 8.0},
    "TEE": {"sku": "TEE", "name": "Tee", "category": "clothing", "unit_price": 19.0},
    "PEN": {"sku": "PEN", "name": "Pen", "category": "stationery", "unit_price": 2.0},
}
SALES = [
    {"order_id": 1, "sku": "MUG", "quantity": 2, "unit_price": 8.0},
    {"order_id": 2, "sku": "TEE", "quantity": 1, "unit_price": 15.0},
    {"order_id": 3, "sku": "HAT", "quantity": 1, "unit_price": 9.0},
]


def test_join_adds_product_fields_and_separates_unknown():
    joined, unknown = join_sales(SALES, PRODUCTS)
    assert [s["order_id"] for s in joined] == [1, 2]
    assert joined[0]["category"] == "kitchen"
    assert joined[0]["revenue"] == 16.0
    assert [s["sku"] for s in unknown] == ["HAT"]


def test_revenue_by_category_biggest_first():
    joined, _ = join_sales(SALES, PRODUCTS)
    assert revenue_by_category(joined) == {"kitchen": 16.0, "clothing": 15.0}


def test_discounted_and_unsold():
    joined, _ = join_sales(SALES, PRODUCTS)
    assert [s["order_id"] for s in discounted_sales(joined, PRODUCTS)] == [2]
    assert unsold_products(joined, PRODUCTS) == ["PEN"]


def test_sample_data():
    products = load_products()
    joined, unknown = join_sales(load_sales(), products)
    assert unknown == []
    assert set(revenue_by_category(joined)) == {"clothing", "kitchen", "bags"}
    assert unsold_products(joined, products) == ["PEN-SET"]
    # the mug got cheaper in February, so nothing sold below the current list price
    assert discounted_sales(joined, products) == []
