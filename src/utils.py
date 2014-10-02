import re

def get_ticker_from_link(link):
    m = re.search("\d{3,}", link)
    return m.group(0)
