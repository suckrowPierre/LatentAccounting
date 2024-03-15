import app.csv_loader.converters as converters

data_columns = ["booking_date", "value_date", "description", "amount", "currency"]


class ConversionBlueprint:
    def __init__(self, target_currency, function_map):
        self.target_currency = target_currency
        self.booking_date = function_map.get(data_columns[0], None)
        self.value_date = function_map.get(data_columns[1], None)
        self.description = function_map.get(data_columns[2], None)
        self.amount = function_map.get(data_columns[3], None)
        self.currency = function_map.get(data_columns[4], None)

    def row_entry(self):
        return {
            "booking_date": self.booking_date,
            "value_date": self.value_date,
            "description": self.description,
            "amount": lambda row: converters.convert_currency(self.amount(row), self.currency(row), self.target_currency, self.booking_date(row)),
            "currency": self.target_currency,
        }