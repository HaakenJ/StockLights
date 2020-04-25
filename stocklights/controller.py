import mysql.connector
import datetime

# Database: stock_db

# Stock Table: stock_data
    # id: Auto
    # entryDate: datetime
    # symbol: varchar(10)
    # price: double

# Portfolio Table: portfolio
    # id: Auto
    # Symbol: varchar(10)
    # cost: double
    # shares: int

# Connect to DB
db = mysql.connector.connect(
    host='localhost',
    user='kramer',
    password='kramer',
    database='stock_db'
)
# Create cursor object
cursor = db.cursor()



def create(time, symbol, price):
    '''
        Creates a new record in the stocks table.

        @param {Datetime} time
        @param {String} symbol
        @param {Double} price
        @return {None}
    '''
    cursor.execute(
        f'INSERT INTO stock_data (entryDate, symbol, price) VALUES ("{time}", "{symbol}", {price});'
    )
    db.commit()
    print(cursor.rowcount, 'record inserted.')


def getMostRecent(symbol):
    '''
        Retrieves the price of the most recent record in the stocks table.

        @param {String} symbol
        @return {results(tuple)}
    '''
    query = """SELECT price FROM stock_data WHERE symbol=%s ORDER BY id DESC LIMIT 1;"""
    params = (symbol,)
    cursor.execute(query, params)
    results = cursor.fetchall()
    return float(results[0][0])

def getPortfolioSymbols():
    '''
        Retrieves the symbols in portfolio.

        @return {results[()]}
    '''
    cursor.execute(
        'SELECT symbol FROM portfolio'
    )
    results = cursor.fetchall()
    return results

def getPortfolioData(column, symbol):
    '''
        Retrieves the requested data of a given stock in portfolio.

        @param {String} column
        @param {String} symbol
        @return {results()}
    '''
    query =  "SELECT " +column+ """ FROM portfolio WHERE symbol=%s;"""
    params = (symbol,)
    cursor.execute(query, params)
    results = cursor.fetchall()

    if column == 'cost':
        return float(results[0][0])
    else:
        return int(results[0][0])
