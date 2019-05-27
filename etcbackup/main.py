#!/usr/bin/env python
import os
import sys
import etcbackup.backends.borg as backend
import shutil
import getpass
import argparse
from collections import ChainMap
from importlib import import_module
#import configparser
import appdirs
import yaml
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

def read_yaml_list(obj,name):
    data=opts.get(name)
    if type(data) is list:
        return data
    elif type(data) is str:
        return [data]
    elif data is None:
        return []
    else:
        sys.exit("Error: "+name+" must be a list or string")
#TODO: autoprune in conf
#TODO:
#--dump: print list to be backed up
#--prune:manually prune
#dryrun
#-c: create
#add_mutually_exclusive_group
parser=argparse.ArgumentParser(description="Borg wrapper that generates paths to be backed up dynamically")
parser.add_argument("repo_dir",help="base directory for Borg repositories with no absolute path configured",nargs="?")
parser.add_argument("-C","--config",help="path of configuration file",default=os.path.join(appdirs.user_config_dir("etcbackup","SunnySeaside"),"config.yaml"))
#parser.add_argument("--dry-run",help="do not actually perform backup",action="store_true")
args=parser.parse_args()

try:
    config_file=open(args.config,"r")
except FileNotFoundError:
    sys.exit("Error: no configuration file found at "+args.config)
config=yaml.load(config_file,Loader=SafeLoader)
config_file.close()

globalopts=config["global"]

repo_base_dir=args.repo_dir or globalopts.get("repo_dir")

passphrase=os.getenv("BORG_PASSPHRASE")
if passphrase is None:
    passphrase=getpass.getpass("Passphrase:")

for reponame,repoopts in config["repos"].items():
    repodir=repoopts.get("repo_dir")
    if repodir is None:
        repodir=reponame
    if not os.path.isabs(repodir): #TODO: does not recognise remote paths
        if repo_base_dir is None:
            sys.exit('Error: repository "'+reponame+'" has no absolute path set, and no base directory specified')
        else:
            repodir=os.path.join(repo_base_dir,repodir)

    opts=ChainMap(repoopts,globalopts)
    modargs={"repodir":repodir,"passphrase":passphrase,"opts":opts}

    mods=[import_module("etcbackup."+i) for i in read_yaml_list(opts,"modules")]
    repotype=None
    for mod in mods:
        if repotype is None:
            repotype=mod.repotype
        elif repotype!=mod.repotype:
            sys.exit('Error: modules of repository "'+reponame+'" have more than one repository types')
    if repotype is None: #support repos with only custom_paths
        repotype="normal"

    if repotype=="normal":
        paths=set().union(*[m.get_paths() for m in mods])
        paths.update(read_yaml_list(opts,"custom_paths"))
        #TODO exclude paths
        backend.backup_files(paths,**modargs)
    elif repotype=="data":
        databackup=backend.RawDataBackup(**modargs)
        for mod in mods:
            mod.write_data(databackup.fileobj)
        for fn in read_yaml_list(opts,"custom_paths"):
            with open(fn,"rb") as f:
                shutil.copyfileobj(f, databackup.fileobj)
        databackup.end()
    else:
        print('Error: unknown repository type "',repotype,'"')

    backend.purge(**modargs)
