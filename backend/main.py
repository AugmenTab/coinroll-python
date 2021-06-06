#! python3

# PSL Imports
from typing import Optional

# 3p Imports
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Internal Imports
from src.coin_api import get_coin_quotes
import src.database as db


app = FastAPI()


class Transaction(BaseModel):
    name: str
    quantity: int


class Watch(BaseModel):
    id: int = None
    name: str = None


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


# @app.post('/sell') :: market_id, name, symbol, sell_time, price_in_USD, quantity_sold
# @app.get('/records/{coin_id}')


if __name__ == '__main__':
    db.establish_db()
    uvicorn.run(app, port=8000, host='0.0.0.0')
