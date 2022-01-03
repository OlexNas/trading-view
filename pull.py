from kucoin.client import Client
from myModels import NewAsset


api_key = "#"
api_secret = "#"
passphrase = "#"



client = Client(api_key, api_secret, passphrase)
tickersPull = client.get_ticker()["ticker"]
asset_names = []

for i in tickersPull:
    asset_names.append(i["symbol"])



