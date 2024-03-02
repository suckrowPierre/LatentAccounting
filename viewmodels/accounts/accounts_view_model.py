from fastapi import Request
from viewmodels.base_view_model import BaseViewModel
import app.database as db


class AccountsViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.accounts = db.get_accounts()

    def add_account(self, name, account_number):
        db_id = db.add_account(name, account_number)
        self.accounts = db.get_accounts()
        return db_id

    def update_account(self, account_id, name, account_number):
        update = db.update_account(account_id, name, account_number)
        self.accounts = db.get_accounts()
        return update

    def delete_account(self, account_id):
        delete = db.delete_account(account_id)
        self.accounts = db.get_accounts()
        return delete
