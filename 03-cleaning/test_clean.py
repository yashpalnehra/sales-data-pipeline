from datetime import date

import pytest

from clean import DEFAULT_FILE, BadRow, clean_row, clean_rows, parse_date, read_clean

GOOD = {
    "order_id": "7",
    "date": "2024-03-01",
    "sku": " mug-01 ",
    "quantity": "2",
    "unit_price": "8.5",
    "region": "North",
}


def test_parse_date_two_formats():
    assert parse_date("2024-01-05") == date(2024, 1, 5)
    assert parse_date("05/01/2024") == date(2024, 1, 5)
    with pytest.raises(BadRow):
        parse_date("Jan 5")


def test_clean_row_normalises():
    assert clean_row(GOOD) == {
        "order_id": 7,
        "date": date(2024, 3, 1),
        "sku": "MUG-01",
        "quantity": 2,
        "unit_price": 8.5,
        "region": "north",
    }


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("quantity", "one", "bad quantity"),
        ("quantity", "0", "bad quantity"),
        ("unit_price", "", "bad price"),
        ("region", "", "missing sku or region"),
        ("order_id", "x1", "bad order id"),
    ],
)
def test_clean_row_rejects(field, value, message):
    with pytest.raises(BadRow, match=message):
        clean_row({**GOOD, field: value})


def test_clean_rows_skips_blank_and_duplicates():
    rows = [GOOD, {k: "" for k in GOOD}, GOOD, {**GOOD, "order_id": "8"}]
    good, problems = clean_rows(enumerate(rows, start=2))
    assert [r["order_id"] for r in good] == [7, 8]
    assert problems == [(4, "duplicate order 7")]


def test_sample_file_reports_real_line_numbers():
    good, problems = read_clean(DEFAULT_FILE)
    assert len(good) == 7
    # line 6 of the file is blank, the numbers after it must still match the file
    assert problems == [
        (8, "bad price ''"),
        (9, "duplicate order 1004"),
        (10, "bad quantity 'one'"),
        (13, "bad quantity '0'"),
        (14, "missing sku or region"),
    ]
