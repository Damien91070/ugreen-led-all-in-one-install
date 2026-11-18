#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
dpkg-deb --build --root-owner-group package dist/ugreen-led-complete_1.0.2_amd64.deb
printf 'Created: %s\n' "$(pwd)/dist/ugreen-led-complete_1.0.2_amd64.deb"
