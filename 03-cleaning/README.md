# Cleaning

Real exports are never tidy. `../data/sales_messy.csv` has stray spaces, two date formats, a blank line and a missing price. It also has a duplicated order, a quantity written as a word and an empty region.

`clean.py` turns each row into typed values (int, date, float) and drops what it can't fix. It reports every dropped row with its line number and the reason, rather than failing on the first bad one.

Run `python3 clean.py` to see the report. Tests: `python3 -m pytest`.
