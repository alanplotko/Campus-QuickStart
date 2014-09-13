import os
import bottle
import mongodbconnect

PROJECT_DIR = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(PROJECT_DIR, 'views'))

mongo_db = mongodbconnect.mongoconn()

@bottle.route('/', method="POST")
def submit_form():
  data = bottle.request.forms
  if data.get('email'):
    tuser = user_find(data.get('email'))
    if tuser:
      return bottle.template('index', result='You are already registered!')
    else:
      nuser = {
        '_id': data.get('email')
        '_pass': data.get('password')
      }
      userid = mongo_db.users.insert(nuser)
      return bottle.template('index', result='You\'ve been signed up! Log in with your credentials.', 
        first_name=str(data.get('full-name').split(" ")[0]), register_success='True')
  else:
    return bottle.template('index', result=None)

def user_find(email):
  if not email:
    return None
  return mongo_db.users.find_one({ '_id': email})

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
      #then we can check password
      mongo_db.users.find_one(tuser)
      return bottle.template('welcome', result='Logged In Succesfully!')
    else:
      return bottle.template('login', result='Incorrect Information.')

@bottle.route('/login')
def login():
  return bottle.template('login')

@bottle.route('/static/assets/<filename:path>', name='static')
def static_file(filename):
  return bottle.static_file(filename, root=os.path.join(PROJECT_DIR, 'static/assets'))

bottle.run(server="waitress", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)