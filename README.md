# ogbon.com

Single-page site for Ogbon, the inference layer for physical AI: big models at edge speed for robots, drones and machines. Built on the 2026-10-17 designed layout (Geist and Newsreader web fonts), with copy rewritten on 2026-10-21 from the physical AI thesis.

Copy rules: say machines, not just robots (we serve drones, inspection rigs, factory lines and more); no em dashes; no sourced market figures or benchmark numbers until we have them.

- `index.html` · the whole site: hero, problem, why now, device/site/city, the latency stack, who it's for, research, careers, SEO tags and structured data
- `styles.css` · all styling; `script.js` · mailto links and small interactions
- `assets/logo.svg` / `assets/logo-light.svg` · pixel wordmark; `assets/glyphs/` · section glyphs; `assets/og.png` · share image; `assets/icons/` · app icons
- `favicon.ico` / `favicon.svg` / `apple-touch-icon.png`, `site.webmanifest`, `robots.txt`, `sitemap.xml`
- `tools/pixels.mjs` · regenerates the logo, icons and glyphs from pixel bitmaps: `node tools/pixels.mjs`
- `tools/og.html` + `tools/og.sh` · source and renderer for `assets/og.png`: `./tools/og.sh`
- `tools/serve.mjs` · local preview: `node tools/serve.mjs 4196`
- `tools/social/social.html` + `tools/social/render.sh` · source and renderer for `social/` (profile pictures, X header, LinkedIn banner and cover, square post, story) at 2x: `./tools/social/render.sh` or name assets to render only those. Not uploaded by `deploy.sh`.
- `archive/2026-10-17-designed/` · the VirtualGPU (CPU research) version this layout came from
- `archive/2026-10-21-launch/` · the plain-HTML launch page (and its share image) that this replaced

Email: early access and research go to hello@ogbon.com, applications to careers@ogbon.com (both set in `script.js`). Each role has an anchor, e.g. `/#role-senior-cpp-engineer`.

Update `lastmod` in `sitemap.xml` when content changes.

## Deploy

Caching: the host caches `styles.css` and `script.js` in browsers for 7 days, so `index.html` links them as `styles.css?v=…` and `script.js?v=…`. Bump that version whenever either file changes, or returning visitors see old styles on the new page. `.htaccess` makes pages revalidate on every visit and redirects www to the bare domain (www still needs an SSL certificate from the host before that works over https).

`./deploy.sh` uploads the site to ogbon.com over FTPS; `./deploy.sh upload index.html` uploads only the files you name. The login comes from `~/.netrc`. `./deploy.sh list` shows the remote folder.

Vercel also works: point it at this folder, no framework preset. `.vercelignore` keeps `tools/`, `archive/`, `deploy.sh` and this README out of that deploy.
