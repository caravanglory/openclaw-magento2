# OpenClaw Magento 2

**对话式运营，Magento 2 全新体验。**

OpenClaw 上面向 Magento 2 的 AI 助手 —— 通过自然语言即可对商城进行巡检、诊断与运营管理。

OpenClaw Magento 2 将您的 Magento / Adobe Commerce 商城转变为对话式运营工作台。无需在多个管理后台页面间反复点击操作，您可直接查询商城健康状态、排查订单或库存问题、生成报表，并在执行操作前安全预览变更内容。

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-blue)](https://github.com/caravanglory/openclaw-magento2)
[![CI](https://img.shields.io/github/actions/workflow/status/caravanglory/openclaw-magento2/python-app.yml?branch=main)](https://github.com/caravanglory/openclaw-magento2/actions)
[![Linting](https://img.shields.io/badge/Linter-Ruff-FCC21B?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

</div>

[中文](./README.zh-CN.md) | [English](./README.md)

## 用自然语言管理您的商店

- “给我一份今日早间简报 —— 今天有什么问题吗？”
- “哪些商品即将缺货？”
- “有没有需要我处理的卡住的订单？”
- “根据 CSV 文件批量更新这 50 个商品的价格。”
- “检查我的商品目录中是否存在价格异常。”
- “显示最近的 5 笔订单。”

## 功能特性

### 核心操作
- **订单管理**：列出订单、查看详情、更新状态、取消、发货（支持物流单号）以及开票。
- **目录管理**：搜索产品、更新价格、管理属性以及浏览分类。
- **客户管理**：搜索客户、查看订单历史以及管理客户组。
- **库存管理**：实时库存检查、批量更新和低库存报表。
- **促销管理**：列出购物车价格规则、创建优惠码并监控使用统计。
- **数据报表**：销售摘要、畅销产品、顶级客户以及库存价值报表。
- **服务发现**：探索已安装的模块和 REST API 架构，发现自定义功能。
- **自定义 API**：与发现的自定义端点交互（例如博客或自定义扩展）。
- **系统工具**：连接状态检查和缓存管理（清理/列表）。

### AI 副驾驶功能
- **晨报 (Morning Brief)**：一条命令获取每日店铺健康摘要，覆盖销售、订单、库存、促销和客户，自动发现需要关注的问题。
- **库存风险雷达**：结合当前库存和销售速度预测断货日期，识别缺货产品和 MSI 源问题。
- **促销审计**：检测过期但仍激活的规则、缺失的优惠码、已用尽的限额以及即将到期的规则。
- **订单异常分诊**：发现卡住的待处理订单、支付审核、处理延迟和取消量突增。
- **价格异常检测**：发现零价格、负价格、倒挂特价和过期特价 — 无需全量拉取目录。
- **批量操作**：通过 CSV 文件或内联输入批量更新价格、库存和发货。执行前预览。

### 多源库存 (MSI)
- 管理 Magento 2.3+ 的库存源、源项目、可售数量和库存配置。

### 多站点支持
- 使用站点别名（`--site us`、`--site eu`）从单个 OpenClaw 实例连接和管理多个 Magento 商店。

### 批量操作
- **批量改价**：通过 CSV 或内联输入更新多个产品价格，执行前预览差异。
- **批量更新库存**：一次性为多个 SKU 补货。
- **批量发货**：通过 CSV 文件为多个订单创建发货。

## 📦 安装

**通过 ClawHub 安装：**

```bash
openclaw skills install magento2
```

**手动安装：**

```bash
git clone https://github.com/caravanglory/openclaw-magento2 ~/.openclaw/workspace/skills/magento2
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

## ⚡ 快速开始（60 秒冒烟测试）

安装并配置环境变量后：

```bash
# 验证 API 连接
python3 scripts/system.py status

# 列出最近的订单
python3 scripts/orders.py list --limit 5

# 获取晨报
python3 scripts/morning_brief.py brief

# 检查库存风险
python3 scripts/diagnose.py inventory-risk
```

如果命令返回数据，说明一切就绪。

## 📄 许可证

本项目采用 MIT 许可证。

## 🛡️ 安全性 (SLSA)

本项目遵循 SLSA (软件工件供应链级别) 指南，以确保软件的完整性。
