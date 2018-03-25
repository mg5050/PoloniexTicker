import websocket
import json
import ccys
import enum
import datetime
import sys
from collections import deque

DEBUG = False
CONTIGUOUS_SMA = False  # require our moving average to be contiguous?
PRINT_IN_PLACE = True  # print in place or show each "tick"?

''' 
Design Choices:

WAMP vs WebSocket:
    WAMP requires a heavy implementation and non-standard libraries. 
    WebSockets are simple and work out of the box. 

Ticker vs Pair feed:
    Pair feed provides a lot of extraneous data.
    Ticker feed is relatively light and gives us visibility on all currencies simultaneously which we can use to display multiple pairs at once. 
'''


class ExchangeMessage(object):
    class Fields(enum.Enum):
        CCY_CODE   = 0
        LAST_PRICE = 1
        LOW_ASK    = 2
        HIGH_BID   = 3
        PCT_CHANGE = 4
        BASE_VOL   = 5
        QUOTE_VOL  = 6
        IS_FROZEN  = 7
        DAY_HIGH   = 8
        DAY_LOW    = 9

    def __init__(self, txt):
        self.data = json.loads(txt)

    def __bool__(self):
        if len(self.data) < 3:  # index 0 = feed id, 1 = status code, 2 = ticker data
            return False
        return True

    def getPairCode(self):
        return int(self.data[2][self.Fields.CCY_CODE.value])

    def getPrice(self):
        return float(self.data[2][self.Fields.LAST_PRICE.value])


class CurrencyPairSMA(object):
    def __init__(self, period, pair):
        self.period = period
        self.pair = pair
        self.last_price = None
        self.closes = deque()
        self.last_close = None
        self.msum = 0.0
        self.sma = 0.0

    def clearCloses(self):
        self.closes = deque()
        self.last_close = None
        self.msum = 0.0
        self.sma = 0.0

    def getLastClose(self):
        return self.last_close

    def addClose(self, ctime):
        self.last_close = ctime
        if len(self.closes) >= self.period:
            self.msum -= self.closes.popleft()

        self.closes.append(self.last_price)
        self.msum += self.last_price
        self.sma = self.msum / len(self.closes)

    def setLastPrice(self, price):
        self.last_price = price

    def getSMA(self):
        return '%.04f' % self.sma

class PoloniexTickerClient(object):
    def __init__(self, pairs, period=12, period_func=lambda dt: dt.minute):
        self.period = period
        self.pairs = pairs
        self.period_func = period_func
        self.pair_codes = {ccys.lookupCCYCode(p): p for p in pairs}
        self.sma = {}

        if DEBUG:
            websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp('wss://api2.poloniex.com/',
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)

    def on_message(self, ws, data):
        msg = ExchangeMessage(data)
        if msg:
            pcode = msg.getPairCode()
            if pcode in self.pair_codes:
                if pcode in self.sma:
                    sma_obj = self.sma[pcode]
                else:
                    sma_obj = CurrencyPairSMA(self.period, pcode)
                    self.sma[pcode] = sma_obj
                self.on_tick(sma_obj, msg)

    def on_tick(self, sma_obj, msg):

        now = self.period_func(datetime.datetime.now())

        if not sma_obj.getLastClose():
            sma_obj.last_close = now
        elif now != sma_obj.getLastClose():
            self.on_period_close(sma_obj, now)
        sma_obj.setLastPrice(msg.getPrice())

    def on_period_close(self, sma_obj, now):
        tdiff = abs(now - sma_obj.getLastClose())

        if CONTIGUOUS_SMA and tdiff != 1 and tdiff != 59:  # TODO - something like closes at 1:00pm and then 2:01pm would produce a bug
            sma_obj.clearCloses()
        else:
            sma_obj.addClose(now)

        self.printAllSMA()

    def printAllSMA(self):
        if PRINT_IN_PLACE:
            sys.stdout.write('\r\t')
        for pname in self.pairs:
            pcode = ccys.lookupCCYCode(pname)
            if pcode in self.sma:
                sys.stdout.write('%s : %s\t' % (pname, self.sma[pcode].getSMA()))
            else:
                sys.stdout.write('%s : %.04f\t' % (pname, 0.0))
        if not PRINT_IN_PLACE:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("--- Connection Closed ---")

    def on_open(self, ws):
        print("--- Connection Established ---")
        ws.send(json.dumps({'command': 'subscribe', 'channel': '1002'}))  # subscribe to all tickers

    def start(self):
        self.ws.run_forever()


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        period_len = int(sys.argv[1])
        assert period_len > 0, 'Invalid period length.'
        period = sys.argv[2]
        assert period in ['hour', 'minute', 'second', 'day', 'year', 'microsecond', 'month'], 'Invalid period function.'
        period_func = lambda dt : getattr(dt, period)
        pairs = sys.argv[3:]
        assert len(set(pairs)) == len(pairs), 'Duplicate pairs specified.'
        client = PoloniexTickerClient(pairs=pairs, period=period_len, period_func=period_func)
        client.start()
    else:
        print('USAGE: python %s PERIOD_LEN PERIOD_FUNC CCY_PAIR [CCY_PAIR, ...]' % sys.argv[0])
