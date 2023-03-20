from ib_socket import IBapi
from option_contract import OptionsMarketData
from one_time_price import UnderLyingData
import threading
import datetime
import time
import math

HOST = "172.20.10.11"
PORT = 7496
CLIENTID = 3

def round_up_to_5(x):
    return math.ceil(x / 5) * 5
def round_down_to_5(x):
    return math.floor(x / 5) * 5

option_e_date = datetime.datetime.now().strftime("%Y%m%d")

class Bot:

    def __init__(self):
        self.one_time_price = UnderLyingData()
        time.sleep(1)
        put_strike = round_down_to_5(self.one_time_price.return_underlying_price())
        call_strike = round_up_to_5(self.one_time_price.return_underlying_price())
        print(f"#####{put_strike}#####")
        print(f"#####{call_strike}#####")

        self.ib = IBapi()
        self.ib.connect(host=HOST, port=PORT, clientId=CLIENTID)
        # self.m_d_u = MarketDataUnderLying("MES", "FUT", "USD", "CME", "202306")
        self.o_m_d_c = OptionsMarketData("MES",
                                         "FOP",
                                         "USD",
                                         "CME",
                                         option_e_date ,
                                         call_strike,
                                         "C",
                                         5)
        self.o_m_d_p = OptionsMarketData("MES",
                                         "FOP",
                                         "USD",
                                         "CME",
                                         option_e_date,
                                         put_strike,
                                         "P",
                                         5)
        self.thread = threading.Thread(target=self.ran_loop,daemon=True)
        self.thread.start()
        time.sleep(1)
        self.req_id = 2
        self. market_data = []
        self.req_market_data()

    def req_market_data(self):
        # self.market_data.append(self.m_d_u)
        self.market_data.append(self.o_m_d_c)
        self.market_data.append(self.o_m_d_p)
        for data in self.market_data:
            self.ib.reqMktData(reqId=self.req_id,
                               contract=data.contract,
                               genericTickList="",
                               snapshot=False,
                               regulatorySnapshot=False,
                               mktDataOptions=[])
            self.req_id += 1

    def ran_loop(self):
        self.ib.run()


bot = Bot()


