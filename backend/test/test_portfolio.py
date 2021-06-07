#! python3

# 3p Imports
from datetime import datetime
from random import randint
import pytest

# Internal Imports
import src.portfolio as portfolio


__quotes = [
    {
        "id":1,
        "name":"Bitcoin",
        "supply":18728718,
        "cap":682406944006.8105,
        "price":36436.393778090445,
        "volume":30054876196.487564,
        "percent_changes":{
            "hour":-0.51644039,
            "day":1.29091284,
            "week":5.97669384
        }
    },
    {
        "id":512,
        "name":"Stellar",
        "supply":23126290505.879074,
        "cap":8951241290.012106,
        "price":0.38705910434432,
        "volume":643123978.2671163,
        "percent_changes":{
            "hour":-0.93399816,
            "day":1.65728534,
            "week":5.49675821
        }
    },
    {
        "id":1027,
        "name":"Ethereum",
        "supply":116187622.499,
        "cap":321853104653.1147,
        "price":2770.1152474815876,
        "volume":26269792225.64838,
        "percent_changes":{
            "hour":-0.553813,
            "day":3.66030549,
            "week":21.05878459
        }
    },
    {
        "id":7455,
        "name":"Audius",
        "supply":120000000,
        "cap":130599825.88493522,
        "price":1.08833188237446,
        "volume":8256312.92319176,
        "percent_changes":{
            "hour":-0.99985001,
            "day":2.91680292,
            "week":14.17906912
        }
    }
]


__summary = {
    "total_usd_invested": 409303.3284320182,
    "total_current_usd_value": 201199.04035962015,
    "total_profit": 2647.6515026377224,
    "coin_summaries": {
        "Bitcoin": {
            "current_coins": 4,
            "usd_invested": 356550.6916029601,
            "current_usd_value": 145745.57511236178,
            "total_coin_profit": 2647.4278851783456
        },
        "Stellar": {
            "current_coins": 90,
            "usd_invested": 56.3838944436945,
            "current_usd_value": 34.8353193909888,
            "total_coin_profit": 0.2733433993001988
        },
        "Ethereum": {
            "current_coins": 20,
            "usd_invested": 52668.6185404462,
            "current_usd_value": 55402.304949631754,
            "total_coin_profit": 0
        },
        "Audius": {
            "current_coins": 15,
            "usd_invested": 27.634394168194998,
            "current_usd_value": 16.3249782356169,
            "total_coin_profit": -0.049725939923599416
        }
    }
}


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


def __filter_quotes(coin: str):
    return [quote for quote in __quotes if quote['name'] == coin][0]


def __filter_test_records(coin:str):
    return [record for record in __create_test_records() if record['name'] == coin]


def test_get_summary_retrieves_an_accurate_summary_with_a_valid_portfolio():
    assert portfolio.get_summary(__create_test_records(), __quotes) == __summary


def test_get_coin_summary_retrieves_an_accurate_summary_with_a_valid_coin_record():
    assert portfolio.get_coin_summary(__filter_test_records('Bitcoin'), __filter_quotes('Bitcoin')) == __summary['coin_summaries']['Bitcoin']
    assert portfolio.get_coin_summary(__filter_test_records('Ethereum'), __filter_quotes('Ethereum')) == __summary['coin_summaries']['Ethereum']
    assert portfolio.get_coin_summary(__filter_test_records('Stellar'), __filter_quotes('Stellar')) == __summary['coin_summaries']['Stellar']
    assert portfolio.get_coin_summary(__filter_test_records('Audius'), __filter_quotes('Audius')) == __summary['coin_summaries']['Audius']


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
