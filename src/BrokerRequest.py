class BrokerRequest:
    def __init__(self, symbol, price, amount, amount_satisfied):
        self._symbol = symbol
        self._price = price
        self._amount  = amount
        self._amount_satisfied = amount_satisfied

    @property
    def symbol(self):
        return self._symbol

    @property
    def price(self):
        return self._price

    @property
    def amount(self):
        return self._amount

    @property
    def amount_satisfied(self):
        return self._amount_satisfied

    def is_satisfied(self):
        return (self._amount - self._amount_satisfied) == 0
