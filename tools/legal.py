"""Privacy policy and terms of service for ogbon.com, as sections the page generator turns into HTML.
Each section is (heading, blocks); a block is a paragraph string or a list of bullet strings.
Text in [brackets] is a placeholder and shows highlighted on the page."""

UPDATED = "28 November 2026"

CONTACT = (
    "Ogbon Security Limited, 14B Grace Anjous Street, Lekki Phase 1, Lekki, Lagos State. "
    "Email secure@ogbon.com or call 0710 714 4122."
)

PRIVACY_INTRO = (
    "This policy explains how Ogbon Security Limited (\"Ogbon\", \"we\") collects and uses personal data when you "
    "visit ogbon.com, ask for a free security report, or use Ogbon, and the rights you have under data protection law, "
    "including the Nigeria Data Protection Act 2023 (NDPA), the UK GDPR and, in the European Union, the GDPR."
)

PRIVACY = [
    ("Who we are", [
        "Ogbon Security Limited is a cybersecurity company registered in Nigeria. We decide how personal data is used "
        "on this website, for free security reports, and when we sell to and bill our customers.",
        "When we work inside a customer's cloud accounts, code or other systems, the customer decides what we process and "
        "why. In that case the customer is the data controller and we process the data on its behalf, under our "
        "agreement with it.",
        CONTACT,
    ]),
    ("What we collect", [
        "When you ask for a free security report:",
        [
            "Your company domain, work email, number of staff, industry and country.",
            "Information about your domain that is already public, such as DNS and email settings, websites and "
            "services open to the internet, public code, and staff email addresses that appear in public data leaks.",
        ],
        "When your company uses Ogbon:",
        [
            "Names, work emails and phone numbers of the people who use your account.",
            "Billing details.",
            "Configuration, access settings and login rules from the systems you connect, and the code repositories "
            "you choose to connect.",
            "What you tell us about an incident or a claim.",
        ],
        "When you contact us by email, phone or WhatsApp, we keep what you send us.",
        "When you visit ogbon.com, our server records your IP address, browser and the pages you ask for. We use "
        "Google Analytics, through Google Tag Manager, to count visits and see how people use the site. It sets analytics "
        "cookies in your browser and sends Google your IP address and the pages you visit. We don't use advertising cookies. Our fonts load from Google Fonts, which receives your IP address.",
        "We don't read emails, chats or documents in your systems.",
    ]),
    ("How we use it, and our legal basis", [
        [
            "To produce your free report and reply to you about it. Our basis is your consent and our legitimate "
            "interest in answering requests.",
            "To provide monitoring, your fix list and incident response. Our basis is our contract with your company.",
            "To provide your cover and handle claims, including giving the insurer that backs our warranty what it needs to assess "
            "a claim. Our basis is our contract and our legal obligations.",
            "To bill you and keep tax records. Our basis is our contract and our legal obligations.",
            "To keep our service secure and prevent fraud. Our basis is our legitimate interests.",
            "To meet legal and regulatory duties. Our basis is our legal obligations.",
        ],
        "We only send marketing messages with your consent, and you can stop them at any time.",
    ]),
    ("Your code and ogbon-1", [
        "We use the code you connect only to review it and to find and fix problems for you. We never use customer "
        "code to train our models. If you run ogbon-1 on your own servers, your code doesn't reach us.",
    ]),
    ("Who we share it with", [
        [
            "The insurer that backs our cover warranty where you are, and its reinsurer, to handle claims. In Africa this is "
            "Casava.",
            "Incident responders and investigators working on your incident.",
            "Companies that host our systems, send our emails and messages, and process payments for us. Our contracts "
            "with them require them to protect the data and use it only for us.",
            "Regulators such as the Nigeria Data Protection Commission (NDPC) or the UK Information Commissioner's Office "
            "(ICO), the police or a court, when the law "
            "requires it or when you ask us to help you report an incident.",
        ],
        "We don't sell personal data.",
    ]),
    ("Transfers outside Nigeria", [
        "We and the companies we use may store data outside the country you're in. When that happens we use a "
        "safeguard the law allows, such as a country with adequate protection, contract terms that protect the data, "
        "or your consent.",
    ]),
    ("How long we keep it", [
        "We keep personal data only for as long as we need it for the purposes above, including the time it takes to "
        "settle any claim and the records the law requires us to keep. After that we delete it or remove anything that "
        "identifies you.",
    ]),
    ("How we protect it", [
        "We protect personal data with access controls, encryption and monitoring. Access to the tools you connect is "
        "read-only, and our staff can see customer data only when their work needs it.",
        "If a breach of personal data is likely to put people at risk, we tell the regulator within the time the law "
        "sets, which is 72 hours under the NDPA and the UK GDPR, and we tell the people affected when the risk to them "
        "is high.",
    ]),
    ("Your rights", [
        "Depending on where you live, data protection law lets you ask us to:",
        [
            "Tell you what personal data we hold about you and give you a copy.",
            "Correct data that is wrong or incomplete.",
            "Delete your data, or stop or limit how we use it.",
            "Give you your data in a format you can take to another provider.",
            "Stop using your data for marketing.",
        ],
        "Where we rely on your consent, you can withdraw it at any time. To use any of these rights, email "
        "secure@ogbon.com. We may need to confirm who you are first. If you're not happy with our reply, you can "
        "complain to the data protection regulator where you live, such as the NDPC in Nigeria or the ICO in the UK.",
    ]),
    ("Children", [
        "Ogbon is a service for organisations. It isn't meant for anyone under 18, and we don't knowingly collect their "
        "data.",
    ]),
    ("Changes to this policy", [
        "We'll post any changes on this page and update the date at the top. If a change affects how we use your data "
        "in an important way, we'll email the contact on your account first.",
    ]),
]

TERMS_INTRO = (
    "These terms apply to ogbon.com, the free security report, and Ogbon's services: the dashboard, monitoring, the "
    "fix list, incident response, ogbon-1, Ogbon Harness and the Ogbon API. When your company signs up for a plan, "
    "your order form and your cover agreement also apply. If they say something different from these terms, the "
    "order form and the cover agreement win."
)

TERMS = [
    ("Who we are", [
        "Ogbon is run by Ogbon Security Limited, a company registered in Nigeria. " + CONTACT,
    ]),
    ("The free security report", [
        "Only ask for a report on a domain your company owns or that you have permission to check. We check only "
        "information that is already public and don't access your systems.",
        "The expected loss figures in a report are estimates, based on what we can see from outside and the typical "
        "cost of attacks on organisations like yours. They are not a quote, an offer of cover or a promise that nothing "
        "else is wrong.",
    ]),
    ("Your account", [
        "Ogbon is for organisations. The person who signs up must have the authority to accept these terms for the "
        "company. Keep your account details accurate and your logins safe. You are responsible for what happens under "
        "your account.",
    ]),
    ("Plans and payment", [
        "You pay the fees in your order form, in advance, for each billing period, in the currency the order form "
        "sets: US dollars, pounds sterling or naira. Your price depends on your team "
        "size, industry and security score, and may change at renewal to reflect your score. Prices don't include VAT "
        "or other taxes unless the order form says so.",
        "If a payment is late, we'll tell you. If it stays unpaid, we may pause the service and your cover until it's "
        "paid.",
    ]),
    ("Cover", [
        "Ogbon is not an insurer, and the cover in your plan is not an insurance policy. It is a warranty from Ogbon "
        "Security Limited: if a covered attack gets through while you're protected, we pay for the loss up to your "
        "plan's limit. For customers in Africa, our obligations under the warranty are backed by Casava, an insurer "
        "licensed by the National Insurance Commission (NAICOM) in Nigeria. For customers in the US and UK, they will "
        "be backed by insurers licensed in those countries. Your Ogbon agreement sets out what is covered, the limits, "
        "the currency, the excess and the "
        "exclusions. You'll get the full warranty terms before you sign.",
        "To stay covered, keep the six basics in place, fix critical issues by their due date or agree a new date with "
        "us before it passes, and report incidents to us within 72 hours.",
    ]),
    ("Connecting your tools", [
        "When you connect your cloud accounts, code or other systems, you give us read-only access to them. Only connect "
        "tools your company has the right to share with us. You can disconnect at any time, but staying connected is "
        "one of the basics your cover depends on.",
    ]),
    ("ogbon-1, Ogbon Harness and the API", [
        [
            "You own your code and the changes ogbon-1 suggests for it. We never use your code to train our models.",
            "Review every change before it goes into your code. ogbon-1 can make mistakes, and your engineers decide "
            "what gets merged.",
            "Keep your API keys secret. You are responsible for use of your keys.",
            "If you run ogbon-1 on your own servers, you may use it only for your company's own work while your plan "
            "is active, and you may not copy, share or resell the model.",
            "We may set fair limits on how much you use the API, and we'll tell you before they affect you.",
        ],
    ]),
    ("Acceptable use", [
        "Don't use Ogbon to test, scan or attack systems you don't own or don't have permission to test, to break the "
        "law, to interfere with our service, or to resell Ogbon without a written agreement with us.",
    ]),
    ("What we promise, and what we can't", [
        "We provide Ogbon with reasonable skill and care. No security service can stop every attack. Monitoring, the "
        "fix list and ogbon-1 lower your risk, and your cover pays for covered losses, but we can't promise that you "
        "won't be attacked.",
    ]),
    ("Confidentiality", [
        "We keep your company's information confidential and use it only to provide Ogbon. You keep confidential "
        "anything we share with you that isn't public, including the terms of your cover.",
    ]),
    ("Ownership", [
        "We own Ogbon, including our software, models and reports. You own your data and your code, and you let us "
        "use them only to provide Ogbon to you. How we handle personal data is set out in our privacy policy.",
    ]),
    ("Limits on our liability", [
        "Payments for covered losses are made under your cover agreement, not these terms. Apart from those, our total "
        "liability to you in any 12 months is limited to the fees you paid us in those 12 months, and we are not "
        "liable for indirect losses such as lost profit or reputation. Nothing in these terms limits liability that "
        "the law doesn't allow us to limit.",
    ]),
    ("Cancelling", [
        "You can cancel at the end of any billing period. We don't refund cover you haven't used. We may end or pause your "
        "account if you don't pay or seriously break these terms. When your account ends, your cover ends, and we "
        "delete your data as described in our privacy policy.",
    ]),
    ("Changes to these terms", [
        "We may update these terms. We'll post the new version here, and for important changes we'll email the "
        "contact on your account at least 30 days before they take effect.",
    ]),
    ("Law and disputes", [
        "These terms are governed by the laws of the Federal Republic of Nigeria. If there's a dispute, we'll first "
        "try to settle it by talking. If that doesn't work, the courts of Lagos State will decide it.",
    ]),
]
