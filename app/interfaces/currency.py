from datetime import date, datetime, time
from currency_converter import CurrencyConverter, ECB_URL

CONVERTER = CurrencyConverter(ECB_URL)


def get_conversion_datetime(date: date) -> datetime:
    # Define a time object for 13:00:00
    conversion_time = time(13, 0, 0)
    # Combine the date and time to get a datetime object
    return datetime.combine(date, conversion_time)

def convert_currency(amount, from_currency, to_currency, date, converter=CONVERTER):
    """
    Convert a given amount from one currency to another.

    :param date: The date of the conversion.
    :param amount: The amount of money to convert.
    :param from_currency: The currency to convert from.
    :param to_currency: The currency to convert to.
    :return: The converted amount.
    """
    date = get_conversion_datetime(date)

    if amount == 0 or from_currency == to_currency:
        return amount

    try:
        return converter.convert(amount, from_currency, to_currency, date=date)
    except Exception as e:
        print(f"Error in currency conversion: {e}")
        raise e