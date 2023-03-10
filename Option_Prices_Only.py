import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

class IBapi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)
    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1:
            print("Real-time price of ES:", price)

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

        # Future_Price_ContractObj = Contract()
        # Future_Price_ContractObj.symbol = "MES"
        # Future_Price_ContractObj.secType = "FUT"
        # Future_Price_ContractObj.exchange = "CME"
        # Future_Price_ContractObj.currency = "USD"
        # Future_Price_ContractObj.lastTradeDateOrContractMonth = "202303"
        # self.ib.reqMktData(1, Future_Price_ContractObj, "", False, False, [])

        Options_Price_ContractObj = Contract()
        Options_Price_ContractObj.symbol = "MES"
        Options_Price_ContractObj.secType = "FOP"
        Options_Price_ContractObj.exchange = "CME"
        Options_Price_ContractObj.currency = "USD"
        Options_Price_ContractObj.lastTradeDateOrContractMonth = "20230310"
        Options_Price_ContractObj.strike = "4000"
        Options_Price_ContractObj.right = "C"
        Options_Price_ContractObj.multiplier = "5"
        self.ib.reqMktData(1, Options_Price_ContractObj, "", False, False, [])

    def ran_loop(self):
        self.ib.run()

bot = Bot()
