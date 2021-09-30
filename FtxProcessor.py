from logging import exception
import ccxt
class FtxProcessor:
    def __init__(self, ApiKey=None, ApiSecret=None,SubAccount=None):
        self.ApiKey=ApiKey
        self.ApiSecret=ApiSecret
        if(ApiKey!=None and ApiSecret!=None):
            if(SubAccount!=None):
                self.cctxConnector=ccxt.ftx({
                    'headers':
                    {
                        'FTX-SUBACCOUNT' : SubAccount,
                    },
                    'apiKey': ApiKey,
                    'secret': ApiSecret,
                    'enableRateLimit': True,
                    })
            else:
                self.cctxConnector=ccxt.ftx({
                    'apiKey': ApiKey,
                    'secret': ApiSecret,
                    'enableRateLimit': True,
                    })
        else:
            self.cctxConnector=ccxt.ftx({
                        'enableRateLimit': True,
            })
        self.cctxConnector.load_markets()
        #self.cctxConnector.set_sandbox_mode(True)

    def getMarkets(self):
        return self.cctxConnector.symbols
    def getBalance(self, ticker):
        return (self.cctxConnector.fetch_balance()[ticker]['free'])
        pass

    def getActualPrice(self,ticker):
       return float(self.cctxConnector.fetchTicker(ticker)['last'])

    def MarketBuy(self,ticker, size,percent=0,isDerivate=0):
        x=""
        if(percent>0):
            tick=ticker.split("/");
            tick.append("X")
            if isDerivate>0:
                tick[1]="USD"            
            size=float(self.getBalance(tick[1]))*size
            print(tick)
            print("BALANCE",self.getBalance(tick[1]))
            print("BUY:",size)
            try:
                x=self.cctxConnector.createMarketBuyOrder(ticker,size/self.getActualPrice(ticker))
            except Exception as e:
               x=str(e)
            print(x)
            return x

    def MarketSell(self,ticker, sizebtc,percent=0,isDerivate=0):
        x=""
        if(percent>0):
            tick=ticker.split("/");
            tick.append("X")
            if isDerivate>0:
                tick=ticker.split("-")
            sizebtc=float(self.getBalance(tick[0]))*sizebtc
            print(tick)
            print("BALANCE",self.getBalance(tick[0]))
            print("BUY:",sizebtc)
        try:
            x=self.cctxConnector.createMarketSellOrder(ticker,sizebtc)
        except Exception as e:
            x=str(e)
        print(x)
        return x

    def getFuturePosition(self,ticker):
        x= self.cctxConnector.private_get_positions()['result']
        for json in x:
            if json['future']==ticker:
                return float(json['netSize'])
        return 0

    def ClosePosition(self,ticker):
        #da sistemare al momento, non ancora funzionante
        size=self.getFuturePosition(ticker)
        if(size>0):
            return self.cctxConnector.createNarketSellOrder(ticker,size,params={'reduce-only': True})
        else:
            return self.cctxConnector.createNarketBuyOrder(ticker,size*-1,params={'reduce-only': True})
        