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
except Exception as e:
    print(e)


class Coin(db.Document):
    """
    Coin represents a cryptocurrency as it is stored in the database.
    
    :param market_id: The CoinMarketCap API market ID for the coin.
    :param name: The common name for the cryptocurrency.
    :param symbol: The ticker symbol for the cryptocurrency.
    """
    market_id = db.IntField()
    name = db.StringField()
    symbol = db.StringField()

    def to_json(self):
        """
        This function converts the Coin object into json.

        :param self: The Coin object.
        :return: The jsonified Coin object.
        """
        return {
            'market_id': self.market_id,
            'name': self.name,
            'symbol': self.symbol,
        }


class Transaction(db.Document):
    """
    Transaction represents a cryptocurrency transaction record as it is stored
    in the database.

    :param market_id: The CoinMarketCap API market ID for the coin.
    :param name: The common name for the cryptocurrency.
    :param type: The type of transaction - a purchase or a sell.
    :param transaction_time: The time the transaction took place.
    :param price_in_usd: The cryptocurrency's price in USD at the time of the
    transaction.
    :param quantity: The quantity of the cryptocurrency being purchased or sold.
    """
    market_id = db.IntField()
    name = db.StringField()
    type = db.StringField()
    transaction_time = db.DateTimeField()
    price_in_usd = db.FloatField()
    quantity = db.IntField()

    def to_json(self):
        """
        This function converts the Transaction object into json.

        :param self: The Transaction object.
        :return: The jsonified Transaction object.
        """
        return {
            'market_id': self.market_id,
            'name': self.name,
            'type': self.type,
            'transaction_time': self.transaction_time,
            'price_in_usd': self.price_in_usd,
            'quantity': self.quantity
        }


class Watch(db.Document):
    """
    Watch represents a cryptocurrency that the user has added to their watchlist
    so that they can receive its current financial information.

    :param market_id: The CoinMarketCap API market ID for the coin.
    :param name: The common name for the cryptocurrency.
    :param symbol: The ticker symbol for the cryptocurrency.
    :param logo: A URL to an image of the cryptocurrency's logo.
    :param website: A URL to the cryptocurrency's official website.
    :param supply: The cryptocurrency's estimated circulating supply.
    :param cap: The total evaluation of all coins that have been mined in USD.
    :param price: The cryptocurrency's current value in USD.
    :param volume: The amount of the cryptocurrency that has been traded in the
    last 24 hours.
    :param hour_change: The cryptocurrency's percent change over the past hour.
    :param day_change: The cryptocurrency's percent change over the past day.
    :param week_change: The cryptocurrency's percent change over the past week.
    :param last_updated: The timestamp of the cryptocurrency's last update in
    the database.
    """
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
        """
        This function converts the Watch object into json.

        :param self: The Watch object.
        :return: The jsonified Watch object.
        """
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
    """
    This function updates the Coin collection in the database with a current map
    of all cryptocurrencies currently available on the market, per the
    CoinMarketCap API this project uses.

    :param data: The list of cryptocurrencies currently available.
    :return: None
    """
    for x in data:
        coin = Coin(
            market_id = x['id'],
            name = x['name'],
            symbol = x['symbol']
        )
        new = Coin.objects(market_id=coin.market_id)
        new.update(name=coin.name, symbol=coin.symbol, upsert=True)


async def update_watchlist(quotes):  # tasks
    """
    This function updates the user's watchlist with recent financial information
    for each cryptocurrency they're currently watching.

    :param quotes: The financial information received from the CoinMarketCap
    API.
    :return: None
    """
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
    """
    This function retrieves cryptocurrency information from the database.

    :param name: The common name of the cryptocurrency.
    :return: The requested Coin.
    """
    return Coin.objects(name=name).first().to_json()


async def get_coin_from_watchlist(_id):
    """
    This function retrieves a coin from the watchlist.

    :param _id: The CoinMarketCap API market ID for the coin.
    :return: The requested Watch.
    """
    return Watch.objects(market_id=_id).first()


async def get_watchlist():
    """
    This function returns the user's watchlist.

    :return: A list of Watch objects representing the watchlist.
    """
    return [coin.to_json() for coin in Watch.objects()]


async def add_watched_coin(_id, metadata, quote):
    """
    This function adds a cryptocurrency to the watchlist.

    :param _id: The CoinMarketCap API market ID for the coin.
    :param metadata: The metadata for the requested cryptocurrency.
    :param quote: The current financial information for the requested
    cryptocurrency.
    :return: A confirmation that the Watch was saved to the database.
    """
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
    """
    This function removes a coin from the watchlist.

    :param _id: The CoinMarketCap API market ID for the coin.
    :return: A confirmation that the Watch has been deleted from the database.
    """
    return Watch.objects(market_id=_id).first().delete()


async def create_transaction(_id, quantity, quote, _type):
    """
    This function creates a Transaction and adds it to the database.

    :param _id: The CoinMarketCap API market ID for the coin.
    :param quantity: The amount of cryptocurrency being purchased or sold.
    :param quote: The current financial information for the requested
    cryptocurrency.
    :param _type: The Transaction type - a purchase or a sell.
    :return: A confirmation that the Transaction was added to the database.
    """
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
    """
    This function returns all Transactions in the database.

    :return: A list of all Transaction objects in the database.
    """
    records = Transaction.objects().order_by('transaction_time')
    return [record.to_json() for record in records]


async def get_all_transactions_by_id(_id):
    """
    This function returns all Transactions in the database for a particular
    cryptocurrency.

    :param _id: The CoinMarketCap API market ID for the coin.
    :return: A list of all Transaction objects for the given ID in the database.
    """
    records = Transaction.objects(market_id=_id).order_by('transaction_time')
    return [record.to_json() for record in records]


def connect_to_db():
    """
    This function connects the app to the database.

    :return: None
    """
    db.connect(
        db=database, 
        host='mongodb://mongodb', 
        port=27017, 
        username=username, 
        password=password
    )
