#!/usr/bin/env python3
"""Test script specifically for 7-day forecast functionality"""

import unittest
from unittest.mock import patch, MagicMock
from weather_api import parse_weather_data, format_weather_display

class Test7DayForecast(unittest.TestCase):
    
    def test_7day_data_parsing(self):
        """Test that parser handles and preserves all 7 days of data"""
        # Create mock data with EXACTLY 7 days
        casts = []
        for i in range(1, 8):
            casts.append({
                "date": f"2024-01-{i:02d}",
                "week": str(i),
                "dayweather": "Sunny",
                "nightweather": "Cloudy",
                "daytemp": str(15 + i),
                "nighttemp": str(5 + i),
                "daywind": "North",
                "nightwind": "South",
                "daypower": "3",
                "nightpower": "2"
            })
        
        mock_data = {
            "status": "1",
            "forecasts": [{
                "city": "Shanghai",
                "province": "Shanghai",
                "reporttime": "2024-01-01 12:00:00",
                "casts": casts
            }]
        }
        
        result = parse_weather_data(mock_data)
        self.assertEqual(len(result["forecasts"]), 7, "Should have exactly 7 days")
        
        # Verify each day
        for i in range(7):
            self.assertIsNotNone(result["forecasts"][i]["date"])
            self.assertIsNotNone(result["forecasts"][i]["day_weather"])
    
    def test_7day_display(self):
        """Test that display formatter shows all 7 days with proper labels"""
        forecasts = []
        for i in range(1, 8):
            forecasts.append({
                "date": f"2024-01-{i:02d}",
                "week": str(i),
                "day_weather": "Sunny",
                "night_weather": "Cloudy",
                "day_temp": "20",
                "night_temp": "10",
                "day_wind": "North",
                "night_wind": "South",
                "day_power": "3",
                "night_power": "2"
            })
        
        data = {
            "city": "Beijing",
            "province": "Beijing",
            "report_time": "2024-01-01 12:00:00",
            "forecasts": forecasts
        }
        
        display = format_weather_display(data)
        
        # Check all days are present in output
        self.assertIn("Total Days: 7", display)
        
        for day_num in range(1, 8):
            self.assertIn(f"[Day {day_num}]", display)
            self.assertIn(f"2024-01-{day_num:02d}", display)

if __name__ == "__main__":
    unittest.main(verbosity=2)
