from logging import exception

from opensearchpy import OpenSearch
#from opensearch_dsl import Search
import os
import json
from dotenv import load_dotenv
import datetime

load_dotenv()
# Todo: not finding envars created using source .env, nor they show env command
api_user= os.getenv('os_user',"Not found")
api_pass= os.getenv('os_pass',"Not found")

host = 'localhost'
port = 9200
auth = (api_user, api_pass)
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.


# TODO: Create os-client class with needed methods.
class OpenSearchClient:
    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    def __init__(self):
        self.client = OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_compress = True, # enables gzip compression for request bodies
            http_auth = auth,
            use_ssl = True,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False,
            ca_certs = ca_certs_path
        )

    def index_create(self, index_name):
        index_name = index_name
        index_body = {
          'settings': {
            'index': {
              'number_of_shards': 2
            }
          },
          'mappings': {

              "properties": {
                  "book": {
                      "properties": {
                          "bidPrice": {"type": "float"},
                          "bidQty": {"type": "float"},
                          "askPrice": {"type": "float"},
                          "askQty": {"type": "float"}
                      }
                  },
                  "info": {
                      "properties": {
                          "priceChange": {"type": "float"},
                          "priceChangePercent": {"type": "float"},
                          "weightedAvgPrice":{"type": "float"},
                          "prevClosePrice": {"type": "float"},
                          "lastPrice": {"type": "float"},
                          "lastQty": {"type": "float"},
                          "bidPrice": {"type": "float"},
                          "bidQty": {"type": "float"},
                          "askPrice": {"type": "float"},
                          "askQty": {"type": "float"},
                          "openPrice": {"type": "float"},
                          "highPrice": {"type": "float"},
                          "lowPrice": {"type": "float"},
                          "volume": {"type": "float"},
                          "quoteVolume": {"type": "float"},
                          "openTime": {"type": "float"},
                          "closeTime": {"type": "date"},
                          "firstId":{"type": "date"},
                          "lastId": {"type": "date"},
                          "count": {"type": "integer"},
                          "avg_price_5m": {"type": "float"}
                      }
                  }
              }
          }

        }
        try:
            response = self.client.indices.create(index_name, index_body)
            print(response)
        except Exception as e:
            print(e)

    def index_data(self,body,index_name):

        try:
            self.index_create(index_name)
            response = self.client.index(
                index = index_name,
                body = body,
                refresh = True)

            print(response)
        except Exception as e:
            print(e)

    def index_bulk(self,data,index_name):
        ts = datetime.datetime.now()
        print(ts)
        data["@timestamp"] = ts
        body = json.dumps(data, indent=4, sort_keys=True, default=str)
        try:
            response = self.client.bulk(
                index = index_name,
                body = body,
                refresh = True)
            print(response)
        except Exception as e:
            print(e)