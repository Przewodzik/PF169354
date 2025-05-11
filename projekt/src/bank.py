from datetime import datetime
import requests
from collections import defaultdict


class Bank:
    """Class representing a bank in Banking System."""

    def __init__(self, name, bank_code):
        """Initializes a new Bank instance.

        Args:
            name (str): name of the bank
            bank_code (str): bank code
        """

        self.name = name
        self.bank_code = bank_code
        self.accounts = {}
        self.users = {}
        self.transactions = defaultdict(list)
        self.currencies = self._fetch_currencies()
        self.created_at = datetime.now()

    def get_user(self, user_id):
        """Returns a user by their unique ID.

        Args:
            user_id (int): Unique identifier of the user.

        Raises:
            ValueError: If the user is not found.

        Returns:
            User: The requested user object.
        """

        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found.")

        return self.users[user_id]

    def get_users(self):
        """Returns all registered users.

        Returns:
            ValuesView[User]: A view of all user objects.
        """

        return self.users.values()

    def add_user(self, user):
        """Adds a new user to the system.

        Args:
            user (User): The user object to be added.
        """

        self.users[user.id] = user

    def _fetch_currencies(self):
        """Fetches current exchange rates from the NBP API.

        Raises:
            Exception: If the API request fails with a non-200 status code.

        Returns:
            dict[str, float]: A dictionary mapping currency codes to their rates.
        """

        url = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.status_code)

        exchange_rates = {
            rate["code"]: rate["mid"] for rate in response.json()[0]["rates"]
        }

        exchange_rates["PLN"] = 1.0

        return exchange_rates

    def update_currencies(self):
        """Updates the stored currency exchange rates.

        Returns:
            bool: True if the update was successful.
        """

        self.currencies = self._fetch_currencies()

        return True

    def add_new_transaction(self, transaction, account_number):
        """Adds a new transaction to the specified account.

        Args:
            transaction (dict): The transaction data.
            account_number (str): The account number to associate with the transaction.

        Returns:
            bool: True if the transaction was added successfully.
        """

        self.transactions[account_number].append(transaction)

        return True

    def get_transactions(self, account_number):
        """Retrieves all transactions for a given account.

        Args:
            account_number (str): The account number.

        Returns:
            list[dict]: A list of transactions for the account.
        """
        return self.transactions[account_number]

    def get_transactions_by_date(self, date_from, date_to, account_number):
        """Retrieves transactions within a date range for a specific account.

        Args:
            date_from (datetime): Start date of the range.
            date_to (datetime): End date of the range.
            account_number (str): The account number.

        Raises:
            TypeError: If the date arguments are not datetime objects.
            ValueError: If the start date is after the end date.

        Returns:
            list[dict]: A list of transactions within the specified date range.
        """

        if not isinstance(date_from, datetime) or not isinstance(date_to, datetime):
            raise TypeError("Dates must be datetime objects.")

        if date_from > date_to:
            raise ValueError("Start date must be before end date.")

        return [
            transaction
            for transaction in self.transactions[account_number]
            if date_from <= transaction["date"] <= date_to
        ]
