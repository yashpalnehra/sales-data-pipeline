from datetime import date

import pytest

from pipeline.cleaning import BadRow, clean_row, clean_rows

GOOD = {
    "order_id": "1",
    "date": "03/01/2024",
    "sku": "mug-01",
    "quantity": "2",
    "unit_price": "8.5",
    "region": " North",
}


def test_clean_row():
    assert clean_row(GOOD) == {
        "order_id": 1,
        "date": date(2024, 1, 3),
        "sku": "MUG-01",
        "quantity": 2,
        "unit_price": 8.5,
        "revenue": 17.0,
        "region": "north",
    }


@pytest.mark.parametrize(
    "field, value",
    [
        ("order_id", ""),
        ("date", "soon"),
        ("quantity", "0"),
        ("unit_price", "free"),
        ("sku", ""),
    ],
)
def test_bad_values(field, value):
    with pytest.raises(BadRow):
        clean_row({**GOOD, field: value})


def test_duplicates_and_blank_rows():
    rows = [(2, GOOD), (3, {k: "" for k in GOOD}), (4, GOOD)]
    good, problems = clean_rows(rows)
    assert len(good) == 1
    assert problems == [(4, "duplicate order 1")]
