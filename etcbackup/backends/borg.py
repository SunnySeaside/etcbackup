import os
import subprocess
import locale

def _borg_popen(repodir,passphrase,args,**popenkw):
    os.putenv("BORG_REPO",repodir) #I think it's safer than using repodir::archvie, because repodir can contain special characters
    pass_r,pass_w=os.pipe()
    os.set_inheritable(pass_r,True)
    os.putenv("BORG_PASSPHRASE_FD",str(pass_r))
    proc=subprocess.Popen(["borg"]+args,close_fds=False,**popenkw)
    os.write(pass_w,passphrase.encode(locale.getpreferredencoding(False)))
    os.close(pass_w)
    return proc

def backup_files(repodir,passphrase,opts,paths):
    proc=_borg_popen(repodir,passphrase,["create","::"+opts["archive_name"]]+paths)     #TODO: argument length limits
    proc.wait()

class BackupRawData:
    def __init__(self,repodir,passphrase,opts):
        self._proc=_borg_popen(repodir,passphrase,["create","::"+opts["archive_name"],"-"],stdin=subprocess.PIPE)
        self.fileobj=self._proc.stdin
    def end(self):
        self.fileobj.close()
        self._proc.wait()
def purge(*args):
    pass        #TODO
