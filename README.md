# Summary #
This is a simple command-line front-end of [Borg](https://www.borgbackup.org/)([Github](https://github.com/borgbackup/borg/)) backup utility. Unlike many other Borg wrappers, it allows you to use external scripts to generate a list of files or some raw data to be backed up. It also allows backing up different kinds of data to their corresponding repositories.

# Quick start #
1. Create some Borg repositories

```cd ~/backup
mkdir sysconf packages
borg -e repokey sysconf
borg -e repokey packages
```

2. Edit config file

   The configuration file format is very simple and intuitive, if you are familiar of Bash array syntax. The default configuration can be used to make a not-so-complete backup of Arch Linux system configuration. It finds modified [package backup files](https://wiki.archlinux.org/index.php/Pacman/Pacnew_and_Pacsave#Package_backup_files)(which are usually user-modifible configuration files) and files in /etc not owned by any package to be backed up into "sysconf" repository, and also backs up a list of installed packages into "packages" repository.
   
3. Run `etcbackup ~/backup`

# TODO list #
* Read configuration from /etc or user home directory
* Using xargs is subject to command line length limitations
It'd be better if [`--files-from`](https://github.com/borgbackup/borg/issues/841) is implemented in Borg. Or we could use `--patterns-from`, which is an experimental feature.
* Support for excluding files
* Make it easier to create repositories and restore from backups

# Similar projects #
Please see https://github.com/borgbackup/community#user-content-backup-scripts--borg-wrappers

# Disclaimer #
THIS SOFTWARE IS PROVIDED "AS-IS", USE IT AT YOUR OWN RISK. IN NO CASES SHALL I BE RESPONSIBLE FOR ANY DIRECT OR INDIRECT DAMAGE CAUSED BY USING THE SOFTWARE, INCLUDING BUT NOT LIMITED TO INCOMPLETE BACKUP OR LOSS OF DATA.
