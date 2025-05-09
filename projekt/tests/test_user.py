import unittest
from unittest.mock import patch

from projekt.src.auth import Auth
from projekt.src.user import User,UserRole
from projekt.src.bank import Bank


# noinspection PyTypeChecker
class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    @patch('projekt.src.bank.Bank._fetch_currencies')
    def setUp(self,mock_fetch):
        """Set up test fixtures."""
        mock_fetch.return_value = {'PLN': 1.0, 'USD': 3.7642, 'EUR': 4.2757, 'GBP': 5.0205, 'CHF': 4.5595}

        self.auth = Auth()
        self.user = User(
            id=1,
            name='John',
            last_name='Doe',
            email='example@gmail.com',
            password='Password123!',
            phone='523456789'
        )
        self.bank = Bank(
            name = 'PKO BP',
            bank_code = '1120'
        )
        self.bank2  = Bank(
            name = 'ING Bank Śląski',
            bank_code = '1150'
        )

    def test_user_initialization(self):
        """Test that a user can be created with valid attributes."""
        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.user.name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'example@gmail.com')
        self.assertEqual(self.user.password, 'Password123!')
        self.assertEqual(self.user.phone, '+48 523-456-789')
        self.assertEqual(self.user.role,UserRole.USER)
        self.assertEqual(self.user.bank_accounts,{})

    def test_invalid_id(self):
        """Test that an invalid user id raises an error."""
        with self.assertRaises(TypeError):
            User(
                id='1',
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )

    def test_invalid_role(self):
        """Test that an invalid user role raises an error."""
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

    def test_invalid_name(self):
        """Test that an invalid user name raises an error."""
        with self.assertRaises(TypeError):
            User(
                id=1,
                name=1,
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John!',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name=' ',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )

    def test_invalid_lastname(self):
        with self.assertRaises(TypeError):
            User(
                id=1,
                name='John',
                last_name=1,
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe!',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe!',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name=' ',
                email='example@gmail.com',
                password='Password123!',
                phone='523456789',
            )

    def test_invalid_email(self):
        """Test that an invalid user email raises an error."""
        with self.assertRaises(TypeError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email=1,
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='@gmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='examplegmail.com',
                password='Password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='',
                password='Password123!',
                phone='523456789',
            )

    def test_invalid_password(self):
        """Test that an invalid user password raises an error."""
        with self.assertRaises(TypeError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password=1,
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='pass',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='password123!',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123',
                phone='523456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password!',
                phone='523456789',
            )

    def test_invalid_phone(self):
        """Test that an invalid user phone raises an error."""
        with self.assertRaises(TypeError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone=123456789,
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='52345678',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='5234567899',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='123456789',
            )
        with self.assertRaises(ValueError):
            User(
                id=1,
                name='John',
                last_name='Doe',
                email='example@gmail.com',
                password='Password123!',
                phone='',
            )

    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_open_bank_account_success(self, mock_account_number):
        """Test that an open bank account is created."""
        mock_account_number.return_value = '123456789'
        result = self.user.open_bank_account(bank=self.bank, pin_code='123456', balance=1000)

        self.assertIn('123456789', self.user.bank_accounts)
        bank_account = self.user.bank_accounts['123456789']

        self.assertEqual(bank_account,self.user.bank_accounts['123456789'])
        self.assertTrue(result)
        self.assertEqual(len(self.user.bank_accounts),1)
        self.assertEqual(bank_account.balance, 1000)
        self.assertEqual(bank_account.pin, '123456')
        self.assertEqual(bank_account.currency,'PLN')
        self.assertEqual(bank_account.bank, self.bank)
        self.assertEqual(bank_account.owner, self.user)

    @patch('projekt.src.bank_account.BankAccount._generate_account_number')
    def test_open_bank_account_multiple_accounts(self, mock_account_number):

        mock_account_number.side_effect = ['123456789','987654321']

        self.user.open_bank_account(bank=self.bank, pin_code='123456', balance=1000)
        self.user.open_bank_account(bank=self.bank2, pin_code='654321', balance=2000)

        self.assertEqual(len(self.user.bank_accounts),2)














