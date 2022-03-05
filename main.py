import requests
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

ALPHA_KEY=os.getenv("ALPHA_KEY")
NEWS_KEY=os.getenv("NEWS_KEY")
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
my_number=os.getenv("PHONE")

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
up_down=None
if price_difference>0:
    up_down="😎"
else:
    up_down="😥"

diff_percent=round((price_difference/float(yesterday_closing_price))*100)
print(diff_percent)

if abs(diff_percent)>=0:
    news_params={
        "apiKey":NEWS_KEY,
        "qInTitle":COMPANY_NAME,
    }
    news_res=requests.get(NEWS_ENDPOINT,params=news_params)
    articles=news_res.json()["articles"]
    three_articles=articles[:3]
    print(three_articles)
    
    formatted_articles=[f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline:{article['title']}. \nBrief:{article['description']}" for article in three_articles]
    client = Client(account_sid, auth_token)
    
    for article in formatted_articles:
        message = client.messages \
            .create(
                body=article,
                from_='+17622165590',
                to=my_number
            )