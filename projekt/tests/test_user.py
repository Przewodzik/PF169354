import unittest
from unittest.mock import patch

from projekt.src.auth import Auth
from projekt.src.user import User,UserRole
from projekt.src.bank import Bank
from projekt.src.bank_account import AccountStatus

# noinspection PyTypeChecker
class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    @patch('projekt.src.bank.Bank._fetch_currencies')
    def setUp(self,mock_fetch,mock_account_number):
        """Set up test fixtures."""
        mock_fetch.return_value = {
            'PLN': 1.0,
            'USD': 3.7642,
            'EUR': 4.2757,
            'GBP': 5.0205,
            'CHF': 4.5595
        }
        mock_account_number.return_value = '123456789'

        self.auth = Auth()

        self.user = User(
            id=1,
            name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='Password123!',
            phone='781234567'
        )

        self.bank = Bank(
            name = 'PKO BP',
            bank_code = '1120'
        )
        self.bank2  = Bank(
            name = 'ING Bank Śląski',
            bank_code = '1150'
        )

        self.admin = User(
            id=2,
            name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='Password123!',
            phone='781234567',
            role=UserRole.ADMIN
        )

        self.user.open_bank_account(bank=self.bank, pin_code='123456', balance=1000)

    def test_user_initialization_success(self):
        """Test that a user can be created with valid attributes."""

        user = User(
            id=2,
            name='John',
            last_name='Doe',
            email='example@gmail.com',
            password='Password123!',
            phone='523456789'
        )

        self.assertEqual(user.id, 2)
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'example@gmail.com')
        self.assertEqual(user.password, 'Password123!')
        self.assertEqual(user.phone, '+48 523-456-789')
        self.assertEqual(user.role,UserRole.USER)
        self.assertEqual(user.bank_accounts,{})

    def test_user_initialization_failure(self):
        """Test that a user cannot be created with invalid attributes."""

        with self.assertRaises(TypeError):
            User(
                id='1',
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )

        with self.assertRaises(TypeError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
                role='admin',
            )

    def test_validate_name_success(self):
        """Test that a user can be created with valid names"""

        valid_names = [
            ('John','John'),
            ('Żaneta','Żaneta'),
            ('martha','Martha'),
            ('don-Beck','Don-Beck'),
            ('   john','John'),
        ]

        for name,expected_name in valid_names:
            with self.subTest(name=name):
                self.assertEqual(self.user._validate_name(name), expected_name)

    def test_validate_name_failure(self):
        """Test that a user cannot be created with invalid names"""

        invalid_types = [1,[],{},4.2]
        invalid_names = [
            'John!',
            'John42',
            '',
            ' '
        ]

        for invalid_type in invalid_types:
            with self.subTest(name=invalid_type):
                with self.assertRaises(TypeError):
                    self.user._validate_name(invalid_type)

        for invalid_name in invalid_names:
            with self.subTest(name=invalid_name):
                with self.assertRaises(ValueError):
                    self.user._validate_name(invalid_name)

    def test_validate_lastname_success(self):
        """Test that a user can be created with valid last names"""

        valid_lastnames = [
            ('Doe','Doe'),
            ('Żak','Żak'),
            ('kowalski','Kowalski'),
            ('   kowalski','Kowalski'),
        ]

        for valid_lastname,expected_lastname in valid_lastnames:
            with self.subTest(lastname=valid_lastname):
                self.assertEqual(self.user._validate_lastname(valid_lastname), expected_lastname)

    def test_validate_lastname_failure(self):
        """Test that a user cannot be created with invalid last names"""

        invalid_types = [1,[],{},4.2]
        invalid_lastnames = [
            'Doe!',
            'Doe42',
            '',
            ' ',
        ]

        for invalid_type in invalid_types:
            with self.subTest(lastname=invalid_type):
                with self.assertRaises(TypeError):
                    self.user._validate_lastname(invalid_type)

        for invalid_lastname in invalid_lastnames:
            with self.subTest(lastname=invalid_lastname):
                with self.assertRaises(ValueError):
                    self.user._validate_lastname(invalid_lastname)

    def test_validate_email_success(self):
        """Test that a user can be created with valid emails"""

        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user@sub.example.com"
        ]
        for valid_email in valid_emails:
            with self.subTest(email=valid_email):
                self.assertEqual(self.user._validate_email(valid_email), valid_email)

    def test_validate_email_failure(self):
        """Test that a user cannot be created with invalid emails"""

        invalid_types = [1,[],{},4.2]
        invalid_emails = [
            '@gmail.com',
            'example@gmail',
            'examplegmail.com',
            '',
            'user<>@example.com',
            'user@exa mple.com',
        ]

        for invalid_type in invalid_types:
            with self.subTest(email=invalid_type):
                with self.assertRaises(TypeError):
                    self.user._validate_email(invalid_type)

        for invalid_email in invalid_emails:
            with self.subTest(email=invalid_email):
                with self.assertRaises(ValueError):
                    self.user._validate_email(invalid_email)

    def test_validate_password_success(self):
        """Test that a user can be created with valid passwords"""

        valid_passwords = [
            "Password123!",
            "Qwerty#2024",
            "Test@1234",
            "Secure*Pass1",
            "Aa1$aaaa"
        ]

        for valid_password in valid_passwords:
            with self.subTest(password=valid_password):
                self.assertEqual(self.user._validate_password(valid_password), valid_password)

    def test_validate_password_failure(self):
        """Test that a user cannot be created with invalid passwords"""

        invalid_types = [1,[],{},4.2]
        invalid_passwords = [
            'pass',
            'password123!',
            'Password123',
            'Password!',
            '<PASSWORD>',
        ]

        for invalid_type in invalid_types:
            with self.subTest(password=invalid_type):
                with self.assertRaises(TypeError):
                    self.user._validate_password(invalid_type)

        for invalid_password in invalid_passwords:
            with self.subTest(password=invalid_password):
                with self.assertRaises(ValueError):
                    self.user._validate_password(invalid_password)

    def test_validate_phone_success(self):
        """Test that user can be created with valid phone numbers"""

        valid_phones = [
            ('523456789', '+48 523-456-789'),
            ('612345678', '+48 612-345-678'),
            ('789654123', '+48 789-654-123'),
            ('456789321', '+48 456-789-321'),
        ]

        for valid_phone,expected_phone in valid_phones:
            with self.subTest(phone=valid_phone):
                self.assertEqual(self.user._validate_phone(valid_phone), expected_phone)

    def test_validate_phone_failure(self):
        """Test that user cannot be created with invalid phone numbers"""

        invalid_types = [1,[],{},4.2]
        invalid_phones = [
            '52345678',
            '5234567899',
            '123456789',
            '',
        ]

        for invalid_type in invalid_types:
            with self.subTest(phone=invalid_type):
                with self.assertRaises(TypeError):
                    self.user._validate_phone(invalid_type)

        for invalid_phone in invalid_phones:
            with self.subTest(phone=invalid_phone):
                with self.assertRaises(ValueError):
                    self.user._validate_phone(invalid_phone)

    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_open_bank_account_success(self, mock_account_number):
        """Test that a bank account is correctly opened by the user."""

        mock_account_number.return_value = '987654321'
        result = self.user.open_bank_account(bank=self.bank2, pin_code='123456', balance=1000)

        self.assertTrue(result)
        self.assertIn('987654321', self.user.bank_accounts)
        self.assertEqual(len(self.user.bank_accounts), 2)

        bank_account = self.user.bank_accounts['987654321']
        self.assertEqual(bank_account.balance, 1000)
        self.assertEqual(bank_account.owner, self.user)
        self.assertEqual(bank_account.bank, self.bank2)


    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_open_bank_account_multiple_accounts(self, mock_account_number):
        """Test that a multiple bank accounts are correctly opened by the user."""

        mock_account_number.return_value = '987654321'

        self.user.open_bank_account(bank=self.bank2, pin_code='654321', balance=2000)

        self.assertEqual(len(self.user.bank_accounts),2)
        self.assertIn('123456789', self.user.bank_accounts)
        self.assertIn('987654321', self.user.bank_accounts)

        bank_account = self.user.bank_accounts['123456789']
        bank_account2 = self.user.bank_accounts['987654321']

        self.assertEqual(bank_account.balance, 1000)
        self.assertEqual(bank_account.owner, self.user)
        self.assertEqual(bank_account.bank, self.bank)

        self.assertEqual(bank_account2.balance, 2000)
        self.assertEqual(bank_account2.owner, self.user)
        self.assertEqual(bank_account2.bank, self.bank2)

    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_open_bank_account_in_the_same_bank(self, mock_account_number):
        """Test that user can't open more than one bank account in the same bank."""

        mock_account_number.return_value = '987654321'

        with self.assertRaises(ValueError):
            self.user.open_bank_account(bank=self.bank, pin_code='654321', balance=2000)

        bank_account = self.user.bank_accounts['123456789']
        bank_account.status = AccountStatus.INACTIVE

        with self.assertRaises(ValueError):
            self.user.open_bank_account(bank=self.bank, pin_code='654321', balance=2000)

        bank_account.status = AccountStatus.LOCKED

        with self.assertRaises(ValueError):
            self.user.open_bank_account(bank=self.bank, pin_code='654321', balance=2000)


    def test_close_bank_account_success(self):
        """Test that user can successfully close a bank account."""

        self.auth.login(user=self.user,email=self.user.email, password=self.user.password)

        self.user.withdraw(account_number='123456789', pin_code='123456', amount=1000, auth=self.auth)

        result = self.user.close_bank_account(account_number='123456789',pin_code='123456',auth=self.auth)
        bank_account = self.user.bank_accounts['123456789']
        self.assertEqual(bank_account.status, AccountStatus.CLOSED)
        self.assertTrue(result)


    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_get_total_balance_different_currency(self,mock_account_number):
        """Test that user can get total balance from all his accounts when accounts have diffrent currencies."""

        mock_account_number.return_value = '987654321'

        self.user.open_bank_account(bank=self.bank2, pin_code='654321',balance=500,currency='EUR')

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        result = self.user.get_total_balance(auth=self.auth)


        self.assertIn('PLN', result)
        self.assertIn('EUR', result)
        self.assertEqual(result['PLN'],1000)
        self.assertEqual(result['EUR'],500)

    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_get_total_balance_same_currency(self,mock_account_number):
        """Test that user can get total balance from all his accounts when accounts have same currencies."""

        mock_account_number.return_value = '987654321'

        self.user.open_bank_account(bank=self.bank2, pin_code='654321',balance=500)

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        result = self.user.get_total_balance(auth=self.auth)

        self.assertIn('PLN', result)
        self.assertEqual(result['PLN'],1500.0)


    def test_get_balance_success(self):
        """Test that user can get balance from a bank account."""

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        result = self.user.get_balance(auth=self.auth,account_number='123456789')

        self.assertEqual('1000.0 PLN',result)


    def test_change_pin_success(self):
        """Test that user can change pin from a bank account."""

        bank_account = self.user.bank_accounts['123456789']

        self.assertEqual(bank_account.pin,'123456')

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)
        result = self.user.change_pin(account_number='123456789',old_pin='123456',new_pin='654321',auth=self.auth)

        self.assertTrue(result)
        self.assertEqual(bank_account.pin,'654321')


    def test_withdraw_success(self):
        """Test that user can withdraw from a bank account."""

        bank_account = self.user.bank_accounts['123456789']

        self.assertEqual(bank_account.balance,1000)

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        result = self.user.withdraw(amount=100,account_number='123456789',pin_code='123456',auth=self.auth)

        self.assertTrue(result)
        self.assertEqual(bank_account.balance,900)


    def test_deposit_success(self):
        """Test that user can deposit from a bank account."""

        bank_account = self.user.bank_accounts['123456789']

        self.assertEqual(bank_account.balance,1000)

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        result = self.user.deposit(amount=100,account_number='123456789',pin_code='123456',auth=self.auth)

        self.assertTrue(result)
        self.assertEqual(bank_account.balance,1100)


    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_transfer_success(self, mock_account_number):
        """Test transferring money between accounts successfully."""

        mock_account_number.return_value = '987654321'

        user2 = User(
            id=5,
            name='Bob',
            last_name='Smith',
            email='bob@example.com',
            password='Password567!',
            phone='678912345'
        )
        user2.open_bank_account(bank=self.bank, pin_code='654321', balance=500)

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        account_from = self.user.bank_accounts['123456789']
        account_to = user2.bank_accounts['987654321']

        self.user.transfer(
            amount=300,
            from_account_number='123456789',
            to_account_number='987654321',
            pin_code='123456',
            bank=self.bank,
            auth=self.auth
        )

        self.assertEqual(account_from.balance,700)
        self.assertEqual(account_to.balance,800)

    def test_transfer_nonexistent_source_account(self):
        """Test that transfer fails if the source account doesn't exist."""
        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        with self.assertRaises(ValueError):
            self.user.transfer(
                amount=100,
                from_account_number='nonexistent',
                to_account_number='987654321',
                pin_code='123456',
                bank=self.bank,
                auth=self.auth
            )

    def test_transfer_not_logged_in(self):
        """Test that transfer fails if the user is not logged in."""
        with self.assertRaises(PermissionError):
            self.user.transfer(
                amount=100,
                from_account_number='123456789',
                to_account_number='987654321',
                pin_code='123456',
                bank=self.bank,
                auth=self.auth
            )

    def test_get_transactions_success(self):
        """Test that user can get transactions successfully."""

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        self.user.deposit(amount=100, account_number='123456789', pin_code='123456', auth=self.auth)
        self.user.withdraw(amount=500,account_number='123456789', pin_code='123456', auth=self.auth)

        result = self.user.get_transactions(account_number='123456789',auth=self.auth)

        self.assertEqual(len(result),2)
        self.assertEqual(result[0]['amount'],100)
        self.assertEqual(result[1]['amount'],500)
        self.assertEqual(result[0]['type'],'deposit')
        self.assertEqual(result[1]['type'],'withdraw')


    @patch('projekt.src.bank_account.datetime')
    def test_get_transactions_by_date(self,mock_now):
        """Test that user can get transactions by date."""
        from datetime import datetime

        mock_now.now.side_effect = [datetime(2025,5,10),datetime(2025,5,11)]

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        self.user.deposit(amount=100, account_number='123456789', pin_code='123456', auth=self.auth)
        self.user.withdraw(amount=500, account_number='123456789', pin_code='123456', auth=self.auth)

        result = self.user.get_transactions_by_date(account_number='123456789',date_from=datetime(2023,1,1),date_to=datetime(2025,12,12),auth=self.auth)

        self.assertEqual(len(result),2)
        self.assertEqual(result[0]['amount'],100)
        self.assertEqual(result[1]['amount'],500)
        self.assertEqual(result[0]['type'],'deposit')
        self.assertEqual(result[1]['type'],'withdraw')

        result = self.user.get_transactions_by_date(account_number='123456789',date_from=datetime(2023,1,1),date_to=datetime(2025,5,10),auth=self.auth)

        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['amount'],100)
        self.assertEqual(result[0]['type'],'deposit')

    def test_get_transactions_by_date_not_logged_in(self):
        """Test that user can't get transactions by date if he is not logged in."""
        from datetime import datetime


        with self.assertRaises(PermissionError):
            self.user.get_transactions_by_date(
                account_number='123456789',
                date_from=datetime(2023, 1, 1),
                date_to=datetime(2025, 12, 12),
                auth=self.auth
            )

    def test_get_transactions_by_date_account_not_found(self):
        """Test that user can't get transactions by date if he tries to get it from not valid bank account."""
        from datetime import datetime

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        with self.assertRaises(ValueError):
            self.user.get_transactions_by_date(
                account_number='987654321',
                date_from=datetime(2023, 1, 1),
                date_to=datetime(2025, 12, 12),
                auth=self.auth
            )

    def test_unlock_account_success(self):
        """Test that a locked account can be successfully unlocked."""

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        bank_account = self.user.bank_accounts['123456789']
        bank_account.status = AccountStatus.LOCKED

        result = self.user.unlock_account(account_number='123456789', pin_code='123456', auth=self.auth)

        self.assertTrue(result)
        self.assertEqual(bank_account.status, AccountStatus.ACTIVE)

    def test_calculate_interest_success(self):
        """Test that an interest can be successfully calculated."""

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        result = self.user.calculate_intrest(days=10,account_number='123456789', auth=self.auth)

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result,0.27,2)


    def test_change_currency_success(self):
        """Test that the currency of an account can be successfully changed."""
        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        bank_account = self.user.bank_accounts['123456789']
        initial_currency = bank_account.currency
        initial_balance = bank_account.balance
        self.assertEqual(initial_currency, 'PLN')

        self.user.change_currency(account_number='123456789', currency='USD', auth=self.auth, pin_code='123456')

        self.assertEqual(bank_account.currency, 'USD')
        self.assertNotEqual(bank_account.balance, initial_balance)


    def test_get_user_success(self):
        """Test that a user can be successfully retrieved."""

        self.auth.login(user=self.admin, email=self.admin.email, password=self.admin.password)

        if self.user.id not in self.bank.users:
            self.bank.add_user(self.user)

        result = self.admin.get_user(user_id=self.user.id, bank=self.bank, auth=self.auth)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.user.id)
        self.assertEqual(result.name, self.user.name)
        self.assertEqual(result.last_name, self.user.last_name)
        self.assertEqual(result.email, self.user.email)

    def test_get_user_not_logged_in(self):
        """Test that user information cannot be retrieved if the user is not logged in."""
        with self.assertRaises(PermissionError):
            self.admin.get_user(user_id=1, bank=self.bank, auth=self.auth)


    def test_get_user_not_admin(self):
        """Test that non-admin users cannot retrieve user information."""
        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        with self.assertRaises(PermissionError):
            self.user.get_user(user_id=3, bank=self.bank, auth=self.auth)

    def test_get_users_success(self):
        """Test that an admin can successfully retrieve all users."""
        self.auth.login(user=self.admin, email=self.admin.email, password=self.admin.password)

        test_user = User(
            id=4,
            name='Alice',
            last_name='Johnson',
            email='alice@example.com',
            password='Password789!',
            phone='567891234'
        )
        self.bank.add_user(test_user)

        result = self.admin.get_users(bank=self.bank, auth=self.auth)

        self.assertIsNotNone(result)
        self.assertIn(self.user, result)
        self.assertIn(test_user, result)
        self.assertEqual(len(result), 2)

    def test_get_users_not_logged_in(self):
        """Test that users cannot be retrieved if the admin is not logged in."""

        with self.assertRaises(PermissionError):
            self.admin.get_users(bank=self.bank, auth=self.auth)


    def test_get_users_not_admin(self):
        """Test that non-admin users cannot retrieve all users."""

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        with self.assertRaises(PermissionError):
            self.user.get_users(bank=self.bank, auth=self.auth)

    def test_get_users_empty_bank(self):
        """Test retrieving users from an empty bank."""

        self.auth.login(user=self.admin, email=self.admin.email, password=self.admin.password)

        empty_bank = Bank(name='Empty Bank', bank_code='0000')

        result = self.admin.get_users(bank=empty_bank, auth=self.auth)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    @patch('projekt.src.bank.Bank._fetch_currencies')
    def test_update_currencies_success(self, mock_fetch_currencies):
        """Test that an admin can successfully update currency exchange rates."""

        self.auth.login(user=self.admin, email=self.admin.email, password=self.admin.password)

        initial_currencies = self.bank.currencies.copy()

        new_currencies = {'PLN': 1.0, 'USD': 3.9, 'EUR': 4.3, 'GBP': 5.1, 'CHF': 4.6}
        mock_fetch_currencies.return_value = new_currencies

        result = self.admin.update_currencies(bank=self.bank, auth=self.auth)

        self.assertTrue(result)

        self.assertEqual(self.bank.currencies, new_currencies)
        self.assertNotEqual(self.bank.currencies, initial_currencies)

    def test_update_currencies_not_logged_in(self):
        """Test that currencies cannot be updated if the admin is not logged in."""

        with self.assertRaises(PermissionError):
            self.admin.update_currencies(bank=self.bank, auth=self.auth)

    def test_update_currencies_not_admin(self):
        """Test that non-admin users cannot update currencies."""

        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        with self.assertRaises(PermissionError):
            self.user.update_currencies(bank=self.bank, auth=self.auth)

    def test_user_not_logged_in_errors(self):
        """Test that methods will trigger PermissionError if user is not logged in."""

        methods_to_test = [
            ('close_bank_account',self.user.close_bank_account,{'account_number':'123456789','pin_code':'123456'}),
            ('get_balance', self.user.get_balance, {'account_number': '123456789'}),
            ('get_total_balance', self.user.get_total_balance, {}),
            ('deposit', self.user.deposit, {'amount': 100, 'account_number': '123456789', 'pin_code': '123456'}),
            ('withdraw', self.user.withdraw, {'amount': 100, 'account_number': '123456789', 'pin_code': '123456'}),
            ('change_pin', self.user.change_pin,
            {'account_number': '123456789', 'old_pin': '123456', 'new_pin': '654321'}),
            ('unlock_account', self.user.unlock_account, {'account_number': '123456789', 'pin_code': '123456'}),
            ('change_currency', self.user.change_currency,
            {'account_number': '123456789', 'currency': 'USD', 'pin_code': '123456'}),
            ('get_transactions', self.user.get_transactions, {'account_number': '123456789'}),
            ('calculate_interest', self.user.calculate_intrest, {'days':30,'account_number': '123456789'}),
        ]

        for method_name, method, kwargs in methods_to_test:
            with self.subTest(f"{method_name} - not logged in"):
                with self.assertRaises(PermissionError):
                    method(auth=self.auth, **kwargs)

    def test_account_not_found(self):
        """Test that methods will trigger ValueError if account is not found."""

        methods_to_test = [
            ('close_bank_account', self.user.close_bank_account, {'account_number': '987654321', 'pin_code': '123456'}),
            ('get_balance', self.user.get_balance, {'account_number': '987654321'}),
            ('deposit', self.user.deposit, {'amount': 100, 'account_number': '987654321', 'pin_code': '123456'}),
            ('withdraw', self.user.withdraw, {'amount': 100, 'account_number': '987654321', 'pin_code': '123456'}),
            ('change_pin', self.user.change_pin,
            {'account_number': '987654321', 'old_pin': '123456', 'new_pin': '654321'}),
            ('unlock_account', self.user.unlock_account, {'account_number': '987654321', 'pin_code': '123456'}),
            ('change_currency', self.user.change_currency,
            {'account_number': '987654321', 'currency': 'USD', 'pin_code': '123456'}),
            ('get_transactions', self.user.get_transactions, {'account_number': '987654321'}),
            ('calculate_interest', self.user.calculate_intrest, {'days': 30, 'account_number': '987654321'}),
        ]
        self.auth.login(user=self.user, email=self.user.email, password=self.user.password)

        for method_name, method, kwargs in methods_to_test:
            with self.subTest(f"{method_name} - account not found"):
                with self.assertRaises(ValueError):
                    method(auth=self.auth, **kwargs)

if __name__ == '__main__':
    unittest.main()




















