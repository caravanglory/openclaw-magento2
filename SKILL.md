---
name: magento2
description: >
  Manage a Magento 2 / Adobe Commerce store via REST API. Use for orders,
  catalog, customers, inventory, promotions, and sales reporting. Triggers on
  requests like "show me today's orders", "update product stock", "create a
  coupon code", "run a sales report", or anything referencing a Magento store.
version: 0.1.0
metadata:
  openclaw:
    emoji: "🛒"
    homepage: https://github.com/CaravanOfGlory/openclaw-magento2
    primaryEnv: MAGENTO_BASE_URL
    requires:
      env:
        - MAGENTO_BASE_URL
        - MAGENTO_CONSUMER_KEY
        - MAGENTO_CONSUMER_SECRET
        - MAGENTO_ACCESS_TOKEN
        - MAGENTO_ACCESS_TOKEN_SECRET
      bins:
        - python3
    install:
      - kind: uv
        packages:
          - requests
          - requests-oauthlib
          - pandas
          - tabulate
        label: "Install Python dependencies (uv)"
---

# Magento 2 Skill

Connect to a Magento 2 or Adobe Commerce store via its REST API using OAuth 1.0a.

## Authentication

All requests are signed with OAuth 1.0a. Credentials are read from environment variables — never ask the user to paste them in chat.

Required env vars:
- `MAGENTO_BASE_URL` — e.g. `https://store.example.com`
- `MAGENTO_CONSUMER_KEY`
- `MAGENTO_CONSUMER_SECRET`
- `MAGENTO_ACCESS_TOKEN`
- `MAGENTO_ACCESS_TOKEN_SECRET`

Optional env vars:
- `MAGENTO_TIMEOUT` — Default is 30 seconds.
- `MAGENTO_DEBUG` — Set to 1 to enable verbose logging to stderr.

All scripts import the shared client from `scripts/magento_client.py`. Never construct raw HTTP requests inline — always use the client.

## Available commands

Run scripts with: `python3 <skill_dir>/scripts/<script>.py [args]`

### Orders — `scripts/orders.py`

```
# List recent orders (default: last 20)
python3 orders.py list [--limit N] [--status pending|processing|complete|cancelled]

# Get a single order
python3 orders.py get <order_id>

# Update order status
python3 orders.py update-status <order_id> <status>

# Cancel an order
python3 orders.py cancel <order_id>

# Ship an order (optional: add tracking number and carrier)
python3 orders.py ship <order_id> [--track N] [--carrier carrier_code] [--title title]

# Invoice an order
python3 orders.py invoice <order_id>
```

### Catalog — `scripts/catalog.py`

```
# Search products
python3 catalog.py search <query> [--limit N]

# Get product by SKU
python3 catalog.py get <sku>

# Update product price
python3 catalog.py update-price <sku> <price>

# Update product name / description
python3 catalog.py update-attribute <sku> <attribute> <value>

# Enable or disable a product
python3 catalog.py update-status <sku> {enabled|disabled}

# Delete a product
python3 catalog.py delete <sku>

# List categories
python3 catalog.py categories
```

### Customers — `scripts/customers.py`

```
# Search customers by email or name
python3 customers.py search <query> [--limit N]

# Get customer by ID
python3 customers.py get <customer_id>

# Get customer orders
python3 customers.py orders <customer_id>

# Update customer group
python3 customers.py update-group <customer_id> <group_id>
```

### Inventory — `scripts/inventory.py`

```
# Check stock for a SKU
python3 inventory.py check <sku>

# Update stock quantity
python3 inventory.py update <sku> <qty>

# List low-stock products (below threshold)
python3 inventory.py low-stock [--threshold N]

# Bulk stock check from a comma-separated SKU list
python3 inventory.py bulk-check <sku1,sku2,...>
```

### Promotions — `scripts/promotions.py`

```
# List active cart price rules
python3 promotions.py list [--active-only]

# Get a rule by ID
python3 promotions.py get <rule_id>

# Create a coupon code for an existing rule
python3 promotions.py create-coupon <rule_id> <code> [--uses N]

# Disable a promotion rule
python3 promotions.py disable <rule_id>

# List coupon usage stats
python3 promotions.py coupon-stats <coupon_code>
```

### Reporting — `scripts/reports.py`

```
# Sales summary for a date range
python3 reports.py sales --from YYYY-MM-DD --to YYYY-MM-DD

# Revenue by product (top N)
python3 reports.py top-products [--limit N] [--from YYYY-MM-DD] [--to YYYY-MM-DD]

# Revenue by customer (top N)
python3 reports.py top-customers [--limit N] [--from YYYY-MM-DD] [--to YYYY-MM-DD]

# Order status breakdown
python3 reports.py order-status [--from YYYY-MM-DD] [--to YYYY-MM-DD]

# Inventory value report
python3 reports.py inventory-value
```

### System — `scripts/system.py`

```
# Check API connection status
python3 system.py status

# List cache types
python3 system.py cache-list

# Flush all caches
python3 system.py cache-flush

# Flush specific caches (comma-separated)
python3 system.py cache-flush --types config,layout,block_html
```

## Output format

All scripts print a UTF-8 table (via `tabulate`) or a JSON summary to stdout. When presenting results to the user, render them as a markdown table. For single-record lookups, format as a definition list.

## Error handling

Scripts exit with code 1 on API errors and print a JSON error to stderr:
```json
{ "error": "404 Not Found", "message": "No such entity with id = 99", "url": "..." }
```

If a script fails, read stderr, extract the `message` field, and tell the user plainly what went wrong. Do not retry automatically unless the user asks.

## Rules

- Never expose OAuth credentials in chat output, logs, or summaries.
- For destructive operations (cancel order, delete product, disable promotion), confirm with the user before running the script.
- Always show the user the exact script invocation you are about to run before executing it.
- When a date range is not specified for reports, default to the last 30 days.
- Monetary values are returned in the store's base currency — include the currency code in output.
- **Production Safety**: After performing updates to products or prices, it is recommended to run `system.py cache-flush` if the changes don't appear on the frontend.