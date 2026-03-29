#!/usr/bin/env python3
"""Orders management — list, get, update status, cancel."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def cmd_list(args):
    client = get_client()
    filters = []
    if args.status:
        filters.append({"field": "status", "value": args.status, "condition_type": "eq"})
    try:
        result = client.search(
            "orders",
            filters=filters,
            page_size=args.limit,
            sort_field="created_at",
            sort_dir="DESC",
        )
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print("No orders found.")
        return

    rows = [
        [
            o.get("increment_id"),
            o.get("status"),
            o.get("customer_email"),
            f"{o.get('base_grand_total', 0):.2f} {o.get('base_currency_code', '')}",
            o.get("created_at", "")[:10],
        ]
        for o in items
    ]
    print(tabulate(rows, headers=["Order #", "Status", "Customer", "Total", "Date"], tablefmt="github"))
    print(f"\nShowing {len(items)} of {result.get('total_count', len(items))} orders.")


def resolve_order_id(client, order_id: str) -> str:
    # If it looks like an increment ID (contains leading zeros or is a long string),
    # search for it first to get the internal entity_id.
    if not order_id.isdigit() or len(order_id) > 6:
        try:
            res = client.search("orders", filters=[{"field": "increment_id", "value": order_id, "condition_type": "eq"}])
            if res.get("items"):
                return str(res["items"][0]["entity_id"])
        except MagentoAPIError:
            pass
    return order_id


def cmd_get(args):
    client = get_client()
    order_id = resolve_order_id(client, args.order_id)

    try:
        o = client.get(f"orders/{order_id}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    fields = [
        ("Order #", o.get("increment_id")),
        ("Status", o.get("status")),
        ("Customer", f"{o.get('customer_firstname', '')} {o.get('customer_lastname', '')}".strip()),
        ("Email", o.get("customer_email")),
        ("Grand Total", f"{o.get('base_grand_total', 0):.2f} {o.get('base_currency_code', '')}"),
        ("Shipping", f"{o.get('base_shipping_amount', 0):.2f}"),
        ("Tax", f"{o.get('base_tax_amount', 0):.2f}"),
        ("Created", o.get("created_at", "")[:19]),
        ("Updated", o.get("updated_at", "")[:19]),
    ]
    print(tabulate(fields, tablefmt="simple"))

    items = o.get("items", [])
    if items:
        print("\nItems:")
        rows = [
            [i.get("sku"), i.get("name"), int(i.get("qty_ordered", 0)), f"{i.get('base_price', 0):.2f}"]
            for i in items
        ]
        print(tabulate(rows, headers=["SKU", "Name", "Qty", "Price"], tablefmt="github"))


def cmd_update_status(args):
    client = get_client()
    order_id = resolve_order_id(client, args.order_id)
    try:
        result = client.post(
            f"orders/{order_id}/comments",
            {"statusHistory": {"comment": f"Status updated by OpenClaw agent", "is_customer_notified": 0, "is_visible_on_front": 0, "status": args.status}},
        )
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Order {args.order_id} status updated to '{args.status}'.")


def cmd_cancel(args):
    client = get_client()
    order_id = resolve_order_id(client, args.order_id)
    try:
        result = client.post(f"orders/{order_id}/cancel", {})
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Order {args.order_id} cancelled successfully.")


def cmd_ship(args):
    client = get_client()
    order_id = resolve_order_id(client, args.order_id)
    body = {"items": [], "notify": True}
    if args.track:
        body["tracks"] = [{
            "track_number": args.track,
            "carrier_code": args.carrier or "custom",
            "title": args.title or "Shipment Tracking"
        }]
    try:
        client.post(f"order/{order_id}/ship", body)
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Shipment created for order {args.order_id}.")
    if args.track:
        print(f"Tracking: {args.track} ({args.carrier or 'custom'})")


def cmd_invoice(args):
    client = get_client()
    order_id = resolve_order_id(client, args.order_id)
    try:
        # Simple invoice for all items
        result = client.post(f"order/{order_id}/invoice", {"capture": True, "notify": True})
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Invoice created and captured for order {args.order_id}.")


def main():
    parser = argparse.ArgumentParser(description="Magento 2 order management")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List recent orders")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--status", choices=["pending", "processing", "complete", "cancelled", "holded", "payment_review"])

    p_get = sub.add_parser("get", help="Get a single order by entity ID")
    p_get.add_argument("order_id")

    p_status = sub.add_parser("update-status", help="Update order status")
    p_status.add_argument("order_id")
    p_status.add_argument("status")

    p_cancel = sub.add_parser("cancel", help="Cancel an order")
    p_cancel.add_argument("order_id")

    p_ship = sub.add_parser("ship", help="Ship an order")
    p_ship.add_argument("order_id")
    p_ship.add_argument("--track", help="Tracking number")
    p_ship.add_argument("--carrier", help="Carrier code (e.g. ups, usps, fedex)")
    p_ship.add_argument("--title", help="Tracking title")

    p_invoice = sub.add_parser("invoice", help="Invoice an order")
    p_invoice.add_argument("order_id")

    args = parser.parse_args()
    {"list": cmd_list, "get": cmd_get, "update-status": cmd_update_status,
     "cancel": cmd_cancel, "ship": cmd_ship, "invoice": cmd_invoice}[args.command](args)


if __name__ == "__main__":
    main()