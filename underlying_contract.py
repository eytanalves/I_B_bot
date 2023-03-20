from ibapi.contract import Contract

class MarketDataUnderLying:
    def __init__(self, symbol, secType, currency, exchange, expiry):
        self.contract = Contract()
        self.contract.symbol = symbol
        self.contract.secType = secType
        self.contract.currency = currency
        self.contract.exchange = exchange
        self.contract.lastTradeDateOrContractMonth = expiry

