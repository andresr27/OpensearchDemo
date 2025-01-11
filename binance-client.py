# From: https://github.com/sammchardy/python-binance


from models.opensearch import OpenSearchClient
import os
from dotenv import load_dotenv, find_dotenv
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager


load_dotenv()
# Todo: not finding envars created using source .env, nor they show on env command
api_key= os.getenv('api_key',"Not found")
api_secret= os.getenv('api_secret',"Not found")

client = Client(api_key, api_secret)
# get all symbol prices
prices = client.get_all_tickers()
#prices = client.get_avg_price(symbol="ETHBTC")
os_conn = OpenSearchClient()
count = 1
body ={"data": prices}

# for ticker in prices:
#     if count < 10:
#         count = count +1
#         data[ticker["symbol"]]= {"symbol": ticker["symbol"], "price": ticker["price"], "other": "this_other_thing"}
try:
    os_conn.index_bulk(body,"test")
except Exception as e:
    print(e)



# # withdraw 100 ETH
# # check docs for assumptions around withdrawals
# from binance.exceptions import BinanceAPIException
# try:
#     result = client.withdraw(
#         asset='ETH',
#         address='<eth_address>',
#         amount=100)
# except BinanceAPIException as e:
#     print(e)
# else:
#     print("Success")
