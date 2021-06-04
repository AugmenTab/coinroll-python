#! python3

# PSL Imports
from typing import Optional

# 3p Imports
from fastapi import FastAPI
import mongoengine as db
import uvicorn

# Internal Imports
try:
    import config
except:
    pass


class Coin(db.Document):
    name = db.StringField()
    price = db.IntField()

    def to_json(self):
        return {
            "name": self.name,
            "price": self.price
        }


def connect_to_db():
    coin = Coin(
        name = "Ethereum", 
        price = 2000
    )
    coin.save()


app = FastAPI()


def add(a, b):
    return a + b


@app.get("/")
def read_root():
    connect_to_db()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    db.connect(
        db=config.database, 
        host='mongodb://mongodb', 
        port=27017, 
        username=config.username, 
        password=config.password
    )
    uvicorn.run(app, port=8000, host="0.0.0.0")
