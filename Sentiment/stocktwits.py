#!/usr/bin/python
import requests
import json
import datetime

INPUT_FILE = "tickers.txt"
FILENAME = "stocktwits.json"
REMOVE_OLDER_THAN = 21 # in days
KEEP_NULL_SENTIMENT = False

class Sentiment():
    def __init__(self):
        self.tickers = []
        self.data = {}

    # write to JSON file and properly formats the file
    def write_to_file(self, nameOfFile, data):
        with open(nameOfFile, 'w+') as f:
            print("Dumping JSON to", nameOfFile)
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))

    # get the data using StockTwits API
    def get_twits(self, ticker):
        url = "https://api.stocktwits.com/api/2/streams/symbol/{0}.json".format(ticker)
        response = requests.get(url).json()
        return response


    # Get data for each ticker in the tickers list
    def get_twits_list(self):
        for ticker in self.tickers:
            print("Getting data for", ticker)
            try:
                data = self.get_twits(ticker)
                symbol = data['symbol']['symbol']
                msgs = data['messages']
                self.data.update({symbol: msgs})
            except Exception as e:
                print(e)
                print("Error getting", ticker)
        return self.data

    def read_tickers(self):
        print("Reading tickers from", INPUT_FILE)
        f = open(INPUT_FILE, 'r')
        self.tickers = []
        for line in f:
            line = line.strip('\n')
            line = line.upper()
            line = line.strip('\t')
            self.tickers.append(line)
        return self.tickers

    # Removes data older than age_limit
    def remove_old(self, original = None, age_limit=REMOVE_OLDER_THAN):
        if original is None:
            original = self.data
        result = {}
        print("Removing tweets that are more than", age_limit, "days old")
        threshold = datetime.datetime.now() - datetime.timedelta(age_limit)

        for ticker in list(original.keys()):
            result[ticker] = []
            for msg in original[ticker]:
                dt = datetime.datetime.strptime(msg["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                sentiment = True if KEEP_NULL_SENTIMENT else msg["entities"]["sentiment"]
                if dt >= threshold and sentiment != None:
                    result[ticker].append(msg)
        return result


if __name__ == "__main__":
    x = input("Do you want to specify name of output file? Type y or Y for yes.\n").lower()

    if x.startswith("y"):
        filename = input("Enter JSON file name:\n")
        if not (filename.endswith(".json")):
            filename = filename + ".json"
        FILENAME = filename

    sentiment = Sentiment()

    codes = sentiment.read_tickers()
    twitdata = sentiment.get_twits_list(codes)
    twitdata = sentiment.remove_old(twitdata)
    sentiment.write_to_file(FILENAME, twitdata)
