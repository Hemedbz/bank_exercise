from abc import *


class Transaction(ABC):

    def __init__(self, amount, currency='ILS'):
        self.amount = amount
        self.currency = currency
        self.timestamp = pass


class Deposit(Transaction):
    pass

class Withdraw(Transaction):
    pass

class pass