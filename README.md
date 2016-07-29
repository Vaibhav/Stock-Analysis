# Stock Analysis

This repository contains python scripts that I am devleoping to perform analysis on stock prices and visualization of stock prices and other data such as volume.  

Some of the goals I want to achieve with this project include: 
  - Get the data I need from Yahoo Finance or other API. Able to speicfy what I need and the time range. 
  - Different regression implementations on the close price data. (Linear, SVM, etc.) Possibly try to fit a polynomial function which follows the data.  
  - Predicting Stock price for the next day. 

## Results

Using my code for linear regression and Nvidia's (NVDA) stock prices of each day. I got a slope of 0.1850399032986727 and a y intercept of 24.54867003005582. The 50.08 number is the price predicted for the next day based on the linear formula it calculated.

```python
[0.1850399032986727, 24.54867003005582]
50.0841766853
```

This is insanely accurate. I decided to compare this result with result's I would get with a widely known API, famous for machine learning and other regression tools in python. The API is called sci-kit-learn.  

```python
[ 0.1850399]
```

Using the linear regression offered from the API We get almost the same result, except with less accuracy.  

My method outputs a number with greater significant figures. 

###Screenshots

Using my regression method: 

![Linear Regression performed on NVDA Stock dat from January 2016](/Regression/NVDA2016.png)

Using Sci-kit-learn API:

![Linear Regression performed on NVDA Stock dat from January 2016](/Regression/NVDA_2016.png)

This barely makes a difference to the naked eye. The two graphs are very similar. 

## Version

**1.0.0 - Released Stock Scraper**

1.0.1 - Minor bug fixes with duplicate entries in the CSV File


### Todo

- SVM Regression
- Use Machine Learning to predict stock close price for the next day
- Algorithm for high frequency trading (UVXY - Price for this data fluctuates every minute)  


#### License


MIT

**Free Software, Hell Yeah!**

