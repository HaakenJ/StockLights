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
    user='root',
    password='kramer',
    database='stock_db',
)
# Create cursor object
mycursor = db.cursor()



def create(time, symbol, price):
    '''
        Creates a new record in the stocks table.

        @param {Datetime} time
        @param {String} symbol
        @param {Double} price
        @return {None}
    '''
    mycursor.execute(
        f'INSERT INTO stock_data (entryDate, symbol, price) VALUES ("{time}", "{symbol}", {price});'
    )
    db.commit()
    print(mycursor.rowcount, 'record inserted.')


def getMostRecent(symbol):
    '''
        Retrieves the most recent record in the stocks table.

        @param {String} symbol
        @return {results(tuple)}
    '''
    query = """SELECT entryDate, symbol, price FROM stock_data WHERE symbol=%s ORDER BY id DESC LIMIT 1;"""
    params = (symbol,)
    mycursor.execute(query, params)
    results = mycursor.fetchall()
    return results[0]


def getPortfolio():
    '''
        Retrieves the symbols and costs in portfolio.

        @return {results[()]}
    '''
    mycursor.execute(
        'SELECT symbol, cost, shares FROM portfolio'
    )
    results = mycursor.fetchall()
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
    mycursor.execute(query, params)
    results = mycursor.fetchall()

    if column == 'cost':
        return float(results[0][0])
    else:
        return int(results[0][0])