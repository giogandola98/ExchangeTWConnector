from logging import exception
import ccxt
class BitMexProcessor:

    def convertTicker(self,ticker):
        x=ticker.split("/")
        if "BTC" in x[0]:
            x[0]="XBT"
        return x[0]+''+x[1]



    def __init__(self, ApiKey=None, ApiSecret=None,subaccount=None):
        print("BITMEX")
        self.ApiKey=ApiKey
        self.ApiSecret=ApiSecret
        if(ApiKey!=None and ApiSecret!=None):
            self.cctxConnector=ccxt.bitmex({
                'apiKey': ApiKey,
                'secret': ApiSecret,
                'enableRateLimit': True,
                })
        else:
            self.cctxConnector=ccxt.bitmex({
                        'enableRateLimit': True,
            })
        '''
        if 'test' in self.cctxConnector.urls:
            self.cctxConnector.urls['api'] = self.cctxConnector.urls['test'] # ←----- switch the base URL to testnet'''

        self.cctxConnector.load_markets()
        
    def getMarkets(self):
        return self.cctxConnector.symbols
        
    def getFreeBTC_Collateral(self):
        '''
        Return free BTC balance collateral for leverage (possible)
        '''
        balance=self.cctxConnector.fetch_balance()
        balance=balance['free']['BTC']*self.getActualPrice("BTC/USD")

        return balance


    def getActualPrice(self,ticker):
       return self.cctxConnector.fetchTicker(ticker)['last']

    def MarketBuy(self,ticker, size,percent=0,isderivate=0):
        self.MarketBuyLimit(ticker,size,percent,isderivate)
        '''size in usd
        print("SIZE",size)
        if percent>0:
            free_collateral=self.getFreeBTC_Collateral()
            size=free_collateral*size
        self.cctxConnector.createMarketBuyOrder(ticker,size)
        pass'''
        
    def MarketSell(self,ticker, size,percent=0,isderivate=0):
        self.MarketSellLimit(ticker,size,percent=percent,isderivate=isderivate)
        '''
        if percent>0:
            free_collateral=self.getFreeBTC_Collateral()
            size=free_collateral*size
        self.cctxConnector.createMarketSellOrder(ticker,size)
        pass'''

    def getPosition(self,ticker):
        ticker=self.convertTicker(ticker)
        try:
            return float(self.cctxConnector.private_get_position({'filter': self.cctxConnector.json({"isOpen":True, "symbol":ticker}) })[0]['currentQty'])
        except Exception as e:
            print(str(e))
            return 0

    def MarketBuyLimit(self,ticker,size,percent=0,isderivate=0):
        if percent>0:
            free_collateral=self.getFreeBTC_Collateral()
            size=free_collateral*size
        x=(self.cctxConnector.create_limit_buy_order(ticker,size,self.getActualPrice(ticker=ticker)+2))
        print(x)
        return str(x)
        pass

    def MarketSellLimit(self,ticker,size,percent=0,isderivate=0):
        if percent>0:
            free_collateral=self.getFreeBTC_Collateral()
            size=free_collateral*size
        x=(self.cctxConnector.create_limit_sell_order(ticker,size,self.getActualPrice(ticker)-2))
        print(x)
        return str(x)

    def ClosePosition(self,ticker):
        self.ClosePositionLimit(ticker)
        '''
        position=self.getPosition(ticker)
        if position>0:
            position = self.cctxConnector.createMarketSellOrder(ticker,position,params={'reduce-only': True})
        else:
            position = self.cctxConnector.createMarketBuyOrder(ticker,position*-1,params={'reduce-only': True})

        return position'''
    
    def ClosePositionLimit(self,ticker):
        position=self.getPosition(ticker)
        if position>0:
            position = self.cctxConnector.create_limit_sell_order(ticker,position,self.getActualPrice(ticker)-2,params={'reduce-only': True})
        else:
            position = self.cctxConnector.create_limit_buy_order(ticker,position,self.getActualPrice(ticker)+2,params={'reduce-only': True})
        return position
       
        