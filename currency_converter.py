import argparse
import json
from currency_api import load_csv_file, get_currency_code, convert


def main():
    # Load currency info from csv files
    currency_dict = load_csv_file('currencies.csv')
    currency_symbols = load_csv_file('symbols.csv')
    currency_list = list(currency_dict.keys())
    accepted_input = currency_list + list(currency_symbols.keys())

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Currency converter.')
    parser.add_argument("--amount", type=float, required=True)
    parser.add_argument("--input_currency", choices=accepted_input, required=True)
    parser.add_argument("--output_currency", choices=accepted_input)
    args = parser.parse_args()

    # Check if inputs are symbols if so convert them to currency codes
    input_currency = get_currency_code(args.input_currency, currency_symbols)
    output_currency = get_currency_code(args.output_currency, currency_symbols)

    # Convert and print json
    json_output = convert(input_currency, output_currency, args.amount, currency_list)
    json_pretty = json.dumps(json_output, indent=4, sort_keys=True)
    print(json_pretty)


if __name__ == '__main__':
    main()
