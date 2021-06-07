#! python3

# PSL Imports
from typing import Optional
import asyncio

# 3p Imports
from celery import Celery
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Internal Imports
import src.coin_api as coin_api
import src.database as db
import src.portfolio as portfolio


def initialize_db(query_api=False):
    db.connect_to_db()
    if query_api:
        db.update_coin_list(coin_api.get_coin_listing())


def make_celery():
    """
    This function establishes and configures an instance of Celery.

    :return: Returns the instance of Celery.
    """
    celery = Celery(
        'celery',
        broker='amqp://rabbit:password@rabbitmq'
    )
    celery.config_from_object('src.config')
    return celery


app = FastAPI()
initialize_db()
celery_app = make_celery()


@celery_app.task
def update_watchlist_prices():
    """
    This function updates the user's watchlist prices in the database, to ensure
    that they are always current to within a number of seconds.

    :return: None
    """
    watchlist = asyncio.run(get_watchlist())
    ids = list(set(str(coin['market_id']) for coin in watchlist))
    quotes = asyncio.run(coin_api.get_coin_quotes(ids))
    asyncio.run(db.update_watchlist(quotes))
    print('Watchlist updated with current crypto prices.')


class Transaction(BaseModel):
    """
    Transaction represents the purchase or sale of a cryptocurrency from
    the user's personal stores.

    :param name: The name of the cryptocurrency.
    :param quantity: The quantity of cryptocurrency involved in the transaction.
    """
    name: str
    quantity: int


class Watch(BaseModel):
    """
    Watch encapsulates an optional market ID (corresponding to the ID from the
    MarketCoinCap API used for this project) and the name for the coin that ID
    represents. The coin this class represents is then added or removed from the
    user's watchlist.

    :param market_id: The optional CoinMarketCap API market ID for the coin.
    :param name: The common name for the coin.
    """
    market_id: Optional[int] = None
    name: str


@app.get('/')
async def get_watchlist():
    """
    This function requests the user's watchlist from the database.

    :return: Returns the user's watchlist.
    """
    return await db.get_watchlist()


@app.post('/watch')
async def watch_coin(watch: Watch):
    coin = await db.get_coin_from_db(watch.name)
    _id = coin.get('market_id')
    coin_in_watchlist = await db.get_coin_from_watchlist(_id)
    if not coin_in_watchlist:
        raw_metadata = await coin_api.get_coin_metadata([str(_id)])
        metadata = raw_metadata[0]
        raw_quote = await coin_api.get_coin_quotes([str(_id)])
        quote = raw_quote[0]
        return await db.add_watched_coin(_id, metadata, quote)
    return {'Msg': 'That coin is already being watched.'}


@app.delete('/watch')
async def unwatch_coin(watch: Watch):
    if not watch.market_id:
        coin = await db.get_coin_from_db(watch.name)
        watch.market_id = coin.get('market_id')
    return await db.remove_watched_coin(watch.market_id)


@app.post('/buy')
async def buy_coin(buy: Transaction):
    coin = await db.get_coin_from_db(buy.name)
    _id = coin.get('market_id')
    raw_quote = await coin_api.get_coin_quotes([str(_id)])
    quote = raw_quote[0]
    return await db.create_transaction(_id, buy.quantity, quote, 'purchase')


@app.post('/sell')
async def sell_coin(sell: Transaction):
    coin = await db.get_coin_from_db(sell.name)
    _id = coin.get('market_id')
    records = await db.get_all_transactions_by_id(_id)
    if portfolio.has_sufficient_coins(records, sell.quantity):
        raw_quote = await coin_api.get_coin_quotes([str(_id)])
        quote = raw_quote[0]
        qty = sell.quantity
        return await db.create_transaction(_id, qty, quote, 'sell')
    return {'Msg': 'Insufficient coins.'}


@app.get('/records')
async def get_all_records():
    return await db.get_all_transactions()


@app.get('/records/{coin_name}')
async def get_coin_records(coin_name: str):
    coin = await db.get_coin_from_db(coin_name)
    _id = coin.get('market_id')
    return await db.get_all_transactions_by_id(_id)


@app.get('/summary')
async def get_portfolio_summary():
    records = await db.get_all_transactions()
    ids = list(set(str(record['market_id']) for record in records))
    quotes = await coin_api.get_coin_quotes(ids)
    return portfolio.get_summary(records, quotes)


@app.get('/summary/{coin_name}')
async def get_coin_summary(coin_name: str):
    coin = await db.get_coin_from_db(coin_name)
    _id = coin.get('market_id')
    records = await db.get_all_transactions_by_id(_id)
    raw_quote = await coin_api.get_coin_quotes([str(_id)])
    quote = raw_quote[0]
    return portfolio.get_coin_summary(records, quote)


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
