#! python3

# PSL Imports
from itertools import groupby


def __get_coin_count(records):
    owned = 0
    for record in records:
        if record['type'] == 'purchase':
            owned += record['quantity']
        elif record['type'] == 'sell':
            owned -= record['quantity']
    return owned


def __make_queue(records):
    queue = []
    for record in records:
        for _ in range(record['quantity']):
            queue.append(record['price_in_usd'])
    return queue


def __get_total_coin_profit(records):
    g = {t: __make_queue(v) for t, v in groupby(records, lambda r: r['type'])}
    profit = 0
    if not g.get('sell'):
        return profit
    for sale in g['sell']:
        profit += sale - g['purchase'].pop(0)
    return profit


def get_coin_summary(records, quote):
    """
    This function formats a provided transaction history and provided price
    information for a given cryptocurrency in the user's portfolio into a
    summary for that cryptocurrency.

    :param records: The user's history of transaction records for a given
    cryptocurrency.
    :param quote: The current financial information for the cryptocurrency.
    :return: The portfolio summary for the given cryptocurrency.
    """
    spent = [r['quantity'] * r['price_in_usd'] 
             for r in records if r['type'] == 'purchase']
    current_coins = __get_coin_count(records)
    return {
        'current_coins': current_coins,
        'usd_invested': sum(spent),
        'current_usd_value': quote['price'] * current_coins,
        'total_coin_profit': __get_total_coin_profit(records)
    }


def get_summary(records, quotes):
    """
    This function formats a provided transaction history and provided price
    information for all cryptocurrencies in the transaction history into a
    complete portfolio summary.

    :param records: The user's complete history of transaction records.
    :param quotes: The current financial information for each cryptocurrency the
    user currently owns.
    :return: The complete portfolio summary.
    """
    coin_groups = {coin: [r for r in records if r['name'] == coin] 
                   for coin, _ in groupby(records, lambda r: r['name'])}
    summaries = {q['name']: get_coin_summary(coin_groups[q['name']], q) 
                 for q in quotes}
    stripped = [summaries[s] for s in summaries]
    total_usd_invested = 0
    total_current_usd_value = 0
    total_profit = 0
    for summary in stripped:
        total_usd_invested += summary['usd_invested']
        total_current_usd_value += summary['current_usd_value']
        total_profit += summary['total_coin_profit']
    return {
        'total_usd_invested': total_usd_invested,
        'total_current_usd_value': total_current_usd_value,
        'total_profit': total_profit,
        'coin_summaries': summaries
    }


def has_sufficient_coins(records, selling):
    """
    This function determines whether the user has sufficient stock of a given
    cryptocurrency in their portfolio to make a sale.

    :param records: The transaction records for the cryptocurrency the user
    wishes to sell.
    :param selling: The quantity of said cryptocurrency the user wishes to sell.
    :return: The boolean value for whether the user has sufficient stock of the
    cryptocurrency in order to make the sale.
    """
    return __get_coin_count(records) >= selling
