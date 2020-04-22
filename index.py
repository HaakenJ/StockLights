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

print(jsonResponse['Global Quote']['05. price'])