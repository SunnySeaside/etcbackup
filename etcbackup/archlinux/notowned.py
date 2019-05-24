from etcbackup.archlinux.common import *
import os

repotype="normal"
def get_paths():
    #owned=set().union(*[(f[0] for f in p.files) for p in localdb.pkgcache])
    owned=set()
    for p in localdb.pkgcache:
        for path,size,mod in p.files:
            owned.add(os.path.join("/",path))
    #print(owned)
    paths=[]
    for dirpath,dirnames,filenames in os.walk("/etc"):
        for filename in filenames:
            path=os.path.join(dirpath,filename)
            if path not in owned:
                paths.append(path)
    return paths

if __name__ == "__main__":
    print("\n".join(get_paths()))

