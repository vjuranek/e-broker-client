class Money:

    def __init__(self, currency, free_money):
        self._currency = currency
        self._free_money = free_money

    @property
    def currency(self):
        return self._currency

    @property
    def free_money(self):
        return self._free_money
