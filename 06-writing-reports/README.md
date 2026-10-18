# Writing reports

Builds one summary and writes it three ways: JSON for other programs, CSV for a spreadsheet, and a text file you can read as-is. The writers only format, all the numbers come from `summarise`.

Run `python3 report.py`. It prints the text version and leaves the three files in `out/`, which git ignores. Tests write to a temporary folder: `python3 -m pytest`.
