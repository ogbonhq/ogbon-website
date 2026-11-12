#!/usr/bin/env bash
# Checks a running site: every page and asset, the redirects, cache and security headers, and that
# nothing outside the site is served. Run from the repo root.
#
#   bash tests/smoke.sh                                   the container (CI, or on the VM)
#   REMOTE=1 bash tests/smoke.sh https://ogbon.com        through Cloudflare (skips the checks
#                                                         that need the origin: www Host, gzip, Server)
#   SMOKE_CURL_ARGS="--doh-url https://1.1.1.1/dns-query"   extra curl args, e.g. to skip stale local DNS
set -uo pipefail
cd "$(dirname "$0")/.."
BASE=${1:-http://127.0.0.1:8092}
REMOTE=${REMOTE:-0}
SMOKE_CURL_ARGS=${SMOKE_CURL_ARGS:-}
fail=0

# expect PATH STATUS [HEADER-REGEX ...] (extra curl args in CURL_ARGS)
expect() {
  local path=$1 status=$2 h got
  shift 2
  h=$(curl -s -o /dev/null -D - $SMOKE_CURL_ARGS "${CURL_ARGS[@]}" "$BASE$path" | tr -d '\r')
  got=$(head -1 <<<"$h" | awk '{print $2}')
  if [ "$got" != "$status" ]; then
    echo "FAIL $path: status ${got:-none}, want $status"; fail=1; return
  fi
  for pat; do
    grep -qiE "$pat" <<<"$h" || { echo "FAIL $path: no header matching /$pat/"; fail=1; return; }
  done
  echo "ok   $path $status"
}
CURL_ARGS=()
PAGE=('^content-type: text/html' '^cache-control: no-cache$')
WEEK='^cache-control: public, max-age=604800$'
SECURITY=('^strict-transport-security: max-age=31536000' '^x-content-type-options: nosniff$'
          '^referrer-policy: strict-origin-when-cross-origin$' '^x-frame-options: SAMEORIGIN$')

for p in / /index.html /research.html; do
  expect "$p" 200 "${PAGE[@]}" "${SECURITY[@]}"
done
for p in /styles.css?v=1 /script.js?v=1 /favicon.ico /favicon.svg /apple-touch-icon.png; do
  expect "$p" 200 "$WEEK"
done
while read -r f; do expect "/$f" 200 "$WEEK"; done < <(find assets -type f ! -name '.*' | sort)
# Through Cloudflare robots.txt gets the zone's Browser Cache TTL (4 h) instead of no-cache.
if [ "$REMOTE" = 0 ]; then
  expect /robots.txt 200 '^content-type: text/plain' '^cache-control: no-cache$'
else
  expect /robots.txt 200 '^content-type: text/plain'
fi
expect /sitemap.xml 200 '^content-type: (text|application)/xml' '^cache-control: no-cache$'
expect /site.webmanifest 200 '^content-type: application/manifest\+json' '^cache-control: no-cache$'

for p in /team.html /team /careers.html /compare.html /compare; do
  expect "$p" 301 '^location: (https://[^/]+)?/$'
done
expect /nope 404 '^content-type: text/html' '^cache-control: no-cache$'
grep -q 'Page not found' <(curl -s $SMOKE_CURL_ARGS "$BASE/nope") || { echo "FAIL /nope: not the 404 page"; fail=1; }
for p in /README.md /deploy.sh /.htaccess /.vercelignore /Dockerfile /nginx.conf /index.launch.html \
         /archive/ /tools/serve.mjs /social/square.png /deploy/compose.yml /tests/smoke.sh /50x.html; do
  expect "$p" 404
done

if [ "$REMOTE" = 0 ]; then
  CURL_ARGS=(-H 'Host: www.ogbon.com')
  expect '/research.html?x=1' 301 '^location: https://ogbon\.com/research\.html\?x=1$'
  CURL_ARGS=(-H 'Accept-Encoding: gzip')
  expect /styles.css 200 '^content-encoding: gzip$'
  CURL_ARGS=()
  expect / 200 '^server: nginx$'
fi

[ $fail = 0 ] && echo "all checks passed" || echo "SOME CHECKS FAILED"
exit $fail
