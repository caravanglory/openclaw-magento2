# OpenClaw Magento 2 Skill

[English](./README.md)

通过 **OpenClaw** 直接管理您的 Magento 2 或 Adobe Commerce 商店。此技能（Skill）允许您的 AI 代理与商店的 REST API 交互，以管理订单、目录、客户、库存和促销活动。

## 🚀 功能特性

- **订单管理**：列出订单、查看详情、更新状态、取消、发货（支持物流单号）以及开票。
- **目录管理**：搜索产品、更新价格、管理属性以及浏览分类。
- **客户管理**：搜索客户、查看订单历史以及管理客户组。
- **库存管理**：实时库存检查、批量更新和低库存报表。
- **促销管理**：列出购物车价格规则、创建优惠码并监控使用统计。
- **数据报表**：销售摘要、畅销产品、顶级客户以及库存价值报表。
- **服务发现**：探索已安装的模块和 REST API 架构，发现自定义功能。
- **自定义 API**：与发现的自定义端点交互（例如博客或自定义扩展）。
- **系统工具**：连接状态检查和缓存管理（清理/列表）。
- **CI/CD**：集成了 GitHub Actions，用于自动化代码质量和语法检查。

## 📦 安装

在您的 OpenClaw 环境中安装此技能：

```bash
openclaw install https://github.com/caravanglory/openclaw-magento2
```

## ⚙️ 配置

在您的 OpenClaw `.env` 文件或系统环境变量中设置以下变量：

```bash
# Magento 2 商店 URL
MAGENTO_BASE_URL="https://your-store.com"

# OAuth 1.0a 凭据 (从 Magento 后台：系统 -> 集成 中获取)
MAGENTO_CONSUMER_KEY="your_consumer_key"
MAGENTO_CONSUMER_SECRET="your_consumer_secret"
MAGENTO_ACCESS_TOKEN="your_access_token"
MAGENTO_ACCESS_TOKEN_SECRET="your_access_token_secret"

# 可选配置
MAGENTO_TIMEOUT=30
MAGENTO_DEBUG=0
```

## 🛠️ 使用示例

安装完成后，您可以直接用自然语言与 OpenClaw 对话：

- “显示最近的 5 个订单。”
- “SKU 'TSHIRT-01' 的库存水平是多少？”
- “将 'BAG-02' 的价格更新为 49.99。”
- “为规则 ID 5 创建一个 20% 的折扣码 'SPRING2026'。”
- “运行过去 7 天的销售报告。”
- “我的 Magento 商店安装了哪些自定义模块？”
- “探索博客模块的 REST API 架构。”
- “刷新 Magento 缓存。”

## 📄 许可证

本项目采用 MIT 许可证。

## 🛡️ 安全性 (SLSA)

本项目遵循 SLSA (软件工件供应链级别) 指南，以确保软件的完整性。