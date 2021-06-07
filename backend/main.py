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


def make_celery():
    # create context tasks in celery
    celery = Celery(
        'celery',
        broker='amqp://rabbit:password@rabbitmq'
    )
    celery.config_from_object('src.config')
    return celery


@celery_app.task
def update_watchlist_prices():
    watchlist = asyncio.run(get_watchlist())
    ids = list(set(str(coin['market_id']) for coin in watchlist))
    quotes = asyncio.run(coin_api.get_coin_quotes(ids))
    asyncio.run(db.update_watchlist(quotes))
    print('Watchlist updated with current crypto prices.')


app = FastAPI()
celery_app = make_celery()
db.establish_db()


class Transaction(BaseModel):
    name: str
    quantity: int


class Watch(BaseModel):
    market_id: Optional[int] = None
    name: str


@app.get('/')
async def get_watchlist():
    results = await db.get_watchlist()
    return results


@app.post('/watch')
async def watch_coin(watch: Watch):
    coin = await db.get_coin_from_db(watch.name)
    _id = coin.get('market_id')
    result_or_default = {'Msg': 'That coin is already being watched.'}
    coin_in_watchlist = await db.get_coin_from_watchlist(_id)
    if not coin_in_watchlist:
        raw_metadata = await coin_api.get_coin_metadata([str(_id)])
        metadata = raw_metadata[0]
        raw_quote = await coin_api.get_coin_quotes([str(_id)])
        quote = raw_quote[0]
        result_or_default = await db.add_watched_coin(_id, metadata, quote)
    return result_or_default


@app.delete('/watch')
async def unwatch_coin(watch: Watch):
    if not watch.market_id:
        coin = await db.get_coin_from_db(watch.name)
        watch.market_id = coin.get('market_id')
    results = await db.remove_watched_coin(watch.market_id)
    return results


@app.post('/buy')
async def buy_coin(buy: Transaction):
    coin = await db.get_coin_from_db(buy.name)
    _id = coin.get('market_id')
    raw_quote = await coin_api.get_coin_quotes([str(_id)])
    quote = raw_quote[0]
    result = await db.create_transaction(_id, buy.quantity, quote, 'purchase')
    return result


@app.post('/sell')
async def sell_coin(sell: Transaction):
    coin = await db.get_coin_from_db(sell.name)
    _id = coin.get('market_id')
    records = await db.get_all_transactions_by_id(_id)
    result_or_default = {'Msg': 'Insufficient coins.'}
    if portfolio.has_sufficient_coins(records, sell.quantity):
        raw_quote = await coin_api.get_coin_quotes([str(_id)])
        quote = raw_quote[0]
        qty = sell.quantity
        result_or_default = await db.create_transaction(_id, qty, quote, 'sell')
    return result_or_default


@app.get('/records')
async def get_all_records():
    records = await db.get_all_transactions()
    return records


@app.get('/records/{coin_name}')
async def get_coin_records(coin_name: str):
    coin = await db.get_coin_from_db(coin_name)
    _id = coin.get('market_id')
    transactions = await db.get_all_transactions_by_id(_id)
    return transactions


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
