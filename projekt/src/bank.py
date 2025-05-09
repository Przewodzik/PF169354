from datetime import datetime
import requests
from collections import defaultdict

class Bank:

    def __init__(self,name,bank_code):

        self.name = name
        self.bank_code = bank_code
        self.accounts = {}
        self.users = {}
        self.transactions = defaultdict(list)
        self.currencies = self._fetch_currencies()
        self.created_at = datetime.now()


    def get_user(self,user_id):

        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found.")

        return self.users[user_id]

    def get_users(self):
        return self.users.values()


    def _fetch_currencies(self):

        url = 'https://api.nbp.pl/api/exchangerates/tables/A/?format=json'

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.status_code)

        exchange_rates = {
            rate['code']: rate['mid']
            for rate in response.json()[0]['rates']
        }

        exchange_rates['PLN'] = 1.0

        return exchange_rates

    def update_currencies(self):

        self.currencies = self._fetch_currencies()

    def add_new_transaction(self,transaction,account_number):

        self.transactions[account_number].append(transaction)

        return True

    def get_latest_transaction(self,account_number):
        return self.transactions[account_number][-1]

    def get_transactions(self,account_number):
        return self.transactions[account_number]

    def get_transactions_by_date(self,date_from,date_to,account_number):

        if not isinstance(date_from, datetime) or not isinstance(date_to, datetime):
            raise TypeError("Dates must be datetime objects.")

        if date_from > date_to:
            raise ValueError("Start date must be before end date.")

        return [
            transaction for transaction in self.transactions[account_number]
            if date_from <= transaction['date'] <= date_to
        ]


