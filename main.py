
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Amap Weather Query System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python main.py                    # Start GUI
  python main.py --cli              # Use CLI
  python main.py --city Beijing     # Query Beijing weather directly
        """
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Use command line interface"
    )
    parser.add_argument(
        "--city",
        type=str,
        help="Query weather for specified city directly"
    )
    args = parser.parse_args()
    
    if args.city:
        from weather_api import (
            get_weather_forecast,
            parse_weather_data,
            format_weather_display,
            WeatherAPIError
        )
        try:
            raw_data = get_weather_forecast(args.city)
            weather_data = parse_weather_data(raw_data)
            print(format_weather_display(weather_data))
        except WeatherAPIError as e:
            print("Error: " + str(e), file=sys.stderr)
            sys.exit(1)
    elif args.cli:
        import cli
        cli.main()
    else:
        try:
            import gui
            gui.main()
        except ImportError:
            print("Hint: tkinter not available, using CLI instead")
            import cli
            cli.main()


if __name__ == "__main__":
    main()
