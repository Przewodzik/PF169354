import unittest
from bank_account import BankAccount

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount(5000)

    def test_deposit(self):
        self.account.deposit(200)
        self.assertEqual(self.account.get_balance(), 5200)

    def test_deposit_multiple(self):
        self.account.deposit(200)
        self.account.deposit(300)
        self.assertEqual(self.account.get_balance(), 5500)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-200)

    def test_withdraw(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.get_balance(), 4800)

    def test_withdraw_multiple(self):
        self.account.withdraw(200)
        self.account.withdraw(300)
        self.assertEqual(self.account.get_balance(), 4500)

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-200)

    def test_withdraw_more_than_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(5200)

    def test_withdraw_all(self):
        self.account.withdraw(5000)
        self.assertEqual(self.account.get_balance(), 0)

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 5000)



    if __name__ == '__main__':
        unittest.main()
