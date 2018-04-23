from forex_python.converter import CurrencyRates, RatesNotAvailableError
import csv


def convert(input_curr, output_curr, amount, currencies):
    """
    :param input_curr: input currency code
    :param output_curr: output currency code
    :param amount: amount to convert
    :param currencies: supported currency codes
    :return: dictionary for json output with converted currencies:
        {
        "input": {
            "amount": <float>,
            "currency": <3 letter currency code>
        }
        "output": {
            <3 letter currency code>: <float>
        }
    }
    """
    json_dict = {"input": {"amount": amount, "currency": input_curr}, "output": {}}
    if output_curr is None:
        json_dict["output"] = convert_to_all(input_curr, amount, currencies)
    else:
        json_dict["output"] = convert_to_one(input_curr, amount, output_curr)
    return json_dict


def get_currency_code(_input, currency_symbols):
    """
    if _input is currency symbol convert to currency code otherwise return _input
    :param _input: value to check
    :param currency_symbols: dictionary, key - currency symbol, value - currency code
    :return: currency code or _input value
    """
    code = currency_symbols.get(_input)
    if code is not None:
        return code
    else:
        return _input


def load_csv_file(csv_file):
    """
    convert csv file to dictionary, skip first line, expect csv file with 2 rows
    :param csv_file: path to file
    :return: dictionary , key - first row, value - second row
    """
    with open(csv_file, mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile)
        next(reader)
        return {rows[0]: rows[1] for rows in reader}


def convert_to_all(input_currency, amount, currencies):
    """
    convert amount of input_currency to all supported currencies
    :param input_currency: input currency code
    :param amount: amount of input currency
    :param currencies: list of supported currencies codes
    :return: dictionary, key - currency code, value - converted amount of input_currency
    {
        <3 letter output currency code>: <float>
        ...
    }
    """
    output_dict = {}
    c = CurrencyRates()
    for curr in currencies:
        if curr == input_currency:
            continue
        try:
            rate = c.get_rate(input_currency, curr)
        except RatesNotAvailableError:
            continue
        output_dict[curr] = round(amount * rate, 2)
    return output_dict


def convert_to_one(input_currency, amount, output_currency):
    """
    Convert amount of input currency to output currency
    :param input_currency: input currency code
    :param amount: amount of input currency
    :param output_currency: output currency code
    :return: if currency rate available returns:
    {
        <3 letter output currency code>: <float>
    }
    otherwise return error message
    """
    c = CurrencyRates()
    try:
        rate = c.get_rate(input_currency, output_currency)
        result = {output_currency: round(amount * rate, 2)}
    except RatesNotAvailableError:
        result = "Currency Rate {0} => {1} not available".format(input_currency, output_currency)
    return result
