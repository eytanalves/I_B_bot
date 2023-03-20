from ibapi.wrapper import EWrapper
from ibapi.client import EClient


class IBapi(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self,self)
        self.under_price = 0


    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        if tickType == 4 and reqId == 1:

            self.under_price = price
            # print(f"Under Lynig Price : {self.under_price}")
        elif tickType == 4 and reqId == 2:
            print(f"Call Option Price : {price}")

        elif tickType == 2 and reqId == 2:
             # print(f"Call 0D ASK  {self.call_strike}: {price}")
            # print()
            pass

        elif tickType == 4 and reqId == 3:
            print(f"put Option Price : {price}")


        elif tickType == 2 and reqId == 3:
            # print(f"put Option ask : {price}")
            # print(f"Call 0D ASK  {self.call_strike}: {price}")
            # print()
            pass


    def error(self, reqId, errorCode, errorString):
        # print(errorCode)
        # print(errorString)
        pass