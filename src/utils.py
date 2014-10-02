import re

def get_ticker_from_link(link):
    m = re.search("\d{3,}", link)
    return m.group(0)

def str2int(to_convert):
    return int(to_convert.replace(" ", ""))

def str2float(to_convert):
    return float(to_convert.replace(" ", "").replace(",", "."))
