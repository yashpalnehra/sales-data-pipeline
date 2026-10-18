# Pipeline

Everything from the earlier folders in one run: read the messy CSV, clean it, join the product file, summarise, write the reports. Settings come from a JSON file instead of flags, so the same run can be repeated.

    pipeline/config.py       reads and checks config.json
    pipeline/readers.py      CSV and JSON input, checks the columns
    pipeline/cleaning.py     typed rows, dropped rows with reasons
    pipeline/transforms.py   join, region filter, totals
    pipeline/writers.py      summary.json, four CSV files, summary.txt
    pipeline/__init__.py     run(config), the steps in order
    run_pipeline.py          command-line entry point

## How to run

    python3 run_pipeline.py                 uses config.json in this folder
    python3 run_pipeline.py -v              also lists every dropped row
    python3 run_pipeline.py other.json      a different config

You should see a few log lines, a warning about dropped rows, then `7 orders, 207.00 in total, 5 rows dropped`. Output lands in `out/`, which git ignores.

The config has five keys. `sales`, `products` and `out_dir` are paths, relative to the config file. `formats` is any of json, csv and text. `region` limits the summary to one region and can be left empty.

A missing file, a bad config or an unknown format logs one error line and exits with 1.

## Tests

    python3 -m pytest

The end-to-end test runs the whole thing on the sample data into a temporary folder and checks the files it leaves behind.
