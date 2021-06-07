#! python3

username = '<Your MongoDB username.>'
password = '<Your MongoDB password.>'
database = '<The name of the MongoDB database you are using.>'
api_key = '<Your CoinMarketCap API key.>'

task_ignore_result = False
timezone = 'UTC'

beat_schedule = {
    'update_watchlist': {
        'task': 'main.update_watchlist_prices',
        'schedule': 30.0
    }
}
