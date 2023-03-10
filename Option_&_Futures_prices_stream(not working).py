import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import math

def round_up_to_5(x):
    return math.ceil(x/5) * 5

def round_down_to_5(x):
    return math.floor(x/5) * 5

class IBapi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)
    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 2:
            print("Real-time price of Call option with strike", round_up_to_5(price), ":", price)

    def error(self, id, errorCode, errorMdg):
        print(errorCode)
        print(errorMdg)

class Bot():
    ib = None
    def __init__(self):
        self.ib = IBapi()
        self.ib.connect(host="127.0.0.1", port=7496, clientId=1)
        ib_thread = threading.Thread(target=self.ran_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)

        Underlying_Price = Contract()
        Underlying_Price.symbol = "MES"
        Underlying_Price.secType = "FUT"
        Underlying_Price.exchange = "CME"
        Underlying_Price.currency = "USD"
        Underlying_Price.lastTradeDateOrContractMonth = "202303"
        self.ib.reqMktData(1, Underlying_Price, "", False, False, [])

        Options_Price = Contract()
        Options_Price.symbol = "MES"
        Options_Price.secType = "FOP"
        Options_Price.exchange = "CME"
        Options_Price.currency = "USD"
        Options_Price.lastTradeDateOrContractMonth = "202303"
        Options_Price.strike = round_up_to_5(Underlying_Price)
        Options_Price.right = "C"
        self.ib.reqMktData(2, Options_Price, "", False, False, [])

    def ran_loop(self):
        self.ib.run()

bot = Bot()
