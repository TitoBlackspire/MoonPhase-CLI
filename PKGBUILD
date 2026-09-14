pkgname=moonphase
pkgver=0.2.0
pkgrel=1
pkgdesc="Terminal based moon phase tracker"
arch=('any')
license=('MIT')
depends=('python')
makedepends=('python-pip' 'python-virtualenv')
sha256sums=()

build() {
    python -m venv "$srcdir/venv"
    source "$srcdir/venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$startdir/requirements.txt"
    deactivate
}

package() {
    install -Dm755 "$startdir/scripts/main.py" "$pkgdir/opt/moonphase/main.py"
    cp -r "$startdir/scripts/MoonFiles" "$pkgdir/opt/moonphase/MoonFiles"
    cp -r "$srcdir/venv" "$pkgdir/opt/moonphase/venv"

    install -Dm755 /dev/stdin "$pkgdir/usr/bin/moonphase" <<EOF
#!/bin/bash
exec "/opt/moonphase/venv/bin/python" "/opt/moonphase/main.py" "\$@"
EOF
}
