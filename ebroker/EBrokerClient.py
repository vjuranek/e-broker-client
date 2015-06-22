# -*- coding: utf-8 -*-

import abc
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from BrokerRequest import BrokerRequest
from Config import Config, Credentials
from Money import Money

import ebroker.utils as u

class EBrokerClient:
    __metaclass__ = abc.ABCMeta

    def __init__(self, executable, config_file = None):     
        self._browser = self._create_browser(executable)
        self._config = Config(config_file)
        credentials = self._config.credentials()
        self.login(credentials.login, credentials.password)

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
        #html = self._browser.execute_script("return document.getElementById('pokyny_full_table').innerHTML")
        html = self._browser.find_element_by_id("pokyny_full_table").get_attribute("innerHTML")
        soup = BeautifulSoup(html)
        trs = soup.find_all("tr")
        for i in range(2, len(trs)): 
            tds = trs[i].find_all("td")
            if len(tds) >= 6:
                ticker = int(u.get_ticker_from_link(tds[1].contents[0]['href']))
                symbol = tds[1].contents[0].contents[0]
                price = u.str2float(tds[4].contents[0])
                amount = u.str2float(tds[5].contents[0])
                amount_satisfied = u.str2float(tds[6].contents[0])
                requests.append(BrokerRequest(ticker, price, amount, symbol, amount_satisfied))
        return requests

    def get_nonepmty_requests(self):
        requests = self.get_broker_requests()
        for req in requests:
            if req.is_nonempty():
                yield req
                
    
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

    def send_request(self, request):
        self._browser.get("https://www.fio.cz/e-broker/e-pokyn_univ.cgi?ceninaId=%i&smer=%i" % (request.ticker, request.req_type))
        #assert "???" in self._browser.title #TODO add assert
        self._browser.find_element_by_name("pocet").send_keys(request.amount)
        self._browser.find_element_by_name("cena").send_keys(request.price)
        valid_till_element = self._browser.find_element_by_name("platnyDo")
        valid_till_element.clear()
        valid_till_element.send_keys(u.shift_today(14))
        #switch to RMS
        self._browser.find_element_by_xpath('//select[@id="trh"]/option[@value="RMS"]').click()
        self._browser.find_element_by_id("easyClick").click()
        self._browser.find_element_by_id("buttonValidate").click()
        #assert "???" in self._browser.title #TODO add assert
        self._browser.find_element_by_xpath('//input[@value="Odeslat"]').click()
        #assert "???" in self._browser.title #TODO add assert

    def get_money(self):
        self._browser.get("https://www.fio.cz/e-broker/e-penize.cgi")
        assert u"Peníze" in self._browser.title

        money = []
        html = self._browser.find_element_by_id("penize_table").get_attribute("innerHTML")
        soup = BeautifulSoup(html)
        trs = soup.find_all("tr")
        for i in range(2, len(trs)):
            tds = trs[i].find_all("td")
            if len(tds) >= 9:
                currency = tds[2].contents[0]
                free_money = u.str2float(tds[8].contents[0])
                money.append(Money(currency, free_money))
        return money

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
