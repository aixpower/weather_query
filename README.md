# Amap Weather Query System

Weather query program based on Amap Open Platform API, supporting both command line and graphical interfaces.

## Features

- Supports Chinese and English city names
- Get 7-day weather forecast
- Display weather conditions, temperature, wind direction and force
- Comprehensive exception handling
- Support for cyclic queries
- Command Line Interface (CLI) and Graphical User Interface (GUI)

## Project Structure

```
weather_query_amap/
├── .env.example       # Environment variable template
├── .gitignore         # Git ignore rules
├── config.py          # Configuration file (loads from .env)
├── weather_api.py     # Core API calling module
├── cli.py             # Command line interface
├── gui.py             # Graphical user interface
├── main.py            # Program entry point
├── test_weather.py    # Test cases
├── requirements.txt   # Dependencies list
└── README.md          # Usage documentation
```

## Requirements

- Python 3.7+
- requests library
- python-dotenv library

## Installation

1. Clone or download the project to local

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and set your actual API key
# AMAP_API_KEY=your_actual_api_key
```

## Configuration

### Getting an API Key

1. Go to [Amap Open Platform Console](https://console.amap.com/dev/key/app)
2. Sign up or log in
3. Create a new application with "Web Service" type
4. Get your API key

### Setting Up Environment Variables

Create a `.env` file in the project root directory with your API key:

```env
# Amap Weather Query System Configuration
AMAP_API_KEY=your_actual_api_key_here

# Amap API Endpoints (usually don't need to change)
AMAP_WEATHER_URL=https://restapi.amap.com/v3/weather/weatherInfo
AMAP_GEOCODE_URL=https://restapi.amap.com/v3/geocode/geo
```

**Important:** Never commit your `.env` file to version control. It contains sensitive information!

## Usage

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
python main.py --city Shanghai
```

### CLI Usage Instructions

- Enter city name (Chinese or English) to query
- Enter `quit` or `exit` to exit the program
- Supports cyclic queries, can query multiple cities consecutively

### GUI Usage Instructions

1. Enter city name in the input box
2. Click "Query" button or press Enter
3. View query results

## Supported Cities

Pre-configured city list:
- Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Chengdu, Wuhan, Xian, Nanjing, Chongqing, Tianjin

Other cities are automatically found through Amap Geocoding API.

## Running Tests

### Unit Tests

```bash
python test_weather.py
```

### Integration Tests

After running `test_weather.py`, follow the prompts to choose whether to run integration tests (requires network connection and valid API key).

## API Description

This program uses two APIs from Amap Open Platform:

1. **Weather Query API**: Get weather forecast
   - URL: https://restapi.amap.com/v3/weather/weatherInfo
   - Documentation: https://developer.amap.com/api/webservice/guide/api-advanced/weatherinfo

2. **Geocoding API**: Convert city name to adcode
   - URL: https://restapi.amap.com/v3/geocode/geo

## Exception Handling

The program includes the following exception handling:

- `NetworkError`: Network connection error
- `APIRateLimitError`: API call limit exceeded or frequency limit exceeded
- `CityNotFoundError`: City not found
- `InvalidAPIKeyError`: Invalid or missing API Key
- `WeatherAPIError`: Other API errors

## Security Notes

- Sensitive credentials are stored in environment variables, not hardcoded
- `.env` file is excluded from version control via `.gitignore`
- Always use `.env.example` as a template for new contributors
- Never commit actual API keys, passwords, or tokens to Git

## Notes

1. Ensure network connection is normal
2. API calls have traffic limits, please do not call frequently
3. Weather data is updated 3 times a day (around 8:00, 11:00, 18:00)
4. If you encounter API rate limiting, please try again later

## Development Standards

- Follow PEP 8 coding standards
- Use type hints
- Comprehensive exception handling
- Modular design, easy to extend

## License

This project is for learning purposes only.
