// Generates the pixel logo, favicons/app icons and hero glyphs.
// Run: node tools/pixels.mjs   (writes into ../assets)
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { deflateSync } from "node:zlib";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "assets");
mkdirSync(join(root, "glyphs"), { recursive: true });

// Merge each row's runs of "#" into rects so the SVG stays small and seam-free.
function rects(rows, ox = 0, oy = 0) {
  const out = [];
  rows.forEach((row, y) => {
    let x = 0;
    while (x < row.length) {
      if (row[x] !== "#") { x++; continue; }
      let w = 0;
      while (row[x + w] === "#") w++;
      out.push(`<rect x="${ox + x}" y="${oy + y}" width="${w}" height="1"/>`);
      x += w;
    }
  });
  return out.join("");
}

function svg(rows, fill = "currentColor", extra = "") {
  const w = Math.max(...rows.map((r) => r.length));
  const h = rows.length;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" shape-rendering="crispEdges" fill="${fill}"${extra}>${rects(rows)}</svg>`;
}

// Wordmark in the "tiny" style: 3-unit x-height, 1-unit ascender and descender,
// corners notched instead of curved, 1-unit letter spacing.
const font = {
  o: ["...", "###", "#.#", "###", "..."],
  g: ["...", "###", "#.#", ".##", "##."],
  b: ["#..", "##.", "#.#", "###", "..."],
  n: ["...", "##.", "#.#", "#.#", "..."],
  ".": [".", ".", ".", "#", "."],
};

function word(text) {
  const rows = ["", "", "", "", ""];
  [...text].forEach((ch, i) => {
    font[ch].forEach((r, y) => (rows[y] += (i ? "." : "") + r));
  });
  return rows;
}

const logo = word("ogbon.");
writeFileSync(join(root, "logo.svg"), svg(logo, "#141413"));
writeFileSync(join(root, "logo-light.svg"), svg(logo, "#EEE9E3"));

// ---------- Icons: the "o" in cream on a dark tile ----------
// Each size gets its own unit and offset so every edge lands on a whole pixel.
const site = join(root, "..");
mkdirSync(join(root, "icons"), { recursive: true });
const TILE = [0x20, 0x1f, 0x1d, 255];
const INK = [0xee, 0xe9, 0xe3, 255];
const oRows = font.o.slice(1, 4);

function tile(size, unit, off) {
  const px = Buffer.alloc(size * size * 4);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const ux = Math.floor((x - off) / unit), uy = Math.floor((y - off) / unit);
      const on = x >= off && y >= off && oRows[uy]?.[ux] === "#";
      px.set(on ? INK : TILE, (y * size + x) * 4);
    }
  }
  return png(size, size, px);
}

const crcTable = Array.from({ length: 256 }, (_, n) => {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});
const crc32 = (buf) => {
  let c = 0xffffffff;
  for (const b of buf) c = crcTable[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
};
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type), data]);
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}
function png(w, h, rgba) {
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4);
  ihdr[8] = 8; ihdr[9] = 6; // 8-bit RGBA
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) rgba.copy(raw, y * (w * 4 + 1) + 1, y * w * 4, (y + 1) * w * 4);
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk("IHDR", ihdr), chunk("IDAT", deflateSync(raw, { level: 9 })), chunk("IEND", Buffer.alloc(0)),
  ]);
}
// ICO container holding PNG frames (supported by every current browser).
function ico(frames) {
  const head = Buffer.alloc(6 + frames.length * 16);
  head.writeUInt16LE(1, 2); head.writeUInt16LE(frames.length, 4);
  let offset = head.length;
  frames.forEach(({ size, data }, i) => {
    const e = 6 + i * 16;
    head[e] = size % 256; head[e + 1] = size % 256;
    head.writeUInt16LE(1, e + 4); head.writeUInt16LE(32, e + 6);
    head.writeUInt32LE(data.length, e + 8); head.writeUInt32LE(offset, e + 12);
    offset += data.length;
  });
  return Buffer.concat([head, ...frames.map((f) => f.data)]);
}

writeFileSync(join(site, "favicon.svg"),
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges"><rect width="16" height="16" fill="#201F1D"/><g fill="#EEE9E3" transform="translate(2 2) scale(4)">${rects(oRows)}</g></svg>`);
writeFileSync(join(site, "favicon.ico"), ico([
  { size: 16, data: tile(16, 4, 2) },
  { size: 32, data: tile(32, 8, 4) },
  { size: 48, data: tile(48, 12, 6) },
]));
writeFileSync(join(site, "apple-touch-icon.png"), tile(180, 30, 45));
writeFileSync(join(root, "icons", "icon-192.png"), tile(192, 32, 48));
writeFileSync(join(root, "icons", "icon-512.png"), tile(512, 84, 130));
// Maskable: keep the mark inside the 80% safe circle.
writeFileSync(join(root, "icons", "icon-maskable-512.png"), tile(512, 64, 160));

// Hero glyphs: compute motifs drawn on the same pixel grid as the wordmark.
const glyphs = {
  chip: [
    "...#..#..#...",
    ".###########.",
    ".#.........#.",
    "##.#######.##",
    ".#.#.....#.#.",
    ".#.#.....#.#.",
    "##.#..#..#.##",
    ".#.#.....#.#.",
    ".#.#.....#.#.",
    "##.#######.##",
    ".#.........#.",
    ".###########.",
    "...#..#..#...",
  ],
  cores: [
    "###..###..###", "###..###..###", "###..###..###", ".............", ".............",
    "###..###..###", "###..###..###", "###..###..###", ".............", ".............",
    "###..###..###", "###..###..###", "###..###..###",
  ],
  mesh: Array.from({ length: 13 }, (_, y) => (y % 2 ? "............." : "#.#.#.#.#.#.#")),
  network: [
    "###.......###",
    "#############",
    "###.......###",
    ".#.#.....#.#.",
    ".#..#...#..#.",
    ".#...###...#.",
    ".#...###...#.",
    ".#...###...#.",
    ".#..#...#..#.",
    ".#.#.....#.#.",
    "###.......###",
    "#############",
    "###.......###",
  ],
  memory: [
    ".............",
    ".............",
    "#############",
    "#...........#",
    "#.##..#..##.#",
    "#.##.###.##.#",
    "#.##..#..##.#",
    "#...........#",
    "#############",
    ".#.#.#.#.#.#.",
    ".#.#.#.#.#.#.",
    ".............",
    ".............",
  ],
  compiler: [
    "...##...##...",
    "..#.......#..",
    "..#.......#..",
    "..#.......#..",
    "..#.......#..",
    ".#.........#.",
    "#...#.#.#...#",
    ".#.........#.",
    "..#.......#..",
    "..#.......#..",
    "..#.......#..",
    "..#.......#..",
    "...##...##...",
  ],
  matrix: [
    "##.........##",
    "#...........#",
    "#..#..#..#..#",
    "#...........#",
    "#...........#",
    "#..#..#..#..#",
    "#...........#",
    "#...........#",
    "#..#..#..#..#",
    "#...........#",
    "#...........#",
    "#...........#",
    "##.........##",
  ].map((r, y) => (y === 11 ? "#...........#" : r)),
  distribute: [
    ".....###.....",
    ".....###.....",
    ".....###.....",
    "......#......",
    "......#......",
    ".###########.",
    ".#....#....#.",
    ".#....#....#.",
    ".#....#....#.",
    ".#....#....#.",
    "###..###..###",
    "###..###..###",
    "###..###..###",
  ],
  rack: [
    "#############",
    "#.#.#.......#",
    "#############",
    ".............",
    "#############",
    "#.#.#.......#",
    "#############",
    ".............",
    "#############",
    "#.#.#.......#",
    "#############",
    ".............",
    "##.........##",
  ],
  quantize: [
    "..........###",
    "..........#..",
    "..........#..",
    ".......####..",
    ".......#.....",
    ".......#.....",
    "....####.....",
    "....#........",
    "....#........",
    ".####........",
    ".#...........",
    ".#...........",
    "##...........",
  ],
};

for (const [name, rows] of Object.entries(glyphs)) {
  writeFileSync(join(root, "glyphs", `${name}.svg`), svg(rows, "#141413"));
}

// Inline-able wordmark for the HTML (uses currentColor so the nav can recolour it).
console.log(svg(logo, "currentColor", ' class="logo-svg" role="img" aria-label="ogbon."'));
