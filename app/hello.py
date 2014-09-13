from bottle import route, run, Bottle
from waitress import serve

app = Bottle()

@app.route('/')
def hello():
    return "Hello World!"

serve(app, host='127.0.0.1', port=8080)