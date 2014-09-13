import os
import bottle

PROJECT_DIR = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(PROJECT_DIR, 'views'))

@bottle.post('/')
def index():
  data = bottle.request.forms
  if data.get('email'):
    # check for pre existance
    tuser = user_find(data.get('email'))
    if tuser:
      return bottle.template('index', result='You are already registered!')
    else:
      nuser = {
        '_id': data.get('email'),
        'pw': data.get('password')
      }
      userid = mongo_db.users.insert(nuser)
      return bottle.template('welcome', result='You\'ve been signed up!', email=data.get('email'))
  else:
    return bottle.template('index', result=None)

@bottle.route('/')
def index():
  return bottle.template('index')

@bottle.route('/about')
def about():
  return bottle.template('about')

@bottle.route('/login')
def login(): 
  data = bottle.request.forms
  if data.get('email'):
    # check for pre existance
    tuser = mongo_db.users.find(data.get('email'))
    if tuser:
      return bottle.template('welcome', result='Logged In Succesfully!')
    else:
      return bottle.template('login', result='Incorrect Information.')

@bottle.route('/login')
def login():
  return bottle.template('login')

@bottle.route('/static/assets/<filename:path>', name='static')
def static_file(filename):
  return bottle.static_file(filename, root=os.path.join(PROJECT_DIR, 'static/assets'))

bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)