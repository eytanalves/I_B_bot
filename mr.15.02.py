import pandas as pd
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
import threading
import datetime
import time
import os
option_e_date = datetime.datetime.now().strftime("%Y%m%d")


class IBapi(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self,self)
        self.num = 0


    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1:
            self.data_collector = {
                "price": price,
                "time": datetime.datetime.now().strftime("%H:%M:%S")
            }
            p = pd.DataFrame(self.data_collector,index=[self.num])
            p.to_csv("underlyingprice.csv", mode="a", header=not os.path.exists("underlyingprice.csv"))
            print(f"Under Lynig Price : {price}")
        elif tickType == 4 and reqId == 2:
            print(f"Call Option Price : {price}")
        elif tickType == 4 and reqId == 3:
            print(f"put Option Price : {price}")

    def error(self, reqId, errorCode, errorString):
        print(errorCode)
        print(errorString)



class MarketDataUnderLying:
    def __init__(self, symbol, secType, currency, exchange, expiry):
        self.contract = Contract()
        self.contract.symbol = symbol
        self.contract.secType = secType
        self.contract.currency = currency
        self.contract.exchange = exchange
        self.contract.lastTradeDateOrContractMonth = expiry

class OptionsMarketData:
    def __init__(self, symbol, secType, currency, exchange, expiry, strike, right, multiplier):
        self.contract = Contract()
        self.contract.symbol = symbol
        self.contract.secType = secType
        self.contract.currency = currency
        self.contract.exchange = exchange
        self.contract.lastTradeDateOrContractMonth = expiry
        self.contract.strike = strike
        self.contract.right = right
        self.contract.multiplier = multiplier


class Bot:

    def __init__(self):
        self.id = IBapi()
        self.num = self.id.num
        self.id.connect(host="172.20.10.11", port=7496, clientId=3)
        self.thread = threading.Thread(target=self.ran_loop,daemon=True)
        self.thread.start()
        time.sleep(1)

        self.reqid = 1
        self. market_data = []
        self.req_market_data()

    def req_market_data(self):
        self.market_data.append(MarketDataUnderLying("MES", "FUT", "USD", "CME", "202306"))
        self.market_data.append(OptionsMarketData("MES", "FOP", "USD","CME", option_e_date, 3895, "C", 5))
        self.market_data.append(OptionsMarketData("MES", "FOP", "USD", "CME", option_e_date, 3895, "P", 5))
        for data in self.market_data:
            self.id.reqMktData(reqId=self.reqid,
                               contract=data.contract,
                               genericTickList="",
                               snapshot=False,
                               regulatorySnapshot=False,
                               mktDataOptions=[])
            self.reqid += 1

    def ran_loop(self):
        self.id.run()

bot = Bot()
