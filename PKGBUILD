pkgname=etcbackup-git
pkgver=0.1
pkgrel=1
pkgdesc="https://github.com/SunnySeaside/etcbackup"
arch=('any')
url=""
license=('BSD')
groups=()
depends=('python' 'borg' 'python-appdirs' 'python-yaml')
makedepends=('git' 'python-setuptools')
optdepends=('pyalpm: for backing up modified /etc files')
replaces=()
backup=()
options=()
install=
source=("${pkgname}::git+https://github.com/SunnySeaside/etcbackup.git")
noextract=()
md5sums=('SKIP')

# Please refer to the 'USING VCS SOURCES' section of the PKGBUILD man page for
# a description of each element in the source array.

pkgver() {
	cd "$srcdir/$pkgname"

# The examples below are not absolute and need to be adapted to each repo. The
# primary goal is to generate version numbers that will increase according to
# pacman's version comparisons with later commits to the repo. The format
# VERSION='VER_NUM.rREV_NUM.HASH', or a relevant subset in case VER_NUM or HASH
# are not available, is recommended.


# Git, tags available
#	printf "%s" "$(git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g')"

# Git, no tags available
	printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}


build() {
	cd "$srcdir/$pkgname"
	python ./setup.py build
}

package() {
	cd "$srcdir/$pkgname"
	python ./setup.py install --root="$pkgdir" --optimize=1 --skip-build
}
