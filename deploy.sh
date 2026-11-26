#!/bin/sh
# Uploads the site over explicit FTPS (TLS required).
# The login is read from ~/.netrc, never from this script:
#   machine server275-2.web-hosting.com login <user> password <password>
#
#   ./deploy.sh list   list the remote folder (read-only)
#   ./deploy.sh files  print what would be uploaded
#   ./deploy.sh        upload everything
#   ./deploy.sh upload index.html styles.css   upload only these files
#
# REMOTE_DIR overrides the target folder. Default is the FTP home, which is
# the ogbon.com web root for this account.
set -eu
cd "$(dirname "$0")"

# ftp.baskiatofficial.com points here; the TLS certificate is issued for *.web-hosting.com.
HOST="server275-2.web-hosting.com"
REMOTE_DIR="${REMOTE_DIR:-}"
BASE="ftp://$HOST${REMOTE_DIR:+/$REMOTE_DIR}"
# TLS 1.3 data connections get cut off by this server (FTP 451), so cap at 1.2.
CURL="curl --netrc --ssl-reqd --tls-max 1.2 --silent --show-error --fail"

# Designed site: the page, its stylesheet and script, icons, logos, glyphs and the share image.
FILES=".htaccess index.html report.html how-it-works.html ogbon-1.html privacy.html terms.html cover.html pricing.html incident.html about.html styles.css script.js favicon.ico favicon.svg apple-touch-icon.png site.webmanifest robots.txt sitemap.xml assets/logo.svg assets/logo-light.svg assets/og.png assets/icons.svg $(find assets/icons assets/glyphs assets/logos -type f ! -name '.*' | sort)"

case "${1:-upload}" in
  list)
    $CURL "$BASE/" --list-only
    ;;
  files)
    for f in $FILES; do echo "$f"; done
    ;;
  upload)
    if [ $# -gt 0 ]; then shift; fi
    [ $# -gt 0 ] && FILES="$*"
    for f in $FILES; do
      src="$f"
      printf "uploading %s\n" "$f"
      $CURL --ftp-create-dirs -T "$src" "$BASE/$f"
      local_size=$(wc -c < "$src" | tr -d " ")
      remote_size=$($CURL -I "$BASE/$f" | tr -d "\r" | awk "/Content-Length/ {print \$2}")
      [ "$local_size" = "$remote_size" ] || { echo "size mismatch on $f: $local_size vs $remote_size" >&2; exit 1; }
    done
    echo "done: $(echo $FILES | wc -w | tr -d " ") files to $HOST/${REMOTE_DIR}"
    ;;
  *)
    echo "usage: $0 [list|files|upload]" >&2; exit 1
    ;;
esac
