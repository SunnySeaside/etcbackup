from etcbackup.modules.archlinux.common import *
import os

repotype="normal"
def get_paths(modarg=None):
    if modarg is None:
        etc="etc"
        etc2="/etc"
    else:
        etc2=os.path.abspath(modarg)
        etc=os.path.relpath(etc2,"/")

    owned={path for p in localdb.pkgcache for path,size,mod in p.files
                                             if path.startswith(etc) or path.startswith(etc2)}

    paths=[]
    for dirpath,dirnames,filenames in os.walk(etc2):
        for filename in filenames:
            path=os.path.join(dirpath,filename)
            if path not in owned:
                paths.append(path)
    return paths

if __name__ == "__main__":
    import sys
    print("\n".join(get_paths(sys.argv[1] if len(sys.argv)>1 else None)))

