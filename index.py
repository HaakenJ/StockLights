import requests
import datetime
from config import API_KEY, LIGHT_TOKEN
import controller

STOCK_URL = 'https://www.alphavantage.co/query'
LIGHT_URL = 'https://api.lifx.com/v1/lights/all/state'
LIGHT_HEADERS = {
    'Authorization': f'Bearer {LIGHT_TOKEN}'
}

# The symbols currently owned.
# symbols = {
#     'ALK': {
#         'price': 0,
#         'cost': 26.46,
#         'shares': 14
#     },
#     'CCL': {
#         'price': 0,
#         'cost': 11.90,
#         'shares': 10
#     },
#     'MSFT': {
#         'price': 0,
#         'cost': 159.00,
#         'shares': 2
#     },
#     'GME': {
#         'price': 0,
#         'cost': 4.66,
#         'shares': 1
#     },
#     'NCLH': {
#         'price': 0,
#         'cost': 11.40,
#         'shares': 1
#     }
# }
symbols = ['ALK', 'CCL', 'MSFT', 'GME', 'NCLH']
portfolio = controller.getPortfolio()

totalPortfolioCost = 0
currentPortfolioValue = 0

# Add records to db for each stock
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
    if ('Global Quote' in jsonResponse):
        price = jsonResponse['Global Quote']['05. price']
    else:
        print('There\'s no quote here')
    
    # Add the price data to the stock_data table.
    controller.create(datetime.datetime.now(), symbol, price)

    totalShares = controller.getPortfolioData('shares', symbol)
    stockCost = controller.getPortfolioData('cost', symbol)

    # Calculate total portfolio cost.
    totalPortfolioCost += (stockCost * totalShares)
    # Calculate the total portfolio value as of the current time.
    currentPortfolioValue += (price * totalShares)


if currentPortfolioValue > totalPortfolioCost:
    lightResponse = requests.put(
        LIGHT_URL,
        data={
            'power': 'on',
            'color': 'green',
            'brightness': 0.1
        },
        headers=LIGHT_HEADERS
    )

    print(lightResponse.json())
else:
    lightResponse = requests.put(
        LIGHT_URL,
        data={
            'power': 'on',
            'color': 'red',
            'brightness': 0.1
        },
        headers=LIGHT_HEADERS
    )
