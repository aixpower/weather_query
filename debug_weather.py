#!/usr/bin/env python3
"""Debug script to verify weather data retrieval"""

import sys
from weather_api import get_weather_forecast, parse_weather_data, format_weather_display

def main():
    try:
        # Test with Beijing
        city = "Beijing"
        print(f"Querying weather for: {city}")
        print("-" * 60)
        
        raw_data = get_weather_forecast(city)
        print(f"Raw data status: {raw_data.get('status')}")
        
        if 'forecasts' in raw_data and raw_data['forecasts']:
            forecast = raw_data['forecasts'][0]
            print(f"City: {forecast.get('city')}")
            print(f"Province: {forecast.get('province')}")
            print(f"Report time: {forecast.get('reporttime')}")
            
            casts = forecast.get('casts', [])
            print(f"\nNumber of forecast days (casts): {len(casts)}")
            print("-" * 60)
            
            for i, cast in enumerate(casts):
                print(f"Day {i+1}: {cast.get('date')} - {cast.get('dayweather')}/{cast.get('nightweather')}")
        
        print("\n" + "="*60)
        print("Parsed and formatted data:")
        print("="*60)
        
        weather_data = parse_weather_data(raw_data)
        print(f"\nNumber of days in parsed data: {len(weather_data['forecasts'])}")
        
        display = format_weather_display(weather_data)
        print("\n" + display)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
