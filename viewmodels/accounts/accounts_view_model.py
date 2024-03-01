from fastapi import Request
from viewmodels.base_view_model import BaseViewModel


class AccountsViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.accounts = [{"name": "Account1", "id": "1"}, {"name": "Account2", "id": "2"}, {"name": "Account3", "id": "3"}]