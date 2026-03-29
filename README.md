# OpenClaw Magento 2 Skill

[简体中文](./README.zh-CN.md)

Manage your Magento 2 or Adobe Commerce store directly from **OpenClaw**. This skill allows your AI agent to interact with your store's REST API to manage orders, catalog, customers, inventory, and promotions.

## 🚀 Features

- **Orders**: List, view, update status, cancel, ship (with tracking), and invoice.
- **Catalog**: Search products, update prices, manage attributes, and browse categories.
- **Customers**: Search, view order history, and manage customer groups.
- **Inventory**: Real-time stock checks, bulk updates, and low-stock reporting.
- **Promotions**: List cart rules, create coupon codes, and monitor usage stats.
- **Reporting**: Sales summaries, top products, top customers, and inventory value reports.
- **System**: Health checks and cache management (flush/list).

## 📦 Installation

To install this skill in your OpenClaw environment:

```bash
openclaw install https://github.com/CaravanOfGlory/openclaw-magento2
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
- "Flush the Magento cache."

## 📄 License

This project is licensed under the MIT License.