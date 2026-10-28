// Application and contact address. Replace with the real inbox before launch.
const CONTACT_EMAIL = "careers@ogbon.com";

// Mailto links: every [data-apply] gets a role-specific subject, [data-email] a plain one.
document.querySelectorAll("[data-apply]").forEach((a) => {
  const role = a.dataset.apply;
  const subject = role ? `Application: ${role}` : "Joining Ogbon";
  a.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}`;
});
document.querySelectorAll("[data-email]").forEach((a) => {
  a.href = `mailto:${CONTACT_EMAIL}`;
  a.textContent = CONTACT_EMAIL;
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

// 1,000 cores, lit in a diagonal sweep.
const cores = document.getElementById("cores");
const frag = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const cell = document.createElement("i");
  const x = i % 40, y = Math.floor(i / 40);
  cell.style.setProperty("--d", `${(x + y) * 28}ms`);
  frag.appendChild(cell);
}
cores.appendChild(frag);

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

// Entrance reveals, and only animate the core grid while it is on screen.
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.target === cores) { cores.classList.toggle("on", e.isIntersecting); return; }
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  });
}, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

document.querySelectorAll(".reveal").forEach((el, i) => {
  // Stagger siblings that enter together.
  el.style.transitionDelay = `${Math.min(i % 4, 3) * 70}ms`;
  io.observe(el);
});
io.observe(cores);

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
