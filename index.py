import requests
from config import API_KEY

url = 'https://www.alphavantage.co/query'

response = requests.get(
    url,
    params={
        'function': 'GLOBAL_QUOTE',
        'symbol': 'ALK',
        'apikey': API_KEY
    }
)

jsonResponse = response.json()
price = jsonResponse['Global Quote']['05. price']
purchasePrice = 26.46

if float(price) > 26.46:
    print('You\'re in the green!')
else:
    print('You\'re in the red...')