import unittest
from unittest.mock import patch, Mock
from datetime import datetime

from projekt.src.bank import Bank
from projekt.src.user import User


# noinspection PyTypeChecker
class TestBank(unittest.TestCase):
    """Test cases for the Bank class."""

    @patch("projekt.src.bank.Bank._fetch_currencies")
    def setUp(self, mock_fetch):
        """Set up test fixtures."""
        mock_fetch.return_value = {
            "PLN": 1.0,
            "USD": 3.7642,
            "EUR": 4.2757,
            "GBP": 5.0205,
            "CHF": 4.5595,
        }

        self.bank = Bank(name="PKO BP", bank_code="1120")

        self.user1 = User(
            id=1,
            name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="Password123!",
            phone="781234567",
        )

        self.user2 = User(
            id=2,
            name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="Password456!",
            phone="612345678",
        )

        self.bank.add_user(user=self.user1)
        self.bank.add_user(user=self.user2)

    def test_bank_initialization(self):
        """Test bank initialization with correct parameters."""

        bank_name = self.bank.name
        bank_code = self.bank.bank_code
        bank_accounts = self.bank.accounts
        bank_users = self.bank.users
        bank_currencies = self.bank.currencies
        bank_created_at = self.bank.created_at

        self.assertEqual(bank_name, "PKO BP")
        self.assertEqual(bank_code, "1120")
        self.assertIsInstance(bank_accounts, dict)
        self.assertIsInstance(bank_users, dict)
        self.assertIsInstance(bank_currencies, dict)
        self.assertIsInstance(bank_created_at, datetime)

        pln_rate = bank_currencies["PLN"]
        usd_rate = bank_currencies["USD"]
        eur_rate = bank_currencies["EUR"]
        gbp_rate = bank_currencies["GBP"]
        chf_rate = bank_currencies["CHF"]

        self.assertEqual(pln_rate, 1.0)
        self.assertEqual(usd_rate, 3.7642)
        self.assertEqual(eur_rate, 4.2757)
        self.assertAlmostEqual(gbp_rate, 5.0205)
        self.assertAlmostEqual(chf_rate, 4.5595)

    @patch("projekt.src.bank.requests.get")
    def test_fetch_currencies_success(self, mock_get):
        """Test successful fetching of currency rates."""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "rates": [
                    {"code": "USD", "mid": 3.7642},
                    {"code": "EUR", "mid": 4.2757},
                    {"code": "GBP", "mid": 5.0205},
                ]
            }
        ]

        mock_get.return_value = mock_response

        currencies = self.bank._fetch_currencies()

        pln_rate = currencies["PLN"]
        usd_rate = currencies["USD"]
        eur_rate = currencies["EUR"]
        gbp_rate = currencies["GBP"]
        chf_exists = "CHF" in currencies

        self.assertEqual(pln_rate, 1.0)
        self.assertEqual(usd_rate, 3.7642)
        self.assertEqual(eur_rate, 4.2757)
        self.assertEqual(gbp_rate, 5.0205)
        self.assertFalse(chf_exists)

        mock_get.assert_called_once_with(
            "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"
        )

        response_status = mock_response.status_code
        self.assertEqual(response_status, 200)

    @patch("projekt.src.bank.requests.get")
    def test_fetch_currencies_failure(self, mock_get):
        """Test handling of API errors when fetching currencies."""

        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.bank._fetch_currencies()

    def test_get_user_success(self):
        """Test retrieving a user by ID successfully."""
        user = self.bank.get_user(user_id=1)

        self.assertEqual(user, self.user1)
        self.assertEqual(user.name, "John")
        self.assertEqual(user.email, "john.doe@example.com")

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user."""
        with self.assertRaises(ValueError):
            self.bank.get_user(user_id=999)

    def test_get_users(self):
        """Test retrieving all users."""
        users = self.bank.get_users()

        users_count = len(users)
        user1_in_users = self.user1 in users
        user2_in_users = self.user2 in users

        self.assertEqual(users_count, 2)
        self.assertTrue(user1_in_users)
        self.assertTrue(user2_in_users)

    def test_add_user(self):
        """Test adding a new user to the bank."""
        user3 = User(
            id=3,
            name="Alice",
            last_name="Johnson",
            email="alice.johnson@example.com",
            password="Password789!",
            phone="712345678",
        )

        self.bank.add_user(user=user3)

        user3_id_in_users = 3 in self.bank.users
        stored_user = self.bank.users.get(3)

        self.assertTrue(user3_id_in_users)
        self.assertEqual(stored_user, user3)

        retrieved_user = self.bank.get_user(user_id=3)
        self.assertEqual(retrieved_user, user3)

    @patch("projekt.src.bank.requests.get")
    def test_update_currencies(self, mock_get):
        """Test updating currency rates."""

        initial_usd_rate = self.bank.currencies["USD"]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "rates": [
                    {"code": "USD", "mid": 3.9},
                    {"code": "EUR", "mid": 4.5},
                    {"code": "GBP", "mid": 5.2},
                    {"code": "CHF", "mid": 4.3},
                ]
            }
        ]
        mock_get.return_value = mock_response

        self.bank.update_currencies()

        new_usd_rate = self.bank.currencies["USD"]
        new_eur_rate = self.bank.currencies["EUR"]
        new_gbp_rate = self.bank.currencies["GBP"]
        new_chf_rate = self.bank.currencies["CHF"]

        self.assertNotEqual(new_usd_rate, initial_usd_rate)
        self.assertEqual(new_usd_rate, 3.9)
        self.assertEqual(new_eur_rate, 4.5)
        self.assertEqual(new_gbp_rate, 5.2)
        self.assertEqual(new_chf_rate, 4.3)

    def test_add_new_transaction(self):
        """Test adding a new transaction to an account."""

        account_number = "123456789"
        transaction = {"type": "deposit", "amount": 1000, "date": datetime.now()}

        result = self.bank.add_new_transaction(
            transaction=transaction, account_number=account_number
        )

        self.assertTrue(result)

        account_exists = account_number in self.bank.transactions
        transactions_count = len(self.bank.transactions[account_number])
        stored_transaction = self.bank.transactions[account_number][0]

        self.assertTrue(account_exists)
        self.assertEqual(transactions_count, 1)
        self.assertEqual(stored_transaction, transaction)

        transaction2 = {"type": "withdraw", "amount": 500, "date": datetime.now()}

        self.bank.add_new_transaction(
            transaction=transaction2, account_number=account_number
        )

        updated_transactions_count = len(self.bank.transactions[account_number])
        first_transaction = self.bank.transactions[account_number][0]
        second_transaction = self.bank.transactions[account_number][1]

        self.assertEqual(updated_transactions_count, 2)
        self.assertEqual(first_transaction, transaction)
        self.assertEqual(second_transaction, transaction2)

    def test_get_transactions(self):
        """Test retrieving all transactions for an account."""
        account_number = "123456789"

        transaction1 = {"type": "deposit", "amount": 1000, "date": datetime.now()}

        transaction2 = {"type": "withdraw", "amount": 500, "date": datetime.now()}

        self.bank.add_new_transaction(
            transaction=transaction1, account_number=account_number
        )
        self.bank.add_new_transaction(
            transaction=transaction2, account_number=account_number
        )

        transactions = self.bank.get_transactions(account_number=account_number)

        transactions_count = len(transactions)
        first_transaction = transactions[0]
        second_transaction = transactions[1]

        self.assertEqual(transactions_count, 2)
        self.assertEqual(first_transaction, transaction1)
        self.assertEqual(second_transaction, transaction2)

    def test_get_transactions_empty_account(self):
        """Test retrieving transactions for an account with no transactions."""

        account_number = "987654321"

        transactions = self.bank.get_transactions(account_number=account_number)

        self.assertEqual(transactions, [])

    def test_get_transactions_by_date(self):
        """Test retrieving transactions by date range."""
        account_number = "123456789"

        date1 = datetime(2023, 1, 15)
        date2 = datetime(2023, 2, 20)
        date3 = datetime(2023, 3, 25)

        transaction1 = {"type": "deposit", "amount": 1000, "date": date1}

        transaction2 = {"type": "withdraw", "amount": 500, "date": date2}

        transaction3 = {"type": "deposit", "amount": 1500, "date": date3}

        self.bank.add_new_transaction(
            transaction=transaction1, account_number=account_number
        )
        self.bank.add_new_transaction(
            transaction=transaction2, account_number=account_number
        )
        self.bank.add_new_transaction(
            transaction=transaction3, account_number=account_number
        )

        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 2, 28)

        filtered_transactions = self.bank.get_transactions_by_date(
            date_from=start_date, date_to=end_date, account_number=account_number
        )

        jan_feb_count = len(filtered_transactions)
        has_transaction1 = transaction1 in filtered_transactions
        has_transaction2 = transaction2 in filtered_transactions
        has_transaction3 = transaction3 in filtered_transactions

        self.assertEqual(jan_feb_count, 2)
        self.assertTrue(has_transaction1)
        self.assertTrue(has_transaction2)
        self.assertFalse(has_transaction3)

        start_date = datetime(2023, 3, 1)
        end_date = datetime(2023, 3, 31)

        filtered_transactions = self.bank.get_transactions_by_date(
            date_from=start_date, date_to=end_date, account_number=account_number
        )

        march_count = len(filtered_transactions)
        has_transaction1_march = transaction1 in filtered_transactions
        has_transaction2_march = transaction2 in filtered_transactions
        has_transaction3_march = transaction3 in filtered_transactions

        self.assertEqual(march_count, 1)
        self.assertTrue(has_transaction3_march)
        self.assertFalse(has_transaction1_march)
        self.assertFalse(has_transaction2_march)

        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 4, 1)

        filtered_transactions = self.bank.get_transactions_by_date(
            date_from=start_date, date_to=end_date, account_number=account_number
        )

        total_count = len(filtered_transactions)
        has_all_transaction1 = transaction1 in filtered_transactions
        has_all_transaction2 = transaction2 in filtered_transactions
        has_all_transaction3 = transaction3 in filtered_transactions

        self.assertEqual(total_count, 3)
        self.assertTrue(has_all_transaction1)
        self.assertTrue(has_all_transaction2)
        self.assertTrue(has_all_transaction3)

    def test_get_transactions_by_date_invalid_dates(self):
        """Test error handling when providing invalid date ranges."""
        account_number = "123456789"

        start_date = datetime(2023, 3, 1)
        end_date = datetime(2023, 2, 1)

        with self.assertRaises(ValueError):
            self.bank.get_transactions_by_date(
                date_from=start_date, date_to=end_date, account_number=account_number
            )

        with self.assertRaises(TypeError):
            self.bank.get_transactions_by_date(
                date_from="2023-01-01",
                date_to=datetime(2023, 2, 1),
                account_number=account_number,
            )

        with self.assertRaises(TypeError):
            self.bank.get_transactions_by_date(
                date_from=datetime(2023, 1, 1),
                date_to="2023-02-01",
                account_number=account_number,
            )

    def test_get_transactions_by_date_empty_result(self):
        """Test retrieving transactions by date when no transactions match the date range."""
        account_number = "123456789"

        transaction = {"type": "deposit", "amount": 1000, "date": datetime(2023, 5, 15)}

        self.bank.add_new_transaction(
            transaction=transaction, account_number=account_number
        )

        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 4, 30)

        filtered_transactions = self.bank.get_transactions_by_date(
            date_from=start_date, date_to=end_date, account_number=account_number
        )

        self.assertEqual(filtered_transactions, [])

    if __name__ == "__main__":
        unittest.main()
