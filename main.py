from flask import Flask

app = Flask(__name__)

@app.route('/helloworld')
def index():
    return "Hello, World! ver 0.0.1"

@app.route('/receipt/analyze')
def analyze_receipt():
    return "Receipt analysis not implemented yet."