#!/usr/bin/python
import requests
import json
import datetime


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
        # error handling
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
    print("Reading tickers from \"tickers.txt\":")
    f = open("tickers.txt", 'r')
    names = []
    # read tickers from tickers.txt
    for line in f:
    	line = line.strip('\n')
    	line = line.upper()
    	line = line.strip('\t')
    	names.append(line)
    print(names)
    return names


def remove_old(original, age_limit=30):
    print("Removing tweets that are more than", age_limit, "days old")
    threshold = datetime.datetime.now() - datetime.timedelta(age_limit)
    result = {}
    # checks if data is more than age_limit and removes if so
    for ticker in list(original.keys()):
        result[ticker] = []
        for msg in original[ticker]:
            dt = datetime.datetime.strptime(msg["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if dt >= threshold:
                result[ticker].append(msg)
    return result

# default file name
FILENAME = "stocktwits.json"

if __name__ == "__main__":

    # Optional file output - Make sure you are using Python 3!
    # To check, import sys and then print(sys.version)
    x = input("Do you want to specify name of output file? Type y or Y for yes. \n").lower()

    # Execute this code if option is taken
    if x.startswith("y") or x.startswith("Y"):
        filename = input("What is file name? \n")
        if not (filename.endswith(".json")):
            filename = filename + ".json"
        FILENAME = filename

    # get list of ticker codes
    codes = read_tickers()

    # print(get_twits('AAPL'))
    # for each ticker code get the data
    twitdata = get_twits_list(codes)
    # remove the data if older than X days, useless
    twitdata = remove_old(twitdata, 21)
    # write to json file
    write_to_file(FILENAME, twitdata)
