import csv
import json
from datetime import date

from report import money, summarise, write_csv, write_json, write_text

ROWS = [
    {
        "date": date(2024, 1, 3),
        "sku": "MUG",
        "region": "north",
        "quantity": 2,
        "revenue": 17.0,
    },
    {
        "date": date(2024, 1, 9),
        "sku": "TEE",
        "region": "south",
        "quantity": 1,
        "revenue": 19.0,
    },
    {
        "date": date(2024, 2, 4),
        "sku": "MUG",
        "region": "east",
        "quantity": 1,
        "revenue": 8.0,
    },
]


def test_summarise():
    assert summarise(ROWS) == {
        "orders": 3,
        "total_revenue": 44.0,
        "by_sku": {
            "MUG": {"units": 3, "revenue": 25.0},
            "TEE": {"units": 1, "revenue": 19.0},
        },
        "by_month": {"2024-01": 36.0, "2024-02": 8.0},
    }


def test_money():
    assert money(8.5) == "8.50"
    assert money(1234.5) == "1,234.50"
    assert money(0) == "0.00"


def test_write_json(tmp_path):
    path = tmp_path / "s.json"
    write_json(summarise(ROWS), path)
    assert json.loads(path.read_text())["total_revenue"] == 44.0


def test_write_csv(tmp_path):
    path = tmp_path / "s.csv"
    write_csv(summarise(ROWS), path)
    with path.open(newline="") as f:
        rows = list(csv.reader(f))
    assert rows == [
        ["sku", "units", "revenue"],
        ["MUG", "3", "25.00"],
        ["TEE", "1", "19.00"],
    ]


def test_write_text(tmp_path):
    path = tmp_path / "s.txt"
    write_text(summarise(ROWS), path)
    text = path.read_text()
    assert text.startswith("3 orders, 44.00 in total")
    assert "MUG           3 units       25.00" in text
    assert "2024-02        8.00" in text
