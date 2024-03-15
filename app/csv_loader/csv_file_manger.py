import os
import csv
import shutil
import pandas as pd
import app.csv_loader.conversion_blueprint as cb

parent_dir = "csv_files"

# create dir "csv_files"
def check_and_create_file_dir():
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

def create_sub_folder_bank_account(id):
    if not os.path.exists(f"{parent_dir}/{id}"):
        os.makedirs(f"{parent_dir}/{id}")

def delete_sub_folder_bank_account(id):
    if os.path.exists(f"{parent_dir}/{id}"):
        shutil.rmtree(f"{parent_dir}/{id}", ignore_errors=False, onerror=None)

async def save_csv_file(file, id):
    with open(f"{parent_dir}/{id}/transactions.csv", 'wb') as f:
        content = await file.read()
        f.write(content)

async def save_dict_to_csv_file(data, id, file_name):
    with open(f"{parent_dir}/{id}/{file_name}.csv", 'w', newline='', encoding='utf-8') as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=data[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(data)

def construct_dtypes_and_extract_dates():
    dtypes = {column: "str" for column in cb.data_columns}
    # pop any entry that has the word date in it
    dates = []
    for column in cb.data_columns:
        if "date" in column:
            dates.append(dtypes.pop(column))
    return dtypes, dates

async def load_converted_csv_to_pandas(id):
    # construct dtypes from cb.data_columns, amount is float and the rest is string
    dtypes, dates = construct_dtypes_and_extract_dates()
    return pd.read_csv(f"{parent_dir}/{id}/converted.csv", delimiter=";", dtype=dtypes, parse_dates=dates)
