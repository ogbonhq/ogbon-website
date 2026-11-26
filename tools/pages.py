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
CSS_V = "20261126-11"
JS_V = "20261126-2"
OG_V = "9"
SITE = "https://ogbon.com"
TAGLINE = "Cybersecurity with cover built in."

LOGO = (ROOT / "tools/partials/logo.svg").read_text().strip()
SOCIAL = (ROOT / "tools/partials/social.html").read_text().strip()


def tbd(text):
    """Highlights every [placeholder] in a string of HTML."""
    return re.sub(r"\[([^\]]+)\]", r'<mark class="tbd">[\1]</mark>', text)


def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="/assets/icons.svg#{name}"/></svg>'


# Links are absolute so the 404 page works at any depth.
NAV = [
    ("/how-it-works", "How it works"),
    ("/ogbon-1", "ogbon-1"),
    ("/cover", "Cover"),
    ("/pricing", "Pricing"),
    ("/about", "About"),
]
FOOTER = [
    ("/how-it-works", "How it works"),
    ("/ogbon-1", "ogbon-1"),
    ("/cover", "Cover"),
    ("/pricing", "Pricing"),
    ("/incident", "Report an incident"),
    ("/about", "About"),
    ("/privacy", "Privacy"),
    ("/terms", "Terms"),
]
LEGAL = (
    "Ogbon is not an insurer, and the cover in Ogbon plans is not an insurance policy. It is a warranty from "
    "Ogbon Security Limited, backed by Casava, an insurer licensed by the National Insurance Commission (NAICOM). "
    "Terms, limits and exclusions apply."
)


def nav(current):
    links = "\n".join(
        f'          <a href="{href}"{" aria-current=\"page\"" if href == "/" + current.removesuffix(".html") else ""}>{label}</a>'
        for href, label in NAV
    )
    inc = ' aria-current="page"' if current == "incident.html" else ""
    return f"""  <header class="nav" id="nav">
    <div class="nav-inner">
      <a class="nav-logo" href="/" aria-label="Ogbon home">{LOGO}</a>
      <nav class="nav-links" aria-label="Primary">
{links}
          <a class="nav-incident" href="/incident"{inc}>Report an incident</a>
      </nav>
      <div class="nav-actions">
        <a class="nav-login" href="https://my.ogbon.com">Log in</a>
        <a class="btn btn-primary btn-sm" href="https://my.ogbon.com">Get started</a>
        <button class="nav-menu" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="Menu"><span></span><span></span></button>
      </div>
    </div>
  </header>"""


def footer():
    links = "\n".join(f'          <li><a href="{h}">{l}</a></li>' for h, l in FOOTER)
    return f"""  <footer class="footer">
    <div class="wrap">
      <div class="footer-top">
        <div class="footer-brand">
          <a class="nav-logo" href="/" aria-label="Ogbon home">{LOGO}</a>
          <p>{TAGLINE}</p>
          {SOCIAL}
        </div>
        <ul class="footer-links">
{links}
        </ul>
      </div>
      <div class="footer-legal">
        <p>{tbd(LEGAL)}</p>
        <p>© 2026 Ogbon Security Limited. Lagos, Nigeria.</p>
      </div>
    </div>
  </footer>"""


def page(slug, title, desc, body, robots="index, follow", ld=""):
    url = SITE + ("/" if slug == "index.html" else "/" + slug.removesuffix(".html"))
    t = html.escape(title, quote=True)
    d = html.escape(desc, quote=True)
    current = slug
    return f"""<!doctype html>
<html lang="en-NG">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#FFFFFF">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Ogbon">
  <meta property="og:locale" content="en_NG">
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
     "No. Ogbon is a cybersecurity company. The cover in every plan is a warranty from Ogbon: if an attack gets through while you're protected, we pay for the loss, up to your plan's limit. Our promise is backed by Casava, an insurer licensed by NAICOM, and we manage your claim with you from start to finish."),
    ("Is the cover an insurance policy?",
     "Not today. It's a warranty from Ogbon, backed by Casava. We plan to offer a full cyber insurance policy, arranged through licensed partners, once we hold a broker or managing agent licence. Existing customers will be able to move across."),
    ("Do you install anything on our laptops?",
     "No. Ogbon focuses on where attacks start: your websites, apps, APIs, cloud and internal systems. We connect to them read-only and don't install anything on staff devices."),
    ("What data can Ogbon see?",
     "Configuration and access settings from the cloud accounts and systems you connect, and the code repositories you choose. We don't read emails, chats or documents. Access is read-only and you can disconnect at any time."),
    ("How long does setup take?",
     "About an hour of your IT team's time. Most companies are covered within a week."),
    ("What is ogbon-1?",
     "ogbon-1 is Ogbon's own 30B security model. It reviews code, finds vulnerabilities and fixes them. Your engineers use it through Ogbon Harness or the Ogbon API, and it's included in every plan."),
    ("Can we keep our code on our own servers?",
     "Yes. ogbon-1 runs on a single GPU, so you can host it yourself and your code never leaves your network. We never use customer code to train our models."),
    ("Do you cover money stolen through hacked accounts or leaked API keys?",
     "Yes, up to your plan's limit. It's one of the most common ways organisations that move money lose it, so it's included in every plan."),
    ("What if we can't fix something in time?",
     "Tell us before the due date and we'll agree a new date or another fix. Your cover is only affected if a critical issue is left open past its due date without telling us."),
    ("How quickly are claims paid?",
     "We aim to decide within 15 working days of getting all documents, and to pay within 5 working days of approval."),
    ("Does Ogbon help with CBN and NDPA compliance?",
     "Yes. Growth and Scale plans include audit evidence mapped to the CBN risk-based cybersecurity framework and the Nigeria Data Protection Act."),
    ("Can we cancel?",
     "Yes, at the end of any billing period. [Confirm refund terms for unused cover.]"),
]

faq_html = "\n".join(
    f"""          <details>
            <summary>{q}{icon("plus")}</summary>
            <p>{tbd(a)}</p>
          </details>""" for q, a in FAQ
)
faq_ld = ",\n".join(
    "          " + json.dumps({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}, ensure_ascii=False)
    for q, a in FAQ if "[" not in a
)

home = f"""    <div class="frame">
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero-main">
          <h1 id="hero-title">Cybersecurity with <span>cover built&nbsp;in</span></h1>
          <p class="hero-sub">Your engineers build with ogbon-1, which catches flaws before they ship. We check your websites, apps, APIs and cloud every day, and pay for the loss if an attacker still gets&nbsp;through.</p>
          <div class="hero-actions">
            <a class="btn btn-light" href="/report">Get free security report</a>
            <a class="btn btn-ghost-light" data-email="Sales" href="#contact">Contact sales</a>
          </div>
          <p class="backed backed-pill">Cover backed by <img src="/assets/partners/casava.png" alt="Casava" width="112" height="27"></p>
        </div>
        <div class="hero-side">
          <figure class="dash" aria-label="Example Ogbon dashboard">
            <div class="dash-top"><span class="dash-domain">yourcompany.com</span><span class="status status-ok">Cover active</span></div>
            <div class="dash-stats">
              <div class="dash-stat"><p>Security score</p><b>72 / 100</b></div>
              <div class="dash-stat"><p>Expected loss this year</p><b>₦48m</b></div>
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
         Line above the logos: "Used by fintechs, lenders and growing organisations across Nigeria" -->

    <section class="section" aria-labelledby="attacks-title">
      <div class="wrap">
        <div class="head">
          <h2 class="h2" id="attacks-title">Most attacks start with <span>something&nbsp;small</span></h2>
          <p class="lead lead-split"><strong>Attackers start with your website and app.</strong> They look for one place that trusts them too much, then use it to reach customer data or move money.</p>
        </div>
        <ul class="cards cards-4" aria-label="Common ways in">
          <li class="card">{'<span class="badge badge-pink">' + icon("code") + '</span>'}<h3>APIs and integrations</h3><p>Public APIs and partner connections that expose more data or actions than they should.</p></li>
          <li class="card">{'<span class="badge">' + icon("naira") + '</span>'}<h3>Business logic</h3><p>Flaws in how your product handles money, limits and approvals. Scanners don't find these.</p></li>
          <li class="card">{'<span class="badge badge-lilac">' + icon("key") + '</span>'}<h3>Identity and access</h3><p>Staff, service accounts and cloud roles with more access than they need.</p></li>
          <li class="card">{'<span class="badge badge-grey">' + icon("globe") + '</span>'}<h3>Forgotten systems</h3><p>Old apps, test servers and subdomains your team no longer tracks.</p></li>
        </ul>
      </div>
    </section>

    <section class="section section-tight" id="product" aria-labelledby="product-title">
      <div class="wrap">
        <div class="head">
          <h2 class="h2" id="product-title">Protected while you build, <span class="nowrap">and once you're live</span></h2>
        </div>
        <div class="cards">
          <article class="card card-wide"><span class="badge badge-blue">{icon("code")}</span><div><h3>While you build: code security</h3><p>Every engineer gets ogbon-1, our security model. It reviews each pull request, finds vulnerabilities and fixes them before they ship, in every application you build or&nbsp;run.</p><a class="link" href="/ogbon-1">ogbon-1 for engineers {icon("arrow")}</a></div></article>
          <article class="card"><span class="badge">{icon("monitor")}</span><h3>Once you're live: daily checks</h3><p>Ogbon checks your websites, apps, APIs, cloud accounts and internal systems every day, from the outside like an attacker and from the inside with read-only&nbsp;access.</p></article>
          <article class="card"><span class="badge badge-pink">{icon("list")}</span><h3>Fix list</h3><p>We rank what needs fixing by how much money it puts at risk, and give your team clear steps for each&nbsp;item.</p></article>
          <article class="card"><span class="badge badge-grey">{icon("phone")}</span><h3>Incident response</h3><p>Report a problem on WhatsApp or from your dashboard at any time. A responder calls you back within an&nbsp;hour.</p></article>
          <article class="card"><span class="badge badge-lilac">{icon("shield")}</span><h3>Cover</h3><p>If an attack gets through while you're protected, we pay for the money lost, the investigation and the cost of getting back to&nbsp;work.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="naira-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="naira-title">See your risk <span>in&nbsp;naira</span></h2>
          <p class="lead">Ogbon turns technical findings into a number your founders and board can act on: how much an attack could cost you this year, and how much each fix brings that&nbsp;down.</p>
          <a class="btn btn-primary" href="/report">Get your free report</a>
        </div>
        <div class="panel">
          <figure class="loss" aria-label="Example from an Ogbon report">
            <p class="loss-label">Expected loss this year</p>
            <p class="loss-num">₦48,000,000</p>
            <div class="loss-fix">
              <span class="badge">{icon("lock")}</span>
              <div>
                <p>Turn on two-step login for cloud and admin accounts</p>
                <span class="loss-save">Reduces expected loss by ₦19,000,000</span>
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
            <li><span class="badge badge-blue">{icon("code")}</span><span>Every change reviewed<small>ogbon-1 on each pull request</small></span></li>
            <li><span class="badge">{icon("monitor")}</span><span>Daily checks<small>Websites, apps, APIs, cloud and internal systems</small></span></li>
            <li><span class="badge badge-pink">{icon("phone")}</span><span>Responder on the line<small>Within an hour of your report</small></span></li>
            <li><span class="badge badge-lilac">{icon("naira")}</span><span>Loss paid<small>Up to your plan's limit</small></span></li>
          </ul>
        </div>
        <div>
          <h2 class="h2" id="covered-title">Cover for the losses that <span>hurt&nbsp;most</span></h2>
          <ul class="checks">
            <li><span class="tick">{icon("check")}</span>Money stolen after attackers take over your accounts, systems or API keys</li>
            <li><span class="tick">{icon("check")}</span>Ransomware investigation and recovery</li>
            <li><span class="tick">{icon("check")}</span>Data breach response, including notifying customers and the NDPC</li>
            <li><span class="tick">{icon("check")}</span>Income lost while your systems are down</li>
            <li><span class="tick">{icon("check")}</span>Incident responders from the first call</li>
          </ul>
          <a class="link" href="/cover">See what's covered {icon("arrow")}</a>
          <p class="backed">Cover backed by <img src="/assets/partners/casava.png" alt="Casava" width="112" height="27"></p>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="who-title">
      <div class="wrap">
        <div class="cards">
          <article class="card">
            <span class="badge badge-lilac">{icon("naira")}</span>
            <h2 class="h2" id="who-title" style="margin-top:18px">Built for organisations that move money</h2>
            <p class="lead">Ogbon is built for fintechs, banks, lenders, microfinance banks, payment companies, enterprises and government agencies. If you hold customer money or customer data, Ogbon is for&nbsp;you.</p>
            <ul class="tags" aria-label="Who uses Ogbon">
              <li>Fintechs</li><li>Lenders</li><li>Microfinance banks</li><li>Payment companies</li><li>20 to 500 staff</li>
            </ul>
          </article>
          <article class="card">
            <span class="badge badge-pink">{icon("shield")}</span>
            <h2 class="h2" style="margin-top:18px">We get paid to keep you safe</h2>
            <p class="lead">Most insurers price cover from a questionnaire and only hear from you when something goes wrong. Ogbon checks your security every day, so we can price cover fairly and help you fix problems early. The more you fix, the less you pay at&nbsp;renewal.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="audit-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="audit-title">Ready for CBN and <span>NDPA&nbsp;audits</span></h2>
          <p class="lead">Download evidence mapped to the CBN risk-based cybersecurity framework and the Nigeria Data Protection Act whenever an auditor asks for&nbsp;it.</p>
        </div>
        <div class="panel">
          <ul class="flow" aria-label="Audit evidence">
            <li><span class="badge">{icon("file")}</span><span>CBN risk-based cybersecurity framework<small>Evidence pack, ready to download</small></span></li>
            <li><span class="badge badge-pink">{icon("file")}</span><span>Nigeria Data Protection Act<small>Evidence pack, ready to download</small></span></li>
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
        "inLanguage": "en-NG",
        "publisher": {{ "@id": "{SITE}/#organization" }}
      }},
      {{
        "@type": "Organization",
        "@id": "{SITE}/#organization",
        "name": "Ogbon",
        "legalName": "Ogbon Security Limited",
        "url": "{SITE}/",
        "areaServed": "NG",
        "sameAs": ["https://x.com/ogbonhq", "https://www.linkedin.com/company/ogbonhq", "https://github.com/ogbonhq", "https://www.instagram.com/ogbonhq"],
        "contactPoint": {{ "@type": "ContactPoint", "contactType": "incident response", "telephone": "+234 710 714 4122", "email": "secure@ogbon.com", "areaServed": "NG", "availableLanguage": "en", "hoursAvailable": {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59" }} }},
        "logo": "{SITE}/assets/icons/icon-512.png",
        "slogan": "{TAGLINE}",
        "description": "Ogbon helps organisations in Nigeria stay safe from cyber attacks, and pays for the loss if an attacker still gets through.",
        "email": "secure@ogbon.com",
        "telephone": "+234 710 714 4122",
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
        <form class="form form-card" id="report-form" action="https://my.ogbon.com/report" method="post">
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
                <option>Fintech</option>
                <option>Lender</option>
                <option>Microfinance bank</option>
                <option>Payment company</option>
                <option>Other</option>
              </select>
            </div>
          </div>
          <button class="btn btn-primary" type="submit">Get my report</button>
          <p class="form-note">{icon("lock")}<span>We only check information that is already public. We don't access your systems. See our <a href="/terms">terms</a> and <a href="/privacy">privacy&nbsp;policy</a>.</span></p>
        </form>
        <div>
          <h2>What's in your report</h2>
          <ol class="numbered" style="margin-top:24px">
            <li>Expected loss for the year, in naira, broken down by account takeover, ransomware, data breach and&nbsp;downtime.</li>
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
          <h1 id="page-title">Your expected loss this year is <span>₦{tbd("[amount]")}</span></h1>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="cards cards-4">
          <article class="card"><span class="badge">{icon("key")}</span><h3>Account takeover</h3><p>₦{tbd("[amount]")}</p></article>
          <article class="card"><span class="badge badge-pink">{icon("lock")}</span><h3>Ransomware</h3><p>₦{tbd("[amount]")}</p></article>
          <article class="card"><span class="badge badge-lilac">{icon("file")}</span><h3>Data breach</h3><p>₦{tbd("[amount]")}</p></article>
          <article class="card"><span class="badge badge-grey">{icon("clock")}</span><h3>Downtime</h3><p>₦{tbd("[amount]")}</p></article>
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
            <li>{tbd("[fix]")} · reduces expected loss by ₦{tbd("[amount]")}</li>
            <li>{tbd("[fix]")} · reduces expected loss by ₦{tbd("[amount]")}</li>
            <li>{tbd("[fix]")} · reduces expected loss by ₦{tbd("[amount]")}</li>
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
    ("Connect your tools", "Add your domains and apps, then connect your cloud accounts on AWS, Google Cloud or Azure, your code on GitHub, GitLab or Bitbucket, and the internal systems you want covered. All access is read-only."),
    ("Fix what matters", "Ogbon lists the five to ten fixes that protect the most money, with clear steps for each. When your team makes a fix, Ogbon checks it automatically and your score updates."),
    ("Get covered", "Once the basics are in place, including two-step login on admin accounts, payout approvals and backups, your cover starts the next day. Your dashboard shows your cover status at all times."),
    ("Get help when you need it", "Report an incident from your dashboard or on WhatsApp, at any time of day. A responder calls back within an hour, helps contain the attack and brings in investigators. Then we handle your claim."),
]
steps_html = "\n".join(
    f"""          <li class="step"><span class="step-num">{i}</span><div><h2>{h}</h2><p>{p}</p></div></li>"""
    for i, (h, p) in enumerate(steps, 1)
)
how = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">How Ogbon <span>works</span></h1>
          <p>Setup takes about an hour of your IT team's time. After that, Ogbon runs in the&nbsp;background.</p>
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
          <p>Ogbon connects to AWS, Google Cloud, Azure, GitHub, GitLab and Bitbucket. For systems that can't be reached from outside, ogbon-1 can run on your own&nbsp;servers.</p>
        </div>
      </div>
    </section>
{cta()}
"""

# ---------------------------------------------------------------- Cover limits (cover and pricing pages)
COVER_LIMITS = [
    ("Total cover per year", "₦25m<small>about $17k</small>", "₦75m<small>about $50k</small>", "₦200m<small>about $133k</small>"),
    ("Stolen funds (account takeover, leaked API keys)", "₦12.5m", "₦37.5m", "₦100m"),
    ("Lost income while systems are down", "₦5m", "₦15m", "₦40m"),
    ("Ransomware, data breach, legal and notification costs", "Up to the full limit", "Up to the full limit", "Up to the full limit"),
    ("Customer pays first (excess)", "₦1m", "₦2.5m", "₦7.5m"),
    ("Incident response in the first 72 hours", "No excess", "No excess", "No excess"),
    ("Option to buy higher cover", "Up to ₦50m", "Up to ₦150m", "Up to ₦500m, or custom"),
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
    ("Customer or staff data was leaked", "Investigation, legal advice, notifying customers and the NDPC, and regulatory costs where the law allows"),
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
    "Payouts above your set limit need two approvals",
    "Backups are kept where attackers can't change them, and tested every quarter",
    "Incidents are reported to us within 72 hours",
]
basics_html = "\n".join(f"          <li>{b}</li>" for b in basics)
cover = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Cyber cover, included in <span>every&nbsp;plan</span></h1>
          <p>If an attack gets through while you're protected by Ogbon, we pay for the loss. Cover is a warranty from Ogbon, backed by Casava, an insurer licensed by&nbsp;NAICOM.</p>
          <p class="backed backed-pill">Cover backed by <img src="/assets/partners/casava.png" alt="Casava" width="112" height="27"></p>
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
        <p class="fine">Cover is a warranty under your Ogbon agreement, not an insurance policy. You'll get the full warranty terms before you&nbsp;sign.</p>
      </div>
    </section>
{cta()}
"""

# ---------------------------------------------------------------- Pricing
YES = f'<span class="yes" aria-label="Included">{icon("check")}</span>'
NO = '<span class="no" aria-label="Not included">·</span>'
plan_rows = [
    ("Total cover per year", "₦25m", "₦75m", "₦200m"),
    ("Daily monitoring and fix list", YES, YES, YES),
    ("Website, app, API and cloud checks", YES, YES, YES),
    ("ogbon-1 and Ogbon Harness for engineers", YES, YES, YES),
    ("Incident response, 24/7", YES, YES, YES),
    ("Audit evidence for CBN and NDPA", NO, YES, YES),
    ("Named security adviser", NO, NO, YES),
]
plan_html = "\n".join(
    f'              <tr><th scope="row">{r}</th><td>{tbd(a)}</td><td class="is-featured">{tbd(b)}</td><td>{tbd(c)}</td></tr>'
    for r, a, b, c in plan_rows
)
pricing = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Plans and <span>pricing</span></h1>
          <p>Every plan includes monitoring, cover and incident response. Choose a plan based on your team&nbsp;size.</p>
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
                <td><a class="btn btn-outline btn-sm" href="https://my.ogbon.com">Get started</a></td>
                <td class="is-featured"><a class="btn btn-primary btn-sm" href="https://my.ogbon.com">Get started</a></td>
                <td><a class="btn btn-outline btn-sm" data-email="Sales: Scale plan" href="#contact">Contact sales</a></td>
              </tr>
            </tfoot>
          </table>
        </div>
        <p class="fine">Your price depends on your team size, industry and security score. Companies that fix more pay less at&nbsp;renewal.</p>
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
    ("Claim decision", "Within 15 working days of full documents"),
    ("Payment", "Within 5 working days of approval"),
]
tl_html = "\n".join(f"              <tr><th scope=\"row\">{a}</th><td>{b}</td></tr>" for a, b in timeline)
incident = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Report an <span>incident</span></h1>
          <p>If you think something is wrong, contact us straight away, even if you're not sure it's an attack. Acting in the first hour makes the biggest&nbsp;difference.</p>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="contact-row">
          <div class="contact"><span class="badge">{icon("chat")}</span><p>WhatsApp</p><b><a href="https://wa.me/2347107144122">0710 714 4122</a></b></div>
          <div class="contact"><span class="badge badge-pink">{icon("phone")}</span><p>Phone</p><b><a href="tel:+2347107144122">0710 714 4122</a></b></div>
          <div class="contact"><span class="badge badge-lilac">{icon("monitor")}</span><p>Or report it from your</p><b><a href="https://my.ogbon.com">Ogbon dashboard</a></b></div>
        </div>
        <p class="available">Available 24 hours a day, 7 days a week</p>
      </div>
    </section>

    <section class="section section-tight">
      <div class="wrap cards" style="align-items:start">
        <article class="card">
          <span class="badge badge-pink">{icon("naira")}</span>
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
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">About <span>Ogbon</span></h1>
          <p>Ogbon means wisdom in&nbsp;Yoruba.</p>
        </div>
      </section>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="prose">
          <p class="strong">Ogbon is a cybersecurity company based in Lagos. We help organisations find and fix the weaknesses attackers use, and we cover the financial loss if an attack still gets&nbsp;through.</p>
          <p>Until now, organisations in Nigeria have bought security tools and insurance separately. Security vendors don't pay when their tools fail, and insurers rarely know enough about a company's setup to price cyber cover well. Ogbon does both, so the company protecting you is also the one that pays if something goes&nbsp;wrong.</p>
        </div>
        <div class="facts">
          <article class="card"><span class="badge">{icon("shield")}</span><h2 style="margin-top:18px">Partners</h2><p class="backed"><img src="/assets/partners/casava.png" alt="Casava" width="112" height="27"></p><p>Our cover warranty is backed by Casava, an insurer licensed by NAICOM, and by a reinsurer. A full insurance policy will follow once we hold a broker or managing agent licence. Investigations are carried out by our own experts.</p></article>
          <article class="card"><span class="badge badge-pink">{icon("list")}</span><h2 style="margin-top:18px">Team</h2><p>Ogbon was founded by Abdul and Prakhar. They previously founded Africa's biggest open banking infrastructure company, which was acquired by Flutterwave, Africa's most valuable fintech.</p></article>
          <article class="card"><span class="badge badge-lilac">{icon("chat")}</span><h2 style="margin-top:18px">Contact</h2><p><a class="link" href="mailto:secure@ogbon.com">secure@ogbon.com</a><br><a href="tel:+2347107144122">0710 714 4122</a><br>14B Grace Anjous Street, Lekki Phase 1, Lekki, Lagos&nbsp;State</p></article>
        </div>
      </div>
    </section>
{cta()}
"""

# ---------------------------------------------------------------- ogbon-1 for engineers
ogbon1 = f"""    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Find and fix vulnerabilities <span>in your own code</span></h1>
          <p>Every Ogbon plan gives your engineering team ogbon-1, our 30B security model. Use it in Ogbon Harness, our desktop app, or call it from your own tools with the Ogbon API.</p>
          <div class="hero-actions">
            <a class="btn btn-light" href="https://my.ogbon.com">Download Ogbon Harness</a>
            <a class="btn btn-ghost-light" href="https://my.ogbon.com">Get an API key</a>
          </div>
        </div>
      </section>
    </div>

    <section class="section" aria-labelledby="does-title">
      <div class="wrap">
        <div class="head"><h2 class="h2" id="does-title">What <span>ogbon-1 does</span></h2></div>
        <ol class="cards cards-3">
          <li class="card"><span class="badge">{icon("list")}</span><h3>Reviews every change</h3><p>Connect GitHub, GitLab or Bitbucket and ogbon-1 checks each pull request for security issues before it's merged.</p></li>
          <li class="card"><span class="badge badge-pink">{icon("key")}</span><h3>Finds vulnerabilities</h3><p>It scans your repositories for exposed secrets and API keys, injection flaws, broken login and access checks, and outdated dependencies with known issues.</p></li>
          <li class="card"><span class="badge badge-lilac">{icon("check")}</span><h3>Fixes them</h3><p>Ask Ogbon Harness to fix an issue and ogbon-1 edits the files. Your engineers review every change before it goes in.</p></li>
        </ol>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="score-title">
      <div class="wrap split">
        <div>
          <h2 class="h2" id="score-title">Part of your <span>risk score</span></h2>
          <p class="lead">What ogbon-1 finds in your code goes on the same fix list as the rest of your security, with the naira it puts at risk. Your founders see the effect on the dashboard; your engineers see the details in Harness and in their pull requests.</p>
        </div>
        <div class="panel">
          <figure class="dash" aria-label="Example Ogbon fix list">
            <div class="dash-top"><span class="dash-domain">Fix list</span><span class="status status-warn">3 open</span></div>
            <div class="dash-list" style="padding-top:12px">
              <ul>
                <li><span>Missing access check on an endpoint<small>Code · ₦12,000,000 at risk</small></span><span class="status status-bad">Critical</span></li>
                <li><span>Two-step login off for cloud admins<small>Cloud · ₦19,000,000 at risk</small></span><span class="status status-warn">Fix</span></li>
                <li><span>Injection flaw in a search endpoint<small>Code · ₦8,500,000 at risk</small></span><span class="status status-warn">Fix</span></li>
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

    <section class="section section-tight" aria-labelledby="api-title">
      <div class="wrap">
        <div class="head head-left"><h2 class="h2" id="api-title">Review a diff from your CI pipeline with the <span>Ogbon API</span></h2></div>
        <figure class="code" aria-label="Example: review a diff with the Ogbon API">
          <div class="code-bar"><span></span><span></span><span></span><p>review.py</p></div>
          <pre><code><span class="k">import</span> os, subprocess
<span class="k">from</span> openai <span class="k">import</span> OpenAI

diff = subprocess.run([<span class="s">"git"</span>, <span class="s">"diff"</span>, <span class="s">"origin/main...HEAD"</span>], capture_output=<span class="k">True</span>, text=<span class="k">True</span>).stdout

client = OpenAI(base_url=<span class="s">"https://api.ogbon.com/v1"</span>, api_key=os.environ[<span class="s">"OGBON_API_KEY"</span>])
review = client.chat.completions.create(
    model=<span class="s">"ogbon-1"</span>,
    messages=[{{<span class="s">"role"</span>: <span class="s">"user"</span>, <span class="s">"content"</span>: <span class="s">"Review this diff for security issues:\\n"</span> + diff}}],
)
print(review.choices[0].message.content)</code></pre>
        </figure>
        <p class="api-link"><a class="link" href="#api-docs">Read the API docs {icon("arrow")}</a> {tbd("[API docs URL]")}</p>
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
      <section class="page-hero" aria-labelledby="page-title">
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
terms = legal_page("Terms of <span>service</span>", legal.TERMS_INTRO, legal.TERMS)

notfound = """    <div class="frame">
      <section class="page-hero" aria-labelledby="page-title">
        <div class="wrap">
          <h1 id="page-title">Page not <span>found</span></h1>
          <p>There is nothing at this address.</p>
          <div class="hero-actions"><a class="btn btn-light" href="/">Go to the home page</a></div>
        </div>
      </section>
    </div>
"""

PAGES = [
    ("index.html", "Ogbon · Cybersecurity with cyber cover in Nigeria",
     "Ogbon reviews your code as you build and checks your systems every day once you're live, and pays for the loss if an attacker still gets through.",
     home, "index, follow", home_ld),
    ("report.html", "Free cybersecurity report for your company · Ogbon",
     "Find out what attackers can see about your company from the outside, and what it could cost you. It takes under 10 minutes and nothing gets installed.",
     report, "index, follow", ""),
    ("how-it-works.html", "How Ogbon works · Cybersecurity and cover in one plan",
     "Setup takes about an hour of your IT team's time. Connect your tools, fix what matters, get covered, and get help when you need it.",
     how, "index, follow", ""),
    ("cover.html", "Cyber cover in every plan · Ogbon",
     "Cyber cover is included in every Ogbon plan. If an attack gets through while you're protected, we pay for the loss.",
     cover, "index, follow", ""),
    ("pricing.html", "Cybersecurity plans and pricing · Ogbon",
     "Every Ogbon plan includes monitoring, cover and incident response. Choose a plan based on your team size.",
     pricing, "index, follow", ""),
    ("incident.html", "Report a cyber incident, 24/7 · Ogbon",
     "If you think something is wrong, contact Ogbon straight away, even if you're not sure it's an attack. Available 24 hours a day, 7 days a week.",
     incident, "index, follow", ""),
    ("ogbon-1.html", "ogbon-1: AI code security for engineers · Ogbon",
     "ogbon-1 is Ogbon's 30B security model. It reviews code, finds vulnerabilities and fixes them, in Ogbon Harness or through the Ogbon API.",
     ogbon1, "index, follow", ""),
    ("privacy.html", "Privacy policy · Ogbon",
     "How Ogbon Security Limited collects, uses and protects personal data, and your rights under the Nigeria Data Protection Act 2023.",
     privacy, "index, follow", ""),
    ("terms.html", "Terms of service · Ogbon",
     "The terms for using ogbon.com, the free security report and Ogbon's services, from Ogbon Security Limited.",
     terms, "index, follow", ""),
    ("about.html", "About Ogbon · Cybersecurity company in Lagos",
     "Ogbon is a cybersecurity company in Lagos. We help organisations fix the weaknesses attackers use, and cover the loss if an attack still gets through.",
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
