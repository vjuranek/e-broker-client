import httplib2

from bs4 import BeautifulSoup

import ebroker.utils as utils

class EasyClickLots:
    
    lot_url = "http://www.rmsystem.cz/burza-sluzby/typy-obchodu/pokyn-easyclick"
    lot_table_id = "ec-lot"

    CEZ = 11392

    def __init__(self):
        self._lots = self.load_lots()

    def load_lots(self):
        http = httplib2.Http()
        (headers, html) = http.request(EasyClickLots.lot_url, "GET")
        soup = BeautifulSoup(html)
        table  = soup.find(id=EasyClickLots.lot_table_id)
        trs = table.find_all("tr")
        
        lots = {}
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            if(len(tds) >= 1):
                ticker = int(utils.get_ticker_from_link(tds[0].contents[0]['href']))
                name  =  tds[0].contents[0].contents[0]
                lot = int(tds[1].contents[0].replace(" ", ""))
                lots.update({ticker : EClot(ticker, name, lot)})

        return lots

    def get_lots(self):
        return self._lots

    def get_ec_lot(self, ticker):
        return self._lots.get(ticker)


class EClot:
    def __init__(self, ticker, name, lot):
        self._ticker = ticker
        self._name = name
        self._lot  = lot

    @property
    def ticker(self):
        return self._ticker

    @property
    def name(self):
        return self._name

    @property
    def lot(self):
        return self._lot

    def round_lots(self, amount):
        '''
        Round the amount always DOWN based on the minimum EC lot amount.
        Returned value is maximum multiple of EC lot, which is less or equal than given amount.
        E.g. if EC lot is 50, than 80 will be rounded to 50, 120 to 100 etc.
        '''
        return (amount // self._lot) * self._lot
