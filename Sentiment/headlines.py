#!/usr/bin/python

import requests
import json
import datetime
from bs4 import BeautifulSoup


names = ["AAPL", "MMM", "AXP", "T", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DD", "XOM", "GE", "GS", "HD", "IBM",
         "INTL", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WMT", "NVS",
         "TM", "PTR", "WFC", "BABA", "TWTR", "FB", "GOOG", "AAPL", "YHOO", "BP", "PEP"]


def get_headlines(ticker):
    URL = "http://www.finviz.com/quote.ashx?t=" + ticker
    connection = requests.get(URL).text.encode("utf-8").decode('ascii', 'ignore')
    soup = BeautifulSoup(connection, "html.parser")
    print("Downloaded data")
    return soup.find(id="news-table").findAll("tr")


def extract_headlines(headlines):
    ret = []
    date = ""
    for headline in headlines:
        tds = headline.findAll("td")
        if len(tds) >= 2 and tds[1].find("script") is None:
            timestamp = tds[0].text.strip()
            url = tds[1].find("a").attrs["href"]
            if timestamp != "":
                timestamp_split = timestamp.split(" ")
                if len(timestamp_split) == 2:
                    date = timestamp_split[0] + " "
                else:
                    timestamp = date + timestamp
                append = {"timestamp": timestamp,
                          "url": url}
                ret.append(append)
    return ret


def get_all_headlines(tickers):
    ret = {}
    for ticker in tickers:
        print("Getting headlines for", ticker)
        try:
            headlines = get_headlines(ticker)
            print("Received headlines")
            extracted = extract_headlines(headlines)
            ret.update({ticker: extracted})
        except Exception as e:
            print(e)
            print("Error getting", ticker)
    return ret


def read_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def write_to_file(filename, data):
    with open(filename, 'w+') as f:
        print("Dumping JSON to", filename)
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))


FILENAME = "headlines.json"

if __name__ == "__main__":

    # Optional file output
    x = input("Do you want to specify name of output file?")

    # Execute this code if option is taken
    if x.startswith("y") or x.startswith("Y"):
        filename = input("What is file name?")
        if not (filename.endswith(".json")):
            filename = filename + ".json"
        FILENAME = filename

    # old = read_from_file(FILENAME)
    new = get_all_headlines(names)
    # new = append(old, new)
    write_to_file(FILENAME, new)
