# Maintainer: TitoBlackspire

pkgname=moonphase
pkgver=0.2.1
pkgrel=2
pkgdesc="Terminal based moon phase tracker"
arch=('any')
url="https://github.com/TitoBlackspire/MoonPhase-CLI"
license=('MIT')

depends=(
    'python'
    'python-requests'
    'python-geopy'
    'python-dotenv'
    'python-toml'
)

source=(
    "moonphase-$pkgver.tar.gz::https://github.com/TitoBlackspire/MoonPhase-CLI/archive/refs/tags/v$pkgver.tar.gz"
)

sha256sums=('351acc590738f35e61a4d9da0c1548bf69f06943665469cb926590e9e1d815f0')


package() {

    install -Dm755 \
        "$srcdir/MoonPhase-CLI-$pkgver/scripts/main.py" \
        "$pkgdir/opt/moonphase/main.py"

    install -Dm644 \
    "$srcdir/MoonPhase-CLI-$pkgver/LICENSE" \
    "$pkgdir/usr/share/licenses/$pkgname/LICENSE"

    cp -r \
        "$srcdir/MoonPhase-CLI-$pkgver/scripts/MoonFiles" \
        "$pkgdir/opt/moonphase/MoonFiles"

    install -Dm755 /dev/stdin "$pkgdir/usr/bin/moonphase" <<EOF

#!/bin/bash
exec /usr/bin/python /opt/moonphase/main.py "\$@"
EOF
}
