# Summaries

Loads the clean sales file and answers the usual questions. Revenue by product, by region and by month, units sold per product, average order value and the busiest day. Each answer is a small function over a list of row dicts. That keeps the tests simple: feed in a handful of rows and check exact numbers.

Run `python3 summarize.py` for the report. Tests: `python3 -m pytest`.
