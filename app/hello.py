from bottle import route, run

@route('/')
def hello():
    return "Hello World!"

run(server='waitress', host='0.0.0.0', port='5000')