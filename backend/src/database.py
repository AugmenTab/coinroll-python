#! python3

# 3p Imports
import mongoengine as db

# Internal Imports
try:
    from config import username, password, database
    from coin_api import get_all_coins
except:
    pass


class Coin(db.Document):
    market_id = db.IntField()
    name = db.StringField()
    symbol = db.StringField()

    def to_json(self):
        return {
            "market_id": self.market_id,
            "name": self.name,
            "symbol": self.symbol,
        }


def update_coin_list():
    data = get_all_coins({})
    for x in data:
        coin = Coin(
            market_id = x['id'],
            name = x['name'],
            symbol = x['symbol']
        )
        new = Coin.objects(market_id=coin.market_id)
        new.update(name=coin.name, symbol=coin.symbol, upsert=True)


def connect_to_db():
    db.connect(
        db=database, 
        host='mongodb://mongodb', 
        port=27017, 
        username=username, 
        password=password
    )
    update_coin_list()
