#! python3

# PSL Imports
from typing import Optional

# 3p Imports
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Internal Imports
try:
    from coin_api import get_coin_quotes
    from database import establish_db, get_coin_from_db, add_watched_coin, get_coin_from_watchlist, remove_watched_coin
except:
    pass


app = FastAPI()


class Watch(BaseModel):
    id: int = None
    name: str = None


def add(a, b):
    return a + b


@app.get('/')
def read_root():
    return {"Hello": "World"}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
    return {'item_id': item_id, 'q': q}


# @app.get('/')  display watched coins


@app.post('/watch')
def watch_coin(watch: Watch):
    id = get_coin_from_db(watch.name).get('market_id')
    if not get_coin_from_watchlist(id):
        return add_watched_coin(id)


@app.delete('/watch')
def unwatch_coin(watch: Watch):
    if not watch.id:
        watch.id = get_coin_from_db(watch.name).get('market_id')
    return remove_watched_coin(watch.id)


# @app.post('/buy')
# @app.post('/sell')
# @app.get('/records/{coin_id}')


if __name__ == '__main__':
    establish_db()
    uvicorn.run(app, port=8000, host='0.0.0.0')
