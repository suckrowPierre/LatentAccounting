import os

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
        os.rmdir(f"{parent_dir}/{id}")
