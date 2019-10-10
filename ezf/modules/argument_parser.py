import argparse

def argument_parser():
    parser = argparse.ArgumentParser(description='Arg parser')
    parser.add_argument("--forecast",
                        choices=["morning", "afternoon"],
                        required=True, type=str, help="Forecast time")

    args = parser.parse_args()
    forecastt = args.forecast
    return forecastt