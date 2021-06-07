#! python3

# PSL Imports
from datetime import datetime
import asyncio

# 3p Imports
import mongoengine as db

# Internal Imports
try:
    from src.config import username, password, database
    import src.coin_api as coin_api
except Exception as e:
    print(e)


class Coin(db.Document):
    """
    ___
    
    :param:
    """
    market_id = db.IntField()
    name = db.StringField()
    symbol = db.StringField()

    def to_json(self):
        return {
            'market_id': self.market_id,
            'name': self.name,
            'symbol': self.symbol,
        }


class Transaction(db.Document):
    market_id = db.IntField()
    name = db.StringField()
    type = db.StringField()
    transaction_time = db.DateTimeField()
    price_in_usd = db.FloatField()
    quantity = db.IntField()

    def to_json(self):
        return {
            'market_id': self.market_id,
            'name': self.name,
            'type': self.type,
            'transaction_time': self.transaction_time,
            'price_in_usd': self.price_in_usd,
            'quantity': self.quantity
        }


class Watch(db.Document):
    market_id = db.IntField()
    name = db.StringField()
    symbol = db.StringField()
    logo = db.StringField()
    website = db.StringField()
    supply = db.IntField()
    cap = db.IntField()
    price = db.FloatField()
    volume = db.IntField()
    hour_change = db.FloatField()
    day_change = db.FloatField()
    week_change = db.FloatField()
    last_updated = db.DateTimeField()

    def to_json(self):
        return {
            'market_id': self.market_id,
            'name': self.name,
            'symbol': self.symbol,
            'logo': self.logo,
            'website': self.website,
            'supply': self.supply,
            'cap': self.cap,
            'price': self.price,
            'volume': self.volume,
            'hour_change': self.hour_change,
            'day_change': self.day_change,
            'week_change': self.week_change,
            'last_updated': self.last_updated
        }


def update_coin_list(data):  # tasks
    for x in data:
        coin = Coin(
            market_id = x['id'],
            name = x['name'],
            symbol = x['symbol']
        )
        new = Coin.objects(market_id=coin.market_id)
        new.update(name=coin.name, symbol=coin.symbol, upsert=True)


async def update_watchlist(quotes):  # tasks
    for quote in quotes:
        Watch.objects(market_id=quote['id']).update(
            supply = quote['supply'],
            cap = quote['cap'],
            price = quote['price'],
            volume = quote['volume'],
            hour_change = quote['percent_changes']['hour'],
            day_change = quote['percent_changes']['day'],
            week_change = quote['percent_changes']['week'],
            last_updated = datetime.utcnow()
        )


async def get_coin_from_db(name):
    return Coin.objects(name=name).first().to_json()


async def get_coin_from_watchlist(_id):
    return Watch.objects(market_id=_id).first()


async def get_watchlist():
    return [coin.to_json() for coin in Watch.objects()]


async def add_watched_coin(_id, metadata, quote):
    watch = Watch(
        market_id = _id,
        name = metadata['name'],
        symbol = metadata['symbol'],
        logo = metadata['logo'],
        website = metadata['website'],
        supply = quote['supply'],
        cap = quote['cap'],
        price = quote['price'],
        volume = quote['volume'],
        hour_change = quote['percent_changes']['hour'],
        day_change = quote['percent_changes']['day'],
        week_change = quote['percent_changes']['week'],
        last_updated = datetime.utcnow()
    )
    return watch.save()


async def remove_watched_coin(_id):
    return Watch.objects(market_id=_id).first().delete()


async def create_transaction(_id, quantity, quote, _type):
    transaction = Transaction(
        market_id = _id,
        name = quote['name'],
        type = _type,
        transaction_time = datetime.utcnow(),
        price_in_usd = quote['price'],
        quantity = quantity
    )
    return transaction.save()


async def get_all_transactions():
    records = Transaction.objects().order_by('transaction_time')
    return [record.to_json() for record in records]


async def get_all_transactions_by_id(_id):
    records = Transaction.objects(market_id=_id).order_by('transaction_time')
    return [record.to_json() for record in records]


def connect_to_db():
    db.connect(
        db=database, 
        host='mongodb://mongodb', 
        port=27017, 
        username=username, 
        password=password
    )
