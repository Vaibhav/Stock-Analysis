import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import json
from pprint import pprint

'''
def sentimentScore(texts):
	analyzer = SentimentIntensityAnalyzer()
	scores = []
	for text in texts:
        score = SentimentIntensityAnalyzer().polarity_scores(text)["compound"]
    try: return score
    except ZeroDivisionError: return 0


text = "shares jump as shipments more than double winning"
print(sentimentScore(text))
'''

nltk.download('vader_lexicon')

# --- examples -------
sentences = ["VADER is smart, handsome, and funny.",      # positive sentence example
            "VADER is not smart, handsome, nor funny.",   # negation sentence example
            "VADER is smart, handsome, and funny!",       # punctuation emphasis handled correctly (sentiment intensity adjusted)
            "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
            "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
            "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
            "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",# booster words & punctuation make this close to ceiling for score
            "The book was good.",                                     # positive sentence
            "The book was kind of good.",                 # qualified positive sentence is handled correctly (intensity adjusted)
            "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
            "At least it isn't a horrible book.",         # negated negative sentence with contraction
            "Make sure you :) or :D today!",              # emoticons handled
            "Today SUX!",                                 # negative slang with capitalization emphasis
            "Today only kinda sux! But I'll get by, lol"  # mixed sentiment example with slang and constrastive conjunction "but"
			]

examples = [
"$AAPL Apple Dividend Stock Analysis  http://dividendvaluebuilder.com/apple-aapl-dividend-stock-analysis/ #dividend #yield #tech #cashcow #growth #DVB #AAAMP",
"Unusual Options Activity - 02.24.2017 - $AAPL $NKE $PBR $JCP $FDX $MBLY $LUV $CMCSA $MTG $ATVI",
"$AAPL The British pound dipped noticeably in early Asian trade on Monday watching the currency for any Brexit-related jitters SELL",
"$AAPL watch the red carpet tomorrow morningFUTURES",
"$SPY  $AAPL $NFLX $AMZN. And tge oscar goes to Hillarious.   C l i t o n",
"$AAPL $SPY First award nomination goes to a guy named a l i.",
"$AAPL $SPY J i m m y. P e r p e t u a l l y    i llo gically  d r u n k.",
"$AAPL one trick pony, back up the truck at $120, soon",
"$AAPL An introduction to Generative Adversarial Networks https://github.com/AYLIEN/gan-intro",
"$AAPL Apple&#39;s first AI research paper focuses on computer vision http://appleinsider.com/articles/16/12/26/apples-first-ai-research-paper-focuses-on-computer-vision via @AppleInsider",
"$NVDA never catch falling knife!!! $AAPL 135 - 90 $GPRO 67 to 7 , $LL 120 to 9 , $MU 33 to 7 , baba 112 to 58 now $NVDA",
"five promises :  $AAPL $GS $C $FB $BA any three can triple or quadruple your girth or worth. 2019 calls.",
"$AAPL May 11th, 2017 Applied Artificial Intelligence Conference https://www.eventbrite.com/e/applied-artificial-intelligence-conference-2017-tickets-30560299679?aff=es2 $AMZN",
"$AAPL about 2 years ago Cook said India&#39;s a long game for Apple 7-10 years. Right on schedule!",
"$AAPL 140c June &#39;17",
"Google Assistant Expands Past Pixel In Fight Vs. Apple&#39;s Siri, Amazon&#39;s Alexa: http://www.investors.com/news/technology/google-assistant-expands-past-pixel-in-fight-vs-apples-siri-amazons-alexa/ $GOOGL $AAPL $AMZN $GPRO",
"Stocks Set To Open At Highs: Workday, Priceline Earnings Due; Trump Looms: http://www.investors.com/market-trend/stock-market-today/dow-looks-to-extend-run-workday-priceline-earnings-due-trump-looms/ $WDAY $PCLN $SNAP $UNH $AAPL $GOOGL $AMZN",
"$AAPL 140p June &#39;17",
"$AAPL 100c June &#39;17",
"$AAPL As a bag holder it hurts me to read this.. http://appleinsider.com/articles/17/02/24/apple-inc-valuation-now-more-than-134-billion-greater-than-alphabets-google guess I shall bag hold this for 10 more years. what do u think?",
"$AAPL Faber on Apple U.S. stock market is vulnerable to a seismic sell-off—one that could start any time in a very unassuming way.",
"$AAPL Apple Inc. valuation now more than $134 billion greater than Alphabet&#39;s Google http://appleinsider.com/articles/17/02/24/apple-inc-valuation-now-more-than-134-billion-greater-than-alphabets-google @AppleInsider",
"$AAPL Someone showed me this-funny.",
"THE BEST WAY TO TEACH YOUR KIDS ABOUT TAXES IS BY EATING 30% OF THEIR ICE CREAM.",
"$AAPL Biz stats, insider trades, news, chart and more via finviz http://finviz.com/quote.ashx?t=AAPL",
"$AAPL option cash value for March &#39;17 using Google data",
"$AAPL volatility, price, &amp; volume",
"$TSLA $AMZN $AAPL $FB WHAT SIDE OF HISTORY ARE YOU ON???????"
]

bullish = 0
bearish = 0

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


def sentimentScore(sentences):
	analyzer = SentimentIntensityAnalyzer()
	results = []
	for sentence in sentences:
		vs = analyzer.polarity_scores(sentence)
		print("vs: " + str(vs))
		results.append(vs)
	return results

# sentimentScore(examples)

with open('feb26.json') as data_file:
    data = json.load(data_file)

list1 = []

for i in data['AAPL']:
	list1.append(i['body'])
	# print(type(i['entities']['sentiment']))
	if not(i['entities']['sentiment'] is None):
		sentiment = i['entities']['sentiment']['basic']
		if (sentiment == "bullish" or sentiment == "Bullish"):
			bullish += 1
		else:
			bearish += 1

tmp = sentimentScore(list1)
sum = 0.0
count = 0.0
for j in tmp:
	if j['compound'] != 0:
		pprint(j['compound'])
		sum += j['compound']
		count += 1.0

print("avg: " + str(sum/count))
print(bullish)
print(bearish)
