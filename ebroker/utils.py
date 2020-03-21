import re
import time

from datetime import date, timedelta


def get_ticker_from_link(link):
    m = re.search(r"\d{3,}", link)
    return m.group(0)


def str2int(to_convert):
    if not to_convert:  # empty string
        return 0
    num = 0
    try:
        int(to_convert.replace(" ", ""))
    except ValueError:
        pass  # TODO: log exception
    return num


def str2float(to_convert):
    if not to_convert:  # empty string
        return 0

    stripped = to_convert.replace(" ", "")
    if stripped.find(",") > 0:
        stripped = stripped.replace(",", ".")
    num = 0
    try:
        num = float(stripped)
    except ValueError:
        pass  # TODO: log exception
    return num


def shift_day(day_str, day_delta):
    day_elem = day_str.parse(".")
    day = date(day_elem[2], day_elem[1], day_elem[0])
    day_shifted = day + timeshift(days=day_delta)
    return "%i.%i.%i" % (day_shifted.day, day_shifted.month, day_shifted.year)


def shift_today(day_delta):
    day_shifted = date.today() + timedelta(days=day_delta)
    return "%i.%i.%i" % (day_shifted.day, day_shifted.month, day_shifted.year)


def sleep(seconds):
    print("Sleeping for %i seconds" % seconds)
    time.sleep(seconds)


def sort_requests_by_amount(requests, reverse=True):
    return sorted(requests, key=lambda request: request.amount, reverse=reverse)


def sort_requests_by_price(requests, reverse=True):
    return sorted(requests, key=lambda request: request.price, reverse=reverse)


def get_sell_requests(requests):
    return filter(lambda req: req.req_type == BrokerRequest.SELL, requests)


def get_buy_requests(requests):
    return filter(lambda req: req.req_type == BrokerRequest.BUY, requests)
