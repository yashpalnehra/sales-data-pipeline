from datetime import date

from summarize import (
    average_order_value,
    busiest_day,
    load_sales,
    revenue_by,
    revenue_by_month,
    units_by_sku,
)


def row(order_id, day, sku, quantity, price, region="north"):
    return {
        "order_id": order_id,
        "date": date.fromisoformat(day),
        "sku": sku,
        "region": region,
        "quantity": quantity,
        "revenue": round(quantity * price, 2),
    }


ROWS = [
    row(1, "2024-01-03", "MUG", 2, 8.5),
    row(2, "2024-01-03", "TEE", 1, 19.0, "south"),
    row(3, "2024-02-10", "MUG", 1, 8.5, "south"),
    row(4, "2024-02-11", "CAP", 3, 14.0),
]


def test_revenue_by_sku_is_sorted_biggest_first():
    assert revenue_by(ROWS, "sku") == [("CAP", 42.0), ("MUG", 25.5), ("TEE", 19.0)]


def test_revenue_by_region_ties_alphabetical():
    rows = [
        row(1, "2024-01-01", "A", 1, 5.0, "west"),
        row(2, "2024-01-01", "A", 1, 5.0, "east"),
    ]
    assert revenue_by(rows, "region") == [("east", 5.0), ("west", 5.0)]


def test_revenue_by_month():
    assert revenue_by_month(ROWS) == {"2024-01": 36.0, "2024-02": 50.5}


def test_units_by_sku():
    assert units_by_sku(ROWS) == {"MUG": 3, "CAP": 3, "TEE": 1}


def test_average_order_value():
    # 86.5 / 4 is 21.625 and python rounds half to even
    assert average_order_value(ROWS) == 21.62
    assert average_order_value([]) == 0.0


def test_busiest_day():
    assert busiest_day(ROWS) == date(2024, 1, 3)
    assert busiest_day([]) is None


def test_sample_file_totals():
    rows = load_sales()
    assert len(rows) == 24
    assert sum(r["revenue"] for r in rows) == 695.5
    assert list(revenue_by_month(rows)) == ["2024-01", "2024-02", "2024-03"]
