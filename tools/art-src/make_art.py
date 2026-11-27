"""Draws the card illustrations in tools/partials/art: thin outlines, one blue accent each, isometric blocks.
Run: python3 tools/art-src/make_art.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "partials" / "art"
C, S = 0.866, 0.5
BLUE = ("#5A95F2", "#1362DD", "#0E4CB0")  # top, left, right faces


def pt(p):
    return f"{p[0]:.1f},{p[1]:.1f}"


def box(x, y, a, b, h, accent=False, cls="", dashed=False):
    """Isometric box. (x, y) is the top face's back corner; a runs down-right, b down-left, h is height."""
    p0 = (x, y)
    p1 = (x + a * C, y + a * S)
    p2 = (p1[0] - b * C, p1[1] + b * S)
    p3 = (x - b * C, y + b * S)
    d = lambda p: (p[0], p[1] + h)
    top = [p0, p1, p2, p3]
    left = [p3, p2, d(p2), d(p3)]
    right = [p2, p1, d(p1), d(p2)]
    poly = lambda ps, f: f'<path d="M{" L".join(pt(p) for p in ps)}Z" fill="{f}"/>'
    if accent:
        body = poly(top, BLUE[0]) + poly(left, BLUE[1]) + poly(right, BLUE[2])
        body = body.replace('"/>', '" stroke="none"/>')
    else:
        dash = ' stroke-dasharray="3 3"' if dashed else ""
        body = (poly(top, "#fff") + poly(left, "#F7F5F8") + poly(right, "#EFECF1")).replace('"/>', f'"{dash}/>')
    c = f' class="{cls}"' if cls else ""
    return f"<g{c}>{body}</g>"


def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" fill="none" stroke="currentColor" stroke-width="1" '
            f'stroke-linejoin="round" aria-hidden="true">\n{body}\n</svg>\n')


def write(name, w, h, body):
    (OUT / f"{name}.svg").write_text(svg(w, h, body))


# Daily checks: three systems on a line; a blue check travels between them.
write("checks", 320, 180, "\n".join([
    box(70, 44, 32, 32, 24), box(160, 38, 32, 32, 30), box(250, 44, 32, 32, 24),
    '<path class="soft" d="M70 132H250" stroke-dasharray="2 4"/>',
    '<circle cx="70" cy="132" r="2.5" fill="#fff"/><circle cx="160" cy="132" r="2.5" fill="#fff"/><circle cx="250" cy="132" r="2.5" fill="#fff"/>',
    '<g class="travel-x">' + box(70, 117, 11, 11, 8, accent=True) + "</g>",
    '<text x="70" y="158" class="t" text-anchor="middle">website</text>',
    '<text x="160" y="158" class="t" text-anchor="middle">api</text>',
    '<text x="250" y="158" class="t" text-anchor="middle">cloud</text>',
]))

# Security score: bars that rise as fixes land; the latest is blue.
write("score", 320, 180, "\n".join([
    '<path class="soft" d="M56 152H264"/>',
    box(98, 112, 20, 20, 18), box(138, 100, 20, 20, 30), box(178, 86, 20, 20, 44),
    '<g class="rise">' + box(218, 64, 20, 20, 66, accent=True) + "</g>",
    '<path class="soft" d="M98 104L138 92L178 78L218 56" stroke-dasharray="2 4"/>',
]))

# Pentest coverage: most systems untested; the few a yearly test covers are blue.
cov = []
for r in range(3):
    for c in range(5):
        x, y = 160 + (c - r) * 26, 36 + (c + r) * 15
        cov.append(box(x, y, 24, 24, 8, accent=(r, c) in {(0, 2), (1, 3)}))
write("coverage", 320, 180, "\n".join(cov))

# Fix list: three plates; the one that matters most is blue and lifts.
write("fixlist", 320, 180, "\n".join([
    box(160, 96, 70, 70, 8), box(160, 72, 70, 70, 8),
    '<g class="float">' + box(160, 40, 70, 70, 8, accent=True) + "</g>",
]))

# Incident response: a call reaching the centre.
write("response", 320, 180, "\n".join([
    '<circle class="soft" cx="160" cy="90" r="70"/>',
    '<circle class="soft" cx="160" cy="90" r="46"/>',
    '<circle class="ping" cx="160" cy="90" r="22" stroke="#1362DD"/>',
    '<path class="soft" d="M20 150L118 104" stroke-dasharray="2 4"/>',
    '<circle cx="20" cy="150" r="4" fill="#fff"/>',
    '<circle cx="160" cy="90" r="14" fill="#1362DD" stroke="none"/>',
]))

# Cover: a solid shield inside two outlines.
shield = "M160 {t}c{a} {b} {c} {d} {e} {d}v{f}c0 {g} -{h} {i} -{e2} {j}c-{e2} -{k} -{e2} -{l} -{e2} -{m}V{n}c{o} 0 {p} -{q} {e2} -{r}z"
write("cover", 320, 180, "\n".join([
    '<path class="soft" d="M160 12c28 15 50 20 68 20v58c0 44-30 66-68 79-38-13-68-35-68-79V32c18 0 40-5 68-20z"/>',
    '<path class="soft" d="M160 28c22 12 40 16 54 16v46c0 35-24 52-54 62-30-10-54-27-54-62V44c14 0 32-4 54-16z"/>',
    '<path d="M160 44c16 9 28 12 38 12v34c0 26-17 39-38 46-21-7-38-20-38-46V56c10 0 22-3 38-12z" fill="#1362DD" stroke="none"/>',
    '<path class="draw" d="M146 92l10 10 20-22" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>',
]))

# ogbon-1: a laptop and a server stack, the model in between.
write("model", 320, 180, "\n".join([
    '<path d="M28 114L66 92V48L28 70Z" fill="#fff"/>',
    box(66, 92, 60, 44, 6),
    box(254, 84, 40, 40, 20), box(254, 64, 40, 40, 20), box(254, 44, 40, 40, 20),
    '<path class="soft" d="M108 100L148 86M176 86L216 100" stroke-dasharray="2 4"/>',
    '<g class="float">' + box(162, 64, 22, 22, 22, accent=True) + "</g>",
]))

# APIs: two systems; one blue block slips out of the stream.
write("apis", 240, 140, "\n".join([
    box(64, 46, 34, 34, 26), box(176, 46, 34, 34, 26),
    '<path class="soft" d="M90 88L150 88" stroke-dasharray="2 4"/>',
    '<g class="leak">' + box(120, 80, 10, 10, 8, accent=True) + "</g>",
]))

# Business logic: a limit line, and the one transfer that goes past it.
write("logic", 240, 140, "\n".join([
    '<path class="soft" d="M30 58H210" stroke-dasharray="4 4"/>',
    box(70, 92, 24, 24, 10), box(70, 82, 24, 24, 10),
    box(120, 92, 24, 24, 10), box(120, 82, 24, 24, 10), box(120, 72, 24, 24, 10),
    box(170, 92, 24, 24, 10), box(170, 82, 24, 24, 10), box(170, 72, 24, 24, 10),
    '<g class="float">' + box(170, 40, 24, 24, 10, accent=True) + "</g>",
]))

# Identity and access: three doors; one is open to more than it should be.
write("identity", 240, 140, "\n".join([
    box(62, 40, 10, 34, 56), box(120, 40, 10, 34, 56),
    '<g class="float">' + box(178, 32, 10, 34, 64, accent=True) + "</g>",
    '<path class="soft" d="M20 120H220"/>',
]))

# Forgotten systems: a tidy grid, and one tile left outside it.
tiles = []
for r in range(2):
    for c in range(3):
        tiles.append(box(70 + c * 26 - r * 26, 44 + c * 15 + r * 15, 26, 26, 6))
write("forgotten", 240, 140, "\n".join(tiles + [
    '<path class="soft" d="M128 100L168 112" stroke-dasharray="2 4"/>',
    '<g class="fade">' + box(196, 82, 26, 26, 6, accent=True) + "</g>",
]))
print("ok")
