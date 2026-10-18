import csv
import json
from pathlib import Path


def write_json(summary, out_dir):
    path = Path(out_dir) / "summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n")
    return path


def write_csv(summary, out_dir):
    """One file per breakdown, two columns each."""
    paths = []
    for name in ("by_category", "by_sku", "by_region", "by_month"):
        path = Path(out_dir) / f"{name}.csv"
        with path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name[3:], "revenue"])
            for key, total in summary[name].items():
                writer.writerow([key, f"{total:.2f}"])
        paths.append(path)
    return paths


def write_text(summary, out_dir):
    lines = [
        f"{summary['orders']} orders, {summary['units']} units, "
        f"{summary['total_revenue']:,.2f} in total",
    ]
    for name in ("by_category", "by_region", "by_month"):
        lines += ["", name[3:].replace("_", " ")]
        for key, total in summary[name].items():
            lines.append(f"  {key:<12} {total:>10,.2f}")
    path = Path(out_dir) / "summary.txt"
    path.write_text("\n".join(lines) + "\n")
    return path


WRITERS = {"json": write_json, "csv": write_csv, "text": write_text}


def write_all(summary, out_dir, formats):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    written = []
    for fmt in formats:
        result = WRITERS[fmt](summary, out_dir)
        written += result if isinstance(result, list) else [result]
    return written
