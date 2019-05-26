# Summary #
This is a simple command-line front-end of [Borg](https://www.borgbackup.org/)([Github](https://github.com/borgbackup/borg/)) backup utility. Unlike many other Borg wrappers, it allows you to dynamically generate list of files or some raw data to be backed up by using plugin modules. It also supports backing up to multiple repositories with one single command.

# Quick start #
1. Install dependencies

   To use this software, you must have Borg and Python 3 installed, along with Python modules "appdirs", "pyyaml" and "pyalpm". Pyalpm is only required if you want to use the bundled plugins for backing up Arch Linux system. It is recommended to use the latest version of Python, as older versions may not work.

2. Create some Borg repositories

```cd ~/backup
mkdir sysconf packages
borg -e repokey sysconf
borg -e repokey packages
```

3. Edit config file

   The configuration file is written in YAML, and usually stored in ~/.config/etcbackup/config.yaml. Its syntax is very simple and intuitive. The sample configuration can be used to make a not-so-complete backup of Arch Linux system configuration. It finds modified [package backup files](https://wiki.archlinux.org/index.php/Pacman/Pacnew_and_Pacsave#Package_backup_files)(which are usually user-modifible configuration files) and files in /etc not owned by any package to be backed up into "sysconf" repository, and also backs up a list of installed packages into "packages" repository.

4. Include this Git repository in PYTHONDIR, and run `python etcbackup/main.py ~/backup`

# Similar projects #
Please see https://github.com/borgbackup/community#user-content-backup-scripts--borg-wrappers

# Disclaimer #
THIS SOFTWARE IS PROVIDED "AS-IS", USE IT AT YOUR OWN RISK. IN NO CASES SHALL I BE RESPONSIBLE FOR ANY DIRECT OR INDIRECT DAMAGE CAUSED BY USING THE SOFTWARE, INCLUDING BUT NOT LIMITED TO INCOMPLETE BACKUP OR LOSS OF DATA.
