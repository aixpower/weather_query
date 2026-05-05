
import unittest
import requests
from unittest.mock import patch, MagicMock
from weather_api import (
    get_adcode,
    get_weather_forecast,
    parse_weather_data,
    format_weather_display,
    WeatherAPIError,
    CityNotFoundError,
    NetworkError,
    APIRateLimitError,
    InvalidAPIKeyError
)


class TestWeatherAPI(unittest.TestCase):
    
    def test_get_adcode_known_city(self):
        adcode = get_adcode("Beijing")
        self.assertEqual(adcode, "110000")
    
    def test_get_adcode_unknown_city(self):
        with patch('weather_api.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"status": "0"}
            mock_get.return_value = mock_response
            
            with self.assertRaises(CityNotFoundError):
                get_adcode("NonExistentCity123456")
    
    def test_parse_weather_data_valid(self):
        mock_data = {
            "status": "1",
            "forecasts": [
                {
                    "city": "Beijing",
                    "province": "Beijing",
                    "reporttime": "2024-01-01 12:00:00",
                    "casts": [
                        {
                            "date": "2024-01-01",
                            "week": "1",
                            "dayweather": "Sunny",
                            "nightweather": "Cloudy",
                            "daytemp": "10",
                            "nighttemp": "-2",
                            "daywind": "North",
                            "nightwind": "Northwest",
                            "daypower": "3",
                            "nightpower": "2"
                        }
                    ]
                }
            ]
        }
        
        result = parse_weather_data(mock_data)
        self.assertEqual(result["city"], "Beijing")
        self.assertEqual(result["province"], "Beijing")
        self.assertEqual(len(result["forecasts"]), 1)
        self.assertEqual(result["forecasts"][0]["day_temp"], "10")
    
    def test_parse_weather_data_7_days(self):
        """Test that parser correctly handles 7-day forecast data"""
        # Create mock data with 7 days
        casts = []
        for i in range(1, 8):
            casts.append({
                "date": f"2024-01-{i:02d}",
                "week": str(i),
                "dayweather": ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy", "Foggy", "Thunder"][i-1],
                "nightweather": ["Cloudy", "Rainy", "Snowy", "Windy", "Foggy", "Thunder", "Sunny"][i-1],
                "daytemp": str(10 + i),
                "nighttemp": str(i - 2),
                "daywind": "North",
                "nightwind": "South",
                "daypower": str(i),
                "nightpower": str(i + 1)
            })
        
        mock_data = {
            "status": "1",
            "forecasts": [
                {
                    "city": "Beijing",
                    "province": "Beijing",
                    "reporttime": "2024-01-01 12:00:00",
                    "casts": casts
                }
            ]
        }
        
        result = parse_weather_data(mock_data)
        self.assertEqual(result["city"], "Beijing")
        self.assertEqual(len(result["forecasts"]), 7)
        
        # Verify each day's data is correctly parsed
        for i in range(7):
            self.assertEqual(result["forecasts"][i]["date"], f"2024-01-{i+1:02d}")
            self.assertEqual(result["forecasts"][i]["week"], str(i + 1))
    
    def test_format_weather_display_7_days(self):
        """Test that display formatter correctly shows all 7 days"""
        forecasts = []
        for i in range(1, 8):
            forecasts.append({
                "date": f"2024-01-{i:02d}",
                "week": str(i),
                "day_weather": "Sunny",
                "night_weather": "Cloudy",
                "day_temp": str(10 + i),
                "night_temp": str(i),
                "day_wind": "North",
                "night_wind": "South",
                "day_power": "3",
                "night_power": "2"
            })
        
        mock_data = {
            "city": "Beijing",
            "province": "Beijing",
            "report_time": "2024-01-01 12:00:00",
            "forecasts": forecasts
        }
        
        display = format_weather_display(mock_data)
        
        # Check that all 7 days are present in the output
        for i in range(1, 8):
            self.assertIn(f"[Day {i}]", display)
            self.assertIn(f"2024-01-{i:02d}", display)
    
    def test_parse_weather_data_invalid(self):
        with self.assertRaises(WeatherAPIError):
            parse_weather_data({})
        
        with self.assertRaises(WeatherAPIError):
            parse_weather_data({"status": "1", "forecasts": []})
    
    def test_format_weather_display(self):
        mock_data = {
            "city": "Beijing",
            "province": "Beijing",
            "report_time": "2024-01-01 12:00:00",
            "forecasts": [
                {
                    "date": "2024-01-01",
                    "week": "1",
                    "day_weather": "Sunny",
                    "night_weather": "Cloudy",
                    "day_temp": "10",
                    "night_temp": "-2",
                    "day_wind": "North",
                    "night_wind": "Northwest",
                    "day_power": "3",
                    "night_power": "2"
                }
            ]
        }
        
        display = format_weather_display(mock_data)
        self.assertIn("Beijing", display)
        self.assertIn("2024-01-01", display)
        self.assertIn("Sunny", display)
    
    @patch('weather_api.requests.get')
    def test_get_weather_forecast_network_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")
        
        with patch('weather_api.get_adcode') as mock_adcode:
            mock_adcode.return_value = "110000"
            
            with self.assertRaises(NetworkError):
                get_weather_forecast("Beijing")
    
    @patch('weather_api.requests.get')
    def test_get_weather_forecast_api_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "0",
            "infocode": "10001",
            "info": "Invalid key"
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with patch('weather_api.get_adcode') as mock_adcode:
            mock_adcode.return_value = "110000"
            
            with self.assertRaises(InvalidAPIKeyError):
                get_weather_forecast("Beijing")
    
    @patch('weather_api.requests.get')
    def test_get_weather_forecast_rate_limit(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "0",
            "infocode": "10003",
            "info": "Rate limit"
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with patch('weather_api.get_adcode') as mock_adcode:
            mock_adcode.return_value = "110000"
            
            with self.assertRaises(APIRateLimitError):
                get_weather_forecast("Beijing")
    
    @patch('weather_api.get_adcode')
    @patch('weather_api.requests.get')
    def test_get_weather_forecast_success(self, mock_get, mock_adcode):
        mock_adcode.return_value = "110000"
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "1",
            "count": "1",
            "info": "OK",
            "infocode": "10000",
            "forecasts": [
                {
                    "city": "Beijing",
                    "adcode": "110000",
                    "province": "Beijing",
                    "reporttime": "2024-01-01 12:00:00",
                    "casts": [
                        {
                            "date": "2024-01-01",
                            "week": "1",
                            "dayweather": "Sunny",
                            "nightweather": "Cloudy",
                            "daytemp": "10",
                            "nighttemp": "-2",
                            "daywind": "North",
                            "nightwind": "Northwest",
                            "daypower": "3",
                            "nightpower": "2"
                        }
                    ]
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_weather_forecast("Beijing")
        self.assertEqual(result["status"], "1")


class TestInputValidation(unittest.TestCase):
    
    def test_empty_input(self):
        from cli import validate_city_input
        self.assertFalse(validate_city_input(""))
        self.assertFalse(validate_city_input("   "))
    
    def test_too_long_input(self):
        from cli import validate_city_input
        self.assertFalse(validate_city_input("a" * 60))
    
    def test_valid_input(self):
        from cli import validate_city_input
        self.assertTrue(validate_city_input("Beijing"))
        self.assertTrue(validate_city_input("Shanghai"))


def run_integration_tests():
    print("\n" + "=" * 60)
    print("Integration Tests")
    print("=" * 60)
    
    test_cities = ["Beijing", "Shanghai", "Guangzhou"]
    
    for city in test_cities:
        try:
            print("\nTesting city: " + city)
            raw_data = get_weather_forecast(city)
            weather_data = parse_weather_data(raw_data)
            print("Query successful - " + weather_data["province"] + " " + weather_data["city"])
            print("  Forecast days: " + str(len(weather_data["forecasts"])))
            print("  Report time: " + weather_data["report_time"])
        except Exception as e:
            print("Query failed: " + str(e))


if __name__ == "__main__":
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n\nRun integration tests? (requires network connection) [y/N]: ", end="")
    try:
        choice = input().strip().lower()
        if choice == 'y' or choice == 'yes':
            run_integration_tests()
    except KeyboardInterrupt:
        print("\n\nSkipping integration tests")
