#!/usr/bin/python
import urllib2
import json
import datetime

def get_tweets(ticker):
    url = "https://api.stocktwits.com/api/2/streams/symbol/{0}.json".format(ticker)
    connection = urllib2.urlopen(url)
    data = connection.read()
    connection.close()
    return json.loads(data)


def get_tweets_list(tickers):
    ret = {}
    for ticker in tickers:
        print "Getting data for", ticker
        try:
            data = get_tweets(ticker)
            symbol = data['symbol']['symbol']
            msgs = data['messages']
            ret.update({symbol: msgs})
        except Exception as e:
            print e
            print "Error getting", ticker
    return ret


def remove_old(original, age_limit=30):
    print "Removing tweets that are more than", age_limit, "days old"
    threshold = datetime.datetime.now() - datetime.timedelta(age_limit)
    result = {}
    for ticker in original.keys():
        result[ticker] = []
        for msg in original[ticker]:
            dt = datetime.datetime.strptime(msg["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if dt >= threshold:
                result[ticker].append(msg)
    return result


def write_to_file(filename, data):
    with open(filename, 'w+') as f:
        print "Dumping JSON to", filename
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))



FILENAME = "stocktwits.json"  # change as necessary

if __name__ == "__main__":

	print "Reading tickers from \"tickers.txt\":"
    f = open("tickers.txt", 'r')
    names = []
    for line in f:
        line = line.strip('\n')
        line = line.strip('\t')
        names.append(line);

    print names + "\n"

    twitdata = get_tweets_list(names)
    twitdata = remove_old(twitdata)
    write_to_file(FILENAME, twitdata)
