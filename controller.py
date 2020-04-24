import mysql.connector
import datetime

# Database: stock_db
# Table: stock_data
    # id: Auto
    # entryDate: datetime
    # symbol: string
    # price: double

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='kramer',
    database='stock_db',
)

mycursor = db.cursor()

def create(time, symbol, price):
    mycursor.execute(
        f'INSERT INTO stock_data (entryDate, symbol, price) VALUES ("{time}", "{symbol}", {price});'
    )
    db.commit()
    print(mycursor.rowcount, 'record inserted.')

currentTime = datetime.datetime.now().strftime('%y-%m-%d %H-%M-%S')

create(currentTime, 'ALK', 26.94)