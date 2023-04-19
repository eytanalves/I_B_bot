import threading
import datetime
import time
import math

from new_ib_socket import IBapi
from option_contract import OptionsMarketData
from underlying_contract import MarketDataUnderLying

HOST = "172.20.10.3"
PORT = 7496
CLIENTID = 1

def round_up_to_5(x):
    return math.ceil(x / 5) * 5

def round_down_to_5(x):
    return math.floor(x / 5) * 5

option_e_date = datetime.datetime.now().strftime("%Y%m%d")

class Bot:

    def __init__(self):
        self.ib = IBapi()
        self.ib.connect(host=HOST, port=PORT, clientId=CLIENTID)
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

        time.sleep(1)
        self.m_d_u = MarketDataUnderLying("MES", "FUT", "USD", "CME", "202306")
        self.request_market_data(reqId=1, contract=self.m_d_u.contract)

        time.sleep(1)
        underlying_price = self.ib.return_price()
        self.call_strike = round_up_to_5(underlying_price)
        self.put_strike = round_down_to_5(underlying_price)

        print(f"UNDERLYING PRICE: {underlying_price}")
        print("#                #                  #")
        print(f"CALL STRIKE: {self.call_strike}")
        print("#                #                  #")
        print(f"PUT STRIKE: {self.put_strike}")
        print("#                #                  #")

        self.call_contract = OptionsMarketData("MES", "FOP", "USD", "CME", option_e_date, self.call_strike, "C", 5)
        self.put_contract = OptionsMarketData("MES", "FOP", "USD", "CME", option_e_date, self.put_strike, "P", 5)
        self.reqid = 2
        self.market_data = [self.call_contract, self.put_contract]
        self.request_all_market_data()

    def request_market_data(self, reqId, contract):
        self.ib.reqMktData(reqId=reqId, contract=contract, genericTickList="", snapshot=False, regulatorySnapshot=False,
                           mktDataOptions=[])

    def request_all_market_data(self):
        for data in self.market_data:
            self.request_market_data(reqId=self.reqid, contract=data.contract)
            self.reqid += 1

    def run_loop(self):
        self.ib.run()

# bot = Bot()
#######################################################################

# from new_ib_socket import IBapi
# from option_contract import OptionsMarketData
# # from one_time_price import UnderlyingData
# import threading
# import datetime
# import time
# import math
#
# from underlying_contract import MarketDataUnderLying
#
#
# HOST = "172.20.10.11"
# PORT = 7496
# CLIENTID = 1
#
# def round_up_to_5(x):
#     return math.ceil(x / 5) * 5
# def round_down_to_5(x):
#     return math.floor(x / 5) * 5
#
# option_e_date = datetime.datetime.now().strftime("%Y%m%d")
# # option_e_date = "20230428"
#
# class Bot:
#
#     def __init__(self):
#         self.ib = IBapi()
#         self.ib.connect(host=HOST, port=PORT, clientId=CLIENTID)
#         self.thread = threading.Thread(target=self.ran_loop, daemon=True)
#         self.thread.start()
#         time.sleep(1)
#         self.m_d_u = MarketDataUnderLying("MES", "FUT", "USD", "CME", "202306")
#         self.ib.reqMktData(reqId=1,
#                            contract=self.m_d_u.contract,
#                            genericTickList="",
#                            snapshot=False,
#                            regulatorySnapshot=False,
#                            mktDataOptions=[])
#         time.sleep(1)
#         underlying_price = self.ib.return_price()
#         self.call_strike = round_up_to_5(underlying_price)
#         self.put_strike = round_down_to_5(underlying_price)
#         print(f"UNDERLYING PRICE: {underlying_price}")
#         print("#                #                  #")
#         print(f"CALL STRIKE: {self.call_strike}")
#         print("#                #                  #")
#         print(f"PUT STRIKE: {self.put_strike}")
#         print("#                #                  #")
#
#
#         # self.m_d_u = MarketDataUnderLying("MES", "FUT", "USD", "CME", "202306")
#         self.call_contract = OptionsMarketData("MES",
#                                          "FOP",
#                                          "USD",
#                                          "CME",
#                                                option_e_date,
#                                                self.call_strike,
#                                          "C",
#                                                5)
#         self.put_contract = OptionsMarketData("MES",
#                                          "FOP",
#                                          "USD",
#                                          "CME",
#                                               option_e_date,
#                                               self.put_strike,
#                                          "P",
#                                               5)
#
#         self.reqid = 2
#         self. market_data = []
#         self.req_market_data()
#
#     def req_market_data(self):
#         # self.market_data.append(self.m_d_u)
#         self.market_data.append(self.call_contract)
#         self.market_data.append(self.put_contract)
#         for data in self.market_data:
#             self.ib.reqMktData(reqId=self.reqid,
#                                contract=data.contract,
#                                genericTickList="",
#                                snapshot=False,
#                                regulatorySnapshot=False,
#                                mktDataOptions=[])
#             self.reqid += 1
#
#     def ran_loop(self):
#         self.ib.run()
#################################################################

# bot = Bot()






# from new_ib_socket import IBapi
# from option_contract import OptionsMarketData
# from one_time_price import UnderLyingData
# import threading
# import time
# import math
# # from tkinter import *
#
# # import random
# # import datetime
#
#
# HOST = "172.20.10.3"
# PORT = 7496
# CLIENTID = 3
#
# def round_up_to_5(x):
#     return math.ceil(x / 10) * 10
# def round_down_to_5(x):
#     return math.floor(x / 10) * 10
#
# # option_e_date = datetime.datetime.now().strftime("%Y%m%d")
# option_e_date = "20230428"
# class Bot:
#
#     def __init__(self):
#         self.put_contract = None
#         self.one_time_price = UnderLyingData()
#         time.sleep(1)
#         put_strike = round_down_to_5(self.one_time_price.return_underlying_price())
#         call_strike = round_up_to_5(self.one_time_price.return_underlying_price())
#         print(f"#####{put_strike}#####")
#         print(f"#####{call_strike}#####")
#
#         self.ib = IBapi()
#
#         self.ib.connect(host=HOST, port=PORT, clientId=CLIENTID)
#         # self.m_d_u = MarketDataUnderLying("MES", "FUT", "USD", "CME", "202306")
#         self.o_m_d_c = OptionsMarketData("MES",
#                                          "FOP",
#                                          "USD",
#                                          "CME",
#                                          option_e_date ,
#                                          call_strike,
#                                          "C",
#                                          5)
#         self.o_m_d_p = OptionsMarketData("MES",
#                                          "FOP",
#                                          "USD",
#                                          "CME",
#                                          option_e_date,
#                                          put_strike,
#                                          "P",
#                                          5)
#         self.thread = threading.Thread(target=self.ran_loop,daemon=True)
#         self.thread.start()
#         time.sleep(1)
#         self.req_id = 2
#         self. market_data = []
#         self.req_market_data()
#
#     def req_market_data(self):
#         # self.market_data.append(self.m_d_u)
#         self.market_data.append(self.o_m_d_c)
#         self.market_data.append(self.o_m_d_p)
#         for data in self.market_data:
#             self.ib.reqMktData(reqId=self.req_id,
#                                contract=data.contract,
#                                genericTickList="",
#                                snapshot=False,
#                                regulatorySnapshot=False,
#                                mktDataOptions=[])
#             self.req_id += 1
#
#     def ran_loop(self):
#         self.ib.run()
#

# bot = Bot()


# plt.style.use('fivethirtyeight')
#
# index = count()
# def animate(i):
#     f = pd.read_csv('csv_directory/price.csv')
#     y = f['price']
#
#     plt.cla()
#     plt.plot(y)
#
# ani = FuncAnimation(plt.gcf(), animate, interval=1000)
#
# plt.tight_layout()
# plt.show()

# while True:
#     file = pd.read_csv("csv_directory/price.csv")
# # print(f'@@@@@@@@@@@@@@{file["price"].tolist()}')
#
#
#     window = Tk()
#     window.title("CALL OF DODY")
#     window.minsize(width=500, height=1000)
#
#     call_label = Label(text="CALL : ", font=("Ariel", 20, "bold"))
#     call_label.grid(column=0, row=0)
#
#     put_label = Label(text="PUT : ", font=("Ariel", 20, "bold"))
#     put_label.grid(column=2, row=0)
#
#     call_listbox = Listbox(height=10, width=8)
#     fruits = file["price"].tolist()
#     for item in fruits:
#         call_listbox.insert(fruits.index(item), item)
#     call_listbox.grid(column=1, row=1)
#
#     put_listbox = Listbox(height=10, width=8)
#     fruits = file["price"].tolist()
#     for item in fruits:
#         put_listbox.insert(fruits.index(item), item)
#     put_listbox.grid(column=3, row=1)
#
#     window.mainloop()
#
