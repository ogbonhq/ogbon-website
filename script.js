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
      const res = await fetch(reportForm.action, { method: "POST", body: new FormData(reportForm), headers: { Accept: "application/json" } });
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

// Amounts are set in US dollars ([data-usd]) and shown in the visitor's own currency: pounds in the UK,
// naira in Nigeria, US dollars everywhere else.
const RATES = { USD: { sign: "$", rate: 1 }, GBP: { sign: "£", rate: 0.8 }, NGN: { sign: "₦", rate: 1500 } };
const short = (v) => {
  for (const [div, suf] of [[1e9, "bn"], [1e6, "m"], [1e3, "k"]]) {
    if (v >= div) return `${+(v / div).toFixed(2)}${suf}`;
  }
  return String(v);
};
const showCurrency = (cur) => {
  const { sign, rate } = RATES[cur] || RATES.USD;
  document.querySelectorAll(".money[data-usd]").forEach((el) => {
    // Naira amounts are set on their own (Nigerian plans have their own limits); pounds are converted.
    const v = cur === "NGN" && el.dataset.ngn ? Number(el.dataset.ngn) : Number(el.dataset.usd) * rate;
    el.textContent = sign + (el.dataset.fmt === "full" ? Math.round(v).toLocaleString("en-GB") : short(v));
  });
};
const store = {
  get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k, v) => { try { localStorage.setItem(k, v); } catch {} },
};
// Until Cloudflare's country lookup answers (or where it isn't available, as on a local preview), the device's
// time zone is the guess: the inline script in <head> uses it too.
let timeZone = "";
try { timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch {}
const TZ_COUNTRY = { "Africa/Lagos": "NG", "Europe/London": "GB" };
const pickCurrency = () => {
  const country = store.get("ogbon-country") || TZ_COUNTRY[timeZone] || "";
  return { NG: "NGN", GB: "GBP" }[country] || "USD";
};
showCurrency(pickCurrency());

// Region: visitors in Africa see Casava, naira and African regulators; everyone else sees the US/UK version.
// The country comes from Cloudflare (/cdn-cgi/trace on ogbon.com), checked once per visit and remembered, so the
// inline script in <head> can set it before the next page paints; before that, and wherever the lookup fails, the
// device's time zone decides. ?region=africa or ?region=global forces one.
const AFRICA = new Set("DZ AO BJ BW BF BI CV CM CF TD KM CG CD CI DJ EG GQ ER SZ ET GA GM GH GN GW KE LS LR LY MG MW ML MR MU YT MA MZ NA NE NG RE RW SH ST SN SC SL SO ZA SS SD TZ TG TN UG EH ZM ZW".split(" "));
// Select options can't be hidden with CSS in every browser, so Africa-only options are switched here.
const showRegionOptions = () => {
  const africa = document.documentElement.dataset.region === "africa";
  document.querySelectorAll("option.r-africa").forEach((o) => { o.hidden = !africa; o.disabled = !africa; });
};
showRegionOptions();
const setRegion = (r) => {
  document.documentElement.dataset.region = r;
  store.set("ogbon-region", r);
  showCurrency(pickCurrency());
  showRegionOptions();
};
const forced = new URLSearchParams(location.search).get("region");
if (forced === "africa" || forced === "global") {
  setRegion(forced);
} else {
  let checked = false;
  try { checked = sessionStorage.getItem("ogbon-geo") === "1"; } catch {}
  if (!checked) {
    fetch("/cdn-cgi/trace", { cache: "no-store" })
      .then((res) => (res.ok ? res.text() : ""))
      .then((text) => {
        const cc = (text.match(/^loc=([A-Z]{2})$/m) || [])[1];
        if (!cc) return;
        try { sessionStorage.setItem("ogbon-geo", "1"); } catch {}
        store.set("ogbon-country", cc);
        setRegion(AFRICA.has(cc) ? "africa" : "global");
      })
      .catch(() => {});
  }
}
