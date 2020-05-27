import datetime
import controller
import index

def updateEODValue():
    currentPortfolioValue = getCurrentPortfolioValue(False)
    controller.createEndOfDayRecord(datetime.datetime.now(), currentPortfolioValue)

if __name__ == "__main__":
    updateEODValue()
