from flask import Flask, request, abort
from currency_api import load_csv_file, get_currency_code, convert
import json

app = Flask(__name__)


@app.route('/currency_converter', methods=['GET'])
def get_convert_curr():
    # Parse arguments
    try:
        amount = float(request.args.get('amount'))
    except ValueError:
        return abort(400)
    input_currency = request.args.get('input_currency')
    output_currency = request.args.get('output_currency')

    # load currency info from csv files
    currency_dict = load_csv_file('currencies.csv')
    currency_symbols = load_csv_file('symbols.csv')

    # if argument is symbol convert to currency code
    input_currency = get_currency_code(input_currency, currency_symbols)
    output_currency = get_currency_code(output_currency, currency_symbols)

    # if arguments are not currency codes return bad request
    if currency_dict.get(input_currency) is None:
        return abort(400)
    if output_currency is not None and currency_dict.get(output_currency) is None:
        return abort(400)

    # convert and crate json
    json_output = convert(input_currency, output_currency, amount, currency_dict.keys())
    return json.dumps(json_output, sort_keys=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug="True")
