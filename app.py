from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'
    
@app.route('/handle_post', methods=['POST'])
def handle_post():
    # Get the JSON data from the request
    data = request.get_json()
    # Print the data to the console
    print(data.stocks)
    print(data.scan_name)
    # Return a success message
    return 'JSON received!'


if __name__ == "__main__":
    app.run()
