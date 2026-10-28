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
  nav.classList.toggle("is-dark", window.scrollY > hero.offsetHeight - 56);
};
setNav();
window.addEventListener("scroll", setNav, { passive: true });

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
    const a1 = -1.95 + 0.38 * Math.sin(t * 0.9);
    const a2 = 1.35 + 0.55 * Math.sin(t * 0.9 + 1.1);
    const x1 = 50 + 34 * Math.cos(a1), y1 = 72 + 34 * Math.sin(a1);
    const x2 = x1 + 28 * Math.cos(a1 + a2), y2 = y1 + 28 * Math.sin(a1 + a2);
    limb(c, 50, 72, x1, y1, 8); limb(c, x1, y1, x2, y2, 6);
    disc(c, 50, 72, 7); disc(c, x1, y1, 5.5);
    const g = a1 + a2, open = 2.6 + 1.6 * Math.sin(t * 1.8);
    for (const s of [-1, 1]) {
      const px = -Math.sin(g) * open * s, py = Math.cos(g) * open * s;
      limb(c, x2 + px, y2 + py, x2 + px + 7 * Math.cos(g), y2 + py + 7 * Math.sin(g), 2.6);
    }
    return [x2, y2];
  };

  const drone = (c, t) => {
    const y = 46 + 3.5 * Math.sin(t * 1.6), tilt = 0.06 * Math.sin(t * 0.8);
    c.save(); c.translate(50, y); c.rotate(tilt);
    for (const [hx, hy] of [[-27, -8], [27, -8], [-20, 2], [20, 2]]) {
      limb(c, 0, 0, hx, hy, 3.4);
      c.fillRect(hx - 1.5, hy - 5, 3, 5);
      const w = 4 + 11 * Math.abs(Math.cos(t * 9 + hx));
      c.fillRect(hx - w, hy - 6.5, w * 2, 2);
    }
    c.beginPath(); c.roundRect(-11, -6, 22, 12, 4); c.fill();
    limb(c, -8, 6, -12, 14, 2.4); limb(c, 8, 6, 12, 14, 2.4);
    c.fillRect(-15, 13.5, 8, 2); c.fillRect(7, 13.5, 8, 2);
    c.restore();
    c.globalAlpha = 0.35; c.beginPath(); c.ellipse(50, 90, 20 - 2 * Math.sin(t * 1.6), 2.4, 0, 0, Math.PI * 2); c.fill(); c.globalAlpha = 1;
    return [50, y];
  };

  const rover = (c, t) => {
    const bob = 0.8 * Math.sin(t * 6);
    c.beginPath(); c.roundRect(20, 56 + bob, 60, 18, 3); c.fill();
    c.fillRect(56, 34 + bob, 4, 22);
    c.beginPath(); c.roundRect(51, 27 + bob, 14, 9, 2); c.fill();
    // Sensor sweep: a faint fan from the mast head.
    const s = 0.5 * Math.sin(t * 1.4);
    c.globalAlpha = 0.28;
    c.beginPath(); c.moveTo(65, 31 + bob);
    c.lineTo(98, 22 + bob + 30 * s); c.lineTo(98, 40 + bob + 30 * s); c.closePath(); c.fill();
    c.globalAlpha = 1;
    for (const wx of [30, 50, 70]) {
      disc(c, wx, 80, 8);
      c.save(); c.globalCompositeOperation = "destination-out"; disc(c, wx, 80, 3.4); c.restore();
      const a = t * 4;
      c.fillRect(wx + 5 * Math.cos(a) - 1, 80 + 5 * Math.sin(a) - 1, 2, 2);
    }
    c.fillRect(8, 88, 84, 2);
    return [58, 31 + bob];
  };

  const scenes = [arm, drone, rover];
  const HOLD = 5.2, FADE = 0.9;
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
    if (!reduce && t - lastSpawn > 0.22) {
      lastSpawn = t;
      packets.push({ born: t, sx: cols - 1 - Math.random() * 3, sy: Math.random() * 3 });
    }
    packets = packets.filter((p) => t - p.born < 1.6);
    ctx.fillStyle = GREEN;
    for (const p of packets) {
      const k = (t - p.born) / 1.6, e = k * k * (3 - 2 * k);
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
