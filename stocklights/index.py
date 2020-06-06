import requests
import datetime
from config import API_KEY, LIGHT_TOKEN
import controller

STOCK_URL = 'https://finnhub.io/api/v1/quote'
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
                'symbol': symbol,
                'token': API_KEY
            }
        )

        jsonResponse = stockResponse.json()
        try:
            price = float(jsonResponse['c'])
        except:
            print('This call did not return a proper response.')
        
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

    print('Prior day value: ' + str(priorDayPortfolioValue))
    print('Current Value: ' + str(currentPortfolioValue))

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
        print('Turning the light green.')
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
        print('Turning the light red.')

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
                'symbol': symbol,
                'token': API_KEY
            }
        )

        jsonResponse = stockResponse.json()
        try:
            price = float(jsonResponse['c'])
        except:
            print('This call did not return a proper response.')
            price = 0

        if (addRecords == True):
            # Add the price data to the stock_data table.
            controller.createStockRecord(datetime.datetime.now(), symbol, price)

        totalShares = controller.getPortfolioData('shares', symbol)
        # Calculate the total portfolio value as of the current time.
        currentPortfolioValue += (price * totalShares)

    return currentPortfolioValue

def changeLightOnSingleStock(symbol, targetPrice):
    stockResponse = requests.get(
        STOCK_URL,
        params={
            'symbol': symbol,
            'token': API_KEY
        }
    )

    jsonResponse = stockResponse.json()
    try:
        price = float(jsonResponse.json['c'])
    except:
        print('This call did not return a proper response.')
        price = 0

    if price >= targetPrice:
        lightResponse = requests.put(
            LIGHT_URL,
            data={
                'power': 'on',
                'color': 'green',
                'brightness': 0.5
            },
            headers=LIGHT_HEADERS
        )
        print('Turning the light green.')
    else:
        lightResponse = requests.put(
            LIGHT_URL,
            data={
                'power': 'on',
                'color': 'red',
                'brightness': 0.5
            },
            headers=LIGHT_HEADERS
        )
        print('Turning the light red.')



if __name__ == "__main__":
    # changeLightOnPriorDay()
    changeLightOnSingleStock('GNUS', 7.03)
#    try:
#        changeLightOnPriorDay()
#    except:
#        print('There was an error with the prior day function')
#        changeLightOnTotalGain()
