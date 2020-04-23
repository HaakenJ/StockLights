import requests
from config import API_KEY, LIGHT_TOKEN

STOCK_URL = 'https://www.alphavantage.co/query'
LIGHT_URL = 'https://api.lifx.com/v1/lights/all/state'
LIGHT_HEADERS = {
    'Authorization': f'Bearer {LIGHT_TOKEN}'
}

# The stocks currently owned.
stocks = {
    'ALK': {
        'price': 0,
        'cost': 26.46,
        'shares': 14
    },
    'CCL': {
        'price': 0,
        'cost': 11.90,
        'shares': 10
    },
    'MSFT': {
        'price': 0,
        'cost': 159.00,
        'shares': 2
    },
    'GME': {
        'price': 0,
        'cost': 4.66,
        'shares': 1
    },
    'NCLH': {
        'price': 0,
        'cost': 11.40,
        'shares': 1
    }
}

totalPortfolioCost = 0
currentPortfolioValue = 0
   
# Populate the current prices for all stocks owned.
for stock in stocks:
    stockResponse = requests.get(
        STOCK_URL,
        params={
            'function': 'GLOBAL_QUOTE',
            'symbol': stock,
            'apikey': API_KEY
        }
    )

    jsonResponse = stockResponse.json()
    if ('Global Quote' in jsonResponse):
        price = jsonResponse['Global Quote']['05. price']
    else:
        print('There\'s no quote here')
    

    stocks[stock]['price'] = price

    totalShares = stocks[stock]['shares']

    # Add the stock price to the currentValue
    currentPortfolioValue = round(currentPortfolioValue + (float(price) * totalShares), 2)
    print(f'Symbol: {stock}:')
    print(f'---price: {price}')
    print(f'---shares: {totalShares}')
    print(f'---currentValue: {float(price) * totalShares}')
    print(f'---currentPortfolioValue: {currentPortfolioValue}')
    print('------------------------------------------------------')

    # Calculate total portfolio cost.


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

