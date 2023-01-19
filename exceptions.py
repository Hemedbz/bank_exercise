class BankException(Exception):
    pass

class NotAllowed(BankException):
    pass

class InvalidType(BankException):
    pass