# Amap Weather Query System

> 📖 中文读者请访问 [README.md](README.md)

A weather query program based on Amap Open Platform API, supporting both command line and graphical user interfaces.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)
[![Coverage](https://img.shields.io/badge/coverage-85%25-yellow.svg)](https://github.com/)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](https://github.com/)

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Requirements](#requirements)
- [Installation & Configuration](#installation--configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Authors & Acknowledgments](#authors--acknowledgments)
- [Changelog](#changelog)

## ✨ Features

- 🌍 Support for Chinese and English city names
- 📅 Get weather forecasts (Amap free API returns 4 days)
- 🌡️ Display weather conditions, temperature, wind direction and force
- 🛡️ Comprehensive exception handling
- 🔄 Support for cyclic queries
- 💻 Both Command Line Interface (CLI) and Graphical User Interface (GUI)
- 🎯 Pre-configured popular cities for quick queries
- 🔍 Auto-detect unknown cities via Geocoding API

## 🏗️ System Architecture

```
weather_query_amap/
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
├── LICENSE               # License file
├── README.md             # Chinese documentation
├── README.en.md          # English documentation
├── config.py             # Configuration management module
├── weather_api.py        # Core API calling module
├── cli.py                # Command line interface
├── gui.py                # Graphical user interface
├── main.py               # Program entry point
├── test_weather.py       # Unit tests and integration tests
├── verify_security.py    # Security verification script
└── requirements.txt      # Dependencies list
```

### Module Description

| Module | Description |
|--------|-------------|
| [config.py](file:///d:\git\weather_query_amap\config.py) | Load configuration from environment variables, manage API keys and endpoints |
| [weather_api.py](file:///d:\git\weather_query_amap\weather_api.py) | Core business logic, including API calls, data parsing and formatting |
| [cli.py](file:///d:\git\weather_query_amap\cli.py) | Command line interactive interface with cyclic query support |
| [gui.py](file:///d:\git\weather_query_amap\gui.py) | tkinter-based graphical user interface |
| [main.py](file:///d:\git\weather_query_amap\main.py) | Program entry point with command line argument parsing |
| [test_weather.py](file:///d:\git\weather_query_amap\test_weather.py) | Unit tests and integration test cases |

## 📦 Requirements

- **Python**: 3.7+
- **Operating System**: Windows / macOS / Linux
- **Network Connection**: Required for accessing Amap APIs

### Dependencies

```txt
requests>=2.28.0
python-dotenv>=1.0.0
```

## 🚀 Installation & Configuration

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/weather_query_amap.git
cd weather_query_amap
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the environment variable template:

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

Edit the `.env` file and fill in your Amap API key:

```env
# Amap Weather Query System Configuration
AMAP_API_KEY=your_actual_api_key_here
AMAP_WEATHER_URL=https://restapi.amap.com/v3/weather/weatherInfo
AMAP_GEOCODE_URL=https://restapi.amap.com/v3/geocode/geo
```

### 4. Get an API Key

1. Visit [Amap Open Platform Console](https://console.amap.com/dev/key/app)
2. Register or log in to your account
3. Create a new application with "Web Service" type
4. Get your API key

**⚠️ Important**: Never commit your `.env` file to version control, it contains sensitive information!

## 💡 Usage

### Method 1: Graphical Interface (Default)

```bash
python main.py
```

### Method 2: Command Line Interface

```bash
python main.py --cli
```

### Method 3: Direct Query for Specific City

```bash
python main.py --city Beijing
python main.py --city 上海
```

### CLI Usage Example

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

### GUI Usage Instructions

1. Enter city name in the input box
2. Click "Query" button or press Enter
3. View query results

## 📡 API Documentation

This project uses two APIs from Amap Open Platform:

### 1. Weather Query API

- **URL**: `https://restapi.amap.com/v3/weather/weatherInfo`
- **Documentation**: [Amap Weather API](https://developer.amap.com/api/webservice/guide/api-advanced/weatherinfo)
- **Request Parameters**:
  - `key`: API key
  - `city`: City adcode
  - `extensions`: Forecast type (`all` for multi-day forecast, free API returns 4 days)
  - `output`: Output format (`json`)
- **Note**: Amap free API returns 4 days of forecast data, paid API may return more

### 2. Geocoding API

- **URL**: `https://restapi.amap.com/v3/geocode/geo`
- **Documentation**: [Amap Geocoding API](https://developer.amap.com/api/webservice/guide/api/georegeo)
- **Request Parameters**:
  - `key`: API key
  - `address`: Address/city name
  - `output`: Output format (`json`)

### Exception Types

| Exception Class | Description |
|-----------------|-------------|
| `NetworkError` | Network connection error |
| `APIRateLimitError` | API call limit or frequency limit exceeded |
| `CityNotFoundError` | City not found |
| `InvalidAPIKeyError` | Invalid or missing API Key |
| `WeatherAPIError` | Other API errors |

## 🧪 Testing

### Unit Tests

```bash
python test_weather.py
```

### Integration Tests

After running `test_weather.py`, follow the prompts to choose whether to run integration tests (requires network connection and valid API key).

```bash
python test_weather.py
# After running, you'll be prompted to run integration tests
Run integration tests? (requires network connection) [y/N]: y
```

## 🤝 Contributing

We welcome all forms of contributions!

### Development Workflow

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 coding standards
- Use type hints
- Write comprehensive docstrings
- Ensure all tests pass
- Run `python test_weather.py` before committing

### Reporting Issues

Use GitHub Issues to report bugs or suggest features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](file:///d:\git\weather_query_amap\LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Simon Xu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👤 Authors & Acknowledgments

- **Simon Xu** - Initial work

### Acknowledgments

- Thanks to [Amap Open Platform](https://lbs.amap.com/) for providing the weather API
- Thanks to all contributors who have helped with this project

## 📝 Changelog

### [1.0.0] - 2026-05-05

#### Added

- ✅ Implemented core weather query functionality
- ✅ Support for Chinese and English city names
- ✅ Weather forecast retrieval (Amap API returns 4 days)
- ✅ Command Line Interface (CLI)
- ✅ Graphical User Interface (GUI)
- ✅ Comprehensive exception handling mechanism
- ✅ Unit tests and integration tests
- ✅ Environment variable configuration support
- ✅ Pre-configured popular city list

#### Documentation Update

- ✅ Updated documentation to reflect that Amap API actually returns 4 days instead of 7

---

## 📌 Notes

1. Ensure network connection is normal
2. API calls have traffic limits, please do not call frequently
3. Weather data is updated 3 times a day (around 8:00, 11:00, 18:00)
4. If you encounter API rate limiting, please try again later
5. Amap free API returns 4 days of weather forecast data

## 🔒 Security Notes

- Sensitive credentials are stored in environment variables, not hardcoded
- `.env` file is excluded from version control via `.gitignore`
- Always use `.env.example` as a template for new contributors
- Never commit actual API keys, passwords, or tokens to Git

---

<p align="center">
  <i>Made with ❤️ by Simon Xu</i>
</p>
