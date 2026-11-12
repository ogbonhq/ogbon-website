// Applications go to careers, early access and research requests to hello.
const CAREERS_EMAIL = "careers@ogbon.com";
const CONTACT_EMAIL = "hello@ogbon.com";

// Mailto links: every [data-apply] gets a role-specific subject. [data-email="Subject"]
// gets that subject; a bare [data-email] shows the address as its text.
document.querySelectorAll("[data-apply]").forEach((a) => {
  const role = a.dataset.apply;
  const subject = role ? `Application: ${role}` : "Joining Ogbon";
  a.href = `mailto:${CAREERS_EMAIL}?subject=${encodeURIComponent(subject)}`;
});
document.querySelectorAll("[data-email]").forEach((a) => {
  const subject = a.dataset.email;
  a.href = `mailto:${CONTACT_EMAIL}${subject ? `?subject=${encodeURIComponent(subject)}` : ""}`;
  if (!subject) a.textContent = CONTACT_EMAIL;
});

// Nav turns dark once the cream hero has scrolled past.
const nav = document.getElementById("nav");
const hero = document.querySelector(".hero");
const setNav = () => {
  nav.classList.toggle("is-scrolled", window.scrollY > 8);
  if (hero) nav.classList.toggle("is-dark", window.scrollY > hero.offsetHeight - 56);
};
setNav();
window.addEventListener("scroll", setNav, { passive: true });

// Small screens: the bar keeps the logo, Log in and a menu button; the other links open in a panel.
const navLinks = nav.querySelector(".nav-links");
const menuItem = document.createElement("li");
menuItem.className = "nav-menu-item";
menuItem.innerHTML = `<button class="nav-menu" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="Menu"><span></span><span></span></button>`;
navLinks.appendChild(menuItem);
const menuBtn = menuItem.querySelector("button");
const panel = document.createElement("div");
panel.className = "nav-panel";
panel.id = "nav-panel";
panel.hidden = true;
panel.innerHTML = `<ul>${[...navLinks.querySelectorAll("a:not(.pill)")].map((a) => `<li>${a.outerHTML.replace(/ aria-current="page"/, "")}</li>`).join("")}</ul>`;
nav.appendChild(panel);
const setMenu = (open) => {
  nav.classList.toggle("is-open", open);
  panel.hidden = !open;
  menuBtn.setAttribute("aria-expanded", String(open));
  menuBtn.setAttribute("aria-label", open ? "Close menu" : "Menu");
};
menuBtn.addEventListener("click", () => setMenu(panel.hidden));
panel.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !panel.hidden) { setMenu(false); menuBtn.focus(); } });
window.matchMedia("(min-width: 761px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });

// Device, site and city grids ([data-grid="COLSxROWS"]), lit in a diagonal sweep.
const grids = [...document.querySelectorAll("[data-grid]")];
grids.forEach((grid) => {
  const [cols, rows] = grid.dataset.grid.split("x").map(Number);
  grid.style.setProperty("--cols", cols);
  const frag = document.createDocumentFragment();
  for (let i = 0; i < cols * rows; i++) {
    const cell = document.createElement("i");
    const x = i % cols, y = Math.floor(i / cols);
    cell.style.setProperty("--d", `${(x + y) * 28}ms`);
    frag.appendChild(cell);
  }
  grid.appendChild(frag);
});

// News reel: duplicate the cards once so the loop is seamless; copies are hidden
// from assistive tech and keyboard focus. Reduced motion keeps a plain scroller.
document.querySelectorAll("[data-reel]").forEach((reel) => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const track = reel.querySelector(".reel-track");
  [...track.children].forEach((item) => {
    const copy = item.cloneNode(true);
    copy.setAttribute("aria-hidden", "true");
    copy.querySelectorAll("a").forEach((a) => a.setAttribute("tabindex", "-1"));
    track.appendChild(copy);
  });
  reel.classList.add("is-looping");
});

// Entrance reveals, and only animate the grids while they are on screen.
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (grids.includes(e.target)) { e.target.classList.toggle("on", e.isIntersecting); return; }
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  });
}, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

document.querySelectorAll(".reveal").forEach((el, i) => {
  // Stagger siblings that enter together.
  el.style.transitionDelay = `${Math.min(i % 4, 3) * 70}ms`;
  io.observe(el);
});
grids.forEach((grid) => io.observe(grid));

// "Explore open positions" opens every role description.
document.querySelectorAll("[data-open-roles]").forEach((btn) => btn.addEventListener("click", (e) => {
  e.preventDefault();
  document.querySelectorAll(".role details").forEach((d) => (d.open = true));
  document.querySelector(".role").scrollIntoView({ block: "start" });
}));

// Deep links to a role (e.g. /#role-senior-cpp-engineer) open its description.
const openRoleFromHash = () => {
  const role = location.hash.startsWith("#role-") && document.getElementById(location.hash.slice(1));
  if (!role) return;
  role.querySelector("details").open = true;
  role.classList.add("in");
  role.scrollIntoView({ block: "start" });
};
openRoleFromHash();
window.addEventListener("hashchange", openRoleFromHash);

// Hero: ogbon-1 at work on a codebase, drawn as a dot matrix. Each scene is painted at grid
// resolution on a small offscreen canvas; every cell's coverage becomes a dot. Scenes dissolve
// into one another cell by cell, and green packets stream in from the top corner (the model).
(() => {
  const canvas = document.querySelector("[data-machines]");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const off = document.createElement("canvas");
  const octx = off.getContext("2d", { willReadFrequently: true });
  const INK = "238, 233, 227", GREEN = "#30D75D";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Scenes draw in a 100x100 box and return the point packets stream to.
  const limb = (c, x1, y1, x2, y2, w) => {
    c.lineWidth = w; c.lineCap = "round";
    c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke();
  };
  const disc = (c, x, y, r) => { c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill(); };

  // How far through its turn on screen a scene is (0 to 1), for things that build up.
  const progress = (t, span) => Math.min(1, (t % HOLD) / span);
  const ease = (k) => k * k * (3 - 2 * k);

  // An editor window and the code lines inside it, as [indent, width] rows.
  const ROWS = [[18, 40], [24, 30], [24, 46], [30, 26], [24, 38], [18, 20]];
  const editor = (c) => {
    c.lineWidth = 3.5;
    c.beginPath(); c.roundRect(10, 16, 80, 68, 5); c.stroke();
    c.fillRect(10, 16, 80, 9);
  };

  // Scan: a bar sweeps down the file and marks the lines with problems in the gutter.
  const scan = (c, t) => {
    editor(c);
    ROWS.forEach(([x, w], i) => c.fillRect(x, 32 + i * 8, w, 4));
    const y = 29 + progress(t, 1.8) * 50;
    for (const i of [2, 4]) if (y > 34 + i * 8) disc(c, 14, 34 + i * 8, 2.4);
    c.globalAlpha = 0.4; c.fillRect(12, y, 76, 3); c.globalAlpha = 1;
    return [88, y];
  };

  // Find: a magnifying glass moves across the code and stops on a bug.
  const find = (c, t) => {
    c.globalAlpha = 0.5;
    ROWS.concat(ROWS.slice(0, 2)).forEach(([x, w], i) => c.fillRect(x - 6, 18 + i * 8, w + 12, 4));
    c.globalAlpha = 1;
    const e = ease(progress(t, 1.4)), cx = 30 + 30 * e, cy = 30 + 24 * e;
    c.save();
    c.globalCompositeOperation = "destination-out"; disc(c, cx, cy, 13);
    c.restore();
    c.lineWidth = 4; c.beginPath(); c.arc(cx, cy, 13, 0, Math.PI * 2); c.stroke();
    limb(c, cx + 9.5, cy + 9.5, cx + 22, cy + 22, 6.5);
    if (e > 0.9) {
      c.beginPath(); c.ellipse(60, 54, 4.2, 5.6, 0, 0, Math.PI * 2); c.fill();
      for (const s of [-1, 1]) for (const dy of [-3, 1, 5]) limb(c, 60 + 3 * s, 54 + dy, 60 + 7.5 * s, 52.5 + dy + Math.sin(t * 14 + dy) * 0.8, 1.8);
    }
    return [cx, cy];
  };

  // Patch: a diff, with the bad line taken out and the fix typed in below it.
  const patch = (c, t) => {
    editor(c);
    const rows = [[24, 40], [24, 30], [24, 44], [24, 36], [24, 26], [24, 34]];
    let cursor = [24, 56];
    rows.forEach(([x, w], i) => {
      const y = 32 + i * 8;
      if (i === 2) {
        c.fillRect(14, y + 0.8, 6, 2.4);
        c.globalAlpha = 0.4; c.fillRect(x, y, w, 4); c.globalAlpha = 1;
      } else if (i === 3) {
        c.fillRect(14, y + 0.8, 6, 2.4); c.fillRect(15.8, y - 1, 2.4, 6);
        const d = progress(t, 1) * w;
        if (d > 0) c.fillRect(x, y, d, 4);
        cursor = [x + d + 2, y];
        if (Math.floor(t * 2.5) % 2) c.fillRect(cursor[0], y - 1, 3, 6);
      } else c.fillRect(x, y, w, 4);
    });
    return cursor;
  };

  // Merge: the fix branches off, gets its commits and merges back as a pull request.
  const merge = (c, t) => {
    const main = [[30, 14], [30, 86]];
    const steps = [[30, 24], [66, 38], [66, 62], [30, 76]];
    limb(c, main[0][0], main[0][1], main[1][0], main[1][1], 4);
    const active = Math.min(steps.length - 1, Math.floor(progress(t, 1.6) * steps.length));
    steps.forEach(([x, y], i) => {
      if (i < steps.length - 1) {
        c.globalAlpha = i < active ? 1 : 0.4;
        limb(c, x, y, steps[i + 1][0], steps[i + 1][1], 4);
        c.globalAlpha = 1;
      }
      if (i <= active) disc(c, x, y, 7);
      else { c.lineWidth = 3; c.beginPath(); c.arc(x, y, 6, 0, Math.PI * 2); c.stroke(); }
    });
    return steps[active];
  };

  // Secured: a shield, with a check drawing in.
  const shield = (c, t) => {
    c.lineWidth = 5; c.lineJoin = "round";
    c.beginPath();
    c.moveTo(50, 12); c.lineTo(80, 22); c.lineTo(80, 46);
    c.quadraticCurveTo(80, 74, 50, 88); c.quadraticCurveTo(20, 74, 20, 46);
    c.lineTo(20, 22); c.closePath(); c.stroke();
    const pts = [[36, 50], [46, 61], [65, 39]];
    let left = progress(t, 0.9) * 44, end = pts[0];
    for (let i = 0; i < 2 && left > 0; i++) {
      const [x1, y1] = pts[i], [x2, y2] = pts[i + 1], len = Math.hypot(x2 - x1, y2 - y1), k = Math.min(1, left / len);
      end = [x1 + (x2 - x1) * k, y1 + (y2 - y1) * k];
      limb(c, x1, y1, end[0], end[1], 7);
      left -= len;
    }
    return end;
  };

  // The loop ogbon-1 runs on a codebase: scan, find, patch, merge, secured.
  const scenes = [scan, find, patch, merge, shield];
  const HOLD = 3.2, FADE = 0.35;
  let cols = 0, rows = 0, cell = 10, noise = [], twinkle = [], packets = [], lastSpawn = 0;

  const resize = () => {
    const r = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
    if (!r.width || !r.height) return;
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cell = r.width < 520 ? 8 : 10;
    cols = Math.floor(r.width / cell); rows = Math.floor(r.height / cell);
    off.width = cols; off.height = rows;
    noise = Array.from({ length: cols * rows }, Math.random);
    twinkle = Array.from({ length: cols * rows }, () => Math.random() * Math.PI * 2);
  };

  // Paint a scene into the grid and return its per-cell coverage and packet target.
  const sample = (scene, t) => {
    octx.setTransform(1, 0, 0, 1, 0, 0);
    octx.clearRect(0, 0, cols, rows);
    const k = Math.min(cols, rows) / 100;
    octx.setTransform(k, 0, 0, k, (cols - 100 * k) / 2, (rows - 100 * k) / 2);
    octx.fillStyle = octx.strokeStyle = "#000";
    const [tx, ty] = scene(octx, t);
    const data = octx.getImageData(0, 0, cols, rows).data;
    const cov = new Float32Array(cols * rows);
    for (let i = 0; i < cov.length; i++) cov[i] = data[i * 4 + 3] / 255;
    return { cov, target: [tx * k + (cols - 100 * k) / 2, ty * k + (rows - 100 * k) / 2] };
  };

  const draw = (now) => {
    if (!cols) return;
    const t = now / 1000;
    const cycle = t % (HOLD * scenes.length), idx = Math.floor(cycle / HOLD), local = cycle - idx * HOLD;
    const cur = sample(scenes[idx], t);
    let mix = 0, next = null;
    if (local > HOLD - FADE) {
      mix = (local - (HOLD - FADE)) / FADE;
      next = sample(scenes[(idx + 1) % scenes.length], t);
    }
    const w = cols * cell, h = rows * cell;
    ctx.clearRect(0, 0, w, h);
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        const i = y * cols + x;
        const v = next && noise[i] < mix ? next.cov[i] : cur.cov[i];
        // The field fades toward the left, top and bottom edges so it melts into the page.
        const edge = Math.min(1, (x / cols) * 2.5) * Math.min(1, (y / rows) * 4) * Math.min(1, ((rows - y) / rows) * 4);
        const px = x * cell + cell / 2, py = y * cell + cell / 2;
        if (v > 0.3) {
          const s = Math.round(2 + (cell - 4) * Math.min(1, v));
          ctx.fillStyle = `rgba(${INK}, ${0.55 + 0.4 * v})`;
          ctx.fillRect(Math.round(px - s / 2), Math.round(py - s / 2), s, s);
        } else {
          const a = (0.15 + 0.08 * Math.sin(t * 1.3 + twinkle[i])) * edge + v * 0.5;
          ctx.fillStyle = `rgba(${INK}, ${a})`;
          ctx.fillRect(Math.round(px - 1), Math.round(py - 1), 2, 2);
        }
      }
    }
    // Packets: from the top-right corner to where the work is happening, snapped to the grid.
    const target = next && mix > 0.5 ? next.target : cur.target;
    if (!reduce && t - lastSpawn > 0.07) {
      lastSpawn = t;
      packets.push({ born: t, sx: cols - 1 - Math.random() * 3, sy: Math.random() * 3 });
    }
    packets = packets.filter((p) => t - p.born < 0.45);
    ctx.fillStyle = GREEN;
    for (const p of packets) {
      const k = (t - p.born) / 0.45, e = k * k * (3 - 2 * k);
      const gx = Math.round(p.sx + (target[0] - p.sx) * e), gy = Math.round(p.sy + (target[1] - p.sy) * e);
      const s = cell - 3;
      ctx.globalAlpha = Math.min(1, (1 - k) * 3);
      ctx.fillRect(gx * cell + (cell - s) / 2, gy * cell + (cell - s) / 2, s, s);
    }
    ctx.globalAlpha = 1;
  };

  let running = false, frame = 0;
  const loop = (now) => { draw(now); if (running) frame = requestAnimationFrame(loop); };
  const start = () => { if (running || reduce) return; running = true; frame = requestAnimationFrame(loop); };
  const stop = () => { running = false; cancelAnimationFrame(frame); };

  resize();
  new ResizeObserver(() => { resize(); draw(performance.now()); }).observe(canvas);
  if (reduce) { draw(1200); return; }
  new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop())).observe(canvas);
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
})();

// Paragraphs longer than six lines are past what text-wrap: balance handles, so [data-balance]
// ones are evened out here: the box narrows until one step more would add a line, which leaves
// every line, the last one included, about the same length.
const balanceLong = () => document.querySelectorAll("[data-balance]").forEach((el) => {
  el.style.maxWidth = "";
  const lineHeight = parseFloat(getComputedStyle(el).lineHeight);
  const lines = () => Math.round(el.getBoundingClientRect().height / lineHeight);
  const target = lines();
  let lo = 0, hi = el.getBoundingClientRect().width;
  while (hi - lo > 1) {
    const mid = (lo + hi) / 2;
    el.style.maxWidth = `${mid}px`;
    if (lines() > target) lo = mid; else hi = mid;
  }
  el.style.maxWidth = `${Math.ceil(hi)}px`;
});
let balanceTimer = 0;
document.fonts.ready.then(balanceLong);
window.addEventListener("resize", () => { clearTimeout(balanceTimer); balanceTimer = setTimeout(balanceLong, 100); });
