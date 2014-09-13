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
def sendemail(efrom, eto, esubject,ebody):
    sg = sendgrid.SendGridClient('SENDGRID_USERNAME', 'SENDGRID_PASSWORD')
    message = sendgrid.Mail(to=eto, subject=esubject, html=ebody, text=ebody, from_email=efrom)
    
    status, msg = sg.send(message)

    return status