from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
import threading
import time
import math
import datetime

#those function are for rounding the underlying security price to the nearest number that can be devided by 5.
#the option strikes are every 5 dollars, so for the call strike the price of the underlying assets should be round up to 5

option_expiry_date = datetime.datetime.now().strftime("%Y%m%d")

def round_up_to_5(x):
    return math.ceil(x / 5) * 5


def round_down_to_5(x):
    return math.floor(x / 5) * 5



class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.call_strike = 0
        self.put_strike = 0


    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1:
            print(f"underlying     {price}")
            print()
        if tickType == 4 and reqId == 2:
            print(f"Call 0D  {self.call_strike}: {price}")
            print()
        if tickType == 4 and reqId == 3:
            print(f"Put 0D   {self.put_strike}: {price}",)
            print()


    def error(self, id, errorCode, errorMsg):
        print(errorCode)
        print(errorMsg)


class IBSnapshot(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.underlying_snapshot = 0

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1003:
            self.underlying_snapshot = price
            # print("snapshot1", self.underlying_snapshot)
            # print()
            # print("     1003     ", price)

        def error(self, id, errorCode, errorMsg):
            print(errorCode)
            print(errorMsg)

class MarketDataOptions():
    def __init__(self, symbol, secType, exchange, currency, expiry, strike=None, right=None, multiplier=None):
        self.contract = Contract()
        self.contract.symbol = symbol
        self.contract.secType = secType
        self.contract.exchange = exchange
        self.contract.currency = currency
        self.contract.lastTradeDateOrContractMonth = expiry
        self.contract.strike = strike
        self.contract.right = right
        self.contract.multiplier = multiplier

class MarketDataUnderlying():
    def __init__(self, symbol, secType, exchange, currency, expiry):
        self.contract = Contract()
        self.contract.symbol = symbol
        self.contract.secType = secType
        self.contract.exchange = exchange
        self.contract.currency = currency
        self.contract.lastTradeDateOrContractMonth = expiry

class Bot():
    def __init__(self):
        self.ib = IBapi()
        self.ib.connect(host="172.20.10.3", port=7496, clientId=2)
        self.market_data = []
        self.req_count = 1

        self.underlying = MarketDataUnderlying("MES", "FUT", "CME", "USD", "202306")
        self.snapshot = IBSnapshot()
        self.snapshot.connect(host="172.20.10.3", port=7496, clientId=1)
        self.snapshot.reqMktData(1003, self.underlying.contract, "", False, False, [])
        self.snapshot_thread = threading.Thread(target=self.run_snapshot, daemon=True)
        self.snapshot_thread.start()
        time.sleep(1)
        self.snapshot_price = self.snapshot.underlying_snapshot
        print("snapshot 22222", self.snapshot_price)

        self.call_strike = round_up_to_5(self.snapshot_price)
        self.ib.call_strike = self.call_strike
        self.put_strike = round_down_to_5(self.snapshot_price)
        self.ib.put_strike = self.put_strike

        self.req_market_data()
        self.ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        self.ib_thread.start()
        time.sleep(1)

    def req_market_data(self):
        self.market_data.append(MarketDataUnderlying("MES", "FUT", "CME", "USD", "202306"))
        self.market_data.append(MarketDataOptions("MES", "FOP", "CME", "USD", "20230315", self.call_strike, "C", 5))
        self.market_data.append(MarketDataOptions("MES", "FOP", "CME", "USD", "20230315", self.put_strike , "P", 5))
        for data in self.market_data:
            self.ib.reqMktData(self.req_count, data.contract, "", False, False, [])
            self.req_count += 1

    def run_snapshot(self):
        self.snapshot.run()

    def run_loop(self):
        self.ib.run()


bot = Bot()
