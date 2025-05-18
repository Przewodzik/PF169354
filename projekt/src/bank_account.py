import random
from datetime import datetime
import re
from enum import Enum

from src.bank import Bank


class AccountStatus(Enum):

    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    CLOSED = "closed"


class BankAccount:

    def __init__(self, owner, bank, pin_code, balance=0, currency="PLN"):
        """Initializes a new BankAccount instance.

        Args:
            owner (User): The owner of the bank account.
            bank (Bank): The bank that holds the account.
            pin_code (str): The PIN code for accessing the account.
            balance (float, optional): Initial account balance. Must be non-negative. Defaults to 0.
            currency (str, optional): Currency code (e.g., 'PLN'). Must be supported by the bank. Defaults to 'PLN'.

        Raises:
            TypeError: If balance is not a number, owner is not a User, bank is not a Bank,
                       or currency is not a string.
            ValueError: If balance is negative or currency is not supported by the bank.
        """
        from src.user import User

        try:
            balance = float(balance)
        except ValueError:
            raise TypeError("Bank account balance must be a number")

        if balance < 0:
            raise ValueError("Bank account balance must be a positive number")

        if not isinstance(owner, User):
            raise TypeError("Bank account owner must be a User")

        if not isinstance(bank, Bank):
            raise TypeError("Bank account bank must be a Bank")

        if not isinstance(currency, str):
            raise TypeError("Bank account currency must be a string")

        if currency not in bank.currencies:
            raise ValueError("Bank account currency must be a valid bank currency code")

        self.balance = balance
        self.owner = owner
        self.bank = bank
        self.status = AccountStatus.ACTIVE
        self.pin = self._validate_pin_code(pin_code)
        self.last_transaction_date = None
        self.created_at = datetime.now()
        self.failedWithdrawCount = 0
        self.currency = currency.upper()
        self.account_number = self._generate_account_number()
        bank.accounts[self.account_number] = self

    def close(self, pin_code):
        """Closes the bank account after validating access and ensuring zero balance.

        Args:
            pin_code (str): The PIN code used to authorize the account closure.

        Raises:
            ValueError: If the account balance is not zero.

        Returns:
            bool: True if the account was successfully closed.
        """

        self._validate_access(pin_code)

        if self.balance != 0:
            raise ValueError("Balance must be withdrawn before closing the account.")

        self.status = AccountStatus.CLOSED
        return True

    def withdraw(self, amount, pin_code):

        self._validate_access(pin_code)

        try:
            amount = float(amount)
        except ValueError:
            raise TypeError("Bank account amount must be a number")

        if amount <= 0:
            raise ValueError("Amount cannot be negative or equal zero.")

        if amount > self.balance:
            raise ValueError("Amount cannot be greater than the balance.")

        self.balance -= amount

        self.last_transaction_date = datetime.now()

        transaction = {
            "type": "withdraw",
            "amount": amount,
            "date": self.last_transaction_date,
        }
        return self.bank.add_new_transaction(transaction, self.account_number)

    def deposit(self, amount, pin_code):
        """Withdraws funds from the bank account after validating access and amount.

        Args:
            amount (float): The amount of money to withdraw.
            pin_code (str): The PIN code used to authorize the withdrawal.

        Raises:
            TypeError: If the amount is not a number.
            ValueError: If the amount is less than or equal to zero, or greater than the current balance.

        Returns:
            bool: True if the transaction was successfully recorded.
        """

        self._validate_access(pin_code)

        try:
            amount = float(amount)
        except ValueError:
            raise TypeError("Bank account amount must be a number")

        if amount <= 0:
            raise ValueError("Bank account amount cannot be negative or equal to zero.")

        self.balance += amount

        self.last_transaction_date = datetime.now()

        transaction = {
            "type": "deposit",
            "amount": amount,
            "date": self.last_transaction_date,
        }

        return self.bank.add_new_transaction(transaction, self.account_number)

    def transfer(self, amount, to_account_number, pin_code, bank):
        """Transfers funds to another bank account, converting currency if needed.

        Args:
            amount (float): The amount to transfer.
            to_account_number (str): The recipient's account number.
            pin_code (str): The PIN code used to authorize the transfer.
            bank (Bank): The bank object managing the accounts and currency rates.

        Raises:
            TypeError: If the amount is not a number.
            ValueError: If the amount is less than or equal to zero, greater than the current balance,
                        the recipient account does not exist, or is not active.

        Returns:
            bool: True if the transfer was successfully recorded.
        """

        self._validate_access(pin_code)

        try:
            amount = float(amount)
        except ValueError:
            raise TypeError("Bank account amount must be a number")

        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero.")

        if amount > self.balance:
            raise ValueError("Bank account amount cannot be greater than the balance.")

        other_account = bank.accounts.get(to_account_number)

        if not other_account:
            raise ValueError("Account not found.")

        if other_account.status != AccountStatus.ACTIVE:
            raise ValueError("Other account is not active.")

        if other_account.currency != self.currency:
            source_rate = bank.currencies[self.currency]
            target_rate = bank.currencies[other_account.currency]

            amount_in_target_currency = round(amount * source_rate / target_rate, 2)

            self.balance -= amount
            other_account.balance += amount_in_target_currency
        else:
            self.balance -= round(amount, 2)
            other_account.balance += round(amount, 2)

        now = datetime.now()
        self.last_transaction_date = now
        other_account.last_transaction_date = now

        other_transaction = {
            "type": "incoming_transfer",
            "from": self.account_number,
            "amount": (
                amount
                if other_account.currency == self.currency
                else amount_in_target_currency
            ),
            "date": now,
        }

        bank.add_new_transaction(other_transaction, other_account.account_number)

        transaction = {
            "type": "transfer",
            "to": to_account_number,
            "bank": bank,
            "amount": amount,
            "date": now,
        }

        return bank.add_new_transaction(transaction, self.account_number)

    def get_transactions(self):
        """Retrieves all transactions associated with this bank account.

        Returns:
            list[dict]: A list of transaction records for this account.
        """

        return self.bank.get_transactions(self.account_number)

    def get_transactions_by_date(self, date_from, date_to):
        """Retrieves transactions for this account within a specified date range.

        Args:
            date_from (datetime): Start date of the range.
            date_to (datetime): End date of the range.

        Returns:
            list[dict]: A list of transactions within the given date range.
        """

        return self.bank.get_transactions_by_date(
            date_from, date_to, self.account_number
        )

    def unlock_account(self, pin_code):
        """Unlocks the bank account if the correct PIN is provided and the account is inactive or locked.

        Args:
            pin_code (str): The PIN code used to authorize unlocking.

        Raises:
            PermissionError: If the provided PIN is incorrect.
            ValueError: If the account status is neither INACTIVE nor LOCKED.

        Returns:
            bool: True if the account was successfully unlocked.
        """

        if pin_code != self.pin:
            raise PermissionError("Incorrect PIN.")

        if self.status not in [AccountStatus.INACTIVE, AccountStatus.LOCKED]:
            raise ValueError("Bank account status must be INACTIVE or LOCKED.")

        self.status = AccountStatus.ACTIVE

        return True

    def change_currency(self, currency, pin_code):
        """Changes the account's currency and converts the balance accordingly.

        Args:
            currency (str): The target currency code (e.g., 'USD', 'EUR').
            pin_code (str): The PIN code used to authorize the change.

        Raises:
            TypeError: If the currency is not a string.
            ValueError: If the currency is invalid, not supported by the bank,
                        or already set as the current account currency.

        Returns:
            bool: True if the currency change was successfully recorded.
        """

        self._validate_access(pin_code)

        if not isinstance(currency, str):
            raise TypeError("Currency must be a string.")

        new_currency = currency.upper()

        if new_currency not in self.bank.currencies:
            raise ValueError("Bank account currency must be a valid bank currency code")

        if new_currency == self.currency:
            raise ValueError("Account is already in this currency.")

        old_currency = self.currency
        old_rate = self.bank.currencies[old_currency]
        new_rate = self.bank.currencies[new_currency]

        self.balance = round(self.balance * old_rate / new_rate, 2)
        self.currency = new_currency

        transaction = {
            "type": "currency_change",
            "from": old_currency,
            "to": new_currency,
            "rate_from": old_rate,
            "rate_to": new_rate,
            "date": datetime.now(),
        }

        return self.bank.add_new_transaction(transaction, self.account_number)

    def change_pin(self, old_pin_code, new_pin_code):
        """Changes the account's PIN code after validating the old one.

        Args:
            old_pin_code (str): The current PIN code for authentication.
            new_pin_code (str): The new PIN code to be set.

        Raises:
            PermissionError: If the old PIN code is incorrect.
            ValueError: If the new PIN code is the same as the old one or invalid.

        Returns:
            bool: True if the PIN was successfully changed.
        """

        self._validate_access(old_pin_code)

        self._validate_pin_code(new_pin_code)

        if old_pin_code == new_pin_code:
            raise ValueError("Pin code cannot be the same as old pin code.")

        self.pin = new_pin_code

        return True

    def calculate_intrest(self, days):
        """Calculates the interest accrued over a given number of days.

        Interest is based on a tiered annual rate:
            - 1% for balances up to 1,000
            - 2% for balances up to 10,000
            - 3% for balances above 10,000

        Args:
            days (int): Number of days over which to calculate interest.

        Returns:
            float: The calculated interest, rounded to 2 decimal places.
        """

        if self.balance <= 0:
            return 0.0

        if self.balance <= 1000:
            annual_rate = 0.01
        elif self.balance <= 10000:
            annual_rate = 0.02
        else:
            annual_rate = 0.03

        interest = self.balance * annual_rate * (days / 365)
        return round(interest, 2)

    def _generate_account_number(self):
        """Generates a pseudo-random 26-digit account number.

        The number is composed of the bank's code followed by 22 random digits.

        Returns:
            str: A 26-digit bank account number.
        """

        return self.bank.bank_code + "".join(
            str(random.randint(0, 9)) for _ in range(22)
        )

    def _validate_pin_code(self, pin_code):
        """Validates the format of a PIN code.

        The PIN must be a string consisting of exactly 6 digits.

        Args:
            pin_code (str): The PIN code to validate.

        Raises:
            TypeError: If the PIN code is not a string.
            ValueError: If the PIN code does not consist of exactly 6 digits.

        Returns:
            str: The validated PIN code.
        """

        if not isinstance(pin_code, str):
            raise TypeError("pin code must be a string")

        if not re.fullmatch(r"\d{6}", pin_code):
            raise ValueError("Pin code to your account has to be exactly 6 digits")

        return pin_code

    def _validate_access(self, pin_code):
        """Validates access to the account using the provided PIN code.

        If the PIN is incorrect, the failed attempt counter increases. After 3 failed attempts,
        the account is locked. Access is also denied if the account is not active.

        Args:
            pin_code (str): The PIN code to authenticate access.

        Raises:
            PermissionError: If the PIN code is incorrect or the account is locked due to too many failed attempts.
            ValueError: If the account is not in an active state.
        """

        if self.failedWithdrawCount >= 3:
            self.status = AccountStatus.LOCKED
            raise PermissionError("Account locked due to too many failed PIN attempts.")

        if self.status != AccountStatus.ACTIVE:
            raise ValueError("Account is not active.")

        if pin_code != self.pin:
            self.failedWithdrawCount += 1
            raise PermissionError("Incorrect PIN.")

        if pin_code == self.pin:
            self.failedWithdrawCount = 0
