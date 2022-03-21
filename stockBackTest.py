import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np

stock_input = input("What stock are you looking for? ")

#default start date of search
startyear = 2021
startmonth = 1
startday = 1

start =dt.datetime(startyear,startmonth,startday)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock_input,start,now)

ema_used = [12,26]

#toggle between iloc[:,3 OR 5] to change between whether MACD is calculcated with adjusted close or close
df[f"Ema_{12}"]=round(df.iloc[:,3].ewm(span=12, adjust=False).mean(),3)
df[f"Ema_{26}"]=round(df.iloc[:,3].ewm(span=26, adjust=False).mean(),3)
df["MACD"] = df["Ema_12"] - df["Ema_26"]
df["Signal Line"] = round(df.iloc[:,8].ewm(span=9, adjust=False).mean(),3)
print(df)

position = 0
num = 0
percentage_change = []

#Logic to decide the buy and sell conditions
for x in df.index:
    close = df["Close"][x]
    print(x,end=" ")
    if (df["MACD"][x] > df["Signal Line"][x]) and ((df["MACD"][x] and df["Signal Line"][x]) < 0):
       print("Golden Bullish Crossover")
       if position == 0:
           position = 1
           buy_price = close
           print(f"Buying in now at {buy_price}...")
    if (df["MACD"][x] > df["Signal Line"][x]):
        print("Bullish Crossover")


    elif (df["MACD"][x] < df["Signal Line"][x]) and ((df["MACD"][x] and df["Signal Line"][x]) > 0):
        print("Death Bearish Crossover")
        if position == 1:
            position = 0
            sell_price = close
            print(f"Selling out now at {sell_price}...")
            percentage_c = ((sell_price-buy_price)/buy_price)*100
            print(f"percentage change in last trade is {percentage_c}")
            percentage_change.append(percentage_c)

    elif (df["MACD"][x] < df["Signal Line"][x]):
        print("Bearish Crossover")

    if num == df["Close"].count()-1 and position == 1:
        position = 0
        sell_price = close
        print(f"Selling out now at {sell_price}...")
        percentage_c = ((sell_price - buy_price) / buy_price) * 100
        print(f"percentage change in last trade is {percentage_c}")
        percentage_change.append(percentage_c)
    num += 1
print(percentage_change)

gains = 0
net_gain = 0
losses = 0
net_losses = 0
totalR = 1

#Calculates the statistics obtained from the period on a given stock
for x in percentage_change:
    if x > 0:
        gains += x
        net_gain += 1
    elif x < 0:
        losses += x
        net_losses += 1
    totalR = totalR*((x/100)+1)
totalR =round((totalR-1)*100,2)

if net_gain> 0:
    avggain=gains/net_gain
    maxR = max(percentage_change)
else:
    avggain = 0
    maxR = "undefined"

if net_losses > 0:
    avgloss = losses/net_losses
    maxL = min(percentage_change)
    ratio = str(-avggain/avgloss)
else:
    avgloss = 0
    minL = "indefinite"
    ratio = "infinite"

if net_gain> 0 or net_losses > 0:
    battingavg= net_gain/(net_gain+net_losses)
else:
    battingavg= 0
print()
print("Results for "+ stock_input +" going back to "+str(df.index[0])+", Sample size: "+str(net_gain+net_losses)+" trades")
print("EMAs used: "+str(ema_used))
print("Batting Avg: "+ str(battingavg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avggain))
print("Average Loss: "+ str(avgloss))
print("Max Return: "+ str(maxR))
print("Max Loss: "+ str(maxL))
print("Total return over "+str(net_gain+net_losses)+ " trades: "+ str(totalR)+"%" )
print()