from fastapi import Request
from viewmodels.base_view_model import BaseViewModel
import app.sqlite_database as db


class SettingsViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.settings = db.get_settings()

    def upsert_settings(self, currency, api_key, gpt_api_model):
        db.update_or_insert_settings(currency, api_key, gpt_api_model)
        self.settings = db.get_settings()
        return self.settings

    def get_settings(self):
        self.settings = db.get_settings()
        return self.settings
