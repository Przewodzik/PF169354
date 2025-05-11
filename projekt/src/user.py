import re
from enum import Enum
from projekt.src.bank_account import BankAccount,AccountStatus


class UserRole(Enum):
    """Enum representing user roles in the banking system."""

    ADMIN = 'admin'
    USER = 'user'

class User:
    """Class representing a user in Banking System."""

    def __init__(self,id, name, last_name, email,password, phone, role = UserRole.USER):

        """Initializes a new UserAccount instance.

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
    def open_bank_account(self, bank, pin_code,currency = 'PLN',balance=0):

        """
          Opens a new bank account for the user in the specified bank.

          Args:
              bank (Bank): The bank where the account will be opened.
              pin_code (str): The PIN code for the new account.
              balance (float, optional): Initial balance of the account. Defaults to 0.
              currency (str, optional): Currency of the account.

          Raises:
              ValueError: If the user already has an active or inactive account in the bank.
              ValueError: If the user has a locked account in the bank and must unlock it first.

          Returns:
              bool: True if the account was successfully created.
          """

        for bank_account in self.bank_accounts.values():
            if bank_account.bank == bank:
                if bank_account.status == AccountStatus.ACTIVE or bank_account.status == AccountStatus.INACTIVE:
                    raise ValueError("You already have an active or inactive account in this bank.")
                elif bank_account.status == AccountStatus.LOCKED:
                    raise ValueError("You have a locked account in this bank. Please unlock it first.")

        try:
            bank.get_user(self.id)
        except ValueError:
            bank.add_user(self)

        bank_account = BankAccount(balance=balance, owner=self, bank=bank, pin_code=pin_code,currency=currency)

        self.bank_accounts[bank_account.account_number] = bank_account

        return True

    def close_bank_account(self, account_number, pin_code,auth):

        """
        Closes the specified bank account after verifying authentication and PIN.

        Args:
            account_number (str): The account number to be closed.
            pin_code (str): The PIN code for verifying account ownership.
            auth (AuthSystem): The authentication system used to verify if the user is logged in.

        Raises:
            PermissionError: If the user is not logged in.
            ValueError: If the account does not exist.

        Returns:
            bool: True if the account was successfully closed
        """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        account = self.bank_accounts.get(account_number)
        if not account:
            raise ValueError("Account not found.")
        return account.close(pin_code)

    def get_total_balance(self,auth):

        """
          Returns the total balance across all user bank accounts, grouped by currency.

          Args:
              auth (AuthSystem): The authentication system used to verify if the user is logged in.

          Raises:
              PermissionError: If the user is not logged in.

          Returns:
              dict: Total balance of the user's all bank accounts.
          """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        balances = {}

        for account in self.bank_accounts.values():
            currency = account.currency.upper()
            balances[currency] = balances.get(currency, 0) + account.balance

        return {currency: round(balance, 2) for currency, balance in balances.items()}

    def get_balance(self, account_number,auth):

        """
          Retrieves the balance and currency for a specific bank account.

          Args:
              account_number (str): The account number for which to retrieve the balance.
              auth (AuthSystem): The authentication system used to verify if the user is logged in.

          Raises:
              PermissionError: If the user is not logged in.
              ValueError: If the account does not exist.

          Returns:
              str: A string representing the balance and its currency
          """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return f"{bank_account.balance} {bank_account.currency}"

    def change_pin(self, account_number, old_pin, new_pin,auth):

        """
           Changes the PIN code for a specific bank account after authentication.

           Args:
               account_number (str): The account number for which to change the PIN.
               old_pin (str): The current PIN code used for verification.
               new_pin (str): The new PIN code to set.
               auth (AuthSystem): The authentication system used to verify if the user is logged in.

           Raises:
               PermissionError: If the user is not logged in.
               ValueError: If the account does not exist.
           """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")

        return bank_account.change_pin(old_pin, new_pin)


    def withdraw(self, amount,account_number,pin_code,auth):

        """
            Withdraws a specified amount of money from the user's bank account after authentication and PIN verification.

            Args:
                amount (float): The amount of money to withdraw.
                account_number (str): The account number from which to withdraw funds.
                pin_code (str): The PIN code used for verification.
                auth (AuthSystem): The authentication system used to verify if the user is logged in.

            Raises:
                PermissionError: If the user is not logged in.
                ValueError: If the account does not exist.
            """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.withdraw(amount,pin_code)

    def deposit(self,amount,account_number,pin_code,auth):

        """
          Deposits a specified amount of money into the user's bank account after authentication and PIN verification.

          Args:
              amount (float): The amount of money to deposit.
              account_number (str): The account number to which the funds will be deposited.
              pin_code (str): The PIN code used for verification.
              auth (AuthSystem): The authentication system used to verify if the user is logged in.

          Raises:
              PermissionError: If the user is not logged in.
              ValueError: If the account does not exist.
          """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")

        return bank_account.deposit(amount,pin_code)

    def transfer(self, amount, from_account_number,to_account_number,pin_code,bank,auth):

        """
          Transfers a specified amount of money from one of the user's bank accounts to another account.

          Args:
              amount (float): The amount of money to transfer.
              from_account_number (str): The account number from which the money will be transferred.
              to_account_number (str): The destination account number.
              pin_code (str): The PIN code used for verification.
              bank (Bank): The bank instance managing the destination account.
              auth (AuthSystem): The authentication system used to verify if the user is logged in.

          Raises:
              PermissionError: If the user is not logged in.
              ValueError: If the source account does not exist.
          """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(from_account_number)
        if not bank_account:
            raise ValueError("Account not found.")

        bank_account.transfer(amount, to_account_number,pin_code,bank)

    def get_transactions(self,account_number,auth):

        """
           Retrieves the transaction history for a specific bank account.

           Args:
               account_number (str): The account number for which to retrieve transactions.
               auth (AuthSystem): The authentication system used to verify if the user is logged in.

           Raises:
               PermissionError: If the user is not logged in.
               ValueError: If the account does not exist.

           Returns:
               list: A list of transactions associated with the specified account.
           """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.get_transactions()

    def get_transactions_by_date(self,account_number,date_from,date_to,auth):

        """
           Retrieves transactions for a specific bank account within a given date range.

           Args:
               account_number (str): The account number for which to retrieve transactions.
               date_from (str): The start date of the range
               date_to (str): The end date of the range
               auth (AuthSystem): The authentication system used to verify if the user is logged in.

           Raises:
               PermissionError: If the user is not logged in.
               ValueError: If the account does not exist.

           Returns:
               list: A list of transactions within the specified date range.
           """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.get_transactions_by_date(date_from,date_to)

    def unlock_account(self,account_number,pin_code,auth):

        """
           Unlocks a locked bank account after verifying the user's PIN code and authentication status.

           Args:
               account_number (str): The account number to be unlocked.
               pin_code (str): The PIN code used for verification.
               auth (AuthSystem): The authentication system used to verify if the user is logged in.

           Raises:
               PermissionError: If the user is not logged in.
               ValueError: If the account does not exist.

           Returns:
               bool: True if the account was successfully unlocked.
           """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.unlock_account(pin_code)


    def change_currency(self,account_number,currency,auth,pin_code):

        """
           Changes the currency of a specific bank account after verifying the user's authentication and PIN.

           Args:
               account_number (str): The account number for which to change the currency.
               currency (str): The target currency code
               auth (AuthSystem): The authentication system used to verify if the user is logged in.
               pin_code (str): The PIN code used for verification.

           Raises:
               PermissionError: If the user is not logged in.
               ValueError: If the account does not exist.
           """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        bank_account.change_currency(currency,pin_code)

    def calculate_intrest(self, days, account_number, auth):
        """
           Calculates the interest accrued on a specific bank account over a given number of days.

           Args:
               days (int): The number of days over which to calculate the interest.
               account_number (str): The account number for which to calculate interest.
               auth (AuthSystem): The authentication system used to verify if the user is logged in.

           Raises:
               PermissionError: If the user is not logged in.
               ValueError: If the account does not exist.

           Returns:
               float: The amount of interest calculated.
        """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')

        bank_account = self.bank_accounts.get(account_number)
        if not bank_account:
            raise ValueError("Account not found.")
        return bank_account.calculate_intrest(days)

    #Methods available for admin
    def get_user(self,user_id,bank,auth):

        """
           Retrieves information about a specific user from the bank. Only available to admins.

           Args:
               user_id (int): The ID of the user to retrieve.
               bank (Bank): The bank instance from which to fetch the user.
               auth (AuthSystem): The authentication system used to verify if the user is logged in and is an admin.

           Raises:
               PermissionError: If the user is not logged in.
               PermissionError: If the user does not have admin privileges.

           Returns:
               User: The user object corresponding to the given ID.
           """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        if not auth.is_admin(self):
            raise PermissionError('U have not permission to perform this action')

        return bank.get_user(user_id)

    def get_users(self,bank,auth):

        """
          Retrieves a list of all users from the bank. Only available to admins.

          Args:
              bank (Bank): The bank instance from which to fetch users.
              auth (AuthSystem): The authentication system used to verify if the user is logged in and is an admin.

          Raises:
              PermissionError: If the user is not logged in.
              PermissionError: If the user does not have admin privileges.

          Returns:
              list: A list of all users registered in the bank.
          """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        if not auth.is_admin(self):
            raise PermissionError('U have not permission to perform this action')

        return bank.get_users()


    def update_currencies(self,bank,auth):

        """
           Updates currency exchange rates in the bank system. Only available to admins.

           Args:
               bank (Bank): The bank instance for which to update currencies.
               auth (AuthSystem): The authentication system used to verify if the user is logged in and is an admin.

           Raises:
               PermissionError: If the user is not logged in.
               PermissionError: If the user does not have admin privileges.

           Returns:
               bool: True if the currency rates were successfully updated.
           """

        if not auth.is_logged_in(self):
            raise PermissionError('User not logged in')
        if not auth.is_admin(self):
            raise PermissionError('U have not permission to perform this action')
        return bank.update_currencies()

    def _validate_email(self, email):

        """
           Validates the user's email address to ensure it matches a standard email format.

           The email must follow the format: local_part@domain.extension

           Args:
               email (str): The user's email address.

           Raises:
               TypeError: If the email is not a string.
               ValueError: If the email does not match a valid format.

           Returns:
               str: The validated email address.
           """

        if not isinstance(email, str):
            raise TypeError("email must be a string")

        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

        if valid:
            return email

        raise ValueError('Invalid email')

    def _validate_phone(self, phone):

        """
           Validates the user's phone number to ensure it has the correct format and structure.

           The phone number must:
           - Be a string of exactly 9 digits
           - Start with one of the digits: 4, 5, 6, 7, or 8

           After validation, the phone number is formatted as: "+48 XXX-XXX-XXX".

           Args:
               phone (str): The user's phone number.

           Raises:
               TypeError: If the phone number is not a string.
               ValueError: If the phone number does not consist of exactly 9 digits or starts with an invalid digit.

           Returns:
               str: The validated and formatted phone number.
           """

        if not isinstance(phone, str):
            raise TypeError("phone must be a string")

        if not re.fullmatch(r'\d{9}', phone):
            raise ValueError("Phone must consist of exactly 9 digits")

        if phone[0] not in '45678':
            raise ValueError('Invalid phone number')

        phone = f"+48 {phone[:3]}-{phone[3:6]}-{phone[6:]}"

        return phone

    def _validate_name(self, name):

        """
           Validates the user's first name to ensure it is a non-empty string containing only valid characters.

           Allowed characters include:
           - Letters (including Polish characters)
           - Spaces, hyphens, and apostrophes

           Args:
               name (str): The user's first name.

           Raises:
               TypeError: If the name is not a string.
               ValueError: If the name contains invalid characters or is empty.

           Returns:
               str: The validated and formatted first name.
           """

        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\'-]+$', name):
            raise ValueError("Name contains invalid characters")

        if len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")

        return name.strip().title()

    def _validate_lastname(self, lastname):

        """
            Validates the user's last name to ensure it is a non-empty string containing only valid characters.

            Allowed characters include:
            - Letters (including Polish characters)
            - Spaces, hyphens, and apostrophes

            Args:
                lastname (str): The user's last name.

            Raises:
                TypeError: If the last name is not a string.
                ValueError: If the last name contains invalid characters or is empty.

            Returns:
                str: The validated and formatted last name.
            """

        if not isinstance(lastname, str):
            raise TypeError("name must be a string")

        if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\'-]+$', lastname):
            raise ValueError("Lastname contains invalid characters")

        if len(lastname.strip()) == 0:
            raise ValueError("Lastname cannot be empty")

        return lastname.strip().title()

    def _validate_password(self, password: str) -> str:

        """
            Validates the user's password to ensure it meets security requirements.

            The password must:
            - Be at least 8 characters long
            - Contain at least one uppercase letter
            - Contain at least one lowercase letter
            - Contain at least one digit
            - Contain at least one special character (e.g., #?!@$%^&*-)

            Args:
                password (str): The user's password.

            Raises:
                TypeError: If the password is not a string.
                ValueError: If the password does not meet the security requirements.

            Returns:
                str: The validated password.
            """

        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        if not re.fullmatch(pattern, password):
            raise ValueError(
                "Password must be at least 8 characters and contain an uppercase letter, lowercase letter, number, and special character.")
        return password











