# Summary #
This is a simple command-line front-end of [Borg](https://www.borgbackup.org/)([Github](https://github.com/borgbackup/borg/)) backup utility. Unlike many other Borg wrappers, it allows you to dynamically generate list of files or some raw data to be backed up using plugin modules. It also supports creating and backing up to multiple repositories with one single command.

# Quick start #

1. Installation

   If you are using Arch Linux, a PKGBUILD file is provided (currently **not** in AUR), simply download it into a temporary directory and run `makepkg`. Otherwise, the recommended way to install is by using `pip`. To do this, you must have Python 3 installed(preferably the latest version), then run one of the following commands:
   * `pip install --user git+https://github.com/SunnySeaside/etcbackup`
   
     This will download and install etcbackup along with all required dependencies into your home directory automatically. Note that you should have `~/.local/bin` in your $PATH, in order to run etcbackup conveniently.
   * `pip install git+https://github.com/SunnySeaside/etcbackup`
   
     Like the above, but install system-wide. Root permission required.

2. Edit config file

   The configuration file is written in YAML, and usually needs to be stored in ~/.config/etcbackup/config.yaml. Its syntax is very simple and intuitive. The sample configuration can be used to make a not-so-complete backup of Arch Linux system configuration. It finds modified [package backup files](https://wiki.archlinux.org/index.php/Pacman/Pacnew_and_Pacsave#Package_backup_files)(which are usually user-modifible configuration files) and files in /etc not owned by any package to be backed up into "sysconf" repository, and also backs up a list of installed packages into "packages" repository.

3. Create some Borg repositories

   ```mkdir ~/backup
   etcbackup -c '-e repokey' ~/backup
   ```

   Or you could create them manually:
   ```cd ~/backup
   mkdir sysconf packages
   borg -e repokey sysconf
   borg -e repokey packages
   ```

4. Run `etcbackup ~/backup`.

# Similar projects #
Please see https://github.com/borgbackup/community#user-content-backup-scripts--borg-wrappers

# Disclaimer #
THIS SOFTWARE IS PROVIDED "AS-IS", USE IT AT YOUR OWN RISK. IN NO CASES SHALL I BE RESPONSIBLE FOR ANY DIRECT OR INDIRECT DAMAGE CAUSED BY USING THE SOFTWARE, INCLUDING BUT NOT LIMITED TO INCOMPLETE BACKUP OR LOSS OF DATA.
