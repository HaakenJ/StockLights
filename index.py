import requests
from config import API_KEY, LIGHT_TOKEN

STOCK_URL = 'https://www.alphavantage.co/query'
LIGHT_URL = 'https://api.lifx.com/v1/lights/all/state'
LIGHT_HEADERS = {
    'Authorization': f'Bearer {LIGHT_TOKEN}'
}
symbols = ['ALK', 'MSFT', 'CCL', 'GME', 'NCLH']
results = {}

for symbol in symbols:
    stockResponse = requests.get(
        STOCK_URL,
        params={
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': API_KEY
        }
    )

    jsonResponse = stockResponse.json()
    price = jsonResponse['Global Quote']['05. price']

    results[symbol] = price

print(results)


purchasePrice = 26.46

# if float(price) > 26.46:
#     lightResponse = requests.put(
#         LIGHT_URL,
#         data={
#             'power': 'on',
#             'color': 'green',
#             'brightness': 0.1
#         },
#         headers=LIGHT_HEADERS
#     )

#     print(lightResponse.json())
# else:
#     lightResponse = requests.put(
#         LIGHT_URL,
#         data={
#             'power': 'on',
#             'color': 'red',
#             'brightness': 0.1
#         },
#         headers=LIGHT_HEADERS
#     )

#     print(lightResponse.status_code)

