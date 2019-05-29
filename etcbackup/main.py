#!/usr/bin/env python
import os
import sys
import etcbackup.backends.borg as backend
import shutil
import getpass
import argparse
from collections import ChainMap
from importlib import import_module
from etcbackup.config import *
def main():
    #TODO:
    #--dump: print list to be backed up
    parser=argparse.ArgumentParser(description="Borg wrapper that generates paths to be backed up dynamically")
    parser.add_argument("repo_dir",help="base directory for Borg repositories with no absolute path configured",nargs="?")
    parser.add_argument("-C","--config",help="path of configuration file")
    #parser.add_argument("-n","--dry-run",help="do not actually perform backup",action="store_true")
    #parser.add_argument("-v","--verbose",help="produce more output",action="store_true")
    group=parser.add_argument_group("actions") #add_mutually_exclusive_group
    group.add_argument("-b","--backup",help="peform backup (default when no actions given)",action="store_true")
    group.add_argument("-c","--create",metavar="CREATEOPTS",help="create configured repositories",action="store")
    group.add_argument("-p","--prune",help="remove old backup archives",action="store_true")
    args=parser.parse_args()
    if not (args.backup or args.create or args.prune):
        args.backup=True

    config=load_config(args.config)

    globalopts=config["global"]

    repo_base_dir=args.repo_dir or globalopts.get("repo-dir")

    passphrase=os.getenv("BORG_PASSPHRASE")
    if passphrase is None:
        passphrase=getpass.getpass("Passphrase:")

    for reponame,repoopts in config["repos"].items():
        repodir=repoopts.get("repo-dir")
        if repodir is None:
            repodir=reponame
        if not os.path.isabs(repodir): #TODO: does not recognise remote paths
            if repo_base_dir is None:
                sys.exit('Error: repository "'+reponame+'" has no absolute path set, and no base directory specified')
            else:
                repodir=os.path.join(repo_base_dir,repodir)

        opts=ChainMap(repoopts,globalopts)
        modargs={"repodir":repodir,"passphrase":passphrase,"opts":opts}

        mods=[import_module("etcbackup."+i) for i in get_yaml_list(opts,"modules")]
        repotype=None
        for mod in mods:
            if repotype is None:
                repotype=mod.repotype
            elif repotype!=mod.repotype:
                sys.exit('Error: modules of repository "'+reponame+'" have more than one repository types')
        if repotype is None: #support repos with only custom-paths
            repotype="normal"
        if args.create:
            backend.create_repository(args.create,**modargs)
        if args.backup:
            if repotype=="normal":
                paths=set().union(*[m.get_paths() for m in mods])
                paths.update(get_yaml_list(opts,"custom-paths"))
                #TODO exclude paths
                backend.backup_files(paths,**modargs)
            elif repotype=="data":
                databackup=backend.RawDataBackup(**modargs)
                for mod in mods:
                    mod.write_data(databackup.fileobj)
                for fn in get_yaml_list(opts,"custom-paths"):
                    with open(fn,"rb") as f:
                        shutil.copyfileobj(f, databackup.fileobj)
                databackup.end()
            else:
                print('Error: unknown repository type "',repotype,'"')

        if args.prune or (args.backup and opts.get("auto-prune")):
            backend.prune(**modargs)


if __name__ == "__main__":
    main()
