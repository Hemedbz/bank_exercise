import datetime
import time
import exceptions


class Transaction:

    def __init__(self, amount, currency, transaction_timestamp):
        self.amount = amount
        self.currency = currency
        self._timestamp = transaction_timestamp

    def __str__(self):
        pass

    def __repr__(self):
        pass

    @property
    def time_of_transaction(self):
        return self._timestamp

    @time_of_transaction.getter
    def time_of_transaction(self):
        return datetime.datetime.fromtimestamp(self._timestamp)

class Deposit(Transaction):

    def __init__(self, amount, type, currency= 'ILS', transaction_timestamp= time.time()):

        super().__init__(self, amount, currency, transaction_timestamp)

        if type in ['Cash via counter', 'Cash via machine', 'Cheque via counter', 'Cheque via machine', 'Cheque via app', 'Bank transfer', 'Direct debit']:
            self._type = type
        else:
            raise exceptions.InvalidType

class Withdraw(Transaction):

    def __init__(self, amount, type, currency= 'ILS', transaction_timestamp= time.time()):

        super().__init__(self, amount, currency, transaction_timestamp)

        if type in ['Cash via counter', 'Cash via machine', 'Cheque', 'Bank transfer', 'Direct debit', 'Credit card']:
            self._type = type
        else:
            raise exceptions.InvalidType

class Convert(Transaction):

    def __init__(self, amount_sold, rate, currency_sold, currency_bought , transaction_timestamp= time.time()):

        super().__init__(self, amount_sold, currency_sold, transaction_timestamp)

        self.to_currency = currency_bought
        self.amount_bought = amount_sold/rate
