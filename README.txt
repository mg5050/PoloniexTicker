## Description

PoloniexTicker is a command-line based service that displays the simple moving average for one or more currency pairs for a given period.


#### Usage

> python ticker.py PERIOD_LEN PERIOD_FUNC CCY_PAIR [CCY_PAIR, ...]

###### Examples

python3 ticker.py 12 second USDT_BTC USDT_ETH BTC_ETH

python3 ticker.py 12 minute USDT_BTC

python3 ticker.py 6 hour USDT_LTC BTC_LTC

python3 ticker.py 1 day BTC_BCH BTC_XRP
