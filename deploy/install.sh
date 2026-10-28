#!/usr/bin/env bash
# One-time setup of the web VM (ogbon-web). After this the VM deploys itself: ogbon-web-update.timer
# pulls ghcr.io/ogbonhq/ogbon-website:main at boot and every 5 minutes (deploy/ogbon-web-update.sh).
#
#   bash deploy/install.sh                         site only (no tunnel yet)
#   TUNNEL_ID=<id> bash deploy/install.sh          site + tunnel
#
# The package is public, so no registry login is needed. For the tunnel, run first as this user:
# `cloudflared tunnel login` (pick ogbon.com) and `cloudflared tunnel create ogbon-web`, which
# writes ~/.cloudflared/<TUNNEL_ID>.json. That file is copied to /etc/ogbon-web/cloudflared/
# (root, readable by the cloudflared container's uid 65532), never printed.
set -euo pipefail
cd "$(dirname "$0")"

command -v docker >/dev/null && docker compose version >/dev/null 2>&1 \
  || sudo apt-get -o DPkg::Lock::Timeout=600 install -y -q docker.io docker-compose-v2
sudo systemctl enable --now docker

if [ -n "${TUNNEL_ID:-}" ]; then
  CREDS=~/.cloudflared/$TUNNEL_ID.json
  [ -s "$CREDS" ] || { echo "missing $CREDS (cloudflared tunnel create ogbon-web)"; exit 1; }
  # cloudflared runs as uid 65532 in its image.
  sudo install -d -m 750 -o root -g 65532 /etc/ogbon-web/cloudflared
  sudo install -m 640 -o root -g 65532 "$CREDS" /etc/ogbon-web/cloudflared/$TUNNEL_ID.json
  sudo tee /etc/ogbon-web/cloudflared/config.yml >/dev/null <<END
tunnel: $TUNNEL_ID
credentials-file: /etc/cloudflared/$TUNNEL_ID.json
protocol: http2
ingress:
  # ogbon.com, www.ogbon.com, web-staging.ogbon.com: nginx answers by Host (www -> apex 301).
  - service: http://127.0.0.1:8092
END
fi

sudo install -m 755 ogbon-web-update.sh /usr/local/bin/ogbon-web-update
sudo install -m 644 systemd/ogbon-web-update.service systemd/ogbon-web-update.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ogbon-web-update.timer
sudo systemctl start ogbon-web-update.service   # first deploy now; the timer takes over
sudo systemctl start ogbon-web-update.timer
sudo docker compose -p ogbon-web ps
echo "logs: journalctl -u ogbon-web-update; sudo docker compose -p ogbon-web logs -f"
