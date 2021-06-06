#! python3

# PSL Imports
from datetime import timedelta
from typing import Optional

# 3p Imports
from celery import Celery
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Internal Imports
import src.coin_api as coin_api
import src.database as db
import src.portfolio as portfolio


app = FastAPI()


def make_celery():
    # create context tasks in celery
    celery = Celery(
        'celery',
        broker='amqp://rabbit:password@rabbitmq'
    )
    celery.config_from_object('src.config')

    return celery


celery_app = make_celery()


class Transaction(BaseModel):
    name: str
    quantity: int


class Watch(BaseModel):
    id: int = None
    name: str = None


@celery_app.task
def update_watchlist_prices():
    print('Updated!')


@app.get('/')
def get_watchlist():
    return db.get_watchlist()


@app.post('/watch')
def watch_coin(watch: Watch):
    id = db.get_coin_from_db(watch.name).get('market_id')
    if not db.get_coin_from_watchlist(id):
        return db.add_watched_coin(id)


@app.delete('/watch')
def unwatch_coin(watch: Watch):
    if not watch.id:
        watch.id = db.get_coin_from_db(watch.name).get('market_id')
    return db.remove_watched_coin(watch.id)


@app.post('/buy')
def buy_coin(buy: Transaction):
    id = db.get_coin_from_db(buy.name).get('market_id')
    return db.create_transaction(id, buy.quantity, 'purchase')


@app.post('/sell')
def sell_coin(sell: Transaction):
    id = db.get_coin_from_db(sell.name).get('market_id')
    records = db.get_all_transactions_by_id(id)
    if portfolio.has_sufficient_coins(records, sell.quantity):
        return db.create_transaction(id, sell.quantity, 'sell')
    else:
        return {'Msg': 'Insufficient coins.'}


@app.get('/records')
def get_all_records():
    return db.get_all_transactions()


@app.get('/records/{coin_name}')
def get_coin_records(coin_name: str):
    id = db.get_coin_from_db(coin_name).get('market_id')
    return db.get_all_transactions_by_id(id)


@app.get('/summary')
def get_portfolio_summary():
    records = db.get_all_transactions()
    ids = list(set(str(record['market_id']) for record in records))
    quotes = coin_api.get_coin_quotes(ids)
    return portfolio.get_summary(records, quotes)


@app.get('/summary/{coin_name}')
def get_coin_summary(coin_name: str):
    id = db.get_coin_from_db(coin_name).get('market_id')
    records = db.get_all_transactions_by_id(id)
    quote = coin_api.get_coin_quotes([str(id)])[0]
    return portfolio.get_coin_summary(records, quote)


if __name__ == '__main__':
    db.establish_db()
    uvicorn.run(app, port=8000, host='0.0.0.0')
