import logging

from pipeline.readers import read_products, read_sales
from pipeline.transforms import filter_region, join_products, summarise
from pipeline.writers import write_all

log = logging.getLogger("pipeline")


def run(config):
    """Read, clean, join, summarise, write. Returns the summary."""
    sales, problems = read_sales(config.sales)
    log.info("read %d sales rows from %s", len(sales), config.sales)
    if problems:
        log.warning("dropped %d rows, run with -v to see which", len(problems))
    for line, reason in problems:
        log.debug("dropped line %d: %s", line, reason)

    products = read_products(config.products)
    joined, unknown = join_products(sales, products)
    for sale in unknown:
        log.warning("order %d has unknown sku %s", sale["order_id"], sale["sku"])

    if config.region:
        joined = filter_region(joined, config.region)
        log.info("kept %d rows for region %s", len(joined), config.region)

    summary = summarise(joined)
    summary["dropped_rows"] = len(problems)
    summary["unknown_skus"] = sorted({s["sku"] for s in unknown})

    for path in write_all(summary, config.out_dir, config.formats):
        log.info("wrote %s", path)
    return summary
