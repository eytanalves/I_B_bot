
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
# from ibapi.order import *
import threading
import time

class IBapi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)
    def realtimeBar(self, reqId, time, open_ , high, low, close,volume, wap, count):
        super().realtimeBar(reqId, time, open_ , high, low, close,volume, wap, count)
        try:
            bot.on_bar_update(reqId, time, open_ , high, low, close,volume, wap, count)
        except Exception as e:
            print(e)
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

        symbol = "TSLA"
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        self.ib.reqRealTimeBars(0, contract, 5, "TRADES",True, [])

    def on_bar_update(self, reqId, time:int, open_: float, high: float, low: float, close: float,
                        volume: int, wap: float, count: int):
        print(close)

    def ran_loop(self):
        self.ib.run()

bot = Bot()