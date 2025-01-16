# From: https://github.com/sammchardy/python-binance
import time

from models.opensearch import OpenSearchClient
import os, json, uuid, datetime
from dotenv import load_dotenv, find_dotenv
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

load_dotenv()
# Todo: not finding envars created using source .env, nor they show on env command
api_key= os.getenv('api_key',"Not found")
api_secret= os.getenv('api_secret',"Not found")
client = Client(api_key, api_secret)
os_conn = OpenSearchClient()

#TODO Define ticker lit
tickers = ["ICPUSDT","BTCUSDT"]
index = "test001"

def send_price_info(ticker):
    ts = datetime.datetime.now(datetime.timezone.utc)
    avg = client.get_avg_price(symbol=ticker)

    resp = client.get_ticker(symbol=ticker)
    resp["avg_price_5m"] = avg["price"]

    print(json.dumps(resp))

    data = {"@timestamp": ts, "type": "24hs_Ticker", "ticker": ticker, "info": resp}
    os_conn.index_data(data, index)

def send_order_book(ticker):
    ts = datetime.datetime.now(datetime.timezone.utc)
    depth = client.get_order_book(symbol=ticker)
    print(json.dumps(depth))

    for i in range(len(depth["bids"])):
        order_book = {"bidPrice": depth["bids"][i][0], "bidQty": depth["bids"][i][1], "askPrice": depth["asks"][i][0],
                      "askQty": depth["asks"][i][1]}
        data = {"@timestamp": ts, "type": "order_book", "ticker": ticker, "book": order_book}
        os_conn.index_data(data, index)

while True:
    for ticker in tickers:
        try:
            #for kline in client.get_historical_klines_generator(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
            # candles = client.get_klines(symbol=ticker, interval=Client.KLINE_INTERVAL_30MINUTE)
            # print(candles)
            # info = client.get_symbol_info(symbol=ticker)
            # info["permissionSets"] = [["REDACTED"]]

            send_price_info(ticker)
            send_order_book(ticker)
        except Exception as e:
            print(e)
    time.sleep(300)
