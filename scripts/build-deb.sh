#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# ZIP extractors and GitHub web uploads may discard executable permissions.
# Restore the executable permissions required by Debian maintainer scripts,
# the DKMS tools and the packaged service executables.
for script in preinst postinst prerm postrm; do
  chmod 755 "package/DEBIAN/$script"
done
chmod 755 package/usr/sbin/ugreen-led-* package/usr/bin/ugreen-diskiomon package/usr/bin/ugreen-probe-leds package/usr/bin/ugreen-netdevmon package/usr/bin/ugreen-blink-disk package/usr/bin/ugreen_leds_cli package/usr/libexec/ugreen-led-* 
mkdir -p dist
dpkg-deb --build --root-owner-group package dist/ugreen-led-complete_1.0.2_amd64.deb
printf 'Created: %s\n' "$(pwd)/dist/ugreen-led-complete_1.0.2_amd64.deb"
