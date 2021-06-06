#! python3

# PSL Imports
from datetime import datetime
# import asyncio

# 3p Imports
import mongoengine as db

# Internal Imports
try:
    from src.config import username, password, database
    import src.coin_api as coin_api
except:
    pass


class Coin(db.Document):
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


def update_watchlist(quotes):
    for quote in quotes:
        # {quote['id']: quote}
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


def get_coin_from_db(name):
    return Coin.objects(name=name).first().to_json()


def get_coin_from_watchlist(id):
    return Watch.objects(market_id=id).first()


def get_watchlist():
    return [coin.to_json() for coin in Watch.objects()]


def add_watched_coin(id):
    metadata = coin_api.get_coin_metadata([str(id)])[0]
    quote = coin_api.get_coin_quotes([str(id)])[0]
    watch = Watch(
        market_id = id,
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
        week_change = quote['percent_changes']['week']
    )
    return watch.save()


def remove_watched_coin(id):
    return Watch.objects(market_id=id).first().delete()


def create_transaction(id, quantity, type):
    quote = coin_api.get_coin_quotes([str(id)])[0]
    transaction = Transaction(
        market_id = id,
        name = quote['name'],
        type = type,
        transaction_time = datetime.utcnow(),
        price_in_usd = quote['price'],
        quantity = quantity
    )
    return transaction.save()


def get_all_transactions_by_id(id):
    records = Transaction.objects(market_id=id).order_by('transaction_time')
    return [record.to_json() for record in records]


def get_all_transactions():
    records = Transaction.objects().order_by('transaction_time')
    return [record.to_json() for record in records]


def __update_coin_list(data):  # tasks
    for x in data:
        coin = Coin(
            market_id = x['id'],
            name = x['name'],
            symbol = x['symbol']
        )
        new = Coin.objects(market_id=coin.market_id)
        new.update(name=coin.name, symbol=coin.symbol, upsert=True)


def establish_db(query_api=False):
    db.connect(
        db=database, 
        host='mongodb://mongodb', 
        port=27017, 
        username=username, 
        password=password
    )
    if query_api:
        __update_coin_list(coin_api.get_coin_listing())
