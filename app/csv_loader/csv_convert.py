import csv
import app.csv_loader.conversion_blueprint as cb


def apply_conversions(row, conversion_mapping):
    result = {}
    for output_column, func in conversion_mapping.items():
        # check if its function or string
        if isinstance(func, str):
            result[output_column] = func
        else:
            result[output_column] = func(row)
    return result


def convert_csv(input_csv_path, input_csv_separator, conversion_functions):
    with open(input_csv_path, newline='', encoding='utf-8-sig') as input_csv:
        reader = csv.DictReader(input_csv, delimiter=input_csv_separator)
        data = []
        for row in reader:
            blueprint = cb.ConversionBlueprint("EUR", conversion_functions)
            converted_row = apply_conversions(row, blueprint.row_entry())
            data.append(converted_row)
        return data
