import json
import re
import threading
import timeit
import urllib.request, urllib.error, urllib.parse
from time import gmtime, strftime

import RSS_URL
import requests
from SA_Scrape import getSaURL
from newspaper import Article
from vaderSentiment import vaderSentiment

#########################################
## ANALYSIS PARAMETERS

# setting lock variable for threading
global lock
lock = threading.Lock()

def SaSentimentRSS(symbol):
    url = "http://seekingalpha.com/symbol/" + symbol + ".xml"
    url2 = "http://feeds.finance.yahoo.com/rss/2.0/headline?s=" + symbol + "&region=US&lang=en-US"
    url3 = "http://www.google.ca/finance/company_news?q=" + symbol + "&output=rss"
    # gets list of links from above RSS feed
    NewsURLs = getSaURL(url)
    NewsURLs += RSS_URL.getURLs2(url2)
    NewsURLs += RSS_URL.getURLs2(url3)

    # String to be written to file
    toBeWrittenToFile = ''

    for link in NewsURLs:
        try:
            # gets article portion of the htmltext
            a = Article(link)
            a.download()
            a.parse()

            # not working if it's RSS title link or has no title or cannot be accessed
            if symbol in a.title and not 'Earnings Call Webcast' in a.title and not 'Stock Market Insights' in a.title and not '400 Bad Request' in a.title and not '403 Forbidden' in a.title and a.title != '':
                UnicodeArticle = a.text
                StringArticle = UnicodeArticle.encode('ascii', 'ignore')
                StrippedArticle = StringArticle.replace('\n', '')

                # not working with articles less than 300 words
                if len(StrippedArticle) > 200:

                    # remove ascii symbols
                    ArticleTitle = a.title.encode('ascii', 'ignore').replace(',', '')

                    # filters out irrelevant articles
                    if 'Transcript' not in ArticleTitle and 'Summary' not in ArticleTitle:

                        # writes sentiment from sentiment API to file
                        # locks this block so that only one thread can write to file at a time

                        # vader sentiment dictionary
                        s = vaderSentiment.sentiment(StrippedArticle)

                        # not writing articles with zero sentiments
                        # collect a string to be written to file
                        if s['compound'] != 0:
                            # print(ArticleTitle)
                            toBeWrittenToFile += (
                                str(symbol) + ',' + str(s['neg']) + ',' + str(s['neu']) + ',' + str(s['pos']) + ',' + str(
                                    s['compound']) + ',' + ArticleTitle + ',' + str(link) + '\n')

        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
    # write variable to file
    lock.acquire()
    try:
        myfile.write(toBeWrittenToFile)
    finally:
        lock.release()


start = timeit.default_timer()

# creating file in local 'data' directory
myfile = open('data\SAsentiment' + strftime("%Y-%m-%d", gmtime()) + '.csv', 'w+')
myfile.write('Ticker,neg,neu,pos,compound,Title,url' + '\n')
myfile.close()

# Getting all symbols into list
symbolfile = open("SAsymbols.txt")
symbolslistR = symbolfile.read()
symbolslist = symbolslistR.split('\n')

symbolfile.close()

# tracks threads running
threadlist = []

# open "myfile" file for SentimentRSS to write in
myfile = open('data\SAsentiment' + strftime("%Y-%m-%d", gmtime()) + '.csv', 'a')

for u in symbolslist:
    t = threading.Thread(target=SaSentimentRSS, args=(u,))
    t.start()
    threadlist.append(t)
    # sets top limit of active threads to 100
    while threading.activeCount() > 3:
        a = 0
# finishes threads before closing file
for b in threadlist:
    b.join()

print(('# of threads: ' + str(len(threadlist))))
# close file
myfile.close()
# timer
stop = timeit.default_timer()
print((stop - start))


###############################################
post_url = 'http://text-processing.com/api/sentiment/'

data_text = 'text='


def analyse(str):
    post = requests.post(url=post_url, data='text=' + str)

    ## JSON PARSING
    pjson_data = json.loads(post.content)

    pos = pjson_data['probability']['pos']
    neg = pjson_data['probability']['neg']
    neutral = pjson_data['probability']['neutral']

    return {'pos': pos, 'neg': neg, 'neutral': neutral}


def getSaURL(rss):
    # setup your header, add anything you want
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive'}

    request = urllib.request.Request(rss, headers=hdr)
    page = urllib.request.urlopen(request)
    RSSContent = page.read()

    regex = '<link>(.+?)</link>'
    pattern = re.compile(regex)
    links = re.findall(pattern, RSSContent)
    return links
