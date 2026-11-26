const CONTACT_EMAIL = "secure@ogbon.com";

// Mailto links: [data-email="Subject"] gets that subject; a bare [data-email] shows the address.
document.querySelectorAll("[data-email]").forEach((a) => {
  const subject = a.dataset.email;
  a.href = `mailto:${CONTACT_EMAIL}${subject ? `?subject=${encodeURIComponent(subject)}` : ""}`;
  if (!subject) a.textContent = CONTACT_EMAIL;
});

// The bar gets a hairline once the page scrolls.
const nav = document.getElementById("nav");
const setNav = () => nav.classList.toggle("is-scrolled", window.scrollY > 8);
setNav();
window.addEventListener("scroll", setNav, { passive: true });

// Small screens: the nav links move into a panel behind the menu button.
const menuBtn = nav.querySelector(".nav-menu");
const panel = document.createElement("div");
panel.className = "nav-panel";
panel.id = "nav-panel";
panel.hidden = true;
const links = [...nav.querySelectorAll(".nav-links a, .nav-login")];
panel.innerHTML = `<ul>${links.map((a) => `<li>${a.outerHTML.replace(/ aria-current="page"/, "")}</li>`).join("")}</ul>`;
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
window.matchMedia("(min-width: 961px)").addEventListener("change", (e) => { if (e.matches) setMenu(false); });

// The domain typed into a "Start with a free security report" box carries over to the report form.
const domainField = document.querySelector("#report-form [name=domain]");
const domain = new URLSearchParams(location.search).get("domain");
if (domainField && domain) domainField.value = domain.trim().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
