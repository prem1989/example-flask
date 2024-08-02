from flask import Flask
from flask import request
from flask import json
from alice import placeBuyOrder
from alice import placeSellOrder
from alice import getScriptDetails
from alice import getUserSession
from alice import getContractDetails
import datetime
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

def time_in_range(start, end, current):
    return start <= current <= end
    
@app.route('/handle_post', methods=['POST'])
def handle_post():
    # Get the JSON data from the request
    data = request.get_json()
    print(data)
    # Print the data to the console
    print(data.get('stocks'))
    scanname=data.get('scan_name')
    print(data.get('scan_name'))
    start = datetime.time(9, 0, 0)
    end = datetime.time(11, 30, 0)
    current = datetime.datetime.now().time()
    print(start)
    print(end)
    print(current)
    if time_in_range(start, end, current):
        sessionid=getUserSession()
        orderHeaders = {
          'Authorization': 'Bearer '+sessionid,
          'Content-Type': 'application/json'
        }
        print(orderHeaders)
        stocklist=data.get('stocks').split(",")
        for i in stocklist:
            contract = getContractDetails(orderHeaders,i)
            print(contract.get('token'))
            script = getScriptDetails(orderHeaders,contract.get('token'))
            ltp=int(float(script.get('LTP')))
            print(script.get('TSymbl'))
            if scanname=='GGG':
                high=int(float(script.get('High')))
                high = high+(ltp*0.001)
                high = round(high,1)
                placeBuyOrder(orderHeaders,script.get('TSymbl'),contract.get('token'),high,high)
            if scanname=='RRR':
                low=int(float(script.get('Low')))
                low = low - (ltp*0.001)
                low = round(low,1)
                placeSellOrder(orderHeaders,script.get('TSymbl'),contract.get('token'),low,low)
        
    # Return a success message
    return 'JSON received!'


if __name__ == "__main__":
    app.run()
