# OpenClaw Magento 2

**Magento 2, operated by conversation.**

AI copilot for Magento 2 in OpenClaw — inspect, diagnose, and operate your store with natural language.

OpenClaw Magento 2 turns your Magento / Adobe Commerce store into a conversational operations workspace. Instead of clicking through multiple admin panels, you can ask for store health, investigate order or inventory issues, run reports, and safely preview changes before execution.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-blue)](https://github.com/caravanglory/openclaw-magento2)
[![CI](https://img.shields.io/github/actions/workflow/status/caravanglory/openclaw-magento2/python-app.yml?branch=main)](https://github.com/caravanglory/openclaw-magento2/actions)
[![Linting](https://img.shields.io/badge/Linter-Ruff-FCC21B?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

</div>

[中文](./README.zh-CN.md) | [English](./README.md)


## Ask your store anything

- "Give me a morning brief — any issues today?"
- "Which products are about to run out of stock?"
- "Are there any stuck orders I need to look at?"
- "Bulk update these 50 product prices from a CSV."
- "Check for pricing anomalies on my catalog."
- "Show me the last 5 orders."

## Features

### Core Operations
- **Orders**: List, view, update status, cancel, ship (with tracking), and invoice.
- **Catalog**: Search products, update prices, manage attributes, and browse categories.
- **Customers**: Search, view order history, and manage customer groups.
- **Inventory**: Real-time stock checks, bulk updates, and low-stock reporting.
- **Promotions**: List cart rules, create coupon codes, and monitor usage stats.
- **Reporting**: Sales summaries, top products, top customers, and inventory value reports.
- **Discovery**: Explore installed modules and REST API schema to discover custom features.
- **Custom API**: Interact with discovered custom endpoints (e.g., Blog or custom extensions).
- **System**: Health checks and cache management (flush/list).

### AI Copilot Features
- **Morning Brief**: One-command daily health summary across sales, orders, inventory, promotions, and customers. Automatically surfaces issues that need attention.
- **Inventory Risk Radar**: Predicts stockout dates by combining current stock levels with sales velocity. Identifies out-of-stock products and MSI source issues.
- **Promotion Audit**: Detects expired-but-active rules, missing coupon codes, exhausted limits, and rules expiring soon.
- **Order Exception Triage**: Finds stuck pending orders, payment review holds, processing delays, and cancellation spikes.
- **Pricing Anomaly Detection**: Finds zero-price products, negative prices, inverted special prices, and expired special prices — without full catalog scans.
- **Bulk Operations**: Batch update prices, stock levels, and create shipments via CSV files or inline input. Preview before execute.

### Multi-Source Inventory (MSI)
- Manage inventory sources, source items, salable quantities, and stock configurations for Magento 2.3+.

### Multi-Site Support
- Connect and manage multiple Magento stores from a single OpenClaw instance using site aliases (`--site us`, `--site eu`).

### Bulk Operations
- **Batch Price Updates**: Update dozens of product prices from CSV or inline input with preview/diff before execution.
- **Batch Stock Updates**: Restock multiple SKUs at once.
- **Batch Shipping**: Create shipments for multiple orders from a CSV file.

## 📦 Installation

**Via ClawHub:**

```bash
openclaw skills install magento2
```

**Manual install:**

```bash
git clone https://github.com/caravanglory/openclaw-magento2 ~/.openclaw/workspace/skills/magento2
```

## ⚙️ Configuration

Set the following environment variables in your OpenClaw `.env` file or system environment:

```bash
# Magento 2 Store URL
MAGENTO_BASE_URL="https://your-store.com"

# OAuth 1.0a Credentials (from Magento Admin: System -> Integrations)
MAGENTO_CONSUMER_KEY="your_consumer_key"
MAGENTO_CONSUMER_SECRET="your_consumer_secret"
MAGENTO_ACCESS_TOKEN="your_access_token"
MAGENTO_ACCESS_TOKEN_SECRET="your_access_token_secret"

# Optional
MAGENTO_TIMEOUT=30
MAGENTO_DEBUG=0
```

## 🛠️ Usage Examples

Once installed, you can talk to OpenClaw naturally:

- "Show me the last 5 orders."
- "What is the stock level for SKU 'TSHIRT-01'?"
- "Update the price of 'BAG-02' to 49.99."
- "Create a 20% discount coupon code 'SPRING2026' for Rule ID 5."
- "Run a sales report for the last 7 days."
- "What custom modules are installed on my Magento store?"
- "Explore the REST API schema for the blog module."
- "Flush the Magento cache."

## ⚡ Quick Start (60-second smoke test)

After installation and configuration:

```bash
# Verify API connection
python3 scripts/system.py status

# List recent orders
python3 scripts/orders.py list --limit 5

# Get a morning brief
python3 scripts/morning_brief.py brief

# Check inventory risks
python3 scripts/diagnose.py inventory-risk
```

If commands return data, you're good to go.

## 📄 License

This project is licensed under the MIT License.

## 🛡️ Security (SLSA)

This project follows SLSA (Supply-chain Levels for Software Artifacts) guidelines to ensure the integrity of the software.
