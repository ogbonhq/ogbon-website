#!/usr/bin/env bash
# Converge the web VM on the latest site image. Run as root by ogbon-web-update.timer at boot and
# every 5 minutes; safe to run by hand any time (idempotent).
#
#   1. Pull ghcr.io/ogbonhq/ogbon-website:main. Same digest as last time: `compose up -d` (restarts
#      whatever died) and stop.
#   2. New digest: copy compose.yml, this script and the systemd units out of the image, start the
#      new nginx next to the old one (same port, reuseport), wait until it is healthy, stop the old
#      one (nginx finishes its open requests on SIGQUIT), then `compose up -d`.
set -euo pipefail
export OGBON_WEB_IMAGE=${OGBON_WEB_IMAGE:-ghcr.io/ogbonhq/ogbon-website:main}
IMAGE=$OGBON_WEB_IMAGE
DIR=/opt/ogbon-web
STATE=/var/lib/ogbon-web
mkdir -p "$DIR" "$STATE"
compose() { docker compose --progress quiet -p ogbon-web -f "$DIR/compose.yml" "$@"; }
webs() { docker ps -q --filter label=com.docker.compose.project=ogbon-web --filter label=com.docker.compose.service=web; }

# cloudflared only once the tunnel is configured (deploy/install.sh writes the config).
services() {
  echo web
  if [ -f /etc/ogbon-web/cloudflared/config.yml ]; then echo cloudflared; fi
}

rollout_web() {
  local old new
  old=$(webs)
  [ -n "$old" ] || return 0  # nothing running: the plain `compose up` starts it
  compose up -d --no-deps --no-recreate --scale web=2 web
  new=$(webs | grep -vxF -f <(printf '%s\n' $old) || true)
  [ -n "$new" ] || { echo "rollout: no new web container started"; return 1; }
  for _ in $(seq 60); do
    [ "$(docker inspect --format '{{.State.Health.Status}}' "$new")" = healthy ] && break
    sleep 1
  done
  if [ "$(docker inspect --format '{{.State.Health.Status}}' "$new")" != healthy ]; then
    echo "rollout: new web container not healthy after 60 s; keeping the old one"
    docker logs --tail 20 "$new" || true
    docker rm -f "$new" >/dev/null
    return 1
  fi
  docker stop --time 30 $old >/dev/null
  docker rm $old >/dev/null
  compose up -d --no-deps --no-recreate --scale web=1 web
  echo "rollout: web replaced without downtime"
}

docker pull --quiet "$IMAGE" >/dev/null
digest=$(docker image inspect --format '{{index .RepoDigests 0}}' "$IMAGE")
if [ -f "$DIR/compose.yml" ] && [ "$(cat "$STATE/deployed" 2>/dev/null)" = "$digest" ]; then
  compose up -d --remove-orphans $(services)
  exit 0
fi
echo "deploying $digest"

staging=$(mktemp -d)
trap 'rm -rf "$staging"; [ -n "${cid:-}" ] && docker rm -f "$cid" >/dev/null' EXIT
cid=$(docker create "$IMAGE")
docker cp "$cid:/opt/ogbon-web/deploy/." "$staging/"
install -m 644 "$staging/compose.yml" "$DIR/compose.yml"
compose pull --quiet --ignore-pull-failures $(services) 2>/dev/null || true
rollout_web
compose up -d --remove-orphans $(services)

install -m 755 "$staging/ogbon-web-update.sh" /usr/local/bin/ogbon-web-update
install -m 644 "$staging/systemd/ogbon-web-update.service" "$staging/systemd/ogbon-web-update.timer" \
  /etc/systemd/system/
systemctl daemon-reload

echo "$digest" > "$STATE/deployed"
echo "deployed $(docker image inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' "$IMAGE")"
