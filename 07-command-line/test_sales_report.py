import json
from datetime import date

import pytest

from sales_report import filter_rows, main, summarise

ROWS = [
    {
        "date": date(2024, 1, 3),
        "sku": "MUG",
        "region": "north",
        "quantity": 2,
        "revenue": 17.0,
    },
    {
        "date": date(2024, 2, 4),
        "sku": "TEE",
        "region": "south",
        "quantity": 1,
        "revenue": 19.0,
    },
    {
        "date": date(2024, 3, 8),
        "sku": "MUG",
        "region": "north",
        "quantity": 1,
        "revenue": 8.0,
    },
]


def test_filter_by_dates_is_inclusive():
    kept = filter_rows(ROWS, start=date(2024, 2, 4), end=date(2024, 3, 8))
    assert [r["sku"] for r in kept] == ["TEE", "MUG"]


def test_filter_by_region():
    assert [r["revenue"] for r in filter_rows(ROWS, region="north")] == [17.0, 8.0]
    assert filter_rows(ROWS, region="west") == []


def test_summarise():
    assert summarise(ROWS) == {
        "orders": 3,
        "total_revenue": 44.0,
        "by_sku": {"MUG": 25.0, "TEE": 19.0},
    }


def test_text_output(capsys):
    assert main(["--region", "north"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("8 orders, 203.50 in total")


def test_json_to_file(tmp_path):
    out = tmp_path / "jan.json"
    code = main(
        [
            "--from",
            "2024-01-01",
            "--to",
            "2024-01-31",
            "--format",
            "json",
            "--out",
            str(out),
        ]
    )
    assert code == 0
    data = json.loads(out.read_text())
    assert data["orders"] == 8
    assert data["total_revenue"] == 211.5


def test_csv_output(capsys):
    main(["--format", "csv", "--to", "2024-01-03"])
    assert capsys.readouterr().out == "sku,revenue\nTEE-BLK,19.00\nMUG-01,17.00\n"


def test_missing_file_is_exit_1(capsys):
    assert main(["--sales", "nope.csv"]) == 1
    assert "no such file" in capsys.readouterr().err


def test_reversed_range_is_exit_2(capsys):
    assert main(["--from", "2024-03-01", "--to", "2024-01-01"]) == 2
    assert "after" in capsys.readouterr().err


def test_bad_date_is_rejected_by_argparse():
    with pytest.raises(SystemExit):
        main(["--from", "yesterday"])
