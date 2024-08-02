import requests
import json
import hashlib
url = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getAPIEncpkey'
sessionurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/customer/getUserSID'
orderurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/placeOrder/executePlaceOrder'
websurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api//ws/createWsSession'
scriptDetailsurl = 'https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/ScripDetails/getScripQuoteDetails'
masterurl = 'https://v2api.aliceblueonline.com/restpy/contract_master?exch=NSE'

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
    return sessionid
    
def placeBuyOrder(orderHeaders,stockName,symbolId,price,trigPrice,stopLoss,target):
    orderPayload = json.dumps([
      {
        "complexty": "regular",
        "discqty": "0",
        "exch": "NSE",
        "pCode": "MIS",
        "prctyp": "BO",
        "price": price,
        "qty": 1,
        "ret": "DAY",
        "symbol_id": symbolId,
        "trading_symbol": stockName,
        "transtype": "BUY",
        "trigPrice": trigPrice,
        "orderTag": "order1",
        "stopLoss":stopLoss,
        "target":target
      }
    ])
    orderResponse = requests.request("POST", orderurl, headers=orderHeaders, data=orderPayload)
    print(orderResponse.json())

def placeSellOrder(orderHeaders,stockName,symbolId,price,trigPrice,stopLoss,target):
    orderPayload = json.dumps([
      {
        "complexty": "regular",
        "discqty": "0",
        "exch": "NSE",
        "pCode": "MIS",
        "prctyp": "BO",
        "price": price,
        "qty": 1,
        "ret": "DAY",
        "symbol_id": symbolId,
        "trading_symbol": stockName,
        "transtype": "SELL",
        "trigPrice": trigPrice,
        "orderTag": "order1",
        "stopLoss":stopLoss,
        "target":target
      }
    ])
    orderResponse = requests.request("POST", orderurl, headers=orderHeaders, data=orderPayload)
    print(orderResponse.json())

def getScriptDetails(orderHeaders,stockName):
    scriptdata = json.dumps(
      {
        "exch": "NSE", 
        "symbol": stockName
      }
    )

    scriptDetailResponse = requests.request("POST", scriptDetailsurl, headers=orderHeaders, data=scriptdata)
    print(scriptDetailResponse.json())
    return json.loads(scriptDetailResponse.text)

def getContractDetails(orderHeaders,symbol):
    print(orderHeaders)
    print(symbol)
    master_contract = requests.request("GET", masterurl, headers=orderHeaders)
    master=json.loads(master_contract.text)
    for contract in master['NSE']:
        if contract.get('symbol')==symbol:
            print(contract)
            return contract
