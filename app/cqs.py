import os
import bottle
import mongodbconnect
from utility import sendemail
import uuid

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
      status = sendemail(data.get('email'), data.get('full-name'))

      if status < 200 or status >= 300:
        return bottle.template('index', result='There was an error trying to send an email to ' + data.get('email') +
          '. Please wait a few minutes before trying to register again.')        
      else:
        nuser = {
          '_id': data.get('email'),
          '_pass': data.get('password'),
          '_fullname': data.get('full-name'),
          '_o-name': data.get('organization-name'),
          '_school': data.get('school-name'),
          '_desc': data.get('description')
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

def user_auth(user, pw):
  if not user: return False
  return user['_pass'] == pw

def get_session():
  session = bottle.request.get_cookie('session', secret='secret')
  return session

def save_session(uid):
  session = {}
  session['uid'] = uid
  session['sid'] = uuid.uuid4().hex
  bottle.response.set_cookie('session', session, secret='secret')
  return session

def invalidate_session():
  bottle.response.delete_cookie('session', secret='secret')
  return

@bottle.route('/')
def index():
  session = get_session()
  if not session:
    return bottle.template('index')
  luser = user_find(session['uid'])
  if not luser: bottle.redirect('/logout')
  bottle.redirect('/dashboard')

@bottle.route('/about')
def about():
  return bottle.template('about')

@bottle.route('/login', method="POST")
def submitlogin():
  if 'email' in bottle.request.POST and 'password' in bottle.request.POST:
    email = bottle.request.POST['email']
    password = bottle.request.POST['password']
    user = user_find(email)
    if user_auth(user, password):
      save_session(user['_id'])
      bottle.redirect('/dashboard')
    else:
      return bottle.template(bottle.request.POST['page'], error='Incorrect Information.')

@bottle.route('/login')
def login():
  return bottle.template('index')

@bottle.route('/dashboard')
def dashboard():
  session = get_session()
  if not session: bottle.redirect('/login')
  luser = user_find(session['uid'])
  if not luser: bottle.redirect('/logout')
  return bottle.template('welcome', username=luser['_id'].split("@")[0], o_name=luser['_o-name'], school=luser['_school'])

@bottle.route('/manage/<step>')
def manage(step):
  step = int(step)
  session = get_session()
  if not session: bottle.redirect('/login')
  luser = user_find(session['uid'])
  if not luser: bottle.redirect('/logout')
  if step == 1:
    return bottle.template('manage', 
      username=luser['_id'].split("@")[0], 
      user=dict(luser),
      step=step,
      desc="If you have anything you'd like to fix since your registration, here's your chance to do so.")

@bottle.route('/account')
def account():
  loggeduser = mongo_db.users.find(request.get_cookie("account", secret='some-secret-key'))
  if not loggeduser:
    return bottle.template('login', result='Incorrect Information.')
  else:
    loggeduser1 = loggeduser[0]
    lemail = loggeduser1['_id']
    return bottle.template('account')

@bottle.route('/logout')
def logout():
  session = get_session()
  if not session:
    return bottle.template('index', logged_out='See you later!')
  else:
    invalidate_session()
    bottle.redirect('/logout')

@bottle.route('/static/assets/<filename:path>', name='static')
def static_file(filename):
  return bottle.static_file(filename, root=os.path.join(PROJECT_DIR, 'static/assets'))

bottle.run(server="waitress", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)