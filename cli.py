
import sys
from weather_api import (
    get_weather_forecast,
    parse_weather_data,
    format_weather_display,
    WeatherAPIError,
    NetworkError,
    APIRateLimitError,
    CityNotFoundError,
    InvalidAPIKeyError
)


def validate_city_input(city_name):
    if not city_name or not city_name.strip():
        print("Error: City name cannot be empty")
        return False
    
    if len(city_name.strip()) > 50:
        print("Error: City name too long")
        return False
    
    return True


def main():
    print("=" * 60)
    print("           Amap Weather Query System")
    print("=" * 60)
    print("Supports Chinese and English city names")
    print("Enter 'quit' or 'exit' to exit")
    print("=" * 60)
    print()
    
    while True:
        try:
            city_name = input("Enter city name: ").strip()
            
            if city_name.lower() in ["quit", "exit"]:
                print("Thank you for using, goodbye!")
                break
            
            if not validate_city_input(city_name):
                continue
            
            print("\nQuerying weather for " + city_name + "...\n")
            
            raw_data = get_weather_forecast(city_name)
            weather_data = parse_weather_data(raw_data)
            display_text = format_weather_display(weather_data)
            
            print(display_text)
            print()
            
        except CityNotFoundError as e:
            print("\nError: " + str(e))
            print("Hint: Please check if the city name is correct\n")
        except NetworkError as e:
            print("\nError: " + str(e))
            print("Hint: Please check your network connection\n")
        except APIRateLimitError as e:
            print("\nError: " + str(e))
            print("Hint: Please try again later\n")
        except InvalidAPIKeyError as e:
            print("\nError: " + str(e))
            print("Hint: Please check API Key configuration\n")
        except WeatherAPIError as e:
            print("\nError: " + str(e) + "\n")
        except KeyboardInterrupt:
            print("\n\nThank you for using, goodbye!")
            break
        except Exception as e:
            print("\nUnknown error: " + str(e) + "\n")


if __name__ == "__main__":
    main()
