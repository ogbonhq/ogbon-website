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
const links = [...nav.querySelectorAll(".nav-links a")];
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

// The report form sends to Formspree in the background and shows a thank-you in place of the form.
const reportForm = document.getElementById("report-form");
if (reportForm) {
  const error = reportForm.querySelector(".form-error");
  const button = reportForm.querySelector("button[type=submit]");
  reportForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    error.hidden = true;
    button.disabled = true;
    button.textContent = "Sending...";
    try {
      // Headline A/B test: record which homepage headline this browser saw (A, B, or none if it never saw the homepage).
      const body = new FormData(reportForm);
      let hv = null;
      try { hv = localStorage.getItem("ogbon_hv"); } catch {}
      body.append("headline", hv === "a" || hv === "b" ? hv.toUpperCase() : "none");
      const res = await fetch(reportForm.action, { method: "POST", body, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error(String(res.status));
      const email = reportForm.querySelector("[name=email]").value;
      const done = document.createElement("div");
      done.className = "form-card form-done";
      done.setAttribute("role", "status");
      done.tabIndex = -1;
      done.innerHTML = "<h2>Thanks, we've got your request</h2><p></p>";
      done.querySelector("p").textContent = `We'll email your report to ${email}. If you have questions, write to ${CONTACT_EMAIL}.`;
      reportForm.replaceWith(done);
      done.focus();
    } catch {
      error.hidden = false;
      button.disabled = false;
      button.textContent = "Get my report";
    }
  });
}

// Products dropdown: opens on hover or focus, and on click for touch screens and keyboards.
const dd = document.querySelector(".nav-dd");
if (dd) {
  const btn = dd.querySelector(".nav-dd-btn");
  const setDd = (open) => { dd.classList.toggle("is-open", open); btn.setAttribute("aria-expanded", String(open)); };
  btn.addEventListener("click", () => setDd(!dd.classList.contains("is-open")));
  document.addEventListener("click", (e) => { if (!dd.contains(e.target)) setDd(false); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && dd.classList.contains("is-open")) { setDd(false); btn.focus(); } });
}
