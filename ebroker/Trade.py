class Trade:

    def __init__(self, date, stock_symbol, price, amount, currency):
        self._date = date
        self._stock_symbol = stock_symbol
        self._price = price
        self._amount = amount
        self._currency = currency

    @property
    def date(self):
        return self._date

    @property
    def stock_symbol(self):
        return self._stock_symbol

    @property
    def price(self):
        return self._price

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    def __str__(self):
        return "Date: {}, symbol: {}, price: {}, amount: {}, currency: {}".format(
            self._date, self._stock_symbol, self._price, self._amount, self._currency)
