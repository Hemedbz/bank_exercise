import exceptions
import transcations
import datetime

class Account:

    def __init__(self, account_number: str, holders: list):
        self.account_number = account_number
        self.account_holders = holders
        self.ILS_balance = 0
        self.can_hold_foreign = False
        self.USD_balance = 0
        self.EUR_balance = 0
        self.credit_limit = 0
        self.transactions_log = {}

    def __str__(self):
        return f"Account {self.account_number}\n" \
               f"current ILS balance: {self.ILS_balance}\n" \
               f"maximum credit limit: {self.credit_limit}"

    def add_holder(self, new_holder):
        #if new_holder has all the details it must have:
        self.account_holders.append(new_holder)
        #else: exception

    def deposit(self, transaction: transcations.Transaction):

        match transaction.currency:
            case 'ILS':
                self.ILS_balance += transaction.amount
            case 'USD':
                if self.can_hold_foreign:
                    self.USD_balance += transaction.amount
                else:
                    raise exceptions.NotAllowed
            case 'EUR':
                if self.can_hold_foreign:
                    self.EUR_balance += transaction.amount
                else:
                    raise exceptions.NotAllowed

        #add to transaction log
        self.transactions_log[transaction.timestamp] = ['deposit', transaction.currency, transaction.amount]]

        return self.transactions_log, self.balance

    def withdraw(self, transaction: transcations.Transaction):
        match transaction.currency:
            case 'ILS':
                if self.ILS_balance+self.credit_limit >= transaction.amount:
                    self.ILS_balance -= transaction.amount
                else:
                    raise exceptions.NotAllowed
            case 'USD':
                if self.can_hold_foreign:
                    if self.USD_balance >= transaction.amount:
                        self.USD_balance -= transaction.amount
                    else:
                        raise exceptions.NotAllowed
                else:
                    raise exceptions.NotAllowed
            case 'EUR':
                if self.can_hold_foreign:
                    if self.EUR_balance >= transaction.amount:
                        self.EUR_balance -= transaction.amount
                    else:
                        raise exceptions.NotAllowed
                else:
                    raise exceptions.NotAllowed

        #add to transaction log
        self.transactions_log[transaction.timestamp] = ['withdraw', transaction.currency, transaction.amount]]

        return self.transactions_log, self.balance

    def convert(self, amount_from, amount_to, from_currency, to_currency): #will change to transaction class later
        if not self.can_hold_foreign:
            raise exceptions.NotAllowed

        match from_currency:
            case 'ILS':
                if amount_from > self.ILS_balance:
                    raise exceptions.NotAllowed
                self.ILS_balance -= amount_from
                match to_currency:
                    case 'USD':
                        self.USD_balance += amount_to
                    case 'EUR':
                        self.EUR_balance += amount_to

            case 'USD':
                if amount_from > self.USD_balance:
                    raise exceptions.NotAllowed
                self.USD_balance -= amount_from
                match to_currency:
                    case 'ILS':
                        self.ILS_balance += amount_to
                    case 'EUR':
                        self.EUR_balance += amount_to

            case 'EUR':
                if amount_from > self.EUR_balance:
                    raise exceptions.NotAllowed
                self.EUR_balance -= amount_from
                match to_currency:
                    case 'ILS':
                        self.ILS_balance += amount_to
                    case 'USD':
                        self.USD_balance += amount_to
        self.transactions_log[transaction.timestamp] = ['convert', to_currency, from_currency, amount_from, amount_to]
        return self.balance


    @property
    def balance(self):
        return \
            {'ILS': self.ILS_balance, 'USD': self.USD_balance, 'EUR': self.EUR_balance}

    @balance.getter
    def balance(self):
        pass

    def get_transactions_per_date(self, given_date):
        relevant_transactions = []
        for transaction_timestamp in self.transactions_log:
            if datetime.date(transaction_timestamp) == given_date:
                relevant_transactions.append({transaction_timestamp:self.transactions_log[transaction_timestamp]})

    def get_monthly_report(self, given_month):
        pass

    def get_annual_report(self, given_year):
        pass
