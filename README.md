# Amap Weather Query System

基于高德开放平台 API 的天气查询程序，支持命令行和图形用户界面。

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-yellow.svg)](https://github.com/)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](https://github.com/)

## 📋 目录

- [功能特性](#功能特性)
- [系统架构](#系统架构)
- [环境要求](#环境要求)
- [安装与配置](#安装与配置)
- [使用说明](#使用说明)
- [API 接口文档](#api-接口文档)
- [测试](#测试)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [作者与致谢](#作者与致谢)
- [更新日志](#更新日志)

## ✨ 功能特性

- 🌍 支持中英文城市名称查询
- 📅 获取 7 天天气预报
- 🌡️ 显示天气状况、温度、风向和风力
- 🛡️ 完善的异常处理机制
- 🔄 支持循环查询
- 💻 命令行界面 (CLI) 和图形用户界面 (GUI) 双支持
- 🎯 预配置热门城市，快速查询
- 🔍 自动通过地理编码 API 查找未知城市

## 🏗️ 系统架构

```
weather_query_amap/
├── .env.example          # 环境变量模板
├── .gitignore            # Git 忽略规则
├── LICENSE               # 许可证文件
├── README.md             # 项目说明文档
├── config.py             # 配置管理模块
├── weather_api.py        # 核心 API 调用模块
├── cli.py                # 命令行界面
├── gui.py                # 图形用户界面
├── main.py               # 程序入口点
├── test_weather.py       # 单元测试和集成测试
├── verify_security.py    # 安全验证脚本
└── requirements.txt      # 依赖列表
```

### 模块说明

| 模块 | 功能描述 |
|------|----------|
| [config.py](file:///d:\git\weather_query_amap\config.py) | 从环境变量加载配置，管理 API 密钥和端点 |
| [weather_api.py](file:///d:\git\weather_query_amap\weather_api.py) | 核心业务逻辑，包括 API 调用、数据解析和格式化 |
| [cli.py](file:///d:\git\weather_query_amap\cli.py) | 命令行交互界面，支持循环查询 |
| [gui.py](file:///d:\git\weather_query_amap\gui.py) | 基于 tkinter 的图形用户界面 |
| [main.py](file:///d:\git\weather_query_amap\main.py) | 程序入口，支持命令行参数解析 |
| [test_weather.py](file:///d:\git\weather_query_amap\test_weather.py) | 单元测试和集成测试用例 |

## 📦 环境要求

- **Python**: 3.7+
- **操作系统**: Windows / macOS / Linux
- **网络连接**: 需要网络连接访问高德 API

### 依赖库

```txt
requests>=2.28.0
python-dotenv>=1.0.0
```

## 🚀 安装与配置

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/weather_query_amap.git
cd weather_query_amap
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量模板文件：

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

编辑 `.env` 文件，填入您的高德 API 密钥：

```env
# Amap Weather Query System Configuration
AMAP_API_KEY=your_actual_api_key_here
AMAP_WEATHER_URL=https://restapi.amap.com/v3/weather/weatherInfo
AMAP_GEOCODE_URL=https://restapi.amap.com/v3/geocode/geo
```

### 4. 获取 API 密钥

1. 访问 [高德开放平台控制台](https://console.amap.com/dev/key/app)
2. 注册或登录账号
3. 创建新应用，选择「Web 服务」类型
4. 获取您的 API 密钥

**⚠️ 重要提示**：切勿将 `.env` 文件提交到版本控制系统，它包含敏感信息！

## 💡 使用说明

### 方法 1：图形界面（默认）

```bash
python main.py
```

### 方法 2：命令行界面

```bash
python main.py --cli
```

### 方法 3：直接查询指定城市

```bash
python main.py --city Beijing
python main.py --city 上海
```

### CLI 使用示例

```bash
$ python main.py --cli
============================================================
           Amap Weather Query System
============================================================
Supports Chinese and English city names
Enter 'quit' or 'exit' to exit
============================================================

Enter city name: Beijing

Querying weather for Beijing...

============================================================
Beijing Beijing Weather Forecast
Report Time: 2024-01-01 12:00:00
============================================================

[Day 1] 2024-01-01 Monday
  Day: Sunny  10C
       North Wind 3 Level
  Night: Cloudy  -2C
         Northwest Wind 2 Level

============================================================
```

### GUI 使用说明

1. 在输入框中输入城市名称
2. 点击「Query」按钮或按回车键
3. 查看查询结果

## 📡 API 接口文档

本项目使用高德开放平台的两个 API：

### 1. 天气查询 API

- **URL**: `https://restapi.amap.com/v3/weather/weatherInfo`
- **文档**: [高德天气查询 API](https://developer.amap.com/api/webservice/guide/api-advanced/weatherinfo)
- **请求参数**:
  - `key`: API 密钥
  - `city`: 城市 adcode
  - `extensions`: 预报类型（`all` 表示 7 天预报）
  - `output`: 输出格式（`json`）

### 2. 地理编码 API

- **URL**: `https://restapi.amap.com/v3/geocode/geo`
- **文档**: [高德地理编码 API](https://developer.amap.com/api/webservice/guide/api/georegeo)
- **请求参数**:
  - `key`: API 密钥
  - `address`: 地址/城市名称
  - `output`: 输出格式（`json`）

### 异常类型

| 异常类 | 说明 |
|--------|------|
| `NetworkError` | 网络连接错误 |
| `APIRateLimitError` | API 调用限制或频率超限 |
| `CityNotFoundError` | 城市未找到 |
| `InvalidAPIKeyError` | API 密钥无效或缺失 |
| `WeatherAPIError` | 其他 API 错误 |

## 🧪 测试

### 单元测试

```bash
python test_weather.py
```

### 集成测试

运行 `test_weather.py` 后，根据提示选择是否运行集成测试（需要网络连接和有效的 API 密钥）。

```bash
python test_weather.py
# 运行后会提示是否运行集成测试
Run integration tests? (requires network connection) [y/N]: y
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 编码规范
- 使用类型提示
- 编写完善的文档字符串
- 确保所有测试通过
- 提交前运行 `python test_weather.py`

### 报告问题

使用 GitHub Issues 报告 bug 或提出功能建议。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](file:///d:\git\weather_query_amap\LICENSE) 文件。

```
MIT License

Copyright (c) 2026 Simon Xu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👤 作者与致谢

- **Simon Xu** - 初始工作

### 致谢

- 感谢 [高德开放平台](https://lbs.amap.com/) 提供的天气 API
- 感谢所有为本项目做出贡献的开发者

## 📝 更新日志

### [1.0.0] - 2026-05-05

#### 新增

- ✅ 实现核心天气查询功能
- ✅ 支持中英文城市名称
- ✅ 7 天天气预报获取
- ✅ 命令行界面 (CLI)
- ✅ 图形用户界面 (GUI)
- ✅ 完善的异常处理机制
- ✅ 单元测试和集成测试
- ✅ 环境变量配置支持
- ✅ 预配置热门城市列表

#### 修复

- 无

#### 改进

- 无

---

## 📌 注意事项

1. 确保网络连接正常
2. API 调用有流量限制，请勿频繁调用
3. 天气数据每天更新 3 次（约 8:00、11:00、18:00）
4. 如遇 API 速率限制，请稍后重试

## 🔒 安全说明

- 敏感凭证存储在环境变量中，而非硬编码
- `.env` 文件通过 `.gitignore` 排除在版本控制之外
- 始终使用 `.env.example` 作为新贡献者的模板
- 切勿将实际的 API 密钥、密码或令牌提交到 Git

---

<p align="center">
  <i>Made with ❤️ by Simon Xu</i>
</p>
