# Sales data pipeline

Working with a small shop's sales data in plain Python. It starts with reading CSV and JSON and cleaning a messy export, then summarising, joining two files and writing reports. The last folder is a configurable pipeline that does all of it in one run. Standard library only, plus pytest.

The sample data lives in `data/`. `sales.csv` is clean, `sales_messy.csv` has the kind of problems a real export has, and `products.json` describes the six products.

1. `01-read-csv`, count orders and total them up.
2. `02-read-json`, list products and group them by category.
3. `03-cleaning`, typed rows, bad rows dropped with a reason and a line number.
4. `04-summaries`, revenue by product, region and month, busiest day.
5. `05-joining`, attach product details to each sale, revenue by category.
6. `06-writing-reports`, the same summary as JSON, CSV and text.
7. `07-command-line`, filters and output format as flags.
8. `08-pipeline`, a package driven by a config file, with logging and an end-to-end test.

Each folder runs on its own. Tests, where a folder has them, run with `python3 -m pytest` from inside the folder.
