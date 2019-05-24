from etcbackup.archlinux.common import *
import hashlib
import os.path

repotype="normal"
def get_paths():
    paths=[]
    for pkg in localdb.pkgcache:
        for oname,omd5 in pkg.backup:
            filename=os.path.join("/",oname)
            try:
                filebytes=open(filename,"rb").read()
                md5=hashlib.md5(filebytes).hexdigest()
                if omd5 != md5:
                    paths.append(filename)
            except OSError as e:
                print(e)
    return paths

if __name__ == "__main__":
    print("\n".join(get_paths()))
