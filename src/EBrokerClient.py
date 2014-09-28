import abc

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from BrokerRequest import BrokerRequest

class EBrokerClient:
    __metaclass__ = abc.ABCMeta

    def __init__(self, executable, login, password):
        self.__browser = self._create_browser(executable)
        self.login(login, password)
        return

    @abc.abstractmethod
    def _create_browser(self, executable):
        return

    def login(self, login, password):
            self.__browser.get("https://www.fio.cz/e-broker/e-broker.cgi")
            assert "e-Broker: Login" in self.__browser.title
            self.__browser.find_element_by_name("LOGIN_USERNAME").send_keys(login)
            self.__browser.find_element_by_name("LOGIN_PASSWORD").send_keys(password)
            self.__browser.find_element_by_name("SUBMIT").click()
            assert "Portfolio/Stav" in self.__browser.title

    def close(self):
        self.__browser.close()

    def get_broker_requests(self):
        self.__browser.get("https://www.fio.cz/e-broker/e-pokyny.cgi")
        assert "Pokyny" in self.__browser.title

        requests = []
        html = self.__browser.execute_script("return document.getElementById('pokyny_full_table').innerHTML")
        soup = BeautifulSoup(html)
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) > 0:
                symbol = tds[1].contents[0].contents[0]
                price = tds[4].contents[0]
                amount = tds[5].contents[0]
                amount_satisfied =  tds[6].contents[0]
                requests.append(BrokerRequest(symbol, price, amount, amount_satisfied))
        return requests

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
