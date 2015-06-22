class BrokerRequest:
    
    BUY = 1
    SELL = -1

    def __init__(self, ticker, price, amount, symbol = "Unknown", amount_satisfied = 0, req_type = 0):
        self._ticker = ticker
        self._price = price
        self._amount  = amount
        self._symbol = symbol
        self._amount_satisfied = amount_satisfied
        self._req_type = req_type

    @property
    def ticker(self):
        return self._ticker        

    @property
    def price(self):
        return self._price

    @property
    def amount(self):
        return self._amount

    @property
    def symbol(self):
        return self._symbol

    @property
    def amount_satisfied(self):
        return self._amount_satisfied

    @property
    def req_type(self):
        return self._req_type

    def is_satisfied(self):
        return (self._amount - self._amount_satisfied) == 0

    def is_nonempty(self):
        '''
        Returns true if request did anything, i.e. if at least some stocks were sold or bought.
        Typically empty requests are those, which were rejected, canceled or cance requests themselves.
        '''
        return self._amount_satisfied != 0
