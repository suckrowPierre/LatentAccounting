from fastapi import Request
from viewmodels.base_view_model import BaseViewModel


class AccountsViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.accounts = ["Account1", "Account2", "Account3", "Account4"]