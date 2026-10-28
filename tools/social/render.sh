#!/bin/sh
# Renders every social image from tools/social/social.html into social/ with headless Chrome.
#   ./tools/social/render.sh            all assets
#   ./tools/social/render.sh x-header   only the named ones
set -e
cd "$(dirname "$0")/../.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
mkdir -p social

size() {
  case "$1" in
    avatar-mark|avatar-wordmark|square) echo 1080,1080 ;;
    x-header) echo 1500,500 ;;
    linkedin-banner) echo 1584,396 ;;
    linkedin-cover) echo 1128,191 ;;
    story) echo 1080,1920 ;;
    *) echo "unknown asset: $1" >&2; exit 1 ;;
  esac
}

ASSETS="${*:-avatar-mark avatar-wordmark x-header linkedin-banner linkedin-cover square story}"
for a in $ASSETS; do
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size="$(size "$a")" --virtual-time-budget=8000 \
    --screenshot="$PWD/social/$a.png" "file://$PWD/tools/social/social.html?a=$a" 2>/dev/null
  echo "social/$a.png"
done
