from bottle import route, run, Bottle
from waitress import serve

app = Bottle()

@app.route('/')
def hello():
    return "Hello World!"

serve(app, host='campusqs14.herokuapp.com')