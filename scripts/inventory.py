#!/usr/bin/env python3
"""Inventory management — stock levels, updates, low-stock alerts."""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def cmd_check(args):
    client = get_client(args.site)
    try:
        item = client.get(f"stockItems/{args.sku}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    fields = [
        ("SKU", args.sku),
        ("Qty", item.get("qty")),
        ("In Stock", "Yes" if item.get("is_in_stock") else "No"),
        ("Manage Stock", "Yes" if item.get("manage_stock") else "No"),
        ("Min Qty", item.get("min_qty")),
        ("Backorders", {0: "No", 1: "Allow (no notify)", 2: "Allow (notify)"}.get(item.get("backorders"), "Unknown")),
    ]
    print(tabulate(fields, tablefmt="simple"))


def cmd_update(args):
    client = get_client(args.site)
    try:
        current = client.get(f"stockItems/{args.sku}")
        item_id = current.get("item_id")
        current["qty"] = float(args.qty)
        current["is_in_stock"] = float(args.qty) > 0
        client.put(f"products/{args.sku}/stockItems/{item_id}", {"stockItem": current})
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Stock for {args.sku} updated to {args.qty}.")


def cmd_low_stock(args):
    client = get_client(args.site)
    threshold = args.threshold

    # Fetch all enabled, in-catalog products and check their stock
    try:
        result = client.search(
            "stockItems",
            filters=[{"field": "qty", "value": str(threshold), "condition_type": "lteq"},
                     {"field": "manage_stock", "value": "1", "condition_type": "eq"}],
            page_size=100,
        )
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print(f"No products below stock threshold of {threshold}.")
        return

    rows = [
        [i.get("sku"), i.get("qty"), "Yes" if i.get("is_in_stock") else "No"]
        for i in items
    ]
    rows.sort(key=lambda r: r[1])
    print(tabulate(rows, headers=["SKU", "Qty", "In Stock"], tablefmt="github"))
    print(f"\n{len(rows)} product(s) at or below {threshold} units.")


def cmd_bulk_check(args):
    client = get_client(args.site)
    skus = [s.strip() for s in args.skus.split(",") if s.strip()]
    if not skus:
        print("No SKUs provided.")
        return

    try:
        # Use 'in' condition for bulk check
        result = client.search(
            "stockItems",
            filters=[{"field": "sku", "value": ",".join(skus), "condition_type": "in"}],
            page_size=len(skus)
        )
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    found_skus = {i.get("sku") for i in items}
    rows = [
        [i.get("sku"), i.get("qty"), "Yes" if i.get("is_in_stock") else "No"]
        for i in items
    ]
    if rows:
        print(tabulate(rows, headers=["SKU", "Qty", "In Stock"], tablefmt="github"))

    missing = [sku for sku in skus if sku not in found_skus]
    if missing:
        print(f"\nNot found: {', '.join(missing)}")


def main():
    parser = argparse.ArgumentParser(description="Magento 2 inventory management")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Check stock for a SKU")
    p_check.add_argument("sku")

    p_update = sub.add_parser("update", help="Update stock quantity")
    p_update.add_argument("sku")
    p_update.add_argument("qty")

    p_low = sub.add_parser("low-stock", help="List products below a stock threshold")
    p_low.add_argument("--threshold", type=int, default=10)

    p_bulk = sub.add_parser("bulk-check", help="Check stock for multiple SKUs")
    p_bulk.add_argument("skus", help="Comma-separated list of SKUs")

    args = parser.parse_args()
    {"check": cmd_check, "update": cmd_update, "low-stock": cmd_low_stock, "bulk-check": cmd_bulk_check}[args.command](args)


if __name__ == "__main__":
    main()