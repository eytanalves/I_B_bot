option_expiry_date = datetime.datetime.now().strftime("%Y%m%d")

def round_up_to_5(x):
    return math.ceil(x / 5) * 5


def round_down_to_5(x):
    return math.floor(x / 5) * 5

df = pd.DataFrame(columns= ["time", "underlying price", "call price", "call ask", "put price", "put ask"])
def add_row(df, **kw):
    df["time"] = kw.get("time")
    df["underlying price"] = kw.get("underlying_price")
    df["call price"] = kw.get("call_price")
    df["call ask"] = kw.get("call_ask")
    df["put price"] = kw.get("put_price")
    df["put ask"] = kw.get("put_ask")


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.call_strike = 0
        self.put_strike = 0
        self.num = 0
        self.price = 0

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1:
            # print(datetime.datetime.now().strftime("%H:%M:%S"), f"underlying     {price}")
            # print()
            pass
        if tickType == 4 and reqId == 2:
            # print(f"Call 0D  {self.call_strike}: {price}")
            # print()
            pass

        elif tickType == 2 and reqId == 2:
            # print(f"Call 0D ASK  {self.call_strike}: {price}")
            # print()
            pass

        if tickType == 4 and reqId == 3:
            # print(f"Put 0D   {self.put_strike}: {price}",)
            # print()
            pass

        elif tickType == 2 and reqId == 3:
            # print(f"Put 0D  ASK {self.put_strike}: {price}", )
            # print()
            pass


    def error(self, id, errorCode, errorMsg):
        print(errorCode)
        print(errorMsg)


class IBSnapshot(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.underlying_snapshot = 0

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1003:
            self.underlying_snapshot = price
            # print("snapshot1", self.underlying_snapshot)
            # print()
            # print("     1003     ", price)

        def error(self, id, errorCode, errorMsg):
            print(errorCode)
            print(errorMsg)

class MarketDataOptions():
    def __init__(self, symbol, secType, exchange, currency, expiry, strike=None, right=None, multiplier=None):
        self.contract = Contract()
        self.contract.symbol = symbol
        self.contract.secType = secType
        self.contract.exchange = exchange
        self.contract.currency = currency
        self.contract.lastTradeDateOrContractMonth = expiry
        self.contract.strike = strike
        self.contract.right = right
        self.contract.multiplier = multiplier

class MarketDataUnderlying():
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
        self.ib.connect(host="172.20.10.11", port=7496, clientId=1)
        self.market_data = []
        self.req_count = 1
        time.sleep(1)

        self.underlying = MarketDataUnderlying("MES", "FUT", "CME", "USD", "202306")
        self.snapshot = IBSnapshot()
        self.snapshot.connect(host="172.20.10.11", port=7496, clientId=2)
        self.snapshot.reqMktData(1003, self.underlying.contract, "", False, False, [])
        self.snapshot_thread = threading.Thread(target=self.run_snapshot, daemon=True)
        self.snapshot_thread.start()
        time.sleep(1)
        self.snapshot_price = self.snapshot.underlying_snapshot
        print("snapshot 22222", self.snapshot_price)

        self.call_strike = round_up_to_5(self.snapshot_price)
        self.ib.call_strike = self.call_strike
        self.put_strike = round_down_to_5(self.snapshot_price)
        self.ib.put_strike = self.put_strike

        self.req_market_data()
        self.ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        self.ib_thread.start()
        time.sleep(1)

        order = Order()
        order.orderType = "MKT"
        order.action = "BUY"
        order.totalQuantity = 1
        order.eTradeOnly = False
        order.firmQuoteOnly = False
        # contract = MarketDataOptions("MES", "FOP", "CME", "USD", option_expiry_date , self.call_strike, "C", 5)
        contract = Contract()
        contract.symbol = "MES"
        contract.secType =  "FUT"
        contract.exchange = "CME"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "202306"
        # contract.strike = self.call_strike
        # contract.right = "C"
        # contract.multiplier = 5
        # self.ib.placeOrder(3, contract, order)

        sell_order = Order()
        sell_order.orderType = "MKT"
        sell_order.action = "SELL"
        sell_order.totalQuantity = 1
        sell_order.eTradeOnly = False
        sell_order.firmQuoteOnly = False
        self.ib.placeOrder(4, contract, sell_order)




    def req_market_data(self):
        self.market_data.append(MarketDataUnderlying("MES", "FUT", "CME", "USD", "202306"))
        self.market_data.append(MarketDataOptions("MES", "FOP", "CME", "USD", option_expiry_date , self.call_strike, "C", 5))
        self.market_data.append(MarketDataOptions("MES", "FOP", "CME", "USD", option_expiry_date, self.put_strike , "P", 5))
        for data in self.market_data:
            self.ib.reqMktData(self.req_count, data.contract, "", False, False, [])
            self.req_count += 1

    def run_snapshot(self):
        self.snapshot.run()

    def run_loop(self):
        self.ib.run()

    def place_order(self, ):
        pass


bot = Bot()
