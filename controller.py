import mysql.connector
import datetime

# Database: stock_db
# Table: stock_data
    # id: Auto
    # entryDate: datetime
    # symbol: string
    # price: double

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


def getMostRecent():
    '''
        Retrieves the most recent record in the stocks table.

        @return {results[]}
    '''
    mycursor.execute(
        'SELECT entryDate, symbol, price FROM stock_data ORDER BY id DESC LIMIT 1'
    )
    results = mycursor.fetchall()
    return results