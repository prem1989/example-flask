from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'
    
@app.route('/handle_post', methods=['POST'])
def handle_post():
    print request


if __name__ == "__main__":
    app.run()
