import datetime

# Limits of the data

CURRENCIES = ['BAT', 'BTC', 'DASH', 'ETC', 'ETH', 'LTC', 'NEO', 'OMG', 'TRX', 'XRP', 'ZEC']
COUNTRIES = ["AUSTRALIA", "BRAZIL", "CANADA", "CHILE", "CHINA", "COLOMBIA", "FRANCE", "GERMANY", "GREECE", "INDIA", "IRELAND",
             "ITALY", "JAPAN", "KOREA", "NETHERLANDS", "RUSSIA", "SPAIN", "UK", "US"]
COUNTRY_CURRENCIES = ['DZD', 'AUD', 'BWP', 'BRL', 'BND', 'CAD', 'CLP', 'CNY', 'COP', 'CZK', 'DKK', 'EUR',
                      'INR', 'ILS', 'JPY', 'KRW', 'KWD', 'MYR', 'MUR', 'MXN', 'NZD', 'NOK', 'OMR', 'PEN',
                      'PHP', 'PLN', 'QAR', 'RUB', 'SAR', 'SGD', 'ZAR', 'SEK', 'CHF', 'THB', 'TTD', 'AED',
                      'GBP', 'USD', 'UYU']

MIN_DATE = datetime.date(2015, 10, 8)
DEFAULT_DATE = datetime.date(2019, 1, 1)
MAX_DATE = datetime.date(2021, 4, 6)