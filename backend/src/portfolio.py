#! python3

# PSL Imports
from itertools import groupby


def __get_coin_count(records):
    owned = 0
    for record in records:
        if record['type'] == 'purchase':
            owned += record['quantity']
        else:
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


def has_sufficient_coins(records, selling):
    return __get_coin_count(records) >= selling


def get_coin_summary(records, quote):
    spent = [r['quantity'] * r['price_in_usd'] 
             for r in records if r['type'] == 'purchase']
    current_coins = __get_coin_count(records)
    return {
        'current_coins': current_coins,
        'usd_invested': sum(spent),
        'current_usd_value': quote['price'] * current_coins,
        'total_coin_profit': __get_total_coin_profit(records)
    }


# def get_summary(records, quote):
#     summaries = [get_coin_summary(record, quote) for record in records]
#     return {
#         'total_usd_invested': _,
#         'total_current_usd_value': _,
#         'total_profit': _,
#         'coin_summaries': summaries
#     }
