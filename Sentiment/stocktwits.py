#!/usr/bin/python
import requests
import json
import datetime

INPUT_FILE = "tickers.txt"
FILENAME = "stocktwits.json"
REMOVE_OLDER_THAN = 21 # in days
KEEP_NULL_SENTIMENT = False

# write to JSON file and properly formats the file
def write_to_file(nameOfFile, data):
    with open(nameOfFile, 'w+') as f:
        print("Dumping JSON to", nameOfFile)
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))


# get the data using StockTwits API
def get_twits(ticker):
    url = "https://api.stocktwits.com/api/2/streams/symbol/{0}.json".format(ticker)
    response = requests.get(url).json()
    return response


# loops through to get data for each ticker in the tickers list
def get_twits_list(tickers):
    ret = {}
    for ticker in tickers:
        print("Getting data for", ticker)
        try:
            data = get_twits(ticker)
            symbol = data['symbol']['symbol']
            msgs = data['messages']
            ret.update({symbol: msgs})
        except Exception as e:
            print(e)
            print("Error getting", ticker)
    return ret


def read_tickers():
    print("Reading tickers from", INPUT_FILE)
    f = open(INPUT_FILE, 'r')
    names = []
    for line in f:
    	line = line.strip('\n')
    	line = line.upper()
    	line = line.strip('\t')
    	names.append(line)
    return names


def remove_old(original, age_limit=30):
    print("Removing tweets that are more than", age_limit, "days old")
    threshold = datetime.datetime.now() - datetime.timedelta(age_limit)
    result = {}
    # Checks if data is more than age_limit and removes
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

    codes = read_tickers()
    twitdata = get_twits_list(codes)
    twitdata = remove_old(twitdata, REMOVE_OLDER_THAN)
    write_to_file(FILENAME, twitdata)
