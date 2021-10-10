import requests
from bs4 import BeautifulSoup
import csv
import pdb
import datetime
# pdb.set_trace() - python step by step debugger command
print(datetime.datetime.now())
print("Finviz Financial Start")
url = "http://www.finviz.com/screener.ashx?v=161&f=geo_usa"
## url = "http://www.finviz.com/screener.ashx?v=121&f=fa_eps5years_pos,fa_epsqoq_pos,fa_epsyoy_pos,fa_epsyoy1_pos,fa_estltgrowth_pos,fa_sales5years_pos,fa_salesqoq_pos,ind_stocksonly,sh_avgvol_o50,sh_curvol_o0,sh_insiderown_o10,sh_instown_o10,sh_price_o10,ta_averagetruerange_o0.25,ta_beta_u1,ta_change_u,ta_changeopen_u,ta_highlow20d_nh,ta_highlow50d_nh,ta_highlow52w_nh,ta_sma20_pa,ta_sma200_pa,ta_sma50_pa"
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)
# print("==============")
# print(soup)
# print("==============")
firstcount = soup.find_all('select', {"id": "pageSelect"})
lastnum = len(firstcount) - 1
print("==============")
print(firstcount)
print("==============")

lastpagenum = firstcount[lastnum].attrs['value']
currentpage = int(lastpagenum)

alldata = []
templist = []
# Overview = 111, Valuation = 121, Financial = 161, Ownership = 131, Performance = 141
#pagesarray = [111,121,161,131,141]
titleslist = soup.find_all('td', {"class": "table-top"})
titleslisttickerid = soup.find_all('td', {"class": "table-top-s"})
titleticker = titleslisttickerid[0].text
titlesarray = [title.text for title in titleslist]

titlesarray.insert(1, titleticker)
i = 0

while(currentpage > 0):
    i += 1
    print(str(i) + " page(s) done")
    secondurl = "http://www.finviz.com/screener.ashx?v=" + str(161) + "&f=geo_usa" + "&r=" + str(currentpage)
    secondresponse = requests.get(secondurl)
    secondhtml = secondresponse.content
    secondsoup = BeautifulSoup(secondhtml)
    stockdata = secondsoup.find_all('a', {"class": "screener-link"})
    stockticker = secondsoup.find_all('a', {"class": "screener-link-primary"})
    datalength = len(stockdata)
    tickerdatalength = len(stockticker)

    while(datalength > 0):
        templist = [stockdata[datalength - 17].text, stockticker[tickerdatalength - 1].text, stockdata[datalength - 16].text, stockdata[datalength - 15].text, stockdata[datalength - 14].text, stockdata[datalength - 13].text, stockdata[datalength - 12].text, stockdata[datalength - 11].text, stockdata[datalength - 10].text, stockdata[datalength - 9].text, stockdata[datalength - 8].text, stockdata[datalength - 7].text, stockdata[datalength - 6].text, stockdata[datalength - 5].text, stockdata[datalength - 4].text, stockdata[datalength - 3].text, stockdata[datalength - 2].text, stockdata[datalength - 1].text, ]
        alldata.append(templist)
        templist = []
        datalength -= 17
        tickerdatalength -= 1
    currentpage -= 20

with open('stockfinancial.csv', 'wb') as csvfile:
    financial = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=titlesarray)
    financial.writeheader()

    for stock in alldata:
        financial.writerow({titlesarray[0]: stock[0], titlesarray[1]: stock[1], titlesarray[2]: stock[2], titlesarray[3]: stock[3], titlesarray[4]: stock[4], titlesarray[5]: stock[5], titlesarray[6]: stock[6], titlesarray[7]: stock[7], titlesarray[8]: stock[8], titlesarray[9]: stock[9], titlesarray[10]: stock[10], titlesarray[11]: stock[11], titlesarray[12]: stock[12], titlesarray[13]: stock[13], titlesarray[14]: stock[14], titlesarray[15]: stock[15], titlesarray[16]: stock[16], titlesarray[17]: stock[17]})

print(datetime.datetime.now())
print("Finviz Financial Completed")
