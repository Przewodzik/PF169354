
class BankAccount:
    def __init__(self,balance):
        self.balance = balance

    def deposit(self,amount):

        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero")

        self.balance += amount

    def withdraw(self,amount):

        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than zero")

        if amount > self.balance:
            raise ValueError("You cannot withdraw more than your balance")

        self.balance -= amount

    def get_balance(self):
        return self.balance