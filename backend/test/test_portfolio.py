#! python3

# 3p Imports
from datetime import datetime
from random import randint
import pytest

# Internal Imports
import src.portfolio as portfolio


def __create_test_record(m_id: int, name: str, _type: str, time: datetime, price: float, qty: int):
    return {
        'market_id': m_id,
        'name': name,
        'type': _type,
        'transaction_time': time,
        'price_in_usd': price,
        'quantity': qty
   }


def __create_test_records():
    return [
        __create_test_record(1027, 'Ethereum', 'purchase', datetime(2021,6,6,0,42,50,910000), 2633.4309270223102, 20),
        __create_test_record(1, 'Bitcoin', 'purchase', datetime(2021,6,6,1,4,2,50000), 35667.03870840223, 7),
        __create_test_record(512, 'Stellar', 'purchase', datetime(2021,6,6,1,4,11,712000), 0.37589262962463, 150),
        __create_test_record(1, 'Bitcoin', 'purchase', datetime(2021,6,6,1,5,48,220000), 35627.14021471484, 3),
        __create_test_record(1, 'Bitcoin', 'sell', datetime(2021,6,6,2,31,58,215000), 36108.27668926529, 6),
        __create_test_record(512, 'Stellar', 'sell', datetime(2021,6,6,2,44,43,979000), 0.3804483529463, 60),
        __create_test_record(7455, 'Audius', 'purchase', datetime(2021,6,7,0,30,33,229000), 1.1053757667278, 25),
        __create_test_record(7455, 'Audius', 'sell', datetime(2021,6,7,0,37,37,593000), 1.10040317273544, 10),
    ]


def __filter_test_records(coin):
    return [record for record in __create_test_records() if record['name'] == coin]


def test_has_sufficient_coins_returns_true_when_portfolio_has_enough_coins_to_sell():
    assert portfolio.has_sufficient_coins(__filter_test_records('Bitcoin'), randint(1, 3))
    assert portfolio.has_sufficient_coins(__filter_test_records('Ethereum'), randint(1, 19))
    assert portfolio.has_sufficient_coins(__filter_test_records('Stellar'), randint(1, 89))
    assert portfolio.has_sufficient_coins(__filter_test_records('Audius'), randint(1, 14))


def test_has_sufficient_coins_returns_false_when_portfolio_has_insufficient_coins_to_sell():
    assert not portfolio.has_sufficient_coins(__filter_test_records('Bitcoin'), 5)
    assert not portfolio.has_sufficient_coins(__filter_test_records('Ethereum'), 21)
    assert not portfolio.has_sufficient_coins(__filter_test_records('Stellar'), 91)
    assert not portfolio.has_sufficient_coins(__filter_test_records('Audius'), 16)


def test_has_sufficient_coins_returns_true_when_user_sells_all_coins():
    assert portfolio.has_sufficient_coins(__filter_test_records('Bitcoin'), 4)
    assert portfolio.has_sufficient_coins(__filter_test_records('Ethereum'), 20)
    assert portfolio.has_sufficient_coins(__filter_test_records('Stellar'), 90)
    assert portfolio.has_sufficient_coins(__filter_test_records('Audius'), 15)
