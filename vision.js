// Vision on compare.html, in two modes. Live: an object detector runs in the browser on the
// visitor's own camera, so no video leaves the device. Race: the same detector runs on a sample
// photo while SwiftInference and GPT-4o Vision replay their measured runs of that photo. The model
// (MediaPipe EfficientDet-Lite0, about 4 MB) only downloads when the visitor starts either one.
const TASKS_URL = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14";
const MODEL_URL = "https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/float16/1/efficientdet_lite0.tflite";

const $ = (s) => document.querySelector(s);
const video = $("[data-video]"), canvas = $("[data-boxes]"), ctx = canvas.getContext("2d");
const idle = $("[data-idle]"), status = $("[data-status]"), cameraBtn = $("[data-camera]"), stopBtn = $("[data-stop]");
const seesEl = $("[data-sees]"), latencyEl = $("[data-latency]"), fpsEl = $("[data-fps]");

let detector = null, stream = null, running = false, lastSentence = "", frames = [], recentMs = [];

// Median of the last 30 frames, so the slow first frames while the model warms up don't skew it.
const medianMs = () => { const s = [...recentMs].sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; };

// "a person", "two cups", joined as "a person, a laptop and two cups".
const WORDS = ["", "a", "two", "three", "four", "five", "six"];
const describe = (names) => {
  if (!names.length) return "Nothing it recognises yet. Try holding up a cup, a phone or a book.";
  const counts = {};
  names.forEach((n) => (counts[n] = (counts[n] || 0) + 1));
  const parts = Object.entries(counts).map(([n, c]) => (c === 1 ? `${/^[aeiou]/.test(n) ? "an" : "a"} ${n}` : `${WORDS[c] || c} ${n}s`));
  const list = parts.length > 1 ? `${parts.slice(0, -1).join(", ")} and ${parts[parts.length - 1]}` : parts[0];
  return `I see ${list}.`;
};

let fileset = null;
async function loadDetector(runningMode = "VIDEO") {
  const { FilesetResolver, ObjectDetector } = await import(`${TASKS_URL}/vision_bundle.mjs`);
  fileset = fileset || (await FilesetResolver.forVisionTasks(`${TASKS_URL}/wasm`));
  const options = (delegate) => ({ baseOptions: { modelAssetPath: MODEL_URL, delegate }, runningMode, scoreThreshold: 0.45, maxResults: 8 });
  try { return await ObjectDetector.createFromOptions(fileset, options("GPU")); }
  catch { return await ObjectDetector.createFromOptions(fileset, options("CPU")); }
}

// Draws boxes on the live canvas by default, or on the race photo's canvas (not mirrored).
function draw(detections, g = ctx, source = video, mirror = true) {
  const ctx = g, c = g.canvas;
  const w = (c.width = source.videoWidth || source.naturalWidth), h = (c.height = source.videoHeight || source.naturalHeight);
  ctx.clearRect(0, 0, w, h);
  ctx.lineWidth = Math.max(2, w / 320);
  ctx.font = `500 ${Math.max(14, Math.round(w / 40))}px Geist, Arial, sans-serif`;
  for (const d of detections) {
    const b = d.boundingBox, label = d.categories[0].categoryName;
    // The live video is mirrored like a selfie, so mirror each box's x to match.
    const x = mirror ? w - b.originX - b.width : b.originX;
    ctx.strokeStyle = "#30D75D";
    ctx.strokeRect(x, b.originY, b.width, b.height);
    const text = `${label} ${Math.round(d.categories[0].score * 100)}%`, pad = 6, th = parseInt(ctx.font.match(/\d+px/)[0], 10) + pad * 2;
    ctx.fillStyle = "#30D75D";
    ctx.fillRect(x, Math.max(0, b.originY - th), ctx.measureText(text).width + pad * 2, th);
    ctx.fillStyle = "#141413";
    ctx.fillText(text, x + pad, Math.max(0, b.originY - th) + th - pad - 2);
  }
}

function loop() {
  if (!running) return;
  if (video.readyState >= 2) {
    const t0 = performance.now();
    const result = detector.detectForVideo(video, t0);
    const ms = performance.now() - t0;
    recentMs.push(ms);
    if (recentMs.length > 30) recentMs.shift();
    frames.push(t0);
    frames = frames.filter((t) => t0 - t < 1000);
    draw(result.detections);
    const med = medianMs();
    latencyEl.textContent = med < 10 ? med.toFixed(1) : Math.round(med);
    fpsEl.textContent = frames.length;
    const sentence = describe(result.detections.map((d) => d.categories[0].categoryName));
    if (sentence !== lastSentence) { lastSentence = sentence; seesEl.textContent = sentence; }
  }
  requestAnimationFrame(loop);
}

async function start() {
  cameraBtn.disabled = true;
  if (!navigator.mediaDevices?.getUserMedia) { status.textContent = "This browser can’t share a camera with web pages."; cameraBtn.disabled = false; return; }
  try {
    status.textContent = "Asking for the camera…";
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } }, audio: false });
    video.srcObject = stream;
    await video.play();
    if (!detector) { status.textContent = "Loading the vision model (about 4 MB)…"; detector = await loadDetector(); }
    idle.hidden = true;
    stopBtn.hidden = false;
    running = true;
    loop();
  } catch (err) {
    stop();
    status.textContent = err && err.name === "NotAllowedError"
      ? "Camera access was blocked. Allow it in your browser settings and try again."
      : "The camera or the model didn’t start. Try again, or use another browser.";
  }
  cameraBtn.disabled = false;
}

function stop() {
  running = false;
  if (stream) stream.getTracks().forEach((t) => t.stop());
  stream = null;
  video.srcObject = null;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  idle.hidden = false;
  stopBtn.hidden = true;
  status.textContent = "Nothing is recorded or uploaded.";
  seesEl.textContent = "Waiting for the camera.";
  latencyEl.textContent = fpsEl.textContent = "–";
  lastSentence = "";
  recentMs = [];
}

cameraBtn.addEventListener("click", start);
stopBtn.addEventListener("click", stop);
document.addEventListener("visibilitychange", () => { if (document.hidden && running) stop(); });

// ---------- Race mode ----------
// Measured October 2026, one run per photo. Anthropic's Claude Vision returned an error on
// every photo, so it has no time.
const PHOTOS = {
  pets: {
    src: "assets/vision/pets.jpg", alt: "Two cats and two dogs on a pink background",
    swift: { ms: 1070, text: "cat (94%), dog (93%), dog (92%), cat (80%)" },
    openai: { ms: 3040, text: "The image shows: 1. A light gray cat. 2. A gray poodle. 3. A corgi dog. 4. Another light gray cat. 5. A pink background." },
  },
  person: {
    src: "assets/vision/person.jpg", alt: "A person in a yoga pose on a beach",
    swift: { ms: 499, text: "person (93%), surfboard (54%)" },
    openai: { ms: 2380, text: "Person practicing yoga in a warrior pose, yoga mat, ocean, sandy beach, sky with clouds." },
  },
  "cat-and-dog": {
    src: "assets/vision/cat-and-dog.jpg", alt: "A cat and a puppy sitting side by side",
    swift: { ms: 686, text: "cat (96%), dog (94%)" },
    openai: { ms: 1830, text: "The image shows a cat and a puppy sitting next to each other on a concrete surface." },
  },
};
const LANES = [
  { key: "ogbon", name: "Ogbon", model: "EfficientDet‑Lite0 · your device", ours: true },
  { key: "swift", name: "SwiftInference", model: "YOLOv8 · measured" },
  { key: "openai", name: "OpenAI", model: "GPT‑4o Vision · measured" },
  { key: "anthropic", name: "Anthropic", model: "Claude Vision · measured" },
];

const raceImg = $("[data-race-img]"), raceCtx = $("[data-race-boxes]").getContext("2d");
const raceRun = $("[data-race-run]"), raceLanesEl = $("[data-race-lanes]"), raceNote = $("[data-race-note]"), chip = $("[data-chip]");
let imageDetector = null, photo = "pets", raceFrame = 0;

const fmt = (ms) => (ms < 1000 ? `${Math.max(1, Math.round(ms))} ms` : `${(ms / 1000).toFixed(2)} s`);
const raceLanes = LANES.map((l) => {
  const el = document.createElement("div");
  el.className = "vrace-lane" + (l.ours ? " is-ours" : "");
  el.innerHTML = `
    <div class="vrace-head"><p class="vrace-name">${l.name}</p><p class="vrace-time" data-time>Ready</p></div>
    <p class="vrace-model">${l.model}</p>
    <p class="vrace-out" data-out></p>
    <div class="lane-track"><span class="lane-stream" data-bar></span></div>`;
  raceLanesEl.appendChild(el);
  return { ...l, el, time: el.querySelector("[data-time]"), out: el.querySelector("[data-out]"), bar: el.querySelector("[data-bar]") };
});

const resetRace = () => {
  cancelAnimationFrame(raceFrame);
  raceCtx.clearRect(0, 0, raceCtx.canvas.width, raceCtx.canvas.height);
  raceLanes.forEach((l) => {
    l.el.classList.remove("is-done", "is-first", "is-failed");
    l.time.textContent = "Ready";
    l.out.textContent = "";
    l.bar.style.width = "0%";
  });
  raceRun.textContent = "Start the race";
  raceRun.disabled = false;
  chip.textContent = "Ready";
};

async function race() {
  resetRace();
  raceRun.disabled = true;
  if (!raceImg.complete) await new Promise((r) => raceImg.addEventListener("load", r, { once: true }));
  if (!imageDetector) {
    raceRun.textContent = "Loading the model…";
    chip.textContent = "Loading about 4 MB";
    try { imageDetector = await loadDetector("IMAGE"); }
    catch { chip.textContent = "The model didn’t load"; raceRun.textContent = "Try again"; raceRun.disabled = false; return; }
  }
  // Warm-up runs on this photo, so the timed run measures inference, not GPU set-up.
  for (let i = 0; i < 3; i++) imageDetector.detect(raceImg);
  raceRun.textContent = "Racing…";
  chip.textContent = "Racing";

  // Ogbon's lane is a real run on this device, timed here; the others replay measured runs.
  const t0 = performance.now();
  const result = imageDetector.detect(raceImg);
  const ogbonMs = performance.now() - t0;
  const p = PHOTOS[photo];
  const runs = {
    ogbon: { ms: ogbonMs, text: result.detections.map((d) => `${d.categories[0].categoryName} (${Math.round(d.categories[0].score * 100)}%)`).join(", ") || "Nothing recognised" },
    swift: p.swift, openai: p.openai,
  };
  const longest = Math.max(...Object.values(runs).map((r) => r.ms));
  const start = performance.now();
  let first = false;
  const tick = (now) => {
    const t = now - start;
    let done = 0;
    for (const l of raceLanes) {
      const r = runs[l.key];
      if (!r) {
        // Anthropic: no time to replay, so it fails once everyone else has finished.
        if (t >= longest) { l.el.classList.add("is-failed"); l.time.textContent = "Error"; l.out.textContent = "No answer."; done++; }
        else l.time.textContent = "Waiting";
        continue;
      }
      l.bar.style.width = `${(Math.min(t, r.ms) / longest) * 100}%`;
      if (t < r.ms) { l.time.textContent = fmt(t); continue; }
      if (!l.el.classList.contains("is-done")) {
        l.el.classList.add("is-done");
        l.time.textContent = fmt(r.ms);
        l.out.textContent = r.text;
        if (!first) { first = true; l.el.classList.add("is-first"); }
        if (l.key === "ogbon") draw(result.detections, raceCtx, raceImg, false);
      }
      done++;
    }
    if (done < raceLanes.length) raceFrame = requestAnimationFrame(tick);
    else { raceRun.textContent = "Race again"; raceRun.disabled = false; chip.textContent = `Ogbon answered in ${fmt(ogbonMs)}`; }
  };
  raceFrame = requestAnimationFrame(tick);
}

raceRun.addEventListener("click", race);
document.querySelectorAll("[data-photo]").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll("[data-photo]").forEach((x) => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
  photo = b.dataset.photo;
  raceImg.src = PHOTOS[photo].src;
  raceImg.alt = PHOTOS[photo].alt;
  resetRace();
}));

document.querySelectorAll("[data-mode]").forEach((b) => b.addEventListener("click", () => {
  const mode = b.dataset.mode;
  document.querySelectorAll("[data-mode]").forEach((x) => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
  document.querySelectorAll("[data-pane]").forEach((pane) => (pane.hidden = pane.dataset.pane !== mode));
  raceNote.hidden = mode !== "race";
  if (mode === "race" && running) stop();
  if (mode === "live") resetRace();
  chip.textContent = "Ready";
}));
