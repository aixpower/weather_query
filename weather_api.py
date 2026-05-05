
import requests
from config import AMAP_API_KEY, AMAP_WEATHER_URL, AMAP_GEOCODE_URL, CITY_ADCODE_MAP


class WeatherAPIError(Exception):
    pass


def validate_api_key():
    if not AMAP_API_KEY or AMAP_API_KEY == 'your_amap_api_key_here' or AMAP_API_KEY == '':
        raise InvalidAPIKeyError("API Key not configured. Please set AMAP_API_KEY in .env file.")


class NetworkError(WeatherAPIError):
    pass


class APIRateLimitError(WeatherAPIError):
    pass


class CityNotFoundError(WeatherAPIError):
    pass


class InvalidAPIKeyError(WeatherAPIError):
    pass


def get_adcode(city_name):
    city_name_lower = city_name.strip().lower()
    
    for name, adcode in CITY_ADCODE_MAP.items():
        if name.lower() == city_name_lower:
            return adcode
    
    try:
        params = {
            "key": AMAP_API_KEY,
            "address": city_name,
            "output": "json"
        }
        response = requests.get(AMAP_GEOCODE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "1" and data.get("geocodes"):
            adcode = data["geocodes"][0].get("adcode")
            if adcode:
                return adcode
    except requests.RequestException:
        pass
    
    raise CityNotFoundError("City not found: " + city_name)


def get_weather_forecast(city_name):
    validate_api_key()
    try:
        adcode = get_adcode(city_name)
        
        params = {
            "key": AMAP_API_KEY,
            "city": adcode,
            "extensions": "all",
            "output": "json"
        }
        
        response = requests.get(AMAP_WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "1":
            infocode = data.get("infocode", "")
            info = data.get("info", "")
            
            if infocode == "10001":
                raise InvalidAPIKeyError("Invalid API Key")
            elif infocode == "10003":
                raise APIRateLimitError("API call limit reached")
            elif infocode == "10004":
                raise APIRateLimitError("API access frequency limit")
            else:
                raise WeatherAPIError("API error: " + info + " (infocode: " + infocode + ")")
        
        return data
        
    except requests.Timeout:
        raise NetworkError("Request timeout, please check network connection")
    except requests.ConnectionError:
        raise NetworkError("Network connection error, please check network status")
    except requests.RequestException as e:
        raise NetworkError("Network request failed: " + str(e))


def parse_weather_data(data):
    if not data or "forecasts" not in data or not data["forecasts"]:
        raise WeatherAPIError("Invalid data format")
    
    forecast = data["forecasts"][0]
    city = forecast.get("city", "")
    province = forecast.get("province", "")
    report_time = forecast.get("reporttime", "")
    casts = forecast.get("casts", [])
    
    result = {
        "city": city,
        "province": province,
        "report_time": report_time,
        "forecasts": []
    }
    
    for cast in casts:
        result["forecasts"].append({
            "date": cast.get("date", ""),
            "week": cast.get("week", ""),
            "day_weather": cast.get("dayweather", ""),
            "night_weather": cast.get("nightweather", ""),
            "day_temp": cast.get("daytemp", ""),
            "night_temp": cast.get("nighttemp", ""),
            "day_wind": cast.get("daywind", ""),
            "night_wind": cast.get("nightwind", ""),
            "day_power": cast.get("daypower", ""),
            "night_power": cast.get("nightpower", "")
        })
    
    return result


def format_weather_display(weather_data):
    if not weather_data:
        return ""
    
    lines = []
    lines.append("=" * 60)
    lines.append(weather_data["province"] + " " + weather_data["city"] + " Weather Forecast")
    lines.append("Report Time: " + weather_data["report_time"])
    lines.append("=" * 60)
    
    week_map = {"1": "Monday", "2": "Tuesday", "3": "Wednesday", "4": "Thursday", 
                "5": "Friday", "6": "Saturday", "7": "Sunday"}
    
    for idx, forecast in enumerate(weather_data["forecasts"], 1):
        week = week_map.get(forecast["week"], forecast["week"])
        lines.append("")
        lines.append("[Day " + str(idx) + "] " + forecast["date"] + " " + week)
        lines.append("  Day: " + forecast["day_weather"] + "  " + forecast["day_temp"] + "C")
        lines.append("       " + forecast["day_wind"] + " Wind " + forecast["day_power"] + " Level")
        lines.append("  Night: " + forecast["night_weather"] + "  " + forecast["night_temp"] + "C")
        lines.append("         " + forecast["night_wind"] + " Wind " + forecast["night_power"] + " Level")
    
    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)
