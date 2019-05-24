#pyalpm does not parse pacman.conf to get synced repositories, resorting to calling pacman directly
import sys
import subprocess
repotype="file"
def get_data(outfile):
    subprocess.run(["pacman","-Qqen"],stdout=outfile)

if __name__ == "__main__":
    get_data(sys.stdout)
