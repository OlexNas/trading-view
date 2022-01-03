from kucoin.client import Client
from myModels import NewAsset


api_key = "6198374f85f69100014e29ad"
api_secret = "4790218a-61df-43c6-8e34-251ade3291ab"
passphrase = "Ioipioipoiop133"



client = Client(api_key, api_secret, passphrase)
tickersPull = client.get_ticker()["ticker"]
asset_names = []

for i in tickersPull:
    asset_names.append(i["symbol"])



