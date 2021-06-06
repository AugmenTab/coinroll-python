#! python3

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
    db.establish_db()
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
    ids = list(set(str(coin['market_id']) for coin in get_watchlist()))
    db.update_watchlist(coin_api.get_coin_quotes(ids))
    print('Watchlist updated with current crypto prices.')


@app.get('/')
def get_watchlist():
    return db.get_watchlist()


@app.post('/watch')
def watch_coin(watch: Watch):
    _id = db.get_coin_from_db(watch.name).get('market_id')
    result_or_default = {'Msg': 'That coin is already being watched.'}
    if not db.get_coin_from_watchlist(_id):
        result_or_default = db.add_watched_coin(_id)
    return result_or_default


@app.delete('/watch')
def unwatch_coin(watch: Watch):
    if not watch.id:
        watch.id = db.get_coin_from_db(watch.name).get('market_id')
    return db.remove_watched_coin(watch.id)


@app.post('/buy')
def buy_coin(buy: Transaction):
    _id = db.get_coin_from_db(buy.name).get('market_id')
    return db.create_transaction(_id, buy.quantity, 'purchase')


@app.post('/sell')
def sell_coin(sell: Transaction):
    _id = db.get_coin_from_db(sell.name).get('market_id')
    records = db.get_all_transactions_by_id(_id)
    result_or_default = {'Msg': 'Insufficient coins.'}
    if portfolio.has_sufficient_coins(records, sell.quantity):
        result_or_default = db.create_transaction(_id, sell.quantity, 'sell')
    return result_or_default


@app.get('/records')
def get_all_records():
    return db.get_all_transactions()


@app.get('/records/{coin_name}')
def get_coin_records(coin_name: str):
    _id = db.get_coin_from_db(coin_name).get('market_id')
    return db.get_all_transactions_by_id(_id)


@app.get('/summary')
def get_portfolio_summary():
    records = db.get_all_transactions()
    ids = list(set(str(record['market_id']) for record in records))
    quotes = coin_api.get_coin_quotes(ids)
    return portfolio.get_summary(records, quotes)


@app.get('/summary/{coin_name}')
def get_coin_summary(coin_name: str):
    _id = db.get_coin_from_db(coin_name).get('market_id')
    records = db.get_all_transactions_by_id(_id)
    quote = coin_api.get_coin_quotes([str(_id)])[0]
    return portfolio.get_coin_summary(records, quote)


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
