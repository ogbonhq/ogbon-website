"""Writes the site's HTML pages from one place, so the head, nav and footer stay the same on
every page. Run from the repo root: python3 tools/pages.py
Placeholders the team still has to fill in are written as [like this] and shown highlighted."""
import html
import json
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import legal  # noqa: E402
CSS_V = "20261128-6"
JS_V = "20261128-5"
OG_V = "9"
SITE = "https://ogbon.com"
TAGLINE = "Cyber cover with security built in."

LOGO = (ROOT / "tools/partials/logo.svg").read_text().strip()
SOCIAL = (ROOT / "tools/partials/social.html").read_text().strip()


def art(name, size=""):
    """A line illustration for a card, from tools/partials/art."""
    cls = "card-art" + (f" card-art-{size}" if size else "")
    return f'<div class="{cls}">' + (ROOT / f"tools/partials/art/{name}.svg").read_text().strip() + "</div>"


def tbd(text):
    """Highlights every [placeholder] in a string of HTML."""
    return re.sub(r"\[([^\]]+)\]", r'<mark class="tbd">[\1]</mark>', text)


def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="/assets/icons.svg?v={CSS_V}#{name}"/></svg>'


def region(africa, other):
    """Text that differs by visitor region: Africa sees the first, everyone else the second.
    The <html data-region> attribute (set from the visitor's country, see script.js) picks one with CSS."""
    return f'<span class="r-africa">{africa}</span><span class="r-global">{other}</span>'


def short_usd(v):
    for div, suf in ((1e9, "bn"), (1e6, "m"), (1e3, "k")):
        if v >= div:
            return f"${v / div:g}{suf}"
    return f"${v:g}"


def money(usd, full=False, ngn=None):
    """An amount set in US dollars. script.js shows it in the visitor's own currency (GBP in the UK, NGN in
    Nigeria). Naira amounts are set separately (ngn), not converted: Nigerian plans keep their own limits."""
    text = f"${usd:,.0f}" if full else short_usd(usd)
    fmt = ' data-fmt="full"' if full else ""
    naira = f' data-ngn="{ngn:g}"' if ngn else ""
    return f'<span class="money" data-usd="{usd:g}"{naira}{fmt}>{text}</span>'


# Links are absolute so the 404 page works at any depth.
NAV = [
    ("/how-it-works", "How it works"),
    ("products", "Products"),
    ("/ogbon-1", "Security LLM"),
    ("/pricing", "Pricing"),
    ("/about", "About"),
]
PRODUCTS = [
    ("/pentesting", "Penetration testing", "AI pentests, every finding proven"),
    ("/pentesting#attack-surface", "Attack surface management", "Find every system you expose"),
    ("/pentesting#active-offense", "Active offense", "Testing that never stops"),
    ("/cover", "Cover", "We pay if an attack gets through"),
]
FOOTER = [
    ("Product", [("/pentesting", "Penetration testing"), ("/ogbon-1", "Security LLM"), ("/cover", "Cover"), ("/how-it-works", "How it works"), ("/pricing", "Pricing")]),
    ("Company", [("/about", "About"), ("/report", "Free security report"), ("/incident", "Under attack?")]),
    ("Legal", [("/cover-terms", "Cover terms"), ("/privacy", "Privacy"), ("/terms", "Terms")]),
]
LEGAL_AFRICA = (
    "Ogbon is not an insurer, and the cover in Ogbon plans is not an insurance policy. It is a warranty from "
    "Ogbon Security Limited. For customers in Africa, the warranty is backed by Casava, an insurer licensed by the "
    "National Insurance Commission (NAICOM) in Nigeria. Terms, limits and exclusions apply."
)
LEGAL_GLOBAL = (
    "Ogbon is not an insurer, and the cover in Ogbon plans is not an insurance policy. It is a warranty from "
    "Ogbon Security Limited. In the US and UK, it will be backed by insurers licensed in those countries. "
    "Terms, limits and exclusions apply."
)
BACKED = ('<p class="backed{cls} r-africa">Cover in Africa backed by <a href="https://casava.com/" target="_blank" rel="noopener" '
          'aria-label="Casava (opens in a new tab)"><img src="/assets/partners/casava.png" alt="Casava" width="112" height="27"></a></p>')


def nav(current):
    here = "/" + current.removesuffix(".html")

    def link(href, label):
        cur = ' aria-current="page"' if href == here else ""
        return f'          <a href="{href}"{cur}>{label}</a>'

    def products():
        items = "\n".join(
            f'            <a href="{h}"{" aria-current=\"page\"" if h == here else ""}><b>{l}</b><span>{d}</span></a>'
            for h, l, d in PRODUCTS
        )
        active = " is-current" if here in {h for h, _, _ in PRODUCTS} else ""
        return f"""          <div class="nav-dd{active}">
            <button class="nav-dd-btn" type="button" aria-expanded="false" aria-controls="nav-products">Products<svg aria-hidden="true" viewBox="0 0 12 12" width="12" height="12"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
            <div class="nav-dd-menu" id="nav-products">
{items}
            </div>
          </div>"""

    links = "\n".join(products() if href == "products" else link(href, label) for href, label in NAV)
    inc = ' aria-current="page"' if current == "incident.html" else ""
    return f"""  <header class="nav" id="nav">
    <div class="nav-inner">
      <a class="nav-logo" href="/" aria-label="Ogbon home">{LOGO}</a>
      <nav class="nav-links" aria-label="Primary">
{links}
          <a class="nav-incident" href="/incident"{inc}><svg class="nav-incident-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M12 2.5 20.5 7.25v9.5L12 21.5 3.5 16.75v-9.5Z"/><path d="M12 7.5v5.5"/><circle cx="12" cy="16.5" r="1" fill="currentColor" stroke="none"/></svg>Under attack?</a>
      </nav>
      <div class="nav-actions">
        <a class="btn btn-primary btn-sm" data-email="Book a demo" href="#contact">Get a demo</a>
        <button class="nav-menu" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="Menu"><span></span><span></span></button>
      </div>
    </div>
  </header>"""


def footer():
    cols = "\n".join(
        f"""        <nav class="footer-col" aria-label="{t}">
          <h2>{t}</h2>
          <ul>
{chr(10).join(f'            <li><a href="{h}">{l}</a></li>' for h, l in items)}
          </ul>
        </nav>"""
        for t, items in FOOTER
    )
    return f"""  <footer class="footer">
    <div class="wrap">
      <div class="footer-top">
        <div class="footer-brand">
          <p>{TAGLINE}</p>
          <p class="footer-contact"><a href="mailto:secure@ogbon.com">secure@ogbon.com</a><span class="r-africa"><br><a href="tel:+2347107144122">+234 710 714 4122</a></span></p>
          {SOCIAL}
        </div>
{cols}
      </div>
      <a class="footer-mark" href="/" aria-label="Ogbon home">{LOGO}</a>
      <div class="footer-legal">
        <p class="r-africa">{LEGAL_AFRICA}</p>
        <p class="r-global">{LEGAL_GLOBAL}</p>
        <p>© 2026 Ogbon Security Limited.</p>
      </div>
    </div>
  </footer>"""


def page(slug, title, desc, body, robots="index, follow", ld=""):
    url = SITE + ("/" if slug == "index.html" else "/" + slug.removesuffix(".html"))
    t = html.escape(title, quote=True)
    d = html.escape(desc, quote=True)
    current = slug
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Google Tag Manager -->
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-KXWLL6LV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    dataLayer.push({{'gtm.start': new Date().getTime(), event: 'gtm.js'}});
  </script>
  <script>
    try {{ var rg = new URLSearchParams(location.search).get("region") || localStorage.getItem("ogbon-region"); if (rg !== "africa" && rg !== "global") rg = (Intl.DateTimeFormat().resolvedOptions().timeZone || "").indexOf("Africa/") === 0 ? "africa" : "global"; document.documentElement.dataset.region = rg; }} catch (e) {{}}
  </script>
  <title>{t}</title>
  <meta name="description" content="{d}">
  <meta name="robots" content="{robots}">
  <meta name="google-site-verification" content="TMQezal_UH2JRRQMls634qto7pwaackCmYipcE6Nakg">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#FFFFFF">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Ogbon">
  <meta property="og:locale" content="en_GB">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:image" content="{SITE}/assets/og.png?v={OG_V}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="The Ogbon logo">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@ogbonhq">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{SITE}/assets/og.png?v={OG_V}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Manrope:wght@500;600&display=swap">
  <link rel="stylesheet" href="/styles.css?v={CSS_V}">{ld}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
{nav(current)}

  <main id="main">
{body.rstrip()}
  </main>

{footer()}

  <script src="/script.js?v={JS_V}" defer></script>
</body>
</html>
"""


def cta(head="Start with a free security report",
        text="Enter your company domain and we'll show what an attacker can see from the outside, your biggest risks, and what they could cost you."):
    return f"""
    <div class="frame">
      <section class="cta" aria-labelledby="cta-title">
        <h2 class="h2" id="cta-title">{head}</h2>
        <p>{text}</p>
        <form class="cta-form" action="/report" method="get">
          <label class="sr-only" for="cta-domain">Company domain</label>
          <input id="cta-domain" name="domain" type="text" inputmode="url" autocomplete="url" placeholder="yourcompany.com" required>
          <button class="btn btn-light" type="submit">Get my report</button>
        </form>
      </section>
    </div>"""


# ---------------------------------------------------------------- Home
FAQ = [
    ("Is Ogbon an insurance company?",
     "No. Ogbon is a cybersecurity company. The cover in every plan is a warranty from Ogbon: if an attack gets through while you're protected, we pay for the loss, up to your plan's limit. We manage your claim with you from start to finish."),
    ("Is the cover an insurance policy?",
     ("No. It's a warranty from Ogbon, backed by Casava, an insurer licensed by NAICOM in Nigeria. You'll get the full warranty terms before you sign.",
      "No. It's a warranty from Ogbon. In the US and UK it will be backed by insurers licensed in each country. You'll get the full warranty terms before you sign.")),
    ("Which countries does Ogbon work in?",
     ("The US, the UK and across Africa. Security work, ogbon-1 and incident response are the same everywhere. Cover for customers in Africa is backed by Casava.",
      "The US and the UK. Security work, ogbon-1 and incident response start straight away. Cover will be backed by insurers licensed in each country. Contact sales for start dates.")),
    ("Do you install anything on our laptops?",
     "Only if you turn on endpoint protection for laptops and servers. Everything else connects read-only to your websites, apps, APIs, cloud and internal systems."),
    ("What data can Ogbon see?",
     "Configuration and access settings from the cloud accounts and systems you connect, and the code repositories you choose. We don't read emails, chats or documents. Access is read-only and you can disconnect at any time."),
    ("How long does setup take?",
     "About an hour of your IT team's time. Most companies are covered within a week."),
    ("What is ogbon-1?",
     "ogbon-1 is Ogbon's own 30B security model. It finds and fixes security problems across your code, cloud and systems. Your engineering and IT teams use it through Ogbon Harness or the Ogbon API, and it's included in every plan."),
    ("Can we keep our code on our own servers?",
     "Yes. ogbon-1 runs on a single GPU, so you can host it yourself and your code never leaves your network. We never use customer code to train our models."),
    ("Do you cover money stolen through hacked accounts or leaked API keys?",
     "Yes, up to your plan's limit, on every plan."),
    ("What if we can't fix something in time?",
     "Tell us before the due date and we'll agree a new date or another fix. Your cover is only affected if a critical issue is left open past its due date without telling us."),
    ("Which currencies do you work in?",
     ("US dollars, pounds sterling and naira. Your plan, cover limits and reports are set in the currency you choose.",
      "US dollars and pounds sterling. Your plan, cover limits and reports are set in the currency you choose.")),
    ("How quickly are claims paid?",
     "Small, clear claims are paid the same day: incident response costs, and confirmed losses up to [$10,000]. For larger claims we decide within 15 working days of getting all documents, and pay within 5 working days of approval. People decide every claim, and a person explains any refusal in writing."),
    ("What is the security giveback?",
     "If the part of your price that pays for cover isn't used for claims during the year, we give [20%] of it back as extra pentests, fixes or a discount at renewal. We earn more when you stay safe, so we have no reason to refuse a fair claim."),
    ("Does Ogbon help with compliance?",
     ("Yes. Growth and Scale plans include audit evidence mapped to SOC 2, ISO 27001, PCI DSS, GDPR and UK GDPR, the Nigeria Data Protection Act and the CBN risk-based cybersecurity framework.",
      "Yes. Growth and Scale plans include audit evidence mapped to SOC 2, ISO 27001, PCI DSS, GDPR and UK GDPR.")),
    ("Can we cancel?",
     "Yes, at the end of any billing period. We don't refund cover you haven't used."),
]

faq_html = "\n".join(
    f"""          <details>
            <summary>{q}{icon("plus")}</summary>
            <p>{region(tbd(a[0]), tbd(a[1])) if isinstance(a, tuple) else tbd(a)}</p>
          </details>""" for q, a in FAQ
)
# Search engines get the version for everyone outside Africa.
faq_ld = ",\n".join(
    "          " + json.dumps({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}, ensure_ascii=False)
    for q, a in ((q, a[1] if isinstance(a, tuple) else a) for q, a in FAQ) if "[" not in a
)

home = f"""    <div class="frame">
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero-main">
          <h1 id="hero-title">Cyber cover with <span>security&nbsp;built&nbsp;in</span></h1>
          <p class="hero-sub">If an attacker gets through, we pay for the loss. To stop that happening, we check your websites, apps, APIs and cloud <br class="br-wide">every day and show your team what&nbsp;to&nbsp;fix.</p>
          <div class="hero-actions">
            <a class="btn btn-light" href="/report">Get free security report</a>
            <a class="btn btn-ghost-light" data-email="Sales" href="#contact">Contact sales</a>
          </div>
          {BACKED.format(cls=" backed-pill")}
        </div>
        <div class="hero-side">
          <figure class="dash" aria-label="Example Ogbon dashboard">
            <div class="dash-top"><span class="dash-domain">yourcompany.com</span><span class="status status-ok">Cover active</span></div>
            <div class="dash-stats">
              <div class="dash-stat"><p>Security score</p><b>72 / 100</b></div>
              <div class="dash-stat"><p>Covered up to</p><b>{money(1_000_000, ngn=75_000_000)}</b></div>
            </div>
            <div class="dash-list">
              <p>Today's checks</p>
              <ul>
                <li><span>Website<small>Admin page open to the internet</small></span><span class="status status-warn">Fix</span></li>
                <li><span>App<small>Access check missing on 1 endpoint</small></span><span class="status status-bad">Critical</span></li>
                <li><span>API<small>Partner API returns full account records</small></span><span class="status status-warn">Fix</span></li>
                <li><span>Cloud<small>3 accounts checked</small></span><span class="status status-ok">OK</span></li>
                <li><span>Code<small>12 repositories checked</small></span><span class="status status-ok">OK</span></li>
              </ul>
            </div>
          </figure>
        </div>
      </section>
    </div>

    <!-- Customer logos: add once there are customers who agree to be named.
         Line above the logos: "Used by digital businesses" -->

    <section class="section" aria-labelledby="attacks-title">
      <div class="wrap">
        <div class="head">
          <h2 class="h2" id="attacks-title">Most attacks start with <span>something&nbsp;small</span></h2>
          <p class="lead lead-split"><strong>Attackers start with your website and app.</strong> They look for one place that trusts them too much, then use it to reach customer data, money or the systems your business runs&nbsp;on.</p>
        </div>
        <ul class="cards cards-4" aria-label="Common ways in">
          <li class="card card-illus">{art("apis", "sm")}<h3>APIs and integrations</h3><p>Public APIs and partner connections that expose more data or actions than they should.</p></li>
          <li class="card card-illus">{art("logic", "sm")}<h3>Business logic</h3><p>Flaws in how your product handles money, limits and approvals. Scanners don't find these.</p></li>
          <li class="card card-illus">{art("identity", "sm")}<h3>Identity and access</h3><p>Staff, service accounts and cloud roles with more access than they need.</p></li>
          <li class="card card-illus">{art("forgotten", "sm")}<h3>Forgotten systems</h3><p>Old apps, test servers and subdomains your team no longer tracks.</p></li>
        </ul>
      </div>
    </section>

    <section class="section section-tight" id="product" aria-labelledby="product-title">
      <div class="wrap">
        <div class="head">
          <h2 class="h2" id="product-title">Everything you need to protect your organisation, <span class="nowrap">from website to code</span></h2>
        </div>
        <div class="cards">
          <article class="card card-illus">{art("checks")}<h3>Daily checks</h3><p>Ogbon checks your websites, apps, APIs, cloud accounts and internal systems every day, from the outside like an attacker and from the inside with read-only&nbsp;access.</p></article>
          <article class="card card-illus">{art("score")}<h3>Security score</h3><p>One score for your whole organisation, updated every day. It goes up as your team fixes issues, and organisations that fix more pay less at&nbsp;renewal.</p></article>
          <article class="card card-illus">{art("fixlist")}<h3>Fix list</h3><p>We rank what needs fixing by how much money it puts at risk, and give your team clear steps for each&nbsp;item.</p></article>
          <article class="card card-illus">{art("response")}<h3>Incident response</h3><p>Report a problem {region("on WhatsApp", "by email")} or from your dashboard at any time. A responder calls you back within an&nbsp;hour.</p></article>
          <article class="card card-illus">{art("cover")}<h3>Cover</h3><p>If an attack gets through while you're protected, we pay for the money lost, the investigation and the cost of getting back to&nbsp;work.</p></article>
          <article class="card card-illus">{art("model")}<h3>ogbon-1 security model</h3><p>Your engineering and IT teams get ogbon-1, our 30B security model. It finds and fixes gaps across your laptops, code, cloud and&nbsp;systems.</p><a class="link" href="/ogbon-1">About ogbon-1 {icon("arrow")}</a></article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="naira-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="naira-title">See your risk <span>as a&nbsp;cost</span></h2>
          <p class="lead">Every finding comes with an amount in {region("dollars, pounds or naira", "dollars or pounds")}: what it could cost you this year, and how much fixing it&nbsp;saves.</p>
          <a class="btn btn-primary" href="/report">Get your free report</a>
        </div>
        <div class="panel">
          <figure class="loss" aria-label="Example from an Ogbon report">
            <p class="loss-label">Expected loss this year</p>
            <p class="loss-num">{money(120_000, True, 48_000_000)}</p>
            <div class="loss-fix">
              <span class="badge">{icon("lock")}</span>
              <div>
                <p>Turn on two-step login for cloud and admin accounts</p>
                <span class="loss-save">Reduces expected loss by {money(45_000, True, 19_000_000)}</span>
              </div>
            </div>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="covered-title">
      <div class="wrap split">
        <div class="panel panel-pink">
          <ul class="flow" aria-label="How cover works">
            <li><span class="badge">{icon("monitor")}</span><span>Daily checks<small>Websites, apps, APIs, cloud and internal systems</small></span></li>
            <li><span class="badge badge-blue">{icon("code")}</span><span>Every change reviewed<small>ogbon-1 on each pull request</small></span></li>
            <li><span class="badge badge-pink">{icon("phone")}</span><span>Responder on the line<small>Within an hour of your report</small></span></li>
            <li><span class="badge badge-lilac">{icon("money")}</span><span>Loss paid<small>Small, clear claims the same day</small></span></li>
          </ul>
        </div>
        <div>
          <h2 class="h2" id="covered-title">What the cover <span>pays&nbsp;for</span></h2>
          <ul class="checks">
            <li><span class="tick">{icon("check")}</span>Money stolen after attackers take over your accounts, systems or API keys</li>
            <li><span class="tick">{icon("check")}</span>Ransomware investigation and recovery</li>
            <li><span class="tick">{icon("check")}</span>Data breach response, including notifying customers and data protection regulators</li>
            <li><span class="tick">{icon("check")}</span>Income lost while your systems are down</li>
            <li><span class="tick">{icon("check")}</span>Incident responders from the first call</li>
          </ul>
          <a class="link" href="/cover">See what's covered {icon("arrow")}</a>
          {BACKED.format(cls="")}
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="who-title">
      <div class="wrap">
        <div class="cards">
          <article class="card">
            <span class="badge badge-lilac">{icon("money")}</span>
            <h2 class="h2" id="who-title" style="margin-top:18px">Built for businesses that run online</h2>
            <p class="lead">Ogbon is for any business that would lose money if its website, app or systems were attacked: software companies, online shops, marketplaces, fintechs, and healthcare and logistics companies, in {region("the US, the UK and across&nbsp;Africa", "the US and the&nbsp;UK")}.</p>
            <ul class="tags" aria-label="Who uses Ogbon">
              <li>Software and SaaS</li><li>E-commerce</li><li>Marketplaces</li><li>Fintech</li><li>Healthcare</li><li>Logistics</li>
            </ul>
          </article>
          <article class="card">
            <span class="badge badge-pink">{icon("shield")}</span>
            <h2 class="h2" style="margin-top:18px">Priced on how secure you are</h2>
            <p class="lead">Insurers usually price cyber cover from a yearly questionnaire. We check your systems every day, so your price reflects how you're really set up. Fix more, and you pay less at renewal. If you don't claim, part of your cover money comes back as security&nbsp;work.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="audit-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="audit-title">Ready for SOC 2, ISO 27001 and <span>GDPR&nbsp;audits</span></h2>
          <p class="lead">Download evidence mapped to the frameworks your customers, auditors and regulators ask for, whenever they ask for&nbsp;it.</p>
        </div>
        <div class="panel">
          <ul class="flow" aria-label="Audit evidence">
            <li><span class="badge">{icon("file")}</span><span>SOC 2 and ISO 27001<small>Evidence pack, ready to download</small></span></li>
            <li><span class="badge badge-pink">{icon("file")}</span><span>{region("GDPR, UK GDPR and the Nigeria Data Protection Act", "GDPR and UK GDPR")}<small>Evidence pack, ready to download</small></span></li>
            <li><span class="badge badge-lilac">{icon("file")}</span><span>{region("PCI DSS and the CBN cybersecurity framework", "PCI DSS")}<small>Evidence pack, ready to download</small></span></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section-tight" id="faq" aria-labelledby="faq-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="faq-title">Questions</h2></div>
        <div class="faq">
{faq_html}
        </div>
      </div>
    </section>
{cta()}
"""

home_ld = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebSite",
        "@id": "{SITE}/#website",
        "url": "{SITE}/",
        "name": "Ogbon",
        "inLanguage": "en",
        "publisher": {{ "@id": "{SITE}/#organization" }}
      }},
      {{
        "@type": "Organization",
        "@id": "{SITE}/#organization",
        "name": "Ogbon",
        "legalName": "Ogbon Security Limited",
        "url": "{SITE}/",
        "areaServed": ["US", "GB", "Africa"],
        "sameAs": ["https://x.com/ogbonhq", "https://www.linkedin.com/company/ogbonhq", "https://github.com/ogbonhq", "https://www.instagram.com/ogbonhq"],
        "contactPoint": {{ "@type": "ContactPoint", "contactType": "incident response", "email": "secure@ogbon.com", "areaServed": ["US", "GB", "Africa"], "availableLanguage": "en", "hoursAvailable": {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }} }},
        "logo": "{SITE}/assets/icons/icon-512.png",
        "slogan": "{TAGLINE}",
        "description": "Ogbon pays for the loss when a cyber attack gets through, and checks the systems of digital businesses every day to keep attackers out.",
        "email": "secure@ogbon.com",
        "address": {{ "@type": "PostalAddress", "streetAddress": "14B Grace Anjous Street, Lekki Phase 1", "addressLocality": "Lekki", "addressRegion": "Lagos State", "addressCountry": "NG" }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
{faq_ld}
        ]
      }}
    ]
  }}
  </script>"""

# ---------------------------------------------------------------- Free security report
report = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Free security <span>report</span></h1>
          <p>Find out what attackers can see about your company from the outside, and what it could cost you. It takes under 10 minutes and nothing gets&nbsp;installed.</p>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap report-grid">
        <form class="form form-card" id="report-form" action="https://formspree.io/f/mqpqjwzn" method="post">
          <input type="hidden" name="_subject" value="Free security report request">
          <div class="hp" aria-hidden="true"><label for="f-gotcha">Leave this empty</label><input id="f-gotcha" name="_gotcha" type="text" tabindex="-1" autocomplete="off"></div>
          <div class="field">
            <label for="f-domain">Company domain</label>
            <input id="f-domain" name="domain" type="text" inputmode="url" placeholder="yourcompany.com" required>
          </div>
          <div class="field">
            <label for="f-email">Work email</label>
            <input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@yourcompany.com" required>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="f-staff">Number of staff</label>
              <select id="f-staff" name="staff" required>
                <option value="" disabled selected>Choose</option>
                <option>Under 20</option>
                <option>20 to 50</option>
                <option>51 to 200</option>
                <option>201 to 500</option>
                <option>More than 500</option>
              </select>
            </div>
            <div class="field">
              <label for="f-industry">Industry</label>
              <select id="f-industry" name="industry" required>
                <option value="" disabled selected>Choose</option>
                <option>Software or SaaS</option>
                <option>E-commerce</option>
                <option>Marketplace</option>
                <option>Fintech</option>
                <option>Healthcare</option>
                <option>Logistics</option>
                <option>Media</option>
                <option>Other</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="f-country">Country</label>
            <select id="f-country" name="country" required>
              <option value="" disabled selected>Choose</option>
              <option>United States</option>
              <option>United Kingdom</option>
              <option class="r-africa">Nigeria</option>
              <option class="r-africa">Kenya</option>
              <option class="r-africa">South Africa</option>
              <option class="r-africa">Ghana</option>
              <option class="r-africa">Another country in Africa</option>
              <option>Somewhere else</option>
            </select>
          </div>
          <button class="btn btn-primary" type="submit">Get my report</button>
          <p class="form-error" role="alert" hidden>Something went wrong. Please try again, or email us at secure@ogbon.com.</p>
          <p class="form-note">{icon("lock")}<span>We only check information that is already public. We don't access your systems. See our <a href="/terms">terms</a> and <a href="/privacy">privacy&nbsp;policy</a>.</span></p>
        </form>
        <div>
          <h2>What's in your report</h2>
          <ol class="numbered" style="margin-top:24px">
            <li>Expected loss for the year, in your currency, broken down by account takeover, ransomware, data breach and&nbsp;downtime.</li>
            <li>Your five biggest risks, such as exposed admin pages, staff passwords in public leaks, public code with secret keys, or email that can be&nbsp;faked.</li>
            <li>What to fix first, and how much each fix reduces your expected&nbsp;loss.</li>
          </ol>
        </div>
      </div>
    </section>
"""

# Results layout, for the app that runs the scan. Not deployed (see Dockerfile) and not indexed.
results = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <p style="margin-top:0">Security report for {tbd("[domain]")}</p>
          <h1 id="page-title">Your expected loss this year is <span>{tbd("[amount]")}</span></h1>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="cards cards-4">
          <article class="card"><span class="badge">{icon("key")}</span><h3>Account takeover</h3><p>{tbd("[amount]")}</p></article>
          <article class="card"><span class="badge badge-pink">{icon("lock")}</span><h3>Ransomware</h3><p>{tbd("[amount]")}</p></article>
          <article class="card"><span class="badge badge-lilac">{icon("file")}</span><h3>Data breach</h3><p>{tbd("[amount]")}</p></article>
          <article class="card"><span class="badge badge-grey">{icon("clock")}</span><h3>Downtime</h3><p>{tbd("[amount]")}</p></article>
        </div>
      </div>
    </section>

    <section class="section section-tight">
      <div class="wrap split">
        <div>
          <h2 class="h2">Your five biggest risks</h2>
          <ol class="numbered" style="margin-top:24px">
            <li>{tbd("[risk]")}</li><li>{tbd("[risk]")}</li><li>{tbd("[risk]")}</li><li>{tbd("[risk]")}</li><li>{tbd("[risk]")}</li>
          </ol>
        </div>
        <div>
          <h2 class="h2">What to fix first</h2>
          <ol class="numbered" style="margin-top:24px">
            <li>{tbd("[fix]")} · reduces expected loss by {tbd("[amount]")}</li>
            <li>{tbd("[fix]")} · reduces expected loss by {tbd("[amount]")}</li>
            <li>{tbd("[fix]")} · reduces expected loss by {tbd("[amount]")}</li>
          </ol>
        </div>
      </div>
    </section>

    <div class="frame">
      <section class="cta" aria-labelledby="cta-title">
        <h2 class="h2" id="cta-title">Ogbon can help you fix these and cover what's&nbsp;left</h2>
        <p>Book a 20-minute call with our&nbsp;team.</p>
        <div class="hero-actions" style="margin-top:32px"><a class="btn btn-light" data-email="Book a call" href="#contact">Book a call</a></div>
      </section>
    </div>
"""

# ---------------------------------------------------------------- How it works
steps = [
    ("Get your free security report", "Tell us your company domain. We check what attackers can see from outside and show you your biggest risks and what they could cost&nbsp;you. Your report comes with a price. On Starter and Growth you can sign up online straight away, or talk it through with our&nbsp;team."),
    ("Connect your systems", "Connect your cloud accounts on AWS, Google Cloud or Azure, your code, and the internal systems you want covered, with read-only access. Install the Ogbon app on staff laptops, on Mac or Windows. Setup takes about an&nbsp;hour."),
    ("Fix what matters", "Ogbon lists the fixes that protect the most money. ogbon-1 prepares each fix, from a cloud setting to a code change, and your team approves it. Your score updates as you&nbsp;go."),
    ("Get covered", "Once the basics are in place, including two-step login on admin accounts, payment approvals and backups, your cover starts the next&nbsp;day."),
    ("We keep watch", "Ogbon checks your systems every day and spots attacks as they happen. Report a problem " + region("on WhatsApp", "by email") + " or from your dashboard at any time. A responder calls back within an hour, and we handle your&nbsp;claim."),
]
steps_html = "\n".join(
    f"""          <li class="step"><span class="step-num">{i}</span><div><h2>{h}</h2><p>{p}</p></div></li>"""
    for i, (h, p) in enumerate(steps, 1)
)
how = f"""    <div class="frame">
      <section class="page-hero theme-purple" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">How Ogbon <span>works</span></h1>
          <p>It starts with a free security report. After about an <br class="br-wide">hour of setup, Ogbon runs in the&nbsp;background.</p>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <ol class="steps">
{steps_html}
        </ol>
        <div class="note">
          <span class="badge badge-blue">{icon("plug")}</span>
          <p>Ogbon connects to AWS, Google Cloud, Azure, Kubernetes, GitHub, GitLab and Bitbucket, and runs on Mac and Windows laptops. For systems that can't be reached from outside, ogbon-1 can run on your own&nbsp;servers.</p>
        </div>
      </div>
    </section>
{cta()}
"""

# ---------------------------------------------------------------- Cover limits (cover and pricing pages)
COVER_LIMITS = [
    ("Total cover per year", money(250_000, ngn=25e6), money(1_000_000, ngn=75e6), money(3_000_000, ngn=200e6)),
    ("Stolen funds (account takeover, leaked API keys)", money(125_000, ngn=12.5e6), money(500_000, ngn=37.5e6), money(1_500_000, ngn=100e6)),
    ("Lost income while systems are down", money(50_000, ngn=5e6), money(200_000, ngn=15e6), money(600_000, ngn=40e6)),
    ("Ransomware, data breach, legal and notification costs", "Up to the full limit", "Up to the full limit", "Up to the full limit"),
    ("Customer pays first (excess)", money(10_000, ngn=1e6), money(25_000, ngn=2.5e6), money(75_000, ngn=7.5e6)),
    ("Incident response in the first 72 hours", "No excess", "No excess", "No excess"),
    ("Option to buy higher cover", "Up to " + money(500_000, ngn=50e6), "Up to " + money(2_000_000, ngn=150e6), "Up to " + money(7_500_000, ngn=500e6) + ", or custom"),
]


def limits_table():
    rows = "\n".join(
        f'              <tr><th scope="row">{r}</th><td>{a}</td><td class="is-featured">{b}</td><td>{c}</td></tr>'
        for r, a, b, c in COVER_LIMITS
    )
    return f"""        <div class="table-wrap">
          <table class="table table-plans table-limits">
            <thead>
              <tr>
                <th scope="col"><span class="sr-only">Cover</span></th>
                <th scope="col"><b>Starter</b><span>Up to 50 staff</span></th>
                <th scope="col" class="is-featured"><b>Growth</b><span>51 to 200 staff</span></th>
                <th scope="col"><b>Scale</b><span>201 to 500 staff</span></th>
              </tr>
            </thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>"""


# ---------------------------------------------------------------- Cover
rows = [
    ("Attackers took over an account, a system or an API key and stole money", "The money lost, up to your plan's limit"),
    ("Ransomware locked your systems", "Investigation, recovery and restoring your data"),
    ("Customer or staff data was leaked", "Investigation, legal advice, notifying customers and data protection regulators, and regulatory costs where the law allows"),
    ("Your systems went down after an attack", "Income lost after the first 12 hours"),
    ("Any covered incident", "Incident responders from the first call"),
]
rows_html = "\n".join(f"              <tr><th scope=\"row\">{a}</th><td>{b}</td></tr>" for a, b in rows)
excl = [
    "Losses caused by a critical issue we flagged that wasn't fixed by its due date",
    "Fraud carried out or approved by an owner or director",
    "Attacks that started before your cover began",
    "War, and outages of national power, telecoms or internet networks",
    "Fines the law doesn't allow to be insured",
    "Lost, stolen or damaged devices",
    "Crypto assets",
]
excl_html = "\n".join(f'            <li><span class="tick tick-x">{icon("x")}</span>{e}</li>' for e in excl)
basics = [
    "Ogbon is connected to your websites, apps, APIs, cloud and code",
    "Two-step login is on for all admin and cloud accounts",
    "No critical issue is left open past its due date",
    "Payments above your set limit need two approvals",
    "Backups are kept where attackers can't change them, and tested every quarter",
    "Incidents are reported to us within 72 hours",
]
basics_html = "\n".join(f"          <li>{b}</li>" for b in basics)
cover = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Cyber cover, included in <span>every&nbsp;plan</span></h1>
          <p>If an attack gets through while you're protected by Ogbon, we pay for the loss. Cover is a warranty from Ogbon, backed by a licensed insurer in each&nbsp;country.</p>
          {BACKED.format(cls=" backed-pill")}
        </div>
      </section>
    </div>

    <section class="section" aria-labelledby="covered-title">
      <div class="wrap">
        <div class="head head-left"><h2 class="h2" id="covered-title">What's covered</h2></div>
        <div class="table-wrap">
          <table class="table">
            <thead><tr><th scope="col">What happened</th><th scope="col">What we pay for</th></tr></thead>
            <tbody>
{rows_html}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section section-tight" id="limits" aria-labelledby="limits-title">
      <div class="wrap">
        <div class="head head-left"><h2 class="h2" id="limits-title">Cover limits by plan</h2></div>
{limits_table()}
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="excl-title">
      <div class="wrap split" style="align-items:start">
        <div>
          <h2 class="h2" id="excl-title">What's not covered</h2>
          <p class="lead">These are the main exclusions. The full list is in your&nbsp;agreement.</p>
        </div>
        <ul class="checks" style="margin-top:0">
{excl_html}
        </ul>
      </div>
    </section>

    <section class="section section-tight" id="claims" aria-labelledby="claims-title">
      <div class="wrap">
        <div class="head head-left">
          <h2 class="h2" id="claims-title">Claims, paid <span>fast</span></h2>
          <p class="lead">We've been checking your systems every day, so we already hold most of the evidence a claim&nbsp;needs.</p>
        </div>
        <div class="cards cards-3">
          <article class="card"><span class="badge">{icon("clock")}</span><h3>Same day for small claims</h3><p>{tbd("Incident response costs, and confirmed losses up to [$10,000], are paid the day you claim.")}</p></article>
          <article class="card"><span class="badge badge-pink">{icon("file")}</span><h3>Larger claims in weeks</h3><p>A decision within 15 working days of getting all documents, and payment within 5 working days of&nbsp;approval.</p></article>
          <article class="card"><span class="badge badge-lilac">{icon("chat")}</span><h3>Decided by people</h3><p>AI helps us gather the evidence. People decide every claim, and a person explains any refusal in&nbsp;writing.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-tight" id="giveback" aria-labelledby="giveback-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="giveback-title">The security <span>giveback</span></h2>
          <p class="lead">{tbd("If the part of your price that pays for cover isn't used for claims during the year, we give [20%] of it back to you. We earn more when you stay safe, so we have no reason to refuse a fair claim.")}</p>
        </div>
        <div class="panel panel-pink">
          <ul class="flow" aria-label="How the giveback can be used">
            <li><span class="badge">{icon("shield")}</span><span>Extra pentests<small>On the systems you choose</small></span></li>
            <li><span class="badge badge-blue">{icon("code")}</span><span>Fixes done for you<small>By our security team</small></span></li>
            <li><span class="badge badge-lilac">{icon("money")}</span><span>A lower price<small>Taken off your renewal</small></span></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="basics-title">
      <div class="wrap">
        <div class="head head-left">
          <h2 class="h2" id="basics-title">Staying covered</h2>
          <p class="lead">Your cover depends on six basics. Each one shows as green or red on your&nbsp;dashboard.</p>
        </div>
        <ol class="basics">
{basics_html}
        </ol>
        <div class="note"><span class="badge badge-blue">{icon("clock")}</span><p>If something falls behind, we'll tell you and give you time to fix it before it affects your&nbsp;cover.</p></div>
        <p class="fine">Cover is a warranty under your Ogbon agreement, not an insurance policy. {region("For customers in Africa it is backed by Casava, an insurer licensed by NAICOM in Nigeria.", "In the US and UK it will be backed by insurers licensed in each country; contact sales for start dates.")} You'll get the full warranty terms before you&nbsp;sign.</p>
        <p class="fine"><a class="link" href="/cover-terms">Read the cover terms in plain words {icon("arrow")}</a></p>
      </div>
    </section>
{cta()}
"""

# ---------------------------------------------------------------- Cover terms, in plain words
COVER_TERMS_INTRO = (
    "This is what your Ogbon cover promises, in plain words. Your Ogbon agreement has the full legal wording, and it "
    "wins if the two ever differ. You'll get it before you sign."
)
COVER_TERMS = [
    ("What the cover is", [
        "Cover is a warranty from Ogbon Security Limited, included in every Ogbon plan. It is not an insurance policy, "
        "and Ogbon is not an insurer.",
        "For customers in Africa, our promise is backed by Casava, an insurer licensed by the National Insurance "
        "Commission (NAICOM) in Nigeria. For customers in the US and UK, it will be backed by insurers licensed in those "
        "countries. Contact sales for start dates.",
    ]),
    ("What we pay for", [[f"{a}: {b[0].lower() + b[1:]}." for a, b in rows]]),
    ("How much we pay", [
        "Each plan has a total limit for the year, and lower limits for stolen money and lost income. The limits for "
        'each plan are on the <a class="link" href="/cover#limits">cover page</a>, in the currency your plan is billed in.',
        "You pay the first part of each loss (the excess). There is no excess for incident response in the first 72 hours.",
    ]),
    ("What we don't pay for", [[e + "." for e in excl]]),
    ("Staying covered", [
        "Your cover depends on six basics. Each one shows as green or red on your dashboard:",
        [b + "." for b in basics],
        "If something falls behind, we'll tell you and give you time to fix it before it affects your cover.",
    ]),
    ("Making a claim", [
        [
            "Tell us within 72 hours of finding an attack, " + region("on WhatsApp, by phone", "by email") + " or from your dashboard.",
            "We've been checking your systems every day, so we already hold most of the evidence. We only ask for what we don't have.",
            "Small, clear claims are paid the same day: incident response costs, and confirmed losses up to [$10,000].",
            "For larger claims we decide within 15 working days of getting all documents, and pay within 5 working days of approval.",
            "People decide every claim. If we refuse all or part of a claim, a person explains why in writing.",
            "If you disagree, someone who wasn't involved in the first decision reviews it. [Independent dispute route].",
        ],
    ]),
    ("The security giveback", [
        "If the part of your price that pays for cover isn't used for claims during the year, we give [20%] of it back "
        "to you. You choose how to use it: extra pentests, fixes done by our security team, or money off your renewal.",
    ]),
    ("Your price", [
        "Your price depends on your team size, industry and security score. Fix more, and you pay less at renewal. If "
        "your score drops, we tell you first and give you time to fix things before it affects your renewal price.",
    ]),
    ("Changing or ending your cover", [
        [
            "You can move to a bigger plan at any time. Your new limits start the same day, and your score and history carry over.",
            "You can cancel at the end of any billing period. Your cover ends when your plan ends.",
            "Attacks that started before your cover began aren't covered.",
        ],
    ]),
]


# ---------------------------------------------------------------- Pricing
YES = f'<span class="yes" aria-label="Included">{icon("check")}</span>'
NO = '<span class="no" aria-label="Not included">·</span>'
plan_rows = [
    ("Total cover per year", money(250_000, ngn=25e6), money(1_000_000, ngn=75e6), money(3_000_000, ngn=200e6)),
    ("Daily monitoring and fix list", YES, YES, YES),
    ("Website, app, API and cloud checks", YES, YES, YES),
    ("ogbon-1 and Ogbon Harness for engineering and IT teams", YES, YES, YES),
    ("Incident response, 24/7", YES, YES, YES),
    ("Small claims paid the same day", YES, YES, YES),
    ("Security giveback in years without a claim", YES, YES, YES),
    ("Sign up online, no sales call", YES, YES, NO),
    ("Audit evidence for SOC 2, ISO 27001, GDPR" + region(" and NDPA", ""), NO, YES, YES),
    ("Named security adviser", NO, NO, YES),
]
plan_html = "\n".join(
    f'              <tr><th scope="row">{r}</th><td>{tbd(a)}</td><td class="is-featured">{tbd(b)}</td><td>{tbd(c)}</td></tr>'
    for r, a, b, c in plan_rows
)
pricing = f"""    <div class="frame">
      <section class="page-hero theme-purple" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Plans and <span>pricing</span></h1>
          <p>Every plan includes cover, monitoring and incident response. <br class="br-wide">Choose a plan based on your team&nbsp;size.</p>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="table-wrap">
          <table class="table table-plans">
            <thead>
              <tr>
                <th scope="col"><span class="sr-only">Feature</span></th>
                <th scope="col"><b>Starter</b><span>Up to 50 staff</span></th>
                <th scope="col" class="is-featured"><b>Growth</b><span>51 to 200 staff</span></th>
                <th scope="col"><b>Scale</b><span>201 to 500 staff</span></th>
              </tr>
            </thead>
            <tbody>
{plan_html}
            </tbody>
            <tfoot>
              <tr>
                <td></td>
                <td><a class="btn btn-outline btn-sm" href="/report">Get started</a></td>
                <td class="is-featured"><a class="btn btn-primary btn-sm" href="/report">Get started</a></td>
                <td><a class="btn btn-outline btn-sm" data-email="Sales: Scale plan" href="#contact">Contact sales</a></td>
              </tr>
            </tfoot>
          </table>
        </div>
        <p class="fine">{tbd("Your price depends on your team size, industry and security score. Move up a plan as you grow: your score and history carry over, and your new limits start the same day.")}</p>
        <div class="note" style="margin-top:32px;align-items:center;justify-content:space-between;flex-wrap:wrap">
          <p>Have more than 500 staff or need a higher cover limit? Contact sales for a custom&nbsp;plan.</p>
          <a class="btn btn-primary btn-sm" data-email="Sales: custom plan" href="#contact">Contact sales</a>
        </div>
      </div>
    </section>

    <section class="section section-tight" id="cover-limits" aria-labelledby="limits-title">
      <div class="wrap">
        <div class="head head-left"><h2 class="h2" id="limits-title">Cover in each plan</h2></div>
{limits_table()}
        <p class="fine"><a class="link" href="/cover">See what's covered and what isn't {icon("arrow")}</a></p>
      </div>
    </section>
{cta()}
"""

# ---------------------------------------------------------------- Report an incident
timeline = [
    ("A responder calls you back", "Within 1 hour"),
    ("Investigators start work", "Within 4 hours"),
    ("You get the investigation report", "Within 10 working days"),
    ("Small, clear claims paid", "The same day"),
    ("Larger claims decided", "Within 15 working days of full documents"),
    ("Payment", "Within 5 working days of approval"),
]
tl_html = "\n".join(f"              <tr><th scope=\"row\">{a}</th><td>{b}</td></tr>" for a, b in timeline)
incident = f"""    <div class="frame">
      <section class="page-hero theme-ink" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Under <span>attack?</span></h1>
          <p>Contact us now, even if you're not sure it's an&nbsp;attack.</p>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="contact-row">
          <div class="contact r-africa"><span class="badge">{icon("chat")}</span><p>WhatsApp</p><b><a href="https://wa.me/2347107144122">+234 710 714 4122</a></b></div>
          <div class="contact r-africa"><span class="badge badge-pink">{icon("phone")}</span><p>Phone</p><b><a href="tel:+2347107144122">+234 710 714 4122</a></b></div>
          <div class="contact r-global"><span class="badge">{icon("chat")}</span><p>Email</p><b><a href="mailto:secure@ogbon.com?subject=Under%20attack">secure@ogbon.com</a></b></div>
          <div class="contact"><span class="badge badge-lilac">{icon("monitor")}</span><p>Or report it from your</p><b><a href="https://my.ogbon.com">Ogbon dashboard</a></b></div>
        </div>
        <p class="available">Available 24 hours a day, 7 days a week</p>
      </div>
    </section>

    <section class="section section-tight">
      <div class="wrap cards" style="align-items:start">
        <article class="card">
          <span class="badge badge-pink">{icon("money")}</span>
          <h2 class="h2" style="margin-top:18px;font-size:26px">If money has left your accounts</h2>
          <ol class="numbered" style="margin-top:24px">
            <li>Call your bank and ask them to freeze or recall the transfer.</li>
            <li>Contact us. We'll stay with you while you deal with the bank.</li>
            <li>Change passwords on the affected accounts and revoke any API keys that may be exposed.</li>
            <li>Keep every email, message and log. Don't delete anything.</li>
            <li>File a police report. We'll tell you what to include.</li>
          </ol>
        </article>
        <article class="card">
          <span class="badge badge-lilac">{icon("lock")}</span>
          <h2 class="h2" style="margin-top:18px;font-size:26px">If your systems are locked or data has leaked</h2>
          <ol class="numbered" style="margin-top:24px">
            <li>Disconnect affected computers from the network, but leave them switched on.</li>
            <li>Contact us. Don't reply to the attackers or pay them.</li>
            <li>Our responders will join within four hours to contain the attack and find out what happened.</li>
          </ol>
        </article>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="next-title">
      <div class="wrap">
        <div class="head head-left"><h2 class="h2" id="next-title">What happens next</h2></div>
        <div class="table-wrap">
          <table class="table">
            <thead><tr><th scope="col">Step</th><th scope="col">When</th></tr></thead>
            <tbody>
{tl_html}
            </tbody>
          </table>
        </div>
        <div class="note"><span class="badge badge-blue">{icon("shield")}</span><p>Ogbon has been checking your setup every day, so we already have most of the evidence a claim needs. You won't have to prove what security you had in&nbsp;place.</p></div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- About
about = f"""    <div class="frame">
      <section class="page-hero theme-deep" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">About <span>Ogbon</span></h1>
          <p>We spent five years inside more than 100 financial institutions. <br class="br-wide">Now we use what we learned to protect digital&nbsp;businesses.</p>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <ol class="timeline">
          <li class="tl-item">
            <span class="tl-dot" aria-hidden="true"></span>
            <div class="prose">
              <p class="eyebrow">Where we started</p>
              <h2 class="h2">We built Mono by getting inside Africa's top financial&nbsp;<span>institutions</span></h2>
              <p>Before Ogbon, we built Mono, the open banking API that lets apps connect to people's accounts. The financial institutions had no APIs for this, so we reverse-engineered how Africa's largest ones really work: their internet banking, mobile apps, logins, one-time passwords, statements and&nbsp;payments.</p>
              <p>Over five years we connected more than 100 financial institutions and linked over 10 million accounts. Moniepoint, OPay, PalmPay, Flutterwave, PiggyVest and Credit Direct built on Mono, and Mono was later acquired by&nbsp;Flutterwave.</p>
              <figure class="story-photo">
                <img src="/assets/team/founders.webp" alt="Prakhar Singh and Abdulhamid Hassan at a table, painted portrait" width="1100" height="922" loading="lazy">
                <figcaption>Prakhar Singh and Abdulhamid Hassan, Ogbon's&nbsp;founders</figcaption>
              </figure>
            </div>
          </li>
          <li class="tl-item">
            <span class="tl-dot" aria-hidden="true"></span>
            <div class="prose">
              <p class="eyebrow">What we learned</p>
              <h2 class="h2">We saw where they <span>break</span></h2>
              <p>To make those connections work, we had to understand every weak point: logins, sessions and APIs that trust too much, and systems nobody had looked at in years. We found the same gaps at institution after institution, and at the fintechs built on top of&nbsp;them.</p>
              <p class="strong">No one has seen more of Africa's financial systems from the inside. That knowledge is what Ogbon is built&nbsp;on.</p>
            </div>
          </li>
          <li class="tl-item">
            <span class="tl-dot" aria-hidden="true"></span>
            <div class="prose">
              <p class="eyebrow">Why Ogbon</p>
              <h2 class="h2">So we built the protection we <span>wished&nbsp;existed</span></h2>
              <p>Most organisations buy security and insurance separately. The security vendor doesn't pay when something goes wrong, and the insurer doesn't know how you're set up. Ogbon does both. We check your systems every day, ogbon-1 helps your teams find and fix gaps, and if an attack still gets through, we pay for the&nbsp;loss.</p>
              <p>Ogbon started in Lagos and works with businesses in {region("the US, the UK and across Africa", "the US and the UK")}. Ogbon means wisdom in&nbsp;Yoruba.</p>
            </div>
          </li>
        </ol>
        <div class="facts">
          <article class="card r-africa"><span class="badge">{icon("shield")}</span><h2 style="margin-top:18px">Partners</h2><p class="backed"><a href="https://casava.com/" target="_blank" rel="noopener" aria-label="Casava (opens in a new tab)"><img src="/assets/partners/casava.png" alt="Casava" width="112" height="27"></a></p><p>In Africa, our cover warranty is backed by Casava, an insurer licensed by NAICOM in Nigeria, and by a reinsurer. In the US and UK it will be backed by insurers licensed there. Investigations are carried out by our own experts.</p></article>
          <article class="card"><span class="badge badge-lilac">{icon("chat")}</span><h2 style="margin-top:18px">Contact</h2><p><a class="link" href="mailto:secure@ogbon.com">secure@ogbon.com</a><span class="r-africa"><br><a href="tel:+2347107144122">+234 710 714 4122</a></span><br>14B Grace Anjous Street, Lekki Phase 1, Lekki, Lagos&nbsp;State</p></article>
        </div>
      </div>
    </section>
{cta()}
"""


# ---------------------------------------------------------------- Penetration testing
pt_steps = [
    ("Map everything you expose", "Ogbon finds your websites, apps, APIs, cloud services and forgotten subdomains, including the ones your team no longer tracks. Each one goes on a live inventory."),
    ("Attack it like a real attacker", "ogbon-1 runs the test: it explores each system, tries the ways in that attackers use today, and chains small flaws into real attack paths. It runs in hours, not weeks."),
    ("Prove every finding", "Our security team checks each finding by hand before it reaches you. You get only real, exploitable issues, each with proof, the steps to reproduce it and the money it puts at&nbsp;risk."),
    ("Fix, then retest", "ogbon-1 prepares the fix and your team approves it. We retest straight away and close the finding when the fix holds. Your report and score update on their&nbsp;own."),
]
pt_steps_html = "\n".join(
    f"""          <li class="step"><span class="step-num">{i}</span><div><h2>{h}</h2><p>{p}</p></div></li>"""
    for i, (h, p) in enumerate(pt_steps, 1)
)
pt_scope = [
    ("Web apps", "Logins, sessions, payments and the business rules behind them."),
    ("APIs", "Partner and mobile APIs that return more data or do more than they&nbsp;should."),
    ("Mobile apps", "Android and iOS apps, and the servers they talk&nbsp;to."),
    ("Cloud", "AWS, Google Cloud and Azure: settings, roles and exposed&nbsp;services."),
    ("Internal network", "What an attacker can reach once they are inside, tested&nbsp;safely."),
    ("AI and LLM apps", "Chatbots and AI features: prompt injection, data leaks and unsafe&nbsp;actions."),
]
pt_scope_html = "\n".join(f'          <article class="card"><h3 style="margin-top:0">{h}</h3><p>{p}</p></article>' for h, p in pt_scope)

pentesting = f"""    <div class="frame">
      <section class="page-hero theme-ink" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">AI pentesting, <span>proven by&nbsp;people</span></h1>
          <p>ogbon-1 attacks your websites, apps, APIs and cloud the way a real attacker would, every day. Our security team proves each finding is real before it reaches you, with the money it puts at&nbsp;risk.</p>
          <div class="hero-actions">
            <a class="btn btn-light" data-email="Book a demo: penetration testing" href="#contact">Get a demo</a>
            <a class="btn btn-ghost-light" href="/report">Get free security report</a>
          </div>
        </div>
      </section>
    </div>

    <section class="section" aria-labelledby="gap-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="gap-title">Most of your systems have never been <span>tested</span></h2>
          <p class="lead">A yearly pentest covers a few apps for a few weeks. Your team ships changes every day, and attackers test whatever you leave out. Ogbon tests all of it, all year, for less than a single traditional&nbsp;engagement.</p>
        </div>
        <div class="card card-illus" style="width:100%">{art("coverage")}<p style="margin-top:18px;color:var(--muted)">Systems a yearly pentest covers, against everything an attacker can&nbsp;reach.</p></div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="how-pt-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="how-pt-title">How an Ogbon pentest <span>works</span></h2></div>
        <ol class="steps">
{pt_steps_html}
        </ol>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="proof-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="proof-title">AI finds more. <span>People prove what&nbsp;matters.</span></h2></div>
        <div class="cards">
          <article class="card">
            <h3 style="margin-top:0">AI scanner on its own</h3>
            <ul class="checks" style="margin-top:18px">
              <li><span class="tick tick-x">{icon("x")}</span>Thousands of alerts for your team to sort through</li>
              <li><span class="tick tick-x">{icon("x")}</span>False alarms that waste engineering time</li>
              <li><span class="tick tick-x">{icon("x")}</span>No proof that an issue can really be used</li>
              <li><span class="tick tick-x">{icon("x")}</span>No idea what each issue could cost you</li>
            </ul>
          </article>
          <article class="card">
            <h3 style="margin-top:0">Ogbon</h3>
            <ul class="checks" style="margin-top:18px">
              <li><span class="tick">{icon("check")}</span>Only real, exploitable findings</li>
              <li><span class="tick">{icon("check")}</span>Proof and steps to reproduce each one</li>
              <li><span class="tick">{icon("check")}</span>Ranked by the money each one puts at risk</li>
              <li><span class="tick">{icon("check")}</span>A fix ready to approve, and a retest when it ships</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="scope-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="scope-title">What we <span>test</span></h2></div>
        <div class="cards cards-3">
{pt_scope_html}
        </div>
      </div>
    </section>

    <section class="section section-tight" id="attack-surface" aria-labelledby="asm-title">
      <div class="wrap split">
        <div class="card card-illus" style="width:100%">{art("forgotten")}<p style="margin-top:18px;color:var(--muted)">The test server from 2019 that nobody remembers is often where an attack&nbsp;starts.</p></div>
        <div>
          <h2 class="h2" id="asm-title">Attack surface <span>management</span></h2>
          <p class="lead">You can't protect what you don't know about. Ogbon keeps a live list of everything you expose to the internet: domains, subdomains, apps, APIs, cloud services and open ports. When something new appears, we test it the same&nbsp;day.</p>
        </div>
      </div>
    </section>

    <section class="section section-tight" id="active-offense" aria-labelledby="offense-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="offense-title">Active <span>offense</span></h2>
          <p class="lead">Attackers don't wait for your yearly test window, so neither do we. Active offense keeps the pentest running: every release, new system and new type of attack gets tested as it appears, and every fix is retested before we close&nbsp;it.</p>
          <ul class="checks" style="margin-top:24px">
            <li><span class="tick">{icon("check")}</span>Tests start when you ship, not when the calendar says</li>
            <li><span class="tick">{icon("check")}</span>New attack methods tested across your systems within days</li>
            <li><span class="tick">{icon("check")}</span>Patterns across findings, so the same mistake stops coming back</li>
          </ul>
        </div>
        <div class="card card-illus" style="width:100%">{art("checks")}<p style="margin-top:18px;color:var(--muted)">Every system, checked every&nbsp;day.</p></div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="reports-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="reports-title">Reports for your engineers, your board and your <span>regulators</span></h2></div>
        <div class="cards cards-3">
          <article class="card"><h3 style="margin-top:0">For engineers</h3><p>Each finding with proof, the steps to reproduce it and a fix ready to&nbsp;review.</p></article>
          <article class="card"><h3 style="margin-top:0">For leadership</h3><p>Your risk in {region("dollars, pounds or naira", "dollars or pounds")}, how it is changing, and what your team fixed this&nbsp;month.</p></article>
          <article class="card"><h3 style="margin-top:0">For auditors</h3><p>A record of every test, finding, fix and retest, ready for SOC 2, ISO 27001, PCI DSS{region(", GDPR and NDPA&nbsp;reviews", " and GDPR&nbsp;reviews")}.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="pt-cover-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="pt-cover-title">The only pentest that comes with <span>cover</span></h2>
          <p class="lead">Every Ogbon plan includes cover. If an attack still gets through while you're protected, we pay for the money lost, the investigation and the cost of getting back to work. Fix more, and you pay less at&nbsp;renewal.</p>
          <a class="link" href="/cover">How cover works {icon("arrow")}</a>
        </div>
        <div class="card card-illus" style="width:100%">{art("cover")}<p style="margin-top:18px;color:var(--muted)">Cover up to {money(3_000_000, ngn=200e6)} a year, depending on your&nbsp;plan.</p></div>
      </div>
    </section>

    <div class="frame">
      <section class="cta" aria-labelledby="cta-title">
        <h2 class="h2" id="cta-title">See an AI pentest on your own&nbsp;systems</h2>
        <p>Book a 30-minute demo. We'll show you what ogbon-1 finds on your website and APIs, and how our team proves&nbsp;it.</p>
        <div class="hero-actions" style="margin-top:32px"><a class="btn btn-light" data-email="Book a demo: penetration testing" href="#contact">Get a demo</a><a class="btn btn-ghost-light" href="/report">Get free security report</a></div>
      </section>
    </div>
"""

# ---------------------------------------------------------------- ogbon-1 for engineers
ogbon1 = f"""    <div class="frame">
      <section class="page-hero theme-ink" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Find and fix security gaps <span>across your organisation</span></h1>
          <p>ogbon-1 is our 30B AI model built for security. It finds weak spots, spots attacks as they happen and prepares the fixes. It's included in every Ogbon plan: use it on your team's Mac and Windows laptops, across your code, cloud and&nbsp;servers.</p>
          <div class="hero-actions">
            <a class="btn btn-light" href="https://my.ogbon.com">{icon("apple")}Download for Mac</a>
            <a class="btn btn-light" href="https://my.ogbon.com">{icon("windows")}Download for Windows</a>
          </div>
        </div>
      </section>
    </div>

    <section class="section" aria-labelledby="does-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="does-title">What <span>ogbon-1 does</span></h2></div>
        <ol class="cards cards-3">
          <li class="card"><span class="badge">{icon("monitor")}</span><h3>Finds gaps everywhere</h3><p>It checks your apps, cloud accounts, servers, laptops and build pipelines for weak spots an attacker could use, like exposed keys, risky settings and accounts with too much&nbsp;access.</p></li>
          <li class="card"><span class="badge badge-pink">{icon("shield")}</span><h3>Spots attacks as they happen</h3><p>It watches for hijacked accounts, unusual logins and suspicious activity on your systems and devices, and joins related alerts into one incident for your&nbsp;team.</p></li>
          <li class="card"><span class="badge badge-lilac">{icon("check")}</span><h3>Fixes them</h3><p>ogbon-1 prepares the fix, from a cloud setting to a code change or a device policy. Your team approves it before it goes&nbsp;in.</p></li>
        </ol>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="where-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="where-title">One model, wherever your <span>teams&nbsp;work</span></h2></div>
        <div class="cards cards-4">
          <article class="card"><span class="badge">{icon("monitor")}</span><h3>Staff laptops</h3><p>Install the Ogbon app on Mac and Windows to protect company laptops from attacks and risky devices.</p></article>
          <article class="card"><span class="badge badge-pink">{icon("code")}</span><h3>Engineers</h3><p>Ogbon Harness, our desktop app, finds and fixes security issues while your engineers&nbsp;build.</p></article>
          <article class="card"><span class="badge badge-lilac">{icon("globe")}</span><h3>Cloud and servers</h3><p>Connect AWS, Google Cloud, Azure and Kubernetes with read-only access. ogbon-1 checks them every&nbsp;day.</p></article>
          <article class="card"><span class="badge badge-grey">{icon("plug")}</span><h3>CI and your tools</h3><p>Call the Ogbon API from your build pipeline or your own tools to check every release before it&nbsp;ships.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="covers-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="covers-title">What ogbon-1 <span>covers</span></h2></div>
        <div class="cov-grid">
          <article class="card cov">
            <span class="badge badge-blue">{icon("code")}</span>
            <h3>Code and apps</h3>
            <p>Before and after you ship</p>
            <dl class="cov-list">
              <div><dt>SAST</dt><dd>Code flaws, like injection and broken access checks</dd></div>
              <div><dt>SCA</dt><dd>Open-source libraries with known vulnerabilities</dd></div>
              <div><dt>Secrets</dt><dd>Passwords and API keys left in code</dd></div>
              <div><dt>SBOM</dt><dd>A full list of the software inside your apps</dd></div>
              <div><dt>DAST</dt><dd>Your website, app and APIs, tested from the outside</dd></div>
              <div><dt>Image scan</dt><dd>Container images, before they ship</dd></div>
            </dl>
          </article>
          <article class="card cov">
            <span class="badge">{icon("lock")}</span>
            <h3>Cloud and data</h3>
            <p>Your cloud and who can access it</p>
            <dl class="cov-list">
              <div><dt>CSPM</dt><dd>Risky settings in your cloud accounts</dd></div>
              <div><dt>KSPM</dt><dd>Kubernetes cluster settings</dd></div>
              <div><dt>CIEM</dt><dd>Accounts and roles with more access than they need</dd></div>
              <div><dt>DSPM</dt><dd>Where sensitive data lives and who can reach it</dd></div>
              <div><dt>CWPP</dt><dd>Servers and containers while they run</dd></div>
              <div><dt>AI-SPM</dt><dd>The AI tools and models your teams use</dd></div>
            </dl>
          </article>
          <article class="card cov">
            <span class="badge badge-pink">{icon("shield")}</span>
            <h3>Attacks and response</h3>
            <p>Spot and stop attacks as they happen</p>
            <dl class="cov-list">
              <div><dt>CDR</dt><dd>Suspicious activity in your cloud</dd></div>
              <div><dt>EDR</dt><dd>Laptops and servers, watched for attacks</dd></div>
              <div><dt>ITDR / UEBA</dt><dd>Hijacked accounts and unusual logins</dd></div>
              <div><dt>Device control</dt><dd>USB drives and other devices on company machines</dd></div>
              <div><dt>Threat intel</dt><dd>Known attackers' addresses and methods</dd></div>
              <div><dt>Correlation</dt><dd>Alerts from everywhere, joined into one incident</dd></div>
            </dl>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="score-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="score-title">Part of your <span>risk score</span></h2>
          <p class="lead">What ogbon-1 finds goes on the same fix list as the rest of your security, with the money it puts at risk. Your founders see the effect on the dashboard; your engineering and IT teams see the details in the Ogbon app.</p>
        </div>
        <div class="panel">
          <figure class="dash" aria-label="Example Ogbon fix list">
            <div class="dash-top"><span class="dash-domain">Fix list</span><span class="status status-warn">3 open</span></div>
            <div class="dash-list" style="padding-top:12px">
              <ul>
                <li><span>Missing access check on an endpoint<small>Code · {money(30_000, True, 12_000_000)} at risk</small></span><span class="status status-bad">Critical</span></li>
                <li><span>Two-step login off for cloud admins<small>Cloud · {money(45_000, True, 19_000_000)} at risk</small></span><span class="status status-warn">Fix</span></li>
                <li><span>Injection flaw in a search endpoint<small>Code · {money(20_000, True, 8_500_000)} at risk</small></span><span class="status status-warn">Fix</span></li>
              </ul>
            </div>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="yours-title">
      <div class="wrap split">
        <div class="panel panel-pink">
          <ul class="flow" aria-label="Where ogbon-1 runs">
            <li><span class="badge">{icon("globe")}</span><span>Ogbon Platform<small>Hosted by us</small></span></li>
            <li><span class="badge badge-pink">{icon("lock")}</span><span>Your own servers<small>Your code never leaves your network</small></span></li>
            <li><span class="badge badge-lilac">{icon("monitor")}</span><span>A single GPU<small>Enough to run ogbon-1</small></span></li>
          </ul>
        </div>
        <div>
          <h2 class="h2" id="yours-title">Your code <span>stays yours</span></h2>
          <p class="lead">Run ogbon-1 on Ogbon Platform, or on your own servers if your code can't leave your network. It runs on a single GPU. We never use your code to train our models.</p>
        </div>
      </div>
    </section>

{cta()}
"""


def legal_page(heading, intro, sections):
    """A legal document: numbered sections with an index at the top."""
    toc = "\n".join(f'            <li><a href="#s{i}">{h}</a></li>' for i, (h, _) in enumerate(sections, 1))
    parts = []
    for i, (h, blocks) in enumerate(sections, 1):
        body = []
        for b in blocks:
            if isinstance(b, list):
                body.append("<ul>" + "".join(f"<li>{tbd(x)}</li>" for x in b) + "</ul>")
            else:
                body.append(f"<p>{tbd(b)}</p>")
        parts.append(f'        <section id="s{i}" aria-labelledby="s{i}-h">\n          <h2 id="s{i}-h">{i}. {h}</h2>\n          ' + "\n          ".join(body) + "\n        </section>")
    return f"""    <div class="frame">
      <section class="page-hero theme-purple" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">{heading}</h1>
          <p>Last updated {legal.UPDATED}</p>
        </div>
      </section>
    </div>

    <div class="section">
      <div class="wrap legal">
        <p class="legal-intro">{intro}</p>
        <nav class="legal-toc" aria-label="Contents">
          <ol>
{toc}
          </ol>
        </nav>
{chr(10).join(parts)}
      </div>
    </div>
"""


privacy = legal_page("Privacy <span>policy</span>", legal.PRIVACY_INTRO, legal.PRIVACY)
cover_terms = legal_page("Cover terms, <span>in plain words</span>", COVER_TERMS_INTRO, COVER_TERMS)
terms = legal_page("Terms of <span>service</span>", legal.TERMS_INTRO, legal.TERMS)

notfound = """    <div class="frame">
      <section class="page-hero theme-ink" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Page not <span>found</span></h1>
          <p>There is nothing at this address.</p>
          <div class="hero-actions"><a class="btn btn-light" href="/">Go to the home page</a></div>
        </div>
      </section>
    </div>
"""

PAGES = [
    ("index.html", "Ogbon · Cyber cover with cybersecurity built in",
     "Cyber cover with security built in, for digital businesses. Ogbon pays for the loss if an attack gets through, and checks your systems every day so you know what to fix.",
     home, "index, follow", home_ld),
    ("report.html", "Free cybersecurity report for your company · Ogbon",
     "Find out what attackers can see about your company from the outside, and what it could cost you. It takes under 10 minutes and nothing gets installed.",
     report, "index, follow", ""),
    ("how-it-works.html", "How Ogbon works · Cover and cybersecurity in one plan",
     "It starts with a free security report. Then connect your systems, fix what matters, get covered, and Ogbon keeps watch every day.",
     how, "index, follow", ""),
    ("cover.html", "Cyber cover in every plan · Ogbon",
     "Cyber cover is included in every Ogbon plan. If an attack gets through while you're protected, we pay for the loss.",
     cover, "index, follow", ""),
    ("pricing.html", "Cyber cover and security plans, pricing · Ogbon",
     "Every Ogbon plan includes cover, monitoring and incident response. Choose a plan based on your team size.",
     pricing, "index, follow", ""),
    ("incident.html", "Under attack? 24/7 emergency help · Ogbon",
     "Under attack? Contact Ogbon now, even if you're not sure it's an attack. A responder calls you back within an hour, 24 hours a day, 7 days a week.",
     incident, "index, follow", ""),
    ("ogbon-1.html", "ogbon-1: AI security for engineering and IT teams · Ogbon",
     "ogbon-1 is Ogbon's 30B security model. It finds and fixes security gaps across your apps, cloud, servers and laptops, on Mac and Windows or through the Ogbon API.",
     ogbon1, "index, follow", ""),
    ("cover-terms.html", "Cover terms in plain words · Ogbon",
     "What Ogbon's cyber cover pays for, what it doesn't, how to stay covered and how claims work, in plain words.",
     cover_terms, "index, follow", ""),
    ("privacy.html", "Privacy policy · Ogbon",
     "How Ogbon Security Limited collects, uses and protects personal data, and your rights under data protection law, including the NDPA, UK GDPR and GDPR.",
     privacy, "index, follow", ""),
    ("terms.html", "Terms of service · Ogbon",
     "The terms for using ogbon.com, the free security report and Ogbon's services, from Ogbon Security Limited.",
     terms, "index, follow", ""),
    ("pentesting.html", "AI penetration testing, proven by people · Ogbon",
     "Ogbon's AI pentesting tests your websites, apps, APIs and cloud every day. Our security team proves each finding, ranked by the money it puts at risk.",
     pentesting, "index, follow", ""),
    ("about.html", "About Ogbon · Cybersecurity with cyber cover built in",
     "Ogbon protects digital businesses. We help you fix the weaknesses attackers use, and cover the loss if an attack still gets through.",
     about, "index, follow", ""),
    ("report-results.html", "Your security report · Ogbon",
     "Your Ogbon security report.", results, "noindex, nofollow", ""),
    ("404.html", "Page not found · Ogbon", "There is nothing at this address.", notfound, "noindex", ""),
]

# Never leave one word alone on a last line: the last two words of each text block are joined
# with a no-break space (blocks end at a closing tag, or at an icon that follows the text).
LAST_GAP = re.compile(r">([^<>]*[^\s<>]) ([^\s<>]+)(?=\s*(?:</(?:p|li|th|td|summary|h1|h2|h3|small|b|span|a)>|<svg class=\"icon\"))")


def keep_last_words(doc):
    head, sep, body = doc.partition("<body>")
    return head + sep + LAST_GAP.sub(lambda m: f">{m.group(1)}&nbsp;{m.group(2)}", body)


for slug, title, desc, body, robots, ld in PAGES:
    out = keep_last_words(page(slug, title, desc, body, robots, ld))
    assert "—" not in out, f"em dash in {slug}"
    (ROOT / slug).write_text(out)
    print("wrote", slug)
