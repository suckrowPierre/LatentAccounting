from fastapi import Request
from viewmodels.base_view_model import BaseViewModel
import app.sqlite_database as db


class TransactionHistoryViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.transaction_history = db.get_transaction_history()

    def upsert_transaction(self, account_id, booking_date, value_date, description, amount, currency, enhanced_description=None, categories=None, embedding=None):
        db.upsert_transaction(account_id, booking_date, value_date, description, amount, currency, enhanced_description, categories, embedding)
        self.transaction_history = db.get_transaction_history()

    def upsert_transactions(self, transactions):
        for transaction in transactions:
            self.upsert_transaction(**transaction)

    def upsert_transaction_pd_df(self, pd_df):
        transactions = pd_df.to_dict('records')
        self.upsert_transactions(transactions)

    def get_transaction_history(self):
        self.transaction_history = db.get_transaction_history()
        return self.transaction_history
