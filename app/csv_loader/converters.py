import datetime
import app.interfaces.currency as currency
import calendar


def string_to_int(string) -> int:
    return int(string)


def string_to_float(string) -> float:
    return float(string.replace(",", "."))


def string_date_to_date_d_m_y(string):
    try:
        # First, attempt to parse the date normally.
        return datetime.datetime.strptime(string, '%d.%m.%Y').date()
    except ValueError as e:
        # If there's a ValueError, it might be because the day is out of range.
        if "day is out of range for month" in str(e):
            try:
                # Extract day, month, and year from the input string.
                day, month, year = map(int, string.split('.'))

                # Use calendar.monthrange to get the last day of the month.
                _, last_day = calendar.monthrange(year, month)

                # Calculate the difference if the input day is beyond the last day of the month.
                if day > last_day:
                    difference = day - last_day
                    # Construct a new date using the last day of the month.
                    corrected_date = datetime.date(year, month, last_day)
                    # If the difference goes beyond one month, adjust further (though for specific use-case, this might not be necessary).
                    return corrected_date - datetime.timedelta(days=difference - 1)
                return datetime.date(year, month, last_day)
            except ValueError as e:
                # Log any errors during the correction attempt.
                print(f"Corrected date error: {e}")
        # If it's not a day-out-of-range error or any correction attempt fails, log the original error.
        print(f"Error: {string} is not a valid date")
        raise e



def concatenate_strings(string1, string2):
    return string1 + " " + string2


def convert_currency(value, current_currency, target_currency, date, conversion_function=currency.convert_currency):
    try:
        return conversion_function(value, current_currency, target_currency, date=date)
    except ValueError:
        return None