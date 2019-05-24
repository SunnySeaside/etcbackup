import pyalpm
handle=pyalpm.Handle("/","/var/lib/pacman")
localdb=handle.get_localdb()
all_pkgs=[i.name for i in localdb.pkgcache]
