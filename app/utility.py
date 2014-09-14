import os
import zipfile
import tarfile
import sendgrid
import _tkinter
import tkFileDialog


'''
import facebook
'''
def zip(src):
    root = Tkinter.Tk()
    root.withdraw()
    dst = tkFileDialog.askopenfilename()
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            #print 'zipping %s as %s' % (os.path.join(dirname, filename), arcname)
            zf.write(absname, arcname)
    zf.close()
    return

def tar(src):
    root = Tkinter.Tk()
    root.withdraw()
    dst = tkFileDialog.askopenfilename()
    tar = tarfile.open("%s.tar.gz" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            #print 'tarring %s as %s' % (os.path.join(dirname, filename),
            #                            arcname)
            tar.add(arcname)
    tar.close()
    return

def sendemail(email_to, full_name):
    sg = sendgrid.SendGridClient(os.environ.get('SENDGRID_USERNAME'), os.environ.get('SENDGRID_PASSWORD'))
    message = sendgrid.Mail()
    message.add_to(full_name + " <" + email_to + ">")
    message.set_subject("Welcome to Campus QuickStart!")
    message.set_html("You now have access to Campus QuickStart, where you can set up your website and social media platforms. Log in with your credentials to see it in action now!")
    message.set_text("You now have access to Campus QuickStart, where you can set up your website and social media platforms. Log in with your credentials to see it in action now!")
    message.set_from('Alan Plotko <aplotko1@binghamton.edu>')
    status, msg = sg.send(message)

    return status

def sendemail2(receiver_email, sender_email, receiver, sender, phone, message):
    sg = sendgrid.SendGridClient(os.environ.get('SENDGRID_USERNAME'), os.environ.get('SENDGRID_PASSWORD'))
    message = sendgrid.Mail()
    message.add_to(receiver + " <" + receiver_email + ">")
    message.set_subject("Contact Form Submission from " + sender)
    message.set_html(sender + " has contacted you via Campus QuickStart with the following message and can be reached by replying to this email or at " + phone + ".<br /><br />Message:<br />" + message)
    message.set_text(sender + " has contacted you via Campus QuickStart with the following message and can be reached by replying to this email or at " + phone + ". Message:" + message)
    message.set_from(sender + ' <' + sender_email + '>')
    status, msg = sg.send(message)

    return status   

'''
def postfacebook(pageid, posttext):
    graphu = facebook.GraphAPI(CAAHnCTQz3dgBACgduWVLApGmNZBPlaFRCBtZBasHnAOmpr7Kpy3NS9irYZAsBcxsEa7XNTZAfZANorxO5txoEgdOtT9mAs4bZAmlTMVU1vzFJY9ubNzP6D0T8pz3pPACIZCkTLgVQji7e8AVD5JmRSUhwP1NpxYuij89zXnWgApqSJsMKMCjwK2HxKJ3eULHPvFC3ayuQWEvM5kuzCREtXPMT0VhWldyUkZD)
    pagestuff = graphu.request('me/accounts')
    page_access_token = pagestuff['data'][0]['access_token']
    graph = facebook.GraphAPI(page_access_token)
    graph.put_object(pageid, "feed", message=posttext)
    return 
'''
'''
User Token  
CAAHnCTQz3dgBACgduWVLApGmNZBPlaFRCBtZBasHnAOmpr7Kpy3NS9irYZAsBcxsEa7XNTZAfZANorxO5txoEgdOtT9mAs4bZAmlTMVU1vzFJY9ubNzP6D0T8pz3pPACIZCkTLgVQji7e8AVD5JmRSUhwP1NpxYuij89zXnWgApqSJsMKMCjwK2HxKJ3eULHPvFC3ayuQWEvM5kuzCREtXPMT0VhWldyUkZD

App Token   
535501693246936|CXJIohDKqAIZPE9NTgUXFoOxBSw
'''




