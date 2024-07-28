from flask import Flask
from flask import request
from flask import json
from alice import placeOrder
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
    print(data.get('scan_name'))
    sessionid=getUserSession()
    orderHeaders = {
      'Authorization': 'Bearer '+sessionid,
      'Content-Type': 'application/json'
    }
    print(orderHeaders)
    contract = getContractDetails(orderHeaders,data.get('stocks'))
    print(contract.get('token'))
    script = getScriptDetails(orderHeaders,contract.get('token'))
    print(script.get('TSymbl'))
    placeOrder(orderHeaders,script.get('TSymbl'))
    # Return a success message
    return 'JSON received!'


if __name__ == "__main__":
    app.run()
