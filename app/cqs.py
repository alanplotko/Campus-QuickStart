import os
import bottle
import mongodbconnect
import utility
import uuid
import shutil
import re
import hashlib

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
      status = utility.sendemail(data.get('email'), data.get('full-name'))
      if status < 200 or status >= 300:
        return bottle.template('index', result='There was an issue with your email address - please try registering again in a few minutes.', 
          first_name=str(data.get('full-name').split(" ")[0]))
      else:      
        nuser = {
          '_id': data.get('email'),
          '_pass': data.get('password'),
          '_fullname': data.get('full-name'),
          '_o-name': data.get('organization-name'),
          '_school': data.get('school-name'),
          '_o-name-lower': (data.get('organization-name').replace(" ", "-")).lower(),
          '_school-lower': (data.get('school-name').replace(" ", "-")).lower(),
          '_const': None,
          '_hosting': None,
          '_theme': None,
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
  return bottle.template('welcome', username=luser['_id'].split("@")[0], o_name=luser['_o-name'], school=luser['_school'],
    theme=luser['_theme'], hosting=luser['_hosting'])

@bottle.route('/manage/step/<step>')
def manage(step):
  step_int = int(float(step))
  session = get_session()
  if not session: bottle.redirect('/login')
  luser = user_find(session['uid'])
  if not luser: bottle.redirect('/logout')
  if luser['_theme'] != None and luser['_hosting'] != None:
    if step_int in (1, 2):
      pass
    elif step_int == 3:
      return bottle.template('manage', user=dict(luser), step=step_int, title="Create a website!", 
        desc="Get your club and organization on the web for all to see!")
    if step_int == 4 and step in ("4.1", "4.2"):
      mongo_db.users.update({'_id': luser['_id']}, { '$set': {
       '_theme': str(step).split(".")[1]
      }})
      bottle.redirect("/manage")
    if step_int == 4 and step not in ("4.1", "4.2"):
      return bottle.template('manage', user=dict(luser), step=step_int, title="How do you want to host your website?",
       desc="Host it with us or export it to host somewhere else. GitHub Pages support coming soon!")
      
  if step_int == 1:
    return bottle.template('manage',
      user=dict(luser),
      step=step_int,
      title="Verify " + luser['_o-name'] + "'s information!",
      desc="If you have anything you'd like to fix since your registration, here's your chance to do so.")
  elif step_int == 2:
    return bottle.template('manage',
      user=dict(luser),
      step=step_int,
      title="Draft a constitution!",
      desc="Every club or organization has a basic set of goals. Can you clarify yours?")
  elif step_int == 3:
    return bottle.template('manage',
      user=dict(luser),
      step=step_int,
      title="Create a website!",
      desc="Get your club and organization on the web for all to see!")
  elif step_int == 4:
    mongo_db.users.update({'_id': luser['_id']}, { '$set': {
      '_theme': str(step).split(".")[1]
    }})
    return bottle.template('manage',
      user=dict(luser),
      step=step_int,
      title="How do you want to host your website?",
      desc="Host it with us or export it to host somewhere else. GitHub Pages support coming soon!")
  elif step_int == 5:
    hosting_string = str(step)
    hosting_option = hosting_string.split(".")[1]
    mongo_db.users.update({'_id': luser['_id']}, { '$set': {
      '_hosting': hosting_option
    }})
    if(hosting_option == "1"):
      description = "  is now hosted with us!"

      # Report
      report = ''
      school = luser['_school-lower']
      organization = luser['_o-name-lower']

      # Create folder for university if it does not exist
      if not os.path.exists(PROJECT_DIR + '/views/organizations/' + school):
        os.makedirs(PROJECT_DIR + '/views/organizations/' + school)
      # Create folder for club or organization if it does not exist
      if not os.path.exists(PROJECT_DIR + '/views/organizations/' + school + '/' + organization):
        os.makedirs(PROJECT_DIR + '/views/organizations/' + school + '/' + organization)
      
      sourcePath = r'' + PROJECT_DIR + '/views/themes_repo/theme-' + str(luser['_theme'])
      destPath = r'' + PROJECT_DIR + '/views/organizations/' + school + '/' + organization
      for root, dirs, files in os.walk(sourcePath):
        #figure out where we're going
        dest = destPath + root.replace(sourcePath, '')
        
        #if we're in a directory that doesn't exist in the destination folder
        #then create a new folder
        if not os.path.isdir(dest):
            os.mkdir(dest)
            report += ('- Directory created at: ' + dest + '\n')

        #loop through all files in the directory
        for f in files:
            #compute current (old) & new file locations
            oldLoc = root + '\\' + f
            newLoc = dest + '\\' + f

            if not os.path.isfile(newLoc):
                try:
                    shutil.copy2(oldLoc, newLoc)
                    report += ('- File ' + f + ' copied.\n')
                except IOError:
                    report += ('- File "' + f + '" already exists\n')
      return bottle.template('manage', user=dict(luser), step=step_int, title="Your website " + description, 
        link="http://campusqs14.herokuapp.com/organizations/" + school + "/" + organization, 
        desc="You can return to your dashboard and restart the process to make changes.", report=report)
    elif(hosting_option == "2"):
      src = luser['_school-lower'] + luser['_o-name-lower']
      zip(src, "/export")
      download("export.zip")
      description = " has been exported as .zip!"
    elif(hosting_option == "3"):
      src = luser['_school-lower'] + luser['_o-name-lower']
      tar(src, "/exports/export")
      download("export.tar.gz")
      description = " has been exported as .tar.gz!"
    else:
      description = "" 
    return bottle.template('manage', user=dict(luser), step=step_int, title="Your website " + description, 
      desc="You can return to your dashboard and restart the process to make changes.")

def download(filename):
    return static_file(filename)

@bottle.route('/manage')
def manage_overall():
  session = get_session()
  if not session: bottle.redirect('/login')
  luser = user_find(session['uid'])
  if not luser: bottle.redirect('/logout')
  if luser['_theme'] == None or luser['_hosting'] == None:
    bottle.redirect('/manage/step/1')
  elif luser['_theme'] != None and luser['_hosting'] != None:
    return bottle.template('manage', user=dict(luser), title="Welcome back!", 
      desc="You've already completed your first time setup. What would you like to manage today?", step=6)

@bottle.route('/manage/step/<step>', method="POST")
def manage_update(step):
  step_int = int(step)
  session = get_session()
  if not session: bottle.redirect('/login')
  luser = user_find(session['uid'])
  if not luser: bottle.redirect('/logout')
  if luser['_theme'] != None and luser['_hosting'] != None and step_int != 1:
    if step_int == 2:    
      mongo_db.users.update({'_id': luser['_id']}, { '$set': {
        '_const': bottle.request.POST['constitution']
      }})
    bottle.redirect('/manage')
  if step_int == 1:
    mongo_db.users.update({'_id': luser['_id']}, { '$set': {
      '_o-name': bottle.request.POST['organization-name'],
      '_school': bottle.request.POST['school-name'],
      '_desc': bottle.request.POST['description'],
      '_o-name-lower': (bottle.request.POST['organization-name'].replace(" ", "-")).lower(),
      '_school-lower': (bottle.request.POST['school-name'].replace(" ", "-")).lower(),
    }})
  elif step_int == 2:
    mongo_db.users.update({'_id': luser['_id']}, { '$set': {
      '_const': bottle.request.POST['constitution']
    }})
  return bottle.redirect(str(step_int + 1))

@bottle.route('/organizations/<school>/<organization>')
def show_site(school, organization):
    user = mongo_db.users.find_one({
      '_school-lower': school,
      '_o-name-lower': organization
    })
    return bottle.template('organizations/' + school + '/' + organization + '/index', title=user['_o-name'], 
      description=user['_desc'], full_name=user['_fullname'], constitution=user['_const'], 
      gravatar=makeGravatar(user['_id']), email=user['_id'], school=school.replace("-", " "), organization=organization.replace("-", " "))

@bottle.route('/organizations/<school>/<organization>/sendcontactform', method="POST")
def sendcontactform(school, organization):
    user = mongo_db.users.find_one({
      '_school-lower': school
      '_o-name-lower': organization
    })
    if 'sender' in bottle.request.POST:
      sender = bottle.request.POST['sender']
    if 'sender_email' in bottle.request.POST:
      sender_email = bottle.request.POST['sender_email']
    if 'receiver' in bottle.request.POST:
      receiver = bottle.request.POST['receiver']
    if 'receiver_email' in bottle.request.POST:
      receiver_email = bottle.request.POST['receiver_email']
    if 'phone' in bottle.request.POST:
      phone = bottle.request.POST['phone']
    if 'sender_message' in bottle.request.POST:
      sender_message = bottle.request.POST['sender_message']
    status = utility.sendemailcontactform(receiver_email, sender_email, receiver, sender, phone, sender_message)
    return bottle.template('organizations/' + school + '/' + organization + '/index', title=user['_o-name'], 
      description=user['_desc'], full_name=user['_fullname'], constitution=user['_const'], 
      gravatar=makeGravatar(user['_id']), email=user['_id'], school=school.replace("-", " "), 
      organization=organization.replace("-", " "), status=status)

def makeGravatar(email):
  return "http://www.gravatar.com/avatar/" + hashlib.md5(email.encode('utf-8')).hexdigest() + "?s=150"

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




