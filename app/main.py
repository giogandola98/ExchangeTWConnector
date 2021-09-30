from logging import exception
from flask import Flask, jsonify, request
#from waitress import serve
from ExchangeAdaptor import ExchangeAdaptor

app = Flask(__name__)
@app.route("/")
def helloword():
    return "ciao"

@app.route('/getmarkets',methods=['GET'])
def returnmarkets():
   print(request.args.get("exchange",None))
   pairs= ExchangeAdaptor().getMarkets(request.args.get("exchange",None))
   return pairs


@app.route('/getexchanges')
def getExchanges():
    print("conn")
    return str(ExchangeAdaptor().get_exchanges())
    
@app.route('/connector',methods=['POST'])
def orderProcessor():
    req=request.get_json()
    print(req)
    no_error=exchange=ExchangeAdaptor(req)
    if (no_error!=True):
        return no_error
    return exchange.processOrder()


#serve(app, host='0.0.0.0', port=80, threads=10)