import os
import subprocess
import locale
import tempfile
from etcbackup.config import get_yaml_list

def _borg_popen(repodir,passphrase,args,**popenkw):
    os.putenv("BORG_REPO",repodir) #I think it's safer than using repodir::archvie, because repodir can contain special characters
    pass_r,pass_w=os.pipe()
    os.set_inheritable(pass_r,True)
    os.putenv("BORG_PASSPHRASE_FD",str(pass_r))
    proc=subprocess.Popen(["borg"]+args,close_fds=False,**popenkw)
    os.write(pass_w,passphrase.encode(locale.getpreferredencoding(False)))
    os.close(pass_w)
    os.close(pass_r)
    return proc

def create_repository(createargs,repodir,passphrase,opts):
    os.putenv("BORG_DISPLAY_PASSPHRASE","n") #todo: make it customizable
    proc=_borg_popen(repodir,passphrase,["init"]+createargs.split(' ')) #todo workaround
    proc.wait()

def backup_files(paths,repodir,passphrase,opts):
    args=["create"]
    if opts.get("use-patterns-file"): #use --patterns-from(experimental for Borg)
        pf=tempfile.NamedTemporaryFile("w",delete=False) #not all OSs support opening the same file two times
        pf.write("P fm\n")
        for i in get_yaml_list(opts,"exclude-patterns"):
            pf.write("-"+i+"\n")
        for i in paths:
            pf.write("R "+i+"\n")
        pf.close()

        args+=["--patterns-from",pf.name,"::"+opts["archive-name"]]
    else:    #subject to argument length limits; better using --patterns-from or --exclude-from
        pf=None
        for i in get_yaml_list(opts,"exclude-patterns"):
            args+=["-e",i]
        args.append("::"+opts["archive-name"])
        args+=paths

    proc=_borg_popen(repodir,passphrase,args)
    proc.wait()

    if pf is not None:
        os.unlink(pf.name)

class RawDataBackup:
    def __init__(self,repodir,passphrase,opts):
        self._proc=_borg_popen(repodir,passphrase,["create","::"+opts["archive-name"],"-"],stdin=subprocess.PIPE)
        self.fileobj=self._proc.stdin
    def end(self):
        self.fileobj.close()
        self._proc.wait()

def prune(repodir,passphrase,opts):
    args=["prune"]
    for i,j in opts["prune-keep"].items():
        args+=["--keep-"+i,str(j)]
    proc=_borg_popen(repodir,passphrase,args)
    proc.wait()
