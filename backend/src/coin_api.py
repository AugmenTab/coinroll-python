#! python3

# PSL Imports
import asyncio

# 3p Imports
import aiohttp
import requests

# Internal Imports
try:
    from src.config import api_key as key
except Exception as e:
    print(e)


def __get_headers():
    return {
        'X-CMC_PRO_API_KEY': key,
        'Accepts': 'application/json'
    }


def __transform_coin_listing(coin):
    return {
        'id': coin['id'],
        'name': coin['name'],
        'symbol': coin['symbol']
    }


def __transform_metadata(coin):
    return {
        'id': coin['id'],
        'name': coin['name'],
        'symbol': coin['symbol'],
        'logo': coin['logo'],
        'website': coin['urls']['website'][0] 
    }


def __transform_coin_quote(coin):
    return {
        'id': coin['id'],
        'name': coin['name'],
        'supply': coin['circulating_supply'],
        'cap': coin['quote']['USD']['market_cap'],
        'price': coin['quote']['USD']['price'],
        'volume': coin['quote']['USD']['volume_24h'],
        'percent_changes': {
            'hour': coin['quote']['USD']['percent_change_1h'],
            'day': coin['quote']['USD']['percent_change_24h'],
            'week': coin['quote']['USD']['percent_change_7d']
        }
    }


def get_coin_listing():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    h = __get_headers()
    listing = requests.get(url, params={}, headers=h).json()['data']
    return [__transform_coin_listing(coin) for coin in listing]


async def get_coin_metadata(ids):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    h = __get_headers()
    p = {'id': ','.join(ids)}
    async with aiohttp.ClientSession() as session:
        metadata_response = await session.get(url, params=p, headers=h)
        metadata = await metadata_response.json()
    return [__transform_metadata(m) for _, m in metadata['data'].items()]


async def get_coin_quotes(ids):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    h = __get_headers()
    p = {'id': ','.join(ids), 'convert': 'USD'}
    async with aiohttp.ClientSession() as session:
        coins_response = await session.get(url, params=p, headers=h)
        coins = await coins_response.json()
    return [__transform_coin_quote(c) for _, c in coins['data'].items()]
