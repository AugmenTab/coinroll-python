#! python3

# 3p Imports
import requests

# Internal Imports
try:
    from config import api_key as key
except:
    pass


def get_all_coins(params):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    headers = {
        'X-CMC_PRO_API_KEY': key,
        'Accepts': 'application/json'
    }
    data = requests.get(url, params=params, headers=headers).json()
    return data['data']


def get_coin_data(slug):
    headers = {
        'X-CMC_PRO_API_KEY': key,
        'Accepts': 'application/json'
    }
    params = {
        'limit': 1,
        'slug': slug,
        'convert': 'USD'
    }
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    data = requests.get(url, params=params, headers=headers).json()
    return data['data']
