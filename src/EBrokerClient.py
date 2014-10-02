import abc

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from BrokerRequest import BrokerRequest

import src.utils as u

class EBrokerClient:
    __metaclass__ = abc.ABCMeta

    def __init__(self, executable, login, password):
        self._browser = self._create_browser(executable)
        self.login(login, password)

    @abc.abstractmethod
    def _create_browser(self, executable):
        pass

    def login(self, login, password):
            self._browser.get("https://www.fio.cz/e-broker/e-broker.cgi")
            assert "e-Broker: Login" in self._browser.title
            self._browser.find_element_by_name("LOGIN_USERNAME").send_keys(login)
            self._browser.find_element_by_name("LOGIN_PASSWORD").send_keys(password)
            self._browser.find_element_by_name("SUBMIT").click()
            assert "Portfolio/Stav" in self._browser.title

    def close(self):
        self._browser.close()

    def get_broker_requests(self):
        self._browser.get("https://www.fio.cz/e-broker/e-pokyny.cgi")
        assert "Pokyny" in self._browser.title

        requests = []
        html = self._browser.execute_script("return document.getElementById('pokyny_full_table').innerHTML")
        soup = BeautifulSoup(html)
        for tr in soup.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) > 0:
                symbol = tds[1].contents[0].contents[0]
                price = u.str2float(tds[4].contents[0])
                amount = u.str2float(tds[5].contents[0])
                amount_satisfied = u.str2float(tds[6].contents[0])
                requests.append(BrokerRequest(symbol, price, amount, amount_satisfied))
        return requests

    def get_portfolio(self):
        self._browser.get("https://www.fio.cz/e-broker/e-portfolio.cgi")
        assert "Portfolio/Stav" in self._browser.title

        html = self._browser.execute_script("return document.getElementById('portfolio_table').innerHTML")
        soup = BeautifulSoup(html)
        trs = soup.find_all("tr")
        for i in range(2, len(trs) - 1):  # skip first two rows (table header) and the last one (summary)
            tds = trs[i].find_all("td")
            if len(tds) >= 4 :
                ticker = int(u.get_ticker_from_link(tds[2].contents[0]['href']))
                symbol = tds[2].contents[0].contents[0]
                amount = u.str2float(tds[3].contents[0])
                price = u.str2float(tds[4].contents[0].contents[0])
                print "%i %s %s %s %s" % (i, ticker, symbol, amount, price)


class PhantomJSClient(EBrokerClient):
    def _create_browser(self, phantom_exec):
        return webdriver.PhantomJS(phantom_exec)


class ChromeClient(EBrokerClient):
    def _create_browser(self, chrome_driver):
        opts = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : os.getcwd()}
        opts.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(executable_path=chrome_driver, chrome_options=opts)
        return browser
