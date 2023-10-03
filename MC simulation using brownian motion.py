#!/usr/bin/env python
# coding: utf-8

# In[4]:


import math
import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data as pdr

# Fetching Apple stock data from Yahoo Finance starting from 1/1/2018
stock_data = pdr.DataReader('AAPL', 'yahoo', start='1/1/2021')
print(stock_data.head())

# Calculating time elapsed in days
time_elapsed = (stock_data.index[-1] - stock_data.index[0]).days

# Calculating total growth percentage
total_growth = stock_data['Adj Close'][-1] / stock_data['Adj Close'][1]

# Converting time elapsed to number of years
number_of_years = time_elapsed / 365.0

# Calculating compounded annualized growth rate (CAGR)
cagr = total_growth ** (1 / number_of_years) - 1

# Calculating standard deviation of daily price changes
std_dev = stock_data['Adj Close'].pct_change().std()

# Scaling standard deviation by an annualization factor
number_of_trading_days = 252
std_dev = std_dev * math.sqrt(number_of_trading_days)

print("CAGR (mean returns): ", str(round(cagr, 4)))
print("Standard Deviation of Returns: ", str(round(std_dev, 4)))

# Number of Monte Carlo simulation trials
number_of_trials = 100

# Generating random price series and plotting random walks
closing_prices = []

for _ in range(number_of_trials):
    daily_return_percentages = np.random.normal(cagr / number_of_trading_days, std_dev / math.sqrt(number_of_trading_days),
                                                number_of_trading_days) + 1
    price_series = [stock_data['Adj Close'][-1]]

    for j in daily_return_percentages:
        price_series.append(price_series[-1] * j)

    closing_prices.append(price_series[-1])
    plt.plot(price_series)

plt.show()

# Plotting histogram of closing prices
plt.hist(closing_prices, bins=40)
plt.show()

# Analyzing results
mean_end_price = round(np.mean(closing_prices), 2)
print("Expected Price: $", mean_end_price)

# Calculating top 10% and bottom 10% of possible outcomes
top_ten = np.percentile(closing_prices, 100 - 10)
bottom_ten = np.percentile(closing_prices, 10)

# Plotting histogram with top 10%, bottom 10%, and current price lines
plt.hist(closing_prices, bins=40)
plt.axvline(top_ten, color='r', linestyle='dashed', linewidth=2, label='Top 10%')
plt.axvline(bottom_ten, color='b', linestyle='dashed', linewidth=2, label='Bottom 10%')
plt.axvline(stock_data['Adj Close'][-1], color='g', linestyle='dashed', linewidth=2, label='Current Price')
plt.legend()
plt.show()

