from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    print("Index Triggered")
    return "The Server is up and running"
app.run()