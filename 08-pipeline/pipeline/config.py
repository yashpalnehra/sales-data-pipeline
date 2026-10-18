import json
from dataclasses import dataclass, field
from pathlib import Path

FORMATS = ("json", "csv", "text")


@dataclass
class Config:
    sales: Path
    products: Path
    out_dir: Path
    formats: list = field(default_factory=lambda: ["json", "text"])
    region: str = ""


def load_config(path):
    """Read config.json and check it before anything runs."""
    path = Path(path)
    try:
        raw = json.loads(path.read_text())
    except FileNotFoundError:
        raise ValueError(f"config file not found: {path}") from None
    except json.JSONDecodeError as e:
        raise ValueError(f"{path} is not valid JSON: {e}") from None

    for key in ("sales", "products", "out_dir"):
        if key not in raw:
            raise ValueError(f"config is missing '{key}'")
    formats = raw.get("formats", ["json", "text"])
    bad = [f for f in formats if f not in FORMATS]
    if bad:
        raise ValueError(f"unknown formats {bad}, choose from {list(FORMATS)}")

    # relative paths are taken from where the config file lives
    base = path.parent
    return Config(
        sales=base / raw["sales"],
        products=base / raw["products"],
        out_dir=base / raw["out_dir"],
        formats=formats,
        region=raw.get("region", ""),
    )
