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

// Hero: machines drawn as a dot matrix. Each scene is painted at grid resolution on a
// small offscreen canvas; every cell's coverage becomes a dot. Scenes dissolve into one
// another cell by cell, and green packets stream in from the top corner (the cloud).
(() => {
  const canvas = document.querySelector("[data-machines]");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const off = document.createElement("canvas");
  const octx = off.getContext("2d", { willReadFrequently: true });
  const INK = "20, 20, 19", GREEN = "#30D75D";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Scenes draw in a 100x100 box and return the point packets stream to.
  const limb = (c, x1, y1, x2, y2, w) => {
    c.lineWidth = w; c.lineCap = "round";
    c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke();
  };
  const disc = (c, x, y, r) => { c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill(); };

  const arm = (c, t) => {
    c.fillRect(26, 86, 48, 6);
    c.fillRect(40, 74, 20, 12);
    const a1 = -1.95 + 0.38 * Math.sin(t * 2.4);
    const a2 = 1.35 + 0.55 * Math.sin(t * 2.4 + 1.1);
    const x1 = 50 + 34 * Math.cos(a1), y1 = 72 + 34 * Math.sin(a1);
    const x2 = x1 + 28 * Math.cos(a1 + a2), y2 = y1 + 28 * Math.sin(a1 + a2);
    limb(c, 50, 72, x1, y1, 8); limb(c, x1, y1, x2, y2, 6);
    disc(c, 50, 72, 7); disc(c, x1, y1, 5.5);
    const g = a1 + a2, open = 2.6 + 1.6 * Math.sin(t * 4.8);
    for (const s of [-1, 1]) {
      const px = -Math.sin(g) * open * s, py = Math.cos(g) * open * s;
      limb(c, x2 + px, y2 + py, x2 + px + 7 * Math.cos(g), y2 + py + 7 * Math.sin(g), 2.6);
    }
    return [x2, y2];
  };

  // Edge security: a wall-mounted camera panning, with its field of view.
  const camera = (c, t) => {
    c.fillRect(14, 20, 6, 30);
    c.fillRect(14, 31, 18, 4);
    const pan = 0.22 * Math.sin(t * 1.8);
    c.save(); c.translate(32, 33); c.rotate(0.28 + pan);
    c.beginPath(); c.roundRect(0, -7, 34, 14, 3); c.fill();
    c.fillRect(30, -9, 8, 18);
    c.globalAlpha = 0.28;
    c.beginPath(); c.moveTo(38, 0); c.lineTo(80, -22); c.lineTo(80, 26); c.closePath(); c.fill();
    c.globalAlpha = 1;
    c.restore();
    c.fillRect(8, 88, 84, 2);
    // A figure walking through the frame.
    const x = 52 + 18 * Math.sin(t * 1.4);
    disc(c, x, 62, 3.6);
    limb(c, x, 66, x, 78, 4.4);
    limb(c, x, 78, x - 3 + 2 * Math.sin(t * 10), 88, 2.6); limb(c, x, 78, x + 3 - 2 * Math.sin(t * 10), 88, 2.6);
    const ex = 32 + 38 * Math.cos(0.28 + pan), ey = 33 + 38 * Math.sin(0.28 + pan);
    return [ex, ey];
  };

  // How far through its turn on screen a scene is (0 to 1), for things that build up.
  const progress = (t, span) => Math.min(1, (t % HOLD) / span);

  // Chat: a reply streaming into a speech bubble, one token run at a time.
  const chat = (c, t) => {
    c.lineWidth = 4;
    c.beginPath(); c.roundRect(12, 20, 76, 50, 9); c.stroke();
    c.beginPath(); c.moveTo(24, 68); c.lineTo(19, 82); c.lineTo(38, 69); c.fill();
    let left = progress(t, 0.6) * 158;
    [56, 62, 40].forEach((w, i) => {
      const d = Math.max(0, Math.min(w, left)); left -= w;
      if (d > 0) c.fillRect(22, 32 + i * 11, d, 5);
    });
    return [88, 20];
  };

  // Coding: an editor typing indented lines, with a blinking cursor.
  const code = (c, t) => {
    c.lineWidth = 3.5;
    c.beginPath(); c.roundRect(10, 16, 80, 68, 5); c.stroke();
    c.fillRect(10, 16, 80, 9);
    const rows = [[18, 30], [24, 36], [24, 22], [30, 28], [24, 18], [18, 10]];
    let left = progress(t, 0.8) * rows.reduce((s, [, w]) => s + w, 0), cursor = [18, 32];
    rows.forEach(([x, w], i) => {
      const d = Math.max(0, Math.min(w, left)); left -= w;
      if (d > 0) { c.fillRect(x, 32 + i * 8, d, 4); cursor = [x + d + 2, 32 + i * 8]; }
    });
    if (Math.floor(t * 2.5) % 2) c.fillRect(cursor[0], cursor[1] - 1, 3, 6);
    return cursor;
  };

  // Voice: a waveform answering as it speaks.
  const voice = (c, t) => {
    for (let i = 0; i < 11; i++) {
      const env = Math.sin(Math.PI * (i + 0.5) / 11);
      const h = 6 + 46 * env * Math.abs(Math.sin(t * 9 + i * 0.7));
      c.fillRect(16 + i * 6.4, 50 - h / 2, 4, h);
    }
    return [50, 22];
  };

  // Agents: a plan of steps, each finishing in turn.
  const agents = (c, t) => {
    const nodes = [[20, 30], [50, 20], [80, 38], [62, 70], [28, 74]];
    const active = Math.min(nodes.length - 1, Math.floor(progress(t, 1) * nodes.length));
    nodes.forEach(([x, y], i) => {
      if (i < nodes.length - 1) {
        c.globalAlpha = i < active ? 1 : 0.4;
        limb(c, x, y, nodes[i + 1][0], nodes[i + 1][1], 2.6);
        c.globalAlpha = 1;
      }
      if (i <= active) disc(c, x, y, 7);
      else { c.lineWidth = 2.6; c.beginPath(); c.arc(x, y, 6, 0, Math.PI * 2); c.stroke(); }
    });
    return nodes[active];
  };

  // One scene per vertical on the homepage: chat, coding, voice, agents, vision, physical AI.
  const scenes = [chat, code, voice, agents, camera, arm];
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
    // Packets: from the top-right corner to the machine, snapped to the grid.
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
