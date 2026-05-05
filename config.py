import os
from dotenv import load_dotenv

load_dotenv()

AMAP_API_KEY = os.getenv('AMAP_API_KEY', '')
AMAP_WEATHER_URL = os.getenv('AMAP_WEATHER_URL', 'https://restapi.amap.com/v3/weather/weatherInfo')
AMAP_GEOCODE_URL = os.getenv('AMAP_GEOCODE_URL', 'https://restapi.amap.com/v3/geocode/geo')

CITY_ADCODE_MAP = {
    "Beijing": "110000",
    "Shanghai": "310000",
    "Guangzhou": "440100",
    "Shenzhen": "440300",
    "Hangzhou": "330100",
    "Chengdu": "510100",
    "Wuhan": "420100",
    "Xian": "610100",
    "Nanjing": "320100",
    "Chongqing": "500000",
    "Tianjin": "120000",
}
