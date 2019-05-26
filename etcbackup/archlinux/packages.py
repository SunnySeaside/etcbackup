#pyalpm does not parse pacman.conf to get synced repositories, resorting to calling pacman directly
import sys
import subprocess
repotype="data"
def write_data(outfile):
    subprocess.run(["pacman","-Qqen"],stdout=outfile)

if __name__ == "__main__":
    write_data(sys.stdout)
