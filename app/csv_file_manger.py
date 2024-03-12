import os
import shutil

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
