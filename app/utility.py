import os
import zipfile
import tarfile
import tarfile
import sendgrid
'''
def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename), arcname)
            zf.write(absname, arcname)
    zf.close()
    return

def tar(src, dst):
    tar = tarfile.open("%s.tar.gz" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'tarring %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            tar.add(arcname)
    tar.close()
    return
'''
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






