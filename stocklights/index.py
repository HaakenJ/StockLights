import requests
import datetime
from config import API_KEY, LIGHT_TOKEN
import controller

STOCK_URL = 'https://www.alphavantage.co/query'
LIGHT_URL = 'https://api.lifx.com/v1/lights/all/state'
LIGHT_HEADERS = {
    'Authorization': f'Bearer {LIGHT_TOKEN}'
}

def getSymbolsArr():
    symbolsArr = controller.getPortfolioSymbols()
    symbols = []
    for symbol in symbolsArr:
        symbols.append(symbol[0])
    return symbols

def changeLightOnTotalGain():
    '''
        Changes the light to red or green depending on if the total portolio
        value is positive or negative.
    '''
    totalPortfolioCost = 0
    currentPortfolioValue = 0
    symbols = getSymbolsArr()

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
            price = float(jsonResponse['Global Quote']['05. price'])
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


    if currentPortfolioValue >= totalPortfolioCost:
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

def changeLightOnDeltaGain():
    '''
        Change the light color to red or green depending on if the portfolio
        has made gains or losses since the last check.
    '''
    priorPortfolioCost = 0
    currentPortfolioValue = 0
    symbols = getSymbolsArr()

    for symbol in symbols:
        totalShares = controller.getPortfolioData('shares', symbol)
        # Use price from most recent record.
        stockCost = controller.getMostRecent(symbol)    
        # Calculate total portfolio cost.
        priorPortfolioCost += (stockCost * totalShares)

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
            price = float(jsonResponse['Global Quote']['05. price'])
        else:
            print('There\'s no quote here')
        
        # Add the price data to the stock_data table.
        controller.create(datetime.datetime.now(), symbol, price)

        totalShares = controller.getPortfolioData('shares', symbol)
        # Calculate the total portfolio value as of the current time.
        currentPortfolioValue += (price * totalShares)

    if currentPortfolioValue >= priorPortfolioCost:
        lightResponse = requests.put(
            LIGHT_URL,
            data={
                'power': 'on',
                'color': 'green',
                'brightness': 0.1
            },
            headers=LIGHT_HEADERS
        )
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
    print(f'Prior portfolio cost: {priorPortfolioCost}')
    print(f'Current portfolio value: {currentPortfolioValue}')
    
changeLightOnDeltaGain()