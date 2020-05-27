import datetime
import controller
from index import getCurrentPortfolioValue

def updateEODValue():
    currentPortfolioValue = getCurrentPortfolioValue(False)
    controller.createEndOfDayRecord(datetime.datetime.now(), currentPortfolioValue)
    print(currentPortfolioValue)

if __name__ == "__main__":
    updateEODValue()
