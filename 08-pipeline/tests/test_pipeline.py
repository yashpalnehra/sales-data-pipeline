import json
from pathlib import Path

import pytest

import run_pipeline
from pipeline import run
from pipeline.config import load_config

HERE = Path(__file__).resolve().parent
DATA = HERE.parent.parent / "data"


def write_config(tmp_path, **overrides):
    raw = {
        "sales": str(DATA / "sales_messy.csv"),
        "products": str(DATA / "products.json"),
        "out_dir": "out",
        "formats": ["json", "csv", "text"],
    }
    raw.update(overrides)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(raw))
    return path


def test_load_config_resolves_relative_paths(tmp_path):
    cfg = load_config(write_config(tmp_path))
    assert cfg.out_dir == tmp_path / "out"
    assert cfg.formats == ["json", "csv", "text"]
    assert cfg.region == ""


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"formats": ["xml"]}, "unknown formats"),
        ({"out_dir": None}, "missing 'out_dir'"),
    ],
)
def test_load_config_rejects(tmp_path, overrides, message):
    raw = json.loads(write_config(tmp_path).read_text())
    for key, value in overrides.items():
        if value is None:
            del raw[key]
        else:
            raw[key] = value
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match=message):
        load_config(path)


def test_end_to_end(tmp_path):
    summary = run(load_config(write_config(tmp_path)))
    assert summary["orders"] == 7
    assert summary["dropped_rows"] == 5
    assert summary["unknown_skus"] == []
    assert summary["total_revenue"] == 207.0
    assert summary["by_category"] == {"clothing": 156.0, "kitchen": 51.0}

    out = tmp_path / "out"
    assert sorted(p.name for p in out.iterdir()) == [
        "by_category.csv",
        "by_month.csv",
        "by_region.csv",
        "by_sku.csv",
        "summary.json",
        "summary.txt",
    ]
    assert json.loads((out / "summary.json").read_text()) == summary
    assert (
        (out / "summary.txt")
        .read_text()
        .startswith("7 orders, 15 units, 207.00 in total")
    )


def test_region_filter(tmp_path):
    summary = run(load_config(write_config(tmp_path, region="north")))
    assert summary["by_region"] == {"north": 31.0}


def test_main_reports_and_exits_zero(tmp_path, capsys):
    assert run_pipeline.main([str(write_config(tmp_path))]) == 0
    assert "7 orders" in capsys.readouterr().out


def test_main_with_bad_config_exits_one(tmp_path):
    assert run_pipeline.main([str(tmp_path / "missing.json")]) == 1
