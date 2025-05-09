import re
from enum import Enum
from projekt.src.bank_account import BankAccount,AccountStatus


class UserRole(Enum):
    """Enum representing user roles in the banking system."""

    ADMIN = 'admin'
    USER = 'user'

class User:

    def __init__(self,id, name, last_name, email,password, phone, role = UserRole.USER):

        """Class representing a user in Banking system.

            Args:
                id (int): id of the user
                name (str): name of the user
                last_name (str): last name of the user
                email (str): email of the user
                password (str): password of the user
                phone (str): phone number of the user
                role (UserRole): role of the user  | default = UserRole.USER

            Raises:
                TypeError: if id is not an integer
                TypeError: if role is not UserRole
        """

        if not isinstance(id, int):
            raise TypeError("id must be an integer")

        if not isinstance(role, UserRole):
            raise TypeError("role must be an instance of UserRole enum")

        self.id = id
        self.name = self._validate_name(name)
        self.last_name = self._validate_lastname(last_name)
        self.email = self._validate_email(email)
        self.password = self._validate_password(password)
        self.phone = self._validate_phone(phone)
        self.role = role
        self.bank_accounts = {}

    #Methods available for basic user
    def open_bank_account(self, bank, pin_code, balance=0):
        for account in self.bank_accounts.values():
            if account.bank == bank:
                if account.status == AccountStatus.ACTIVE or account.status == AccountStatus.INACTIVE:
                    raise ValueError("You already have an active or inactive account in this bank.")
                elif account.status == AccountStatus.LOCKED:
                    raise ValueError("You have a locked account in this bank. Please unlock it first.")

        if self.id not in bank.users:
            bank.users[self.id] = self

        bank_account = BankAccount(balance=balance, owner=self, bank=bank, pin_code=pin_code)

        self.bank_accounts[bank_account.account_number] = bank_account

        return True

    def close_bank_account(self, account_number, pin_code,auth):

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        account = self.bank_accounts.get(account_number)
        if not account:
            raise ValueError("Account not found.")
        return account.close(pin_code)

    def get_total_balance(self,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        balances = {}

        for account in self.bank_accounts.values():
            currency = account.currency.upper()
            balances[currency] = balances.get(currency, 0) + account.balance

        return {currency: round(balance, 2) for currency, balance in balances.items()}

    def get_balance(self, account_number,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return f"{bank_account.balance} {bank_account.currency}"

    def change_pin(self, account_number, old_pin, new_pin,auth):

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        bank_account.change_pin(old_pin, new_pin)


    def withdraw(self, amount,account_number,pin_code,auth):

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        bank_account.withdraw(amount,pin_code)

    def deposit(self,amount,account_number,pin_code,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        bank_account.deposit(amount,pin_code)

    def transfer(self, amount, from_account_number,to_account_number,pin_code,bank,auth):

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(from_account_number)
        if not bank_account:
            raise ValueError("Account not found.")

        bank_account.transfer(amount, to_account_number,pin_code,bank)

    def get_transactions(self,account_number,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.get_transactions()

    def get_latest_transaction(self,account_number,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.get_latest_transaction()

    def get_transactions_by_date(self,account_number,date_from,date_to,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.get_transactions_by_date(date_from,date_to)

    def unlock_account(self,account_number,pin_code,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.unlock_account(pin_code)

    def calculate_intrest(self,days,account_number,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.calculate_intrest(days)

    def change_currency(self,account_number,currency,auth,pin_code):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        bank_account.change_currency(currency,pin_code)

    def change_pin_code(self,account_number,pin_code,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        bank_account.change_pin_code(pin_code)

    #Methods available for admin
    def get_user(self,user_id,bank,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        if not auth.is_admin(self):
            raise PermissionError('U have not permission to perform this action')

        return bank.get_user(user_id,self)

    def get_users(self,bank,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        if not auth.is_admin(self):
            raise PermissionError('U have not permission to perform this action')

        return bank.get_all_users(self)

    def update_currencies(self,bank,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        if not auth.is_admin(self):
            raise PermissionError('U have not permission to perform this action')
        return bank.update_currencies(self)

    def get_accounts_by_status(self, status,auth):
        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        if not auth.is_admin(self):
            raise PermissionError('U have not permission to perform this action')

        return [bank_account for bank_account in self.bank_accounts.values() if bank_account.status  == status]

    def _validate_email(self, email):

        """Validate email format

            Args:
                email (str): email to validate

            Raises:
                ValueError: if the email is invalid
                TypeError: if the email is not a string

            Returns:
                str: validated email
        """
        if not isinstance(email, str):
            raise TypeError("email must be a string")

        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

        if valid:
            return email

        raise ValueError('Invalid email')

    def _validate_phone(self, phone):

        """Validate phone format

            Args:
                phone (str): phone number to validate

            Raises:
                ValueError: if the phone is invalid
                TypeError: if the phone is not a string

            Returns:
                str: validated phone
        """

        if not isinstance(phone, str):
            raise TypeError("phone must be a string")

        if not re.fullmatch(r'\d{9}', phone):
            raise ValueError("Phone must consist of exactly 9 digits")

        if phone[0] not in '45678':
            raise ValueError('Invalid phone number')

        phone = f"+48 {phone[:3]}-{phone[3:6]}-{phone[6:]}"

        return phone

    def _validate_name(self, name) :
        """Validate name format

            Args:
                name (str): name to validate

            Raises:
                ValueError: if the name contains invalid characters
                TypeError: if the name is not a string

            Returns:
                str: validated name
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\'-]+$', name):
            raise ValueError("Name contains invalid characters")

        if len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")

        return name.strip().title()

    def _validate_lastname(self, lastname):
        """Validate lastname format

            Args:
                lastname (str): lastname to validate

            Raises:
                ValueError: if the name contains invalid characters
                TypeError: if the name is not a string

            Returns:
                str: validated name
        """
        if not isinstance(lastname, str):
            raise TypeError("name must be a string")

        if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\'-]+$', lastname):
            raise ValueError("Lastname contains invalid characters")

        if len(lastname.strip()) == 0:
            raise ValueError("Lastname cannot be empty")

        return lastname.strip().title()

    def _validate_password(self, password: str) -> str:
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        if not re.fullmatch(pattern, password):
            raise ValueError(
                "Password must be at least 8 characters and contain an uppercase letter, lowercase letter, number, and special character.")
        return password











