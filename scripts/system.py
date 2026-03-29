#!/usr/bin/env python3
"""System management — health checks and cache management."""

import sys
import argparse
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def cmd_status(args):
    client = get_client()
    try:
        # Check basic connection by fetching store info
        store_info = client.get("store/storeConfigs")
        print("API Connection: OK")
        if store_info:
            print(f"Store Count: {len(store_info)}")
            print(f"Base URL: {store_info[0].get('base_url')}")
    except MagentoAPIError as e:
        print(f"API Connection: FAILED ({e.status})")
        print_error_and_exit(e)


def cmd_cache_list(args):
    client = get_client()
    try:
        caches = client.get("cache")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    rows = [[c.get("id"), c.get("status"), c.get("label")] for c in caches]
    print(tabulate(rows, headers=["ID", "Status", "Label"], tablefmt="github"))


def cmd_cache_flush(args):
    client = get_client()
    # If no types specified, flush all
    try:
        if not args.types:
            # Fetch all types first
            caches = client.get("cache")
            types = [c.get("id") for c in caches]
        else:
            types = [t.strip() for t in args.types.split(",")]

        # Magento expects IDs in the request
        for cache_type in types:
            client.post("cache/clear", {"ids": [cache_type]})
            print(f"Cache '{cache_type}' cleared.")
        
        print("\nAll specified caches have been cleared.")
    except MagentoAPIError as e:
        print_error_and_exit(e)


def main():
    parser = argparse.ArgumentParser(description="Magento 2 system management")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Check API connection status")
    sub.add_parser("cache-list", help="List cache types and statuses")
    
    p_flush = sub.add_parser("cache-flush", help="Flush specific or all caches")
    p_flush.add_argument("--types", help="Comma-separated list of cache IDs to flush (default: all)")

    args = parser.parse_args()
    {"status": cmd_status, "cache-list": cmd_cache_list, "cache-flush": cmd_cache_flush}[args.command](args)


if __name__ == "__main__":
    main()