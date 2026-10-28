#!/bin/sh
# Renders tools/og.html to assets/og.png (1200x630) with headless Chrome.
set -e
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --virtual-time-budget=8000 \
  --screenshot="$PWD/assets/og.png" "file://$PWD/tools/og.html"
