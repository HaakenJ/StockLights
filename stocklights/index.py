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
        controller.createStockRecord(datetime.datetime.now(), symbol, price)

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
    currentPortfolioValue = getCurrentPortfolioValue(True)
    symbols = getSymbolsArr()

    for symbol in symbols:
        totalShares = controller.getPortfolioData('shares', symbol)
        # Use price from most recent record.
        stockCost = controller.getMostRecent(symbol)    
        # Calculate total portfolio cost.
        priorPortfolioCost += (stockCost * totalShares)

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


def changeLightOnPriorDay():
    '''
        Change the light color to red or green depending on if the portfolio
        has made gains or losses since the prior day.
    '''
    # Get prior day's portfolio value
    priorDayPortfolioValue = controller.getPriorDayValue()
    currentPortfolioValue = getCurrentPortfolioValue(False)

    if currentPortfolioValue >= priorDayPortfolioValue:
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
    print(f'Prior portfolio cost: {priorDayPortfolioValue}')
    print(f'Current portfolio value: {currentPortfolioValue}')

def getCurrentPortfolioValue(addRecords):
    '''
        Returns the current value of the client's portfolio with an optional
        flag to add the data to the stock_db.

        @param {Boolean} addRecords
        @return {Double} value
    '''
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
            print(f'There\'s no quote for {symbol}')
            price = 0
        
        print (addRecords)
        if (addRecords == True):
            # Add the price data to the stock_data table.
            controller.createStockRecord(datetime.datetime.now(), symbol, price)

        totalShares = controller.getPortfolioData('shares', symbol)
        # Calculate the total portfolio value as of the current time.
        currentPortfolioValue += (price * totalShares)

    return currentPortfolioValue



if __name__ == "__main__":
    # If the application is being run for the first time there will be no recent
    # data to base the delta gain on.  In this case the total gain function will
    # be run and the table will be populated.
    try:
        changeLightOnDeltaGain()
    except:
        changeLightOnTotalGain()




# TODO - Create a function to change the light based on gain since the prior day.
