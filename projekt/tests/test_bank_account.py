import unittest
from unittest.mock import patch
from datetime import datetime

from projekt.src.bank import Bank
from projekt.src.user import User
from projekt.src.bank_account import BankAccount, AccountStatus
from projekt.src.auth import Auth


# noinspection PyTypeChecker
class TestBankAccount(unittest.TestCase):
    """Test cases for the BankAccount class."""

    @patch("projekt.src.bank_account.BankAccount._generate_account_number")
    @patch("projekt.src.bank.Bank._fetch_currencies")
    def setUp(self, mock_fetch, mock_account_number):
        """Set up test fixtures."""
        mock_fetch.return_value = {
            "PLN": 1.0,
            "USD": 3.7,
            "EUR": 4.2757,
            "GBP": 5.0205,
            "CHF": 4.5595,
        }
        mock_account_number.return_value = "123456789"

        self.bank = Bank(name="PKO BP", bank_code="1120")

        self.bank2 = Bank(name="ING Bank Śląski", bank_code="1150")

        self.user = User(
            id=1,
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="Password123!",
            phone="781234567",
        )

        self.user2 = User(
            id=2,
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="Password123!",
            phone="781234567",
        )

        self.user3 = User(
            id=3,
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="Password123!",
            phone="781234567",
        )

        self.account = BankAccount(
            owner=self.user, bank=self.bank, pin_code="123456", balance=1000
        )

        self.auth = Auth()

    def test_initialization_success(self):
        """Test bank account initialization with correct parameters."""
        self.assertEqual(self.account.balance, 1000)
        self.assertEqual(self.account.owner, self.user)
        self.assertEqual(self.account.bank, self.bank)
        self.assertEqual(self.account.status, AccountStatus.ACTIVE)
        self.assertEqual(self.account.pin, "123456")
        self.assertEqual(self.account.currency, "PLN")
        self.assertEqual(self.account.account_number, "123456789")
        self.assertEqual(self.account.failedWithdrawCount, 0)
        self.assertIsNone(self.account.last_transaction_date)
        self.assertIsInstance(self.account.created_at, datetime)

    def test_initialization_failure(self):
        """Test bank account initialization with incorrect parameters."""

        with self.assertRaises(TypeError):
            BankAccount(
                owner="not a user", bank=self.bank, pin_code="123456", balance=1000
            )

        with self.assertRaises(TypeError):
            BankAccount(
                owner=self.user, bank="not a bank", pin_code="123456", balance=1000
            )

        with self.assertRaises(TypeError):
            BankAccount(
                owner=self.user,
                bank=self.bank,
                pin_code="123456",
                balance="not a number",
            )

        with self.assertRaises(ValueError):
            BankAccount(
                owner=self.user, bank=self.bank, pin_code="123456", balance=-100
            )

        with self.assertRaises(TypeError):
            BankAccount(
                owner=self.user,
                bank=self.bank,
                pin_code="123456",
                balance=1000,
                currency=123,
            )

        with self.assertRaises(ValueError):
            BankAccount(
                owner=self.user,
                bank=self.bank,
                pin_code="123456",
                balance=1000,
                currency="XYZ",
            )

    def test_validate_pin_code_success(self):
        """Test PIN code validation with valid PINs."""

        valid_pins = ["123456", "000000", "999999"]

        for pin in valid_pins:
            with self.subTest(pin=pin):
                self.assertEqual(self.account._validate_pin_code(pin), pin)

    def test_validate_pin_code_failure(self):
        """Test PIN code validation with invalid PINs."""

        with self.assertRaises(TypeError):
            self.account._validate_pin_code(pin_code=123456)

        invalid_pins = ["12345", "1234567", "abcdef", "12345a"]
        for pin in invalid_pins:
            with self.subTest(pin=pin):
                with self.assertRaises(ValueError):
                    self.account._validate_pin_code(pin)

    def test_validate_access_success(self):
        """Test account access validation with correct PIN."""

        self.account._validate_access(pin_code="123456")
        self.assertEqual(self.account.failedWithdrawCount, 0)

    def test_validate_access_incorrect_pin(self):
        """Test account access validation with incorrect PIN."""

        with self.assertRaises(PermissionError):
            self.account._validate_access(pin_code="654321")

        self.assertEqual(self.account.failedWithdrawCount, 1)

    def test_validate_access_locked_account(self):
        """Test account access validation with a locked account."""

        for i in range(4):
            try:
                self.account._validate_access("654321")
            except PermissionError:
                pass

        self.assertEqual(self.account.status, AccountStatus.LOCKED)

        with self.assertRaises(PermissionError):
            self.account._validate_access(pin_code="123456")

    def test_validate_access_inactive_account(self):
        """Test account access validation with an inactive account."""
        self.account.status = AccountStatus.INACTIVE

        with self.assertRaises(ValueError):
            self.account._validate_access("123456")

    def test_validate_access_failed_withdraw_count_back_to_zero(self):
        """Test that failed withdraw count is back to zero after successful validation."""

        for i in range(2):
            try:
                self.account._validate_access(pin_code="654321")
            except PermissionError:
                pass

        self.assertEqual(self.account.failedWithdrawCount, 2)

        self.account._validate_access(pin_code="123456")

        self.assertEqual(self.account.failedWithdrawCount, 0)

    def test_generate_account_number(self):
        """Test that account generation generates unique account number."""

        bank_account = BankAccount(owner=self.user2, bank=self.bank, pin_code="123456")
        bank_account2 = BankAccount(
            owner=self.user2, bank=self.bank2, pin_code="123456"
        )
        bank_account3 = BankAccount(owner=self.user3, bank=self.bank, pin_code="123456")
        bank_account4 = BankAccount(
            owner=self.user3, bank=self.bank2, pin_code="123456"
        )

        self.assertNotEqual(bank_account.account_number, bank_account2.account_number)
        self.assertNotEqual(bank_account.account_number, bank_account3.account_number)
        self.assertNotEqual(bank_account.account_number, bank_account4.account_number)
        self.assertNotEqual(bank_account2.account_number, bank_account3.account_number)
        self.assertNotEqual(bank_account2.account_number, bank_account4.account_number)
        self.assertNotEqual(bank_account3.account_number, bank_account4.account_number)

        self.assertEqual(bank_account.account_number[0], "1")
        self.assertEqual(bank_account.account_number[1], "1")
        self.assertEqual(bank_account.account_number[2], "2")
        self.assertEqual(bank_account.account_number[3], "0")

        self.assertEqual(bank_account2.account_number[0], "1")
        self.assertEqual(bank_account2.account_number[1], "1")
        self.assertEqual(bank_account2.account_number[2], "5")
        self.assertEqual(bank_account2.account_number[3], "0")

    def test_close_bank_account_success(self):
        """Test account close success."""

        self.account.balance = 0

        result = self.account.close(pin_code="123456")

        self.assertTrue(result)
        self.assertEqual(self.account.status, AccountStatus.CLOSED)
        self.assertEqual(
            self.bank.accounts[self.account.account_number].status, AccountStatus.CLOSED
        )

    def test_close_bank_account_balance_is_not_zero(self):
        """Test that account can't be closed with no empty balance"""

        with self.assertRaises(ValueError):
            self.account.close(pin_code="123456")

    def test_withdraw_success(self):
        """Test withdraw success."""

        self.account.withdraw(amount=100, pin_code="123456")

        self.assertEqual(self.account.balance, 900)
        self.assertIsNotNone(self.account.last_transaction_date)

        transactions = self.bank.get_transactions(
            account_number=self.account.account_number
        )

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["type"], "withdraw")
        self.assertEqual(transactions[0]["amount"], 100)
        self.assertIsInstance(transactions[0]["date"], datetime)

    def test_withdraw_invalid_amount(self):
        """Test that is not possible to withdraw with invalid amount."""

        with self.assertRaises(ValueError):
            self.account.withdraw(amount=-100, pin_code="123456")

        with self.assertRaises(ValueError):
            self.account.withdraw(amount=0, pin_code="123456")

    def test_withdraw_invalid_type_amount(self):
        """Test that is not possible to withdraw with invalid amount type."""

        invalid_types = ["number", [], {}, "tekst"]

        for invalid_type in invalid_types:
            with self.subTest(amount=invalid_type):
                with self.assertRaises(TypeError):
                    self.account.withdraw(amount=invalid_type, pin_code="123456")

    def test_withdraw_greater_amount_than_balance(self):
        """Test that is not possible to withdraw with greater amount than balance."""

        with self.assertRaises(ValueError):
            self.account.withdraw(amount=1100, pin_code="123456")

    def test_deposit_success(self):
        """Test successful deposit."""

        self.account.deposit(amount=100, pin_code="123456")

        self.assertEqual(self.account.balance, 1100)
        self.assertIsNotNone(self.account.last_transaction_date)

        transactions = self.bank.get_transactions(
            account_number=self.account.account_number
        )

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["type"], "deposit")
        self.assertEqual(transactions[0]["amount"], 100)
        self.assertIsInstance(transactions[0]["date"], datetime)

    def test_deposit_invalid_amount(self):
        """Test that is not possible to deposit with invalid amount."""

        with self.assertRaises(ValueError):
            self.account.deposit(amount=-100, pin_code="123456")

        with self.assertRaises(ValueError):
            self.account.deposit(amount=0, pin_code="123456")

    def test_deposit_invalid_type_amount(self):
        """Test that is not possible to deposit with invalid amount type."""

        invalid_types = ["number", [], {}, "tekst"]

        for invalid_type in invalid_types:
            with self.subTest(amount=invalid_type):
                with self.assertRaises(TypeError):
                    self.account.deposit(amount=invalid_type, pin_code="123456")

    def test_transfer_success_same_currency(self):
        """Test successful transfer with same currencies"""

        bank_account = BankAccount(
            owner=self.user2, bank=self.bank, pin_code="123456", balance=200
        )

        self.account.transfer(
            amount=500,
            to_account_number=bank_account.account_number,
            pin_code="123456",
            bank=bank_account.bank,
        )

        self.assertEqual(self.account.balance, 500)
        self.assertEqual(bank_account.balance, 700)
        self.assertIsNotNone(self.account.last_transaction_date)
        self.assertIsNotNone(bank_account.last_transaction_date)

        transactions = self.bank.get_transactions(
            account_number=self.account.account_number
        )
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["type"], "transfer")
        self.assertEqual(transactions[0]["to"], bank_account.account_number)
        self.assertEqual(transactions[0]["bank"], bank_account.bank)
        self.assertEqual(transactions[0]["amount"], 500)
        self.assertIsInstance(transactions[0]["date"], datetime)

        transactions = self.bank.get_transactions(
            account_number=bank_account.account_number
        )
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["type"], "incoming_transfer")
        self.assertEqual(transactions[0]["from"], self.account.account_number)
        self.assertEqual(transactions[0]["amount"], 500)
        self.assertIsInstance(transactions[0]["date"], datetime)

    def test_transfer_success_different_currency(self):
        """Test successful transfer with different currencies"""
        bank_account = BankAccount(
            owner=self.user2,
            bank=self.bank,
            pin_code="123456",
            balance=200,
            currency="USD",
        )

        self.account.transfer(
            amount=500,
            to_account_number=bank_account.account_number,
            pin_code="123456",
            bank=bank_account.bank,
        )

        self.assertEqual(self.account.balance, 500)
        self.assertEqual(bank_account.balance, 335.14)
        self.assertIsNotNone(self.account.last_transaction_date)
        self.assertIsNotNone(bank_account.last_transaction_date)

        transactions = self.bank.get_transactions(
            account_number=self.account.account_number
        )
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["type"], "transfer")
        self.assertEqual(transactions[0]["to"], bank_account.account_number)
        self.assertEqual(transactions[0]["bank"], bank_account.bank)
        self.assertEqual(transactions[0]["amount"], 500)
        self.assertIsInstance(transactions[0]["date"], datetime)

        transactions = self.bank.get_transactions(
            account_number=bank_account.account_number
        )
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["type"], "incoming_transfer")
        self.assertEqual(transactions[0]["from"], self.account.account_number)
        self.assertEqual(transactions[0]["amount"], 135.14)
        self.assertIsInstance(transactions[0]["date"], datetime)

    def test_transfer_invalid_amount(self):
        """Test that is not possible to transfer with invalid amount."""
        bank_account = BankAccount(
            owner=self.user2, bank=self.bank, pin_code="123456", balance=200
        )

        with self.assertRaises(ValueError):
            self.account.transfer(
                amount=-100,
                pin_code="123456",
                to_account_number=bank_account.account_number,
                bank=bank_account.bank,
            )
        with self.assertRaises(ValueError):
            self.account.transfer(
                amount=0,
                pin_code="123456",
                to_account_number=bank_account.account_number,
                bank=bank_account.bank,
            )

    def test_transfer_invalid_type_amount(self):
        """Test that is not possible to transfer with invalid amount type."""

        bank_account = BankAccount(
            owner=self.user2, bank=self.bank, pin_code="123456", balance=200
        )
        invalid_types = ["number", [], {}, "tekst"]

        for invalid_type in invalid_types:
            with self.subTest(amount=invalid_type):
                with self.assertRaises(TypeError):
                    self.account.transfer(
                        amount=invalid_type,
                        pin_code="123456",
                        to_account_number=bank_account.account_number,
                        bank=bank_account.bank,
                    )

    def test_transfer_amount_greater_than_balance(self):
        """Test that is not possible to transfer with amount greater than balance."""

        bank_account = BankAccount(
            owner=self.user2, bank=self.bank, pin_code="123456", balance=200
        )

        with self.assertRaises(ValueError):
            self.account.transfer(
                amount=1100,
                to_account_number=bank_account.account_number,
                pin_code="123456",
                bank=bank_account.bank,
            )

    def test_transfer_to_not_active_account(self):
        """Test that is not possible to transfer to not active account."""

        bank_account = BankAccount(
            owner=self.user2, bank=self.bank, pin_code="123456", balance=200
        )
        bank_account.status = AccountStatus.INACTIVE

        with self.assertRaises(ValueError):
            self.account.transfer(
                amount=900,
                to_account_number=bank_account.account_number,
                pin_code="123456",
                bank=bank_account.bank,
            )

    def test_transfer_non_existing_to_account(self):
        """Test that is not possible to transfer money to no existing account"""

        with self.assertRaises(ValueError):
            self.account.transfer(
                amount=100,
                to_account_number="987654321",
                pin_code="123456",
                bank=self.bank,
            )

    def test_unlock_account_success(self):
        """Test successful unlock."""

        self.account.status = AccountStatus.LOCKED

        self.assertEqual(self.account.status, AccountStatus.LOCKED)

        self.account.unlock_account(pin_code="123456")

        self.assertEqual(self.account.status, AccountStatus.ACTIVE)

    def test_unlock_account_incorrect_pin(self):
        """Test unlock with incorrect pin code."""

        self.account.status = AccountStatus.INACTIVE

        with self.assertRaises(PermissionError):
            self.account.unlock_account(pin_code="623456")

    def test_unlock_account_invalid_account_status(self):
        """Test unlock with incorrect account status."""

        with self.assertRaises(ValueError):
            self.account.unlock_account(pin_code="123456")

        self.account.status = AccountStatus.CLOSED

        with self.assertRaises(ValueError):
            self.account.unlock_account(pin_code="123456")

    def test_change_currency_invalid_type(self):
        """Test change_currency with incorrect type."""

        invalid_types = [1, [], {}, 4.2]

        for invalid_type in invalid_types:
            with self.subTest(currency=invalid_type):
                with self.assertRaises(TypeError):
                    self.account.change_currency(
                        currency=invalid_type, pin_code="123456"
                    )

    def test_change_currency_failure(self):
        """Test change currency if currency does not exist or is the same."""

        with self.assertRaises(ValueError):
            self.account.change_currency(currency="XYZ", pin_code="123456")

        with self.assertRaises(ValueError):
            self.account.change_currency(currency="PLN", pin_code="123456")

    def test_change_pin_is_the_same(self):
        """Test change pin if pin_code is same."""

        with self.assertRaises(ValueError):
            self.account.change_pin(old_pin_code="123456", new_pin_code="123456")

    def test_calculate_interest_different_balances(self):
        """Test interest calculation for different account balances and time periods."""

        test_cases = [
            {"balance": 500, "days": 30, "expected": 0.41},
            {"balance": 2000, "days": 90, "expected": 9.86},
            {"balance": 15000, "days": 365, "expected": 450.0},
            {"balance": 0, "days": 365, "expected": 0.0},
        ]

        for case in test_cases:
            with self.subTest(balance=case["balance"], days=case["days"]):

                self.account.balance = case["balance"]

                interest = self.account.calculate_intrest(days=case["days"])

                self.assertAlmostEqual(interest, case["expected"], places=2)


    if __name__ == "__main__":
        unittest.main()
