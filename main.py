from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1 :
            print("Real-time price of Call option with strike", round(price, 2), ":", price)

    def error(self, id, errorCode, errorMsg):
        print(errorCode)
        print(errorMsg)


# class MarketData_o():
#     def __init__(self, symbol, secType, exchange, currency, expiry, strike=None, right=None, multiplier=None):
#         self.contract = Contract()
#         self.contract.symbol = symbol
#         self.contract.secType = secType
#         self.contract.exchange = exchange
#         self.contract.currency = currency
#         self.contract.lastTradeDateOrContractMonth = expiry
#         self.contract.strike = strike
#         self.contract.right = right
#         self.contract.multiplier = multiplier

class MarketData():
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
        self.ib.connect(host="127.0.0.1", port=7496, clientId=1)
        self.market_data = []
        self.req_count = 1
        self.req_market_data()
        self.ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        self.ib_thread.start()
        time.sleep(1)

    def req_market_data(self):
        self.market_data.append(MarketData("AAPL", "STK", "SMART", "USD", "202303"))
        # self.market_data.append(MarketData_o("AAPL", "OPT", "SMART", "USD", "202303", 135, "C", 100))
        for data in self.market_data:
            self.ib.reqMktData(self.req_count, data.contract, "", False, False, [])
            self.req_count += 0

    def run_loop(self):
        self.ib.run()


bot = Bot()
