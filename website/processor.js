var BASEURI='https://twexchangeconnector.herokuapp.com'

function loadExchanges()
{
    $.ajax(
        {
        url : BASEURI+"/getexchanges",
        //url: "https://raw.githubusercontent.com/giogandola98/ExchangeTWConnector/main/listTemplate.html",
        data: { format: 'html',},
        error : function(){alert("backend error");},
        success : function(data) 
        {
            document.getElementById("exchange").innerHTML="";
            document.getElementById("exchange").innerHTML+=data;
            console.log(data);

        },
        type: 'GET'
        });
}

function loadMarkets()
{
    console.log("loadMarkets");
    $.ajax(
        {
        url : BASEURI+"/getmarkets?exchange="+document.getElementById("exchange").value,
        //url: "https://raw.githubusercontent.com/giogandola98/ExchangeTWConnector/main/listTemplate.html",
        data: { format: 'html',},
        error : function(){alert("backend error");},
        success : function(data) 
        {
            document.getElementById("pair").innerHTML="";
            document.getElementById("pair").innerHTML+=data;
            console.log(data);

        },
        type: 'GET'
        });

}
function buildJson()
{
    var exchange = document.forms.exchange.value;
    console.log(exchange);
}

function jsonBuild(exchange,api,secret,pair,isderivate,size,percent,side)
        {
            var jsonObj={};
            jsonObj['exchange']=exchange;
            jsonObj['api']=api;
            jsonObj['secret']=secret;
            jsonObj['pair']=pair.toUpperCase();
            jsonObj['isderivate']=isderivate;
            jsonObj['size']=size;
            jsonObj['percent']=percent;
            jsonObj['side']=side;
            var x= JSON.stringify(jsonObj);
            document.getElementById('processedjson').value=x;
        }


function process_form()
{
    var exchange =   document.getElementById("exchange").value;
    var apikey=     document.getElementById("apikey").value;
    var secret=     document.getElementById("apisecret").value;
    var pair=       document.getElementById("pair").value;
    var size=       document.getElementById("size").value;
    var side=       document.getElementById("side").value;
    var percent=       document.getElementById("percent").value;
    var isderivate=       document.getElementById("isderivate").value;
    jsonBuild(exchange,apikey,secret,pair,isderivate,size,percent,side);
}