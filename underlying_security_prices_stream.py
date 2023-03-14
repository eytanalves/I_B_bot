
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
            print("Real-time price of AAPL:", price)

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

        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        self.ib.reqMktData(1, contract, "", False, False, [])

    def ran_loop(self):
        self.ib.run()

bot = Bot()