import os
import subprocess
import locale
from etcbackup.config import get_yaml_list

def _borg_popen(repodir,passphrase,args,**popenkw):
    os.putenv("BORG_REPO",repodir) #I think it's safer than using repodir::archvie, because repodir can contain special characters
    pass_r,pass_w=os.pipe()
    os.set_inheritable(pass_r,True)
    os.putenv("BORG_PASSPHRASE_FD",str(pass_r))
    proc=subprocess.Popen(["borg"]+args,close_fds=False,**popenkw)
    os.write(pass_w,passphrase.encode(locale.getpreferredencoding(False)))
    os.close(pass_w)
    return proc

def backup_files(paths,repodir,passphrase,opts):
    #TODO: subject to argument length limits; better using --exclude-from and --patterns-from
    args=["create"]
    for i in get_yaml_list(opts,"exclude-patterns"):
        args+=["-e",i]
    args.append("::"+opts["archive-name"])
    args+=paths
    proc=_borg_popen(repodir,passphrase,args)
    proc.wait()

class RawDataBackup:
    def __init__(self,repodir,passphrase,opts):
        self._proc=_borg_popen(repodir,passphrase,["create","::"+opts["archive-name"],"-"],stdin=subprocess.PIPE)
        self.fileobj=self._proc.stdin
    def end(self):
        self.fileobj.close()
        self._proc.wait()

def purge(**args):
    pass        #TODO
