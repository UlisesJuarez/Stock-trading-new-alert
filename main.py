import requests
from dotenv import load_dotenv
import os

load_dotenv()

ALPHA_KEY=os.getenv("ALPHA_KEY")
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":ALPHA_KEY
}

res=requests.get(STOCK_ENDPOINT,params=stock_params)
data=res.json()["Time Series (Daily)"]

#convertimos estos datos a un lista

data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_price=yesterday_data["4. close"]

day_before_yesterday_data=data_list[1]
day_before_yesterday_closing_price=day_before_yesterday_data["4. close"]

print(yesterday_closing_price)
print(day_before_yesterday_closing_price)

price_difference=abs(float(yesterday_closing_price)-float(day_before_yesterday_closing_price))
print(price_difference)

diff_percent=(price_difference/float(yesterday_closing_price))*100
print(diff_percent)

if(diff_percent>0.1):
    print("Get news")
#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

