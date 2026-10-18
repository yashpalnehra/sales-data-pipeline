# Joining

Sales only carry a sku. The product file knows the name, category and list price. `join.py` puts the two together, which makes revenue by category, below-list-price sales and never-sold products easy to answer.

A sale with a sku that isn't in the product file is handed back in a separate list. That way it can be reported instead of silently vanishing.

Run `python3 join.py`. Tests: `python3 -m pytest`.
