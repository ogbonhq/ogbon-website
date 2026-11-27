# ogbon.com

The website for Ogbon Security: cybersecurity with cover built in. Engineers build with ogbon-1, Ogbon checks websites, apps, APIs, cloud and internal systems every day, and a cover warranty backed by Casava pays for the loss if an attacker still gets through.

Copy rules: plain words, no em dashes, say organisations (not businesses), and call v1 cover a warranty, not an insurance policy.

- `tools/pages.py` · writes every HTML page (home, report, how it works, ogbon-1, cover, pricing, incident, about, privacy, terms, 404) from one place, so the head, nav and footer stay the same: `python3 tools/pages.py`. Legal text is in `tools/legal.py`. Edit these, not the HTML.
- `styles.css` · all styling; `script.js` · small interactions
- `assets/` · logo, icons, glyphs, share image (`og.png`) and partner logos (`partners/`)
- `favicon.ico` / `favicon.svg` / `apple-touch-icon.png`, `site.webmanifest`, `robots.txt`, `sitemap.xml`
- `tools/pixels.mjs` · regenerates the logo, icons and glyphs from pixel bitmaps: `node tools/pixels.mjs`
- `tools/og.html` + `tools/og.sh` · source and renderer for `assets/og.png`: `./tools/og.sh`
- `tools/serve.mjs` · local preview: `node tools/serve.mjs 4196`
- `tools/social/` · source and renderer for the `social/` images (profile pictures, banners, posts)

Update `lastmod` in `sitemap.xml` when content changes.

## Headline A/B test (started 2026-11-27)

The homepage shows one of two headlines, 50/50, chosen once per browser by a small inline script above the `<h1>` in `index.html` (and in `tools/pages.py`):

- A: "Cybersecurity with cover built in"
- B: "Cyber cover with security built in"

The choice is kept in `localStorage` (`ogbon_hv`), not a cookie. When someone requests a free report, `script.js` adds a `headline` field (`A`, `B`, or `none` if they never saw the homepage) to the Formspree submission. To read the result, count report requests by `headline` in Formspree: visitors are split at random, so the counts compare directly. Add `?hv=a` or `?hv=b` to the homepage URL to see a given headline. To end the test, keep the winning `<span class="hv">` text as the plain `<h1>`, and remove the script and the `.hv` CSS rules.

## Deploy

Push to `main` and it goes live. Work on `dev` (the default branch), then fast-forward or PR `dev` → `main`.

- CI (`.github/workflows/ci.yml`) builds the nginx image (`Dockerfile`, `nginx.conf`), runs it and checks every page, asset, redirect and header (`tests/smoke.sh`), then pushes `ghcr.io/ogbonhq/ogbon-website:<branch>` and `:sha-<short>` (public package).
- The GCP VM `ogbon-web` (europe-west8-c, e2-small) pulls `:main` at boot and every 5 minutes (`deploy/ogbon-web-update.sh`, systemd timer `ogbon-web-update.timer`) and swaps nginx without dropping requests. So a push to `main` is live about 5-8 minutes later. To deploy at once: `gcloud compute ssh ogbon-web --zone europe-west8-c --command "sudo systemctl start ogbon-web-update"`.
- No open ports: Cloudflare (DNS, TLS, cache) reaches nginx on `127.0.0.1:8092` through the cloudflared tunnel `ogbon-web` (ogbon.com, www.ogbon.com). Everything on the VM is in `deploy/` (`compose.yml`, the updater, `install.sh` for a new VM).
- Only the site files are in the image; `tools/`, `social/`, this README and the deploy scripts are not served (the `Dockerfile` lists what is).
- To check a deploy: `REMOTE=1 bash tests/smoke.sh https://ogbon.com` (Git Bash).

Caching (`nginx.conf`, same rules the old `.htaccess` had): pages (`.html .xml .txt .webmanifest`) revalidate on every visit; everything else, including `styles.css` and `script.js`, is cached in browsers for 7 days, so `index.html` links them as `styles.css?v=…` and `script.js?v=…`. Bump that version whenever either file changes, or returning visitors see old styles on the new page. www redirects to the bare domain, `/careers.html` to `/team.html#careers`.

Rollback: to an older version, revert the commit on `main` (CI redeploys), or pin an image on the VM: `echo OGBON_WEB_IMAGE=ghcr.io/ogbonhq/ogbon-website:sha-<short> | sudo tee /etc/ogbon-web/update.env` then `sudo systemctl start ogbon-web-update` (delete the file to follow `main` again). To the old host, in Cloudflare DNS for ogbon.com set `ogbon.com` back to an A record `199.188.201.77` (proxied) and `www` to a CNAME to `ogbon.com` (proxied); the Namecheap hosting plan is kept for mail.

Emergency fallback only: `./deploy.sh` still uploads the site to the old Namecheap hosting over FTPS (login from `~/.netrc`; `./deploy.sh upload index.html` uploads only the files you name, `./deploy.sh list` shows the remote folder). It is not live unless DNS is rolled back as above. `.htaccess` is for that host only.
