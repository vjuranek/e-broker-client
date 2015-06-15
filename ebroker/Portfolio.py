class PortfolioItem:
    def __init__(self, ticker, symbol, amount, price):
        self._ticker = ticker
        self._symbol = symbol
        self._amount  = amount
        self._price = price

    @property
    def ticker(self):
        return self._ticker

    @property
    def symbol(self):
        return self._symbol

    @property
    def amount(self):
        return self._amount

    @property
    def price(self):
        return self._price
