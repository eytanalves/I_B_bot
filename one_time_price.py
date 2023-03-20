import time
from ib_socket import IBapi
import threading
from underlying_contract import MarketDataUnderLying

HOST = "172.20.10.11"
PORT = 7496
CLIENTID = 4

class UnderLyingData:
    def __init__(self):
        self.one_time = IBapi()
        self.one_time.connect(host=HOST, port=PORT, clientId=CLIENTID)
        self.thread = threading.Thread(target=self.ran_loop, daemon=True)
        self.thread.start()
        time.sleep(1)

        self.under_lying_price = None
        self.m_d_u = MarketDataUnderLying("MES", "FUT", "USD", "CME", "202306")
        self.one_time.reqMktData(reqId=1,
                           contract=self.m_d_u.contract,
                           genericTickList="",
                           snapshot=False,
                           regulatorySnapshot=False,
                           mktDataOptions=[])

    def return_underlying_price(self):
        self.under_lying_price = self.one_time.under_price
        return self.under_lying_price


    def ran_loop(self):
         self.one_time.run()

