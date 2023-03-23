from data_manager import Bot
from ibapi.order import Order
import time
import math

def round_down_to_025(x):
    return math.floor(x / 0.25) * 0.25

class EntryOrder():
    def __init__(self, leg):
        self.entry_order = Order()
        self.entry_order.orderType = "BOX TOP"
        self.entry_order.action = leg
        self.entry_order.totalQuantity = 1
        self.entry_order.eTradeOnly = False
        self.entry_order.firmQuoteOnly = False

# class EntryOrder():
#     def __init__(self, leg, limitprice):
#         self.entry_order = Order()
#         self.entry_order.orderType = "LMT"
#         self.entry_order.action = leg
#         self.entry_order.totalQuantity = 1
#         self.entry_order.eTradeOnly = False
#         self.entry_order.firmQuoteOnly = False
#         self.entry_order.lmtPrice = limitprice
# class limit_order():
#     def __init__(self, parentId, somePrice):
#         self.order = Order()
#         self.order.action = "SELL"
#         self.order.orderType = "STP LMT"
#         self.order.lmtPrice = somePrice
#         self.order.auxPrice = somePrice * 0.95
#         self.order.totalQuantity = 1
#         self.order.eTradeOnly = False
#         self.order.firmQuoteOnly = False
#         self.order.parentId = parentId


class RiskManagementOrder():
    def __init__(self, leg ,entry_price, parentId):
        self.order = Order()
        self.order.action = "SELL"
        self.order.orderType = "TRAIL"
        self.order.totalQuantity = 1
        self.order.eTradeOnly = False
        self.order.firmQuoteOnly = False
        # self.order.trailStopPrice = round_down_to_025(entry_price * 0.9)
        self.order.trailingPercent = 0.5
        # print(f"Stop Price: {round_down_to_025(entry_price * 0.9)}")



bot = Bot()
time.sleep(1)
CALL_ORDER_ID = bot.ib.return_nextvalidid()
CALL_SUN_ID = CALL_ORDER_ID + 1
PUT_ORDER_ID = CALL_SUN_ID + 1
PUT_SUN_ID = PUT_ORDER_ID + 1

long = "BUY"
short = "SELL"


long_leg = EntryOrder("BUY")
print(f"O{CALL_ORDER_ID},   S{CALL_SUN_ID},  PO{PUT_ORDER_ID},  PS{PUT_SUN_ID}")
bot.ib.placeOrder(CALL_ORDER_ID, bot.o_m_d_c.contract, long_leg.entry_order)

long_leg_call_entry_price = bot.ib.return_call_entry_price()
stl_long_leg = RiskManagementOrder(long, long_leg_call_entry_price, CALL_ORDER_ID)
bot.ib.placeOrder(CALL_SUN_ID, bot.o_m_d_c.contract, stl_long_leg.order)

'''BUY PUT OPTION'''
bot.ib.placeOrder(PUT_ORDER_ID, bot.o_m_d_p.contract, long_leg.entry_order)

long_leg_put_entry_price = bot.ib.return_put_entry_price()
stl_short_leg = RiskManagementOrder(long, long_leg_put_entry_price, PUT_ORDER_ID)
bot.ib.placeOrder(PUT_SUN_ID, bot.o_m_d_p.contract, stl_short_leg.order)

