import requests
import json
import hashlib
url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getAPIEncpkey'
sessionurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getUserSID'
orderurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/executePlaceOrder'
websurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api//ws/createWsSession'
scriptDetailsurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/ScripDetails/getScripQuoteDetails'


def getUserSession():

    payload = json.dumps({
      "userId": "AB128122"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    json_obj = json.loads(response.text)
    enc_key = (json_obj['encKey'])

    token = 'AB128122'+'dF979Ui02GulOjB997DtC2ADKgzPtSOk9uihzAhpQ6h2zD0yLnyLKEKRqXvzBAqbyu6omPFOIrvecO87JVdttYhCIvGvg57nHhQYujdYx6Jz3pr1tzkgMYurvCIhbSPK'+enc_key
    hashToken = hashlib.sha256(token.encode()).hexdigest()
    print (hashToken)

    sessionpayload = json.dumps({
      "userId": "AB128122",
      "userData": hashToken
    })

    sessionresponse = requests.request("POST", sessionurl, headers=headers, data=sessionpayload)
    print(sessionresponse.text)
    json_obj_session = json.loads(sessionresponse.text)
    sessionid = (json_obj_session['sessionID'])
    
def placeOrder(stockName):
    sessionid = getUserSession()
    orderPayload = json.dumps([
      {
        "complexty": "regular",
        "discqty": "0",
        "exch": stockName,
        "pCode": "MIS",
        "prctyp": "L",
        "price": "3550.00",
        "qty": 1,
        "ret": "DAY",
        "symbol_id": "212",
        "trading_symbol": "ASHOKLEY-EQ",
        "transtype": "BUY",
        "trigPrice": "",
        "orderTag": "order1"
      }
    ])
    orderHeaders = {
      'Authorization': 'Bearer '+sessionid,
      'Content-Type': 'application/json'
    }
    orderResponse = requests.request("POST", orderurl, headers=orderHeaders, data=orderPayload)
    print(orderResponse.text)

def getScriptDetails(stockName):
    sessionid = getUserSession()
    orderHeaders = {
      'Authorization': 'Bearer '+sessionid,
      'Content-Type': 'application/json'
    }
    scriptdata = json.dumps(
      {
        "exch": "NSE", 
        "symbol": stockName
      }
    )

    scriptDetailResponse = requests.request("POST", scriptDetailsurl, headers=orderHeaders, data=scriptdata)
    print(scriptDetailResponse.json())
