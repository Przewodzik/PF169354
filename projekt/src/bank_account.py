import random
from datetime import datetime
import re
from enum import Enum

from projekt.src.bank import Bank

class AccountStatus(Enum):

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    LOCKED = 'locked'
    CLOSED = 'closed'

class BankAccount:

    def __init__(self, owner, bank, pin_code, balance,currency='PLN'):
        from projekt.src.user import User

        try:
            balance = float(balance)
        except TypeError:
            raise TypeError('Bank account balance must be a number')

        if balance < 0:
            raise ValueError('Bank account balance must be a positive number')

        if not isinstance(owner, User):
            raise TypeError('Bank account owner must be a User')

        if not isinstance(bank, Bank):
            raise TypeError('Bank account bank must be a Bank')

        if not isinstance(currency, str):
            raise TypeError('Bank account currency must be a string')

        if not currency in bank.currencies:
            raise ValueError('Bank account currency must be a valid bank currency code')


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

    def __str__(self):
        return f"Konto {self.account_number}: {self.balance} {self.currency}"

    def close(self, pin_code):

        self._validate_access(pin_code)

        self.failedWithdrawCount = 0

        if self.balance != 0:
            raise ValueError("Balance must be withdrawn before closing the account.")

        if self.status != AccountStatus.ACTIVE:
            raise PermissionError("Bank account status must be ACTIVE.")

        self.status = AccountStatus.CLOSED
        return True

    def withdraw(self, amount,pin_code):

        self._validate_access(pin_code)

        if amount <= 0:
            raise ValueError('Amount cannot be negative or equal zero.')

        if amount > self.balance:
            raise ValueError('Amount cannot be greater than the balance.')

        self.balance -= amount
        self.failedWithdrawCount = 0

        self.last_transaction_date = datetime.now()

        transaction = {
            'type': 'withdraw',
            'amount': amount,
            'date': self.last_transaction_date
        }
        return self.bank.add_new_transaction(transaction,self.account_number)


    def deposit(self, amount,pin_code):

        self._validate_access(pin_code)

        if amount <= 0:
            raise ValueError('Bank account amount cannot be negative or equal to zero.')

        self.balance += amount
        self.failedWithdrawCount = 0

        self.last_transaction_date = datetime.now()

        transaction  =  {
            'type': 'deposit',
            'amount': amount,
            'date': self.last_transaction_date
        }

        return self.bank.add_new_transaction(transaction,self.account_number)

    def transfer(self,amount,to_account_number,pin_code,bank):

        self._validate_access(pin_code)

        if amount <= 0:
            raise ValueError('Amount cannot be negative.')

        if amount > self.balance:
            raise ValueError('Bank account amount cannot be greater than the balance.')

        other_account  = bank.accounts.get(to_account_number)

        if not other_account:
            raise ValueError("Account not found.")

        if other_account.status != AccountStatus.ACTIVE:
            raise ValueError("Other account is  not active.")

        self.balance -= amount
        other_account.balance += amount
        self.failedWithdrawCount = 0

        self.last_transaction_date = datetime.now()

        other_account.last_transaction_date = datetime.now()
        other_transaction = {
            'type': 'incoming_transfer',
            'from': self.account_number,
            'amount': amount,
            'date': self.last_transaction_date
        }

        self.bank.add_new_transaction(other_transaction,other_account.account_number)

        transaction = {
            'type': 'transfer',
            'to': to_account_number,
            'bank': bank,
            'amount': amount,
            'date': self.last_transaction_date
        }
        return self.bank.add_new_transaction(transaction,self.account_number)


    def get_transactions(self):
        return self.bank.get_transactions(self.account_number)

    def get_latest_transaction(self):
        return self.bank.get_latest_transaction(self.account_number)

    def get_transactions_by_date(self, date_from, date_to):

        return self.bank.get_transactions_by_date(date_from, date_to,self.account_number)

    def unlock_account(self,pin_code):

        self._validate_access(pin_code)

        self.status = AccountStatus.ACTIVE

    def calculate_intrest(self, days):
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

    def change_currency(self, currency,pin_code):
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

        transaction  = {
            "type": "currency_change",
            "from": old_currency,
            "to": new_currency,
            "rate_from": old_rate,
            "rate_to": new_rate,
            "date": datetime.now()
        }

        return self.bank.add_new_transaction(transaction,self.account_number)

    def change_pin_code(self,old_pin_code,new_pin_code):

        self._validate_access(old_pin_code)

        self._validate_pin_code(new_pin_code)

        self.pin = new_pin_code

    def _generate_account_number(self):
        """Generate a pseudo-random 26-digit account number."""
        return self.bank.bank_code + ''.join(str(random.randint(0, 9)) for _ in range(22))

    def _validate_pin_code(self,pin_code):

        if not isinstance(pin_code, str):
            raise TypeError("pin code must be a string")

        if not re.fullmatch(r'\d{6}', pin_code):
            raise ValueError("Pin code to your account has to be exactly 6 digits")

        return pin_code

    def _validate_access(self,pin_code):

        if self.status != AccountStatus.ACTIVE:
            raise ValueError("Account is not active.")

        if self.failedWithdrawCount >= 3:
            self.status = AccountStatus.LOCKED
            raise PermissionError("Account locked due to too many failed PIN attempts.")

        if pin_code != self.pin:
            self.failedWithdrawCount += 1
            raise PermissionError("Incorrect PIN.")

