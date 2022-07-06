import requests
import json
from config import keys

class ConvException(Exception):
    pass

class CurrencyConv:
    @staticmethod
    def conv(quote: str, base: str, amount: str):
        pass

        if quote == base:
            raise ConvException(f'Одинаковые валюты "{base}"')

        try:
            quote_ticker = keys[base]
        except KeyError:
            raise ConvException(f'Неверная валюта "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvException(f'Неверная валюта "{base}"')
        
        try:
            amount = float(amount)
        except ValueError:
            raise ConvException(f'Неверное количество валюты "{amount}"')

        quote_ticker, base_ticker = keys[quote], keys[base]

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=19ab88331e35d18256253602171f7eda')
        total = float(json.loads(r.content)['data'][f'{keys[quote]}{keys[base]}'])

        return total * amount