from logging import exception
from FtxProcessor import FtxProcessor

'''
ADAPTOR TO EXCHANGE

json format
{
    exchange: "FTX"
    api: "API CODE"
    secret: "SECRET CODE"
    pair : ticker
    isderivate : 0|1
    size : percent from 0 to 1 or size usd
    percent: 0|1
    side: 0 buy, 1 sell, -1 close position (only derivates)
}



'''
class ExchangeAdaptor:

    def printlist(self,list):
        to_return="<option value='-'>Select Value</option>"
        for l in list:
            to_return=to_return+'<option value="'+l+'">'+l+'</option>';
        return to_return

    def connectable_exchanges(self):
        self.exchanges=[]
        self.FTX="FTX"
        self.BINANCE="BINANCE"

        self.exchanges.append(self.FTX)
        #self.exchanges.append(self.BINANCE)




    def get_exchanges(self):
        return self.printlist(self.exchanges)

    def __init__(self,jsonitem=None):
        self.connectable_exchanges()
        self.exchange=None
        self.ticker=None
        self.isderivate=None
        self.size=None
        self.side=None
        self.percent=None
        self.api=None
        self.secret=None
        self.subaccount=None
        if jsonitem!=None:
            try:
                self.exchange=jsonitem['exchange']
                self.ticker=jsonitem['pair']
                self.isderivate=int(jsonitem['isderivate'])
                self.size=float(jsonitem['size'])
                self.side=int(jsonitem['side']) 
                self.percent=int(jsonitem['percent'])
                self.api=jsonitem['api']
                self.secret=jsonitem['secret']
                try:
                    self.subaccount=jsonitem['subaccount']
                except:
                    pass
            except Exception as e:
                return str(e)
            return True

    def processOrder(self):
        try:
            connector=""
            if self.exchange == self.FTX :
                connector=FtxProcessor(self.api,self.secret,self.subaccount)

            if self.side==0:
                return connector.MarketBuy(self.ticker,self.size,self.percent,self.isderivate)
            else:
                if self.side==1:
                    return connector.MarketSell(self.ticker,self.size,self.percent,self.isderivate)  
                else:
                    if self.side==-1:
                        return connector.ClosePosition(self.ticker)


        except Exception as e:
            return str(e)
    def getMarkets(self,exchange):
        if exchange==self.FTX:
            connector=FtxProcessor()
            pairs=connector.getMarkets()
            return self.printlist(pairs)