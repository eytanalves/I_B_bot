from underlying_contract import MarketDataUnderLying

class OptionsMarketData(MarketDataUnderLying):
    def __init__(self,symbol, secType, currency, exchange, expiry,strike, right, multiplier):
        super().__init__( symbol, secType, currency, exchange, expiry)
        self.contract.strike = strike
        self.contract.right = right
        self.contract.multiplier = multiplier
