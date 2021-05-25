#!/usr/bin/python
import requests
import json
from bs4 import BeautifulSoup

INPUT_FILE = "tickers.txt"
FILENAME = "headlines.json"


# TODO: Needs to support JS when scraping Finviz
class Headlines():
    def __init__(self) -> None:
        self.data = {}
        self.tickers = [
            "AAPL", "MMM", "AXP", "T", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DD", "XOM", "GE", "GS", "HD", "IBM",
            "INTL", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UNH", "VZ", "V", "WMT", "NVS", "TM",
            "PLTR", "WFC", "BABA", "TWTR", "FB", "GOOG", "AAPL", "YHOO", "BP", "PEP"
        ]

    @staticmethod
    def get_headlines(ticker):
        print("Downloading data..")
        URL = "http://www.finviz.com/quote.ashx?t=" + ticker
        connection = requests.get(URL).text.encode("utf-8").decode('ascii', 'ignore')
        soup = BeautifulSoup(connection, "html.parser")
        return soup.find(id="news-table").findAll("tr")

    def extract_headlines(self, headlines):
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

    def get_all_headlines(self, tickers=None):
        if tickers is None:
            tickers = self.tickers
        for ticker in tickers:
            print("Getting headlines for", ticker)
            try:
                headlines = Headlines.get_headlines(ticker)
                print("Received headlines")
                extracted = self.extract_headlines(headlines)
                self.data.update({ticker: extracted})
            except Exception as e:
                print(e)
                print("Error getting", ticker)
        return self.data

    def write_to_file(self, filename, data):
        with open(filename, 'w+') as f:
            print("Dumping JSON to", filename)
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))

    def read_tickers(self, input_file = INPUT_FILE):
        print("Reading tickers from", input_file)
        f = open(input_file, 'r')
        for line in f:
            line = line.strip('\n\t')
            line = line.upper()
            self.tickers.append(line)
        return self.tickers


if __name__ == "__main__":
    x = input("Do you want to specify name of output file?")
    if x.startswith("y") or x.startswith("Y"):
        filename = input("What is file name?")
        if not (filename.endswith(".json")):
            filename = filename + ".json"
        FILENAME = filename

    headlines = Headlines()
    data = headlines.get_all_headlines()
    headlines.write_to_file(FILENAME, data)
