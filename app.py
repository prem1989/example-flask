from flask import Flask
from flask import request
from flask import json
from alice import placeBuyOrder
from alice import placeSellOrder
from alice import getScriptDetails
from alice import getUserSession
from alice import getContractDetails
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'
    
@app.route('/handle_post', methods=['POST'])
def handle_post():
    # Get the JSON data from the request
    data = request.get_json()
    # Print the data to the console
    print(data.get('stocks'))
    scanname=data.get('scan_name')
    print(data.get('scan_name'))
    sessionid=getUserSession()
    orderHeaders = {
      'Authorization': 'Bearer '+sessionid,
      'Content-Type': 'application/json'
    }
    print(orderHeaders)
    if type(data.get('stocks')) is list:
        for i in data.get('stocks'):
            contract = getContractDetails(orderHeaders,i)
            print(contract.get('token'))
            script = getScriptDetails(orderHeaders,contract.get('token'))
            print(script.get('TSymbl'))
            if scanname=='GGG':
                placeBuyOrder(orderHeaders,script.get('TSymbl'),contract.get('token'),script.get('LTP'),script.get('LTP'))
            if scanname=='RRR':
                placeSellOrder(orderHeaders,script.get('TSymbl'),contract.get('token'),script.get('LTP'),script.get('LTP'))

    else:
        contract = getContractDetails(orderHeaders,i)
        print(contract.get('token'))
        script = getScriptDetails(orderHeaders,contract.get('token'))
        print(script.get('TSymbl'))
        if scanname=='GGG':
            placeBuyOrder(orderHeaders,script.get('TSymbl'),contract.get('token'),script.get('LTP'),script.get('LTP'))
        if scanname=='RRR':
            placeSellOrder(orderHeaders,script.get('TSymbl'),contract.get('token'),script.get('LTP'),script.get('LTP'))
        
    # Return a success message
    return 'JSON received!'


if __name__ == "__main__":
    app.run()
