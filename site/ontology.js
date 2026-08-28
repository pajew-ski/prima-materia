import { onThemeChange } from "./theme.js";

// One shape per kind of term. The distinction the ontology cares about most —
// process classes against the instances asserted under them — is the one the
// eye gets for free: round for the vocabulary, angular for what is said in it.
const KINDS = {
  root: { shape: "ellipse", legend: "Root process", plural: "root processes" },
  class: { shape: "ellipse", legend: "Class", plural: "classes" },
  property: { shape: "round-tag", legend: "Property", plural: "properties" },
  instance: { shape: "round-rectangle", legend: "Instance", plural: "instances" },
  tradition: { shape: "round-diamond", legend: "Tradition", plural: "traditions" },
};

// Rings from the center outward: the root process, the classes that divide it,
// the properties that relate them, and the instances asserted under them.
const RING = { root: 0, class: 1, property: 2, instance: 3, tradition: 3 };
// Ring radii. The gap between rings stays wider than a wrapped label, and the
// outermost ring sits close enough in that the fitted graph still resolves its
// labels: the canvas is roughly square at desktop sizes, so what the layout
// costs in radius it gains in zoom.
const RADIUS = [0, 140, 260, 380];

// Cytoscape draws on a canvas and understands neither CSS custom properties
// nor oklch, so tokens are resolved to plain rgb through a one pixel canvas.
const probe = document.createElement("canvas");
probe.width = probe.height = 1;
function resolve(token) {
  const ctx = probe.getContext("2d", { willReadFrequently: true });
  ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue(token).trim();
  ctx.fillRect(0, 0, 1, 1);
  const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
  return `rgb(${r}, ${g}, ${b})`;
}

function graphStyle() {
  const bg = resolve("--bg");
  const border = resolve("--border");
  const text = resolve("--text");
  const muted = resolve("--text-muted");
  const font = getComputedStyle(document.body).fontFamily;
  return [
    {
      selector: "node",
      style: {
        shape: (n) => KINDS[n.data("kind")].shape,
        width: 21,
        height: 21,
        "background-color": bg,
        "border-width": 1,
        "border-color": muted,
        label: (n) => n.data("label"),
        "font-family": font,
        "font-size": 10,
        color: muted,
        "text-valign": "bottom",
        "text-margin-y": 5,
        "text-wrap": "wrap",
        "text-max-width": 68,
      },
    },
    {
      selector: 'node[kind = "root"]',
      style: { width: 34, height: 34, "background-color": text, "border-color": text },
    },
    {
      selector: "node:selected",
      style: {
        "border-color": text,
        color: text,
        "underlay-color": muted,
        "underlay-opacity": 0.2,
        "underlay-padding": 5,
      },
    },
    {
      selector: "edge",
      style: {
        width: 1,
        "curve-style": "bezier",
        "line-color": border,
        "target-arrow-shape": "triangle",
        "target-arrow-color": border,
        "arrow-scale": 0.7,
        opacity: 0.55,
        // The predicate rides on the edge itself, so the meaning of a link is
        // legible in the graph without opening the panel. autorotate keeps it
        // aligned with the line; the background chip lifts it off crossing edges.
        label: (e) => e.data("rel"),
        "font-family": font,
        "font-size": 7,
        color: muted,
        "text-rotation": "autorotate",
        "text-background-color": bg,
        "text-background-opacity": 1,
        "text-background-padding": 1,
        "text-background-shape": "roundrectangle",
      },
    },
    {
      selector: "edge.adjacent",
      style: { "line-color": muted, "target-arrow-color": muted, opacity: 1, color: text, "font-size": 10 },
    },
  ];
}

const data = await (await fetch("ontology-data.json")).json();
const panel = document.querySelector("#panel");
const nodesById = new Map(data.nodes.map((n) => [n.id, n]));

// The prose above the graph counts the vocabulary. Take those numbers from the
// same data the visualization is drawn from, so adding a term can never leave
// the sentence behind. It runs before cytoscape is touched, so a failed CDN
// load costs the graph but not the text.
const ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
  "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
const TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
function spell(n) {
  if (n < 20) return ONES[n];
  if (n < 100) return n % 10 ? `${TENS[(n / 10) | 0]}-${ONES[n % 10]}` : TENS[(n / 10) | 0];
  return String(n); // past ninety-nine the digits read better than the words anyway
}
document.querySelector("#term-count").textContent =
  `${spell(data.nodes.length)} terms bound by ${spell(data.edges.length)} relations`;

// The footer states when the site was generated and from how many triples, so a
// stale deployment is visible rather than merely suspected.
const built = new Date(data.meta.generated);
document.querySelector("#build-meta").textContent =
  `${data.meta.triples} triples, built ${built.toISOString().slice(0, 10)} · `;

// Legend entries are derived from the kinds actually present. An ontology that
// has grown its first tradition shows a tradition swatch; one that has not,
// does not — the key never promises a shape the graph is not drawing.
const SWATCH = {
  ellipse: (fill) => `<circle cx="8" cy="6" r="${fill ? 5.5 : 5}" ${fill ? 'fill="currentColor"' : 'fill="none" stroke="currentColor"'}/>`,
  "round-rectangle": () => '<rect x="1.5" y="1.5" width="13" height="9" rx="2.5" fill="none" stroke="currentColor"/>',
  "round-tag": () => '<path d="M1.5 3.5a2 2 0 0 1 2-2h7l4 4.5-4 4.5h-7a2 2 0 0 1-2-2z" fill="none" stroke="currentColor"/>',
  "round-diamond": () => '<path d="M8 1 14.5 6 8 11 1.5 6z" fill="none" stroke="currentColor"/>',
};
const legend = document.querySelector("#legend");
for (const [kind, { shape, legend: name }] of Object.entries(KINDS)) {
  if (!data.nodes.some((n) => n.kind === kind)) continue;
  const item = document.createElement("span");
  item.innerHTML =
    `<svg width="16" height="12" viewBox="0 0 16 12" aria-hidden="true">${SWATCH[shape](kind === "root")}</svg>`;
  item.append(name);
  legend.append(item);
}

// Radial layout: the root process sits at the center, the classes form the
// inner ring, and properties and instances sit on outer rings. Each outer node
// is pulled toward the mean angle of the inner neighbours it connects to, so a
// property lands between its domain and range and an instance beside its class.
// Positions are in model space; cytoscape fits them to the canvas.
function radialPositions(nodes, edges) {
  const neighbours = new Map(nodes.map((n) => [n.id, []]));
  for (const e of edges) {
    neighbours.get(e.source)?.push(e.target);
    neighbours.get(e.target)?.push(e.source);
  }
  const angle = new Map(); // only ring nodes get an angle; the center has none
  const pos = {};
  const place = (id, r, a) => {
    angle.set(id, a);
    pos[id] = { x: r * Math.cos(a), y: r * Math.sin(a) };
  };
  const meanAngle = (as) => {
    if (!as.length) return null;
    const x = as.reduce((s, a) => s + Math.cos(a), 0);
    const y = as.reduce((s, a) => s + Math.sin(a), 0);
    return x === 0 && y === 0 ? null : Math.atan2(y, x);
  };
  const anchorOf = (id) =>
    meanAngle(neighbours.get(id).map((t) => angle.get(t)).filter((v) => v != null));

  // Center: position only, no angle, so it never biases an outer node's anchor.
  const center = nodes.find((n) => n.kind === "root");
  if (center) pos[center.id] = { x: 0, y: 0 };

  // Inner ring: classes, evenly spaced, with the subclasses of the root process
  // grouped ahead of the classes that stand on their own.
  const subclassOfRoot = new Set(
    edges.filter((e) => e.rel === "subClassOf" && e.target === center?.id).map((e) => e.source),
  );
  const classes = nodes
    .filter((n) => RING[n.kind] === 1)
    .sort(
      (a, b) =>
        Number(subclassOfRoot.has(b.id)) - Number(subclassOfRoot.has(a.id)) ||
        a.id.localeCompare(b.id),
    );
  classes.forEach((n, i) => place(n.id, RADIUS[1], -Math.PI / 2 + (i * 2 * Math.PI) / classes.length));

  // Widest circular gap in a sorted angle list; returns its midpoint. Used to
  // slot nodes that have no inner neighbour to anchor to.
  const widestGapMid = (sorted) => {
    if (sorted.length === 0) return -Math.PI / 2;
    let gi = 0, best = -1;
    for (let i = 0; i < sorted.length; i++) {
      let g = sorted[(i + 1) % sorted.length] - sorted[i];
      if (g <= 0) g += 2 * Math.PI;
      if (g > best) { best = g; gi = i; }
    }
    let a1 = sorted[gi], a2 = sorted[(gi + 1) % sorted.length];
    if (a2 <= a1) a2 += 2 * Math.PI;
    return (a1 + a2) / 2;
  };

  // Place one ring: order the nodes by the angle of their inner neighbours, then
  // space them evenly (so labels never collide) and rotate the whole ring by the
  // offset that best lines the nodes up with those neighbours. Nodes without an
  // inner neighbour drop into the widest gap so they land somewhere sensible.
  const placeRing = (ring, radius) => {
    const n = ring.length;
    if (n === 0) return;
    const items = ring.map((node) => ({ id: node.id, a: anchorOf(node.id) }));
    const used = items.filter((it) => it.a != null).map((it) => it.a).sort((x, y) => x - y);
    for (const it of items) {
      if (it.a != null) continue;
      it.a = widestGapMid(used);
      used.push(((it.a % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI));
      used.sort((x, y) => x - y);
    }
    items.sort((p, q) => p.a - q.a);
    let sx = 0, sy = 0;
    items.forEach((it, i) => {
      const anchor = anchorOf(it.id);
      if (anchor == null) return;
      const even = (i * 2 * Math.PI) / n;
      sx += Math.cos(anchor - even);
      sy += Math.sin(anchor - even);
    });
    const offset = sx === 0 && sy === 0 ? -Math.PI / 2 : Math.atan2(sy, sx);
    items.forEach((it, i) => place(it.id, radius, (i * 2 * Math.PI) / n + offset));
  };

  placeRing(nodes.filter((node) => RING[node.kind] === 2), RADIUS[2]);
  placeRing(nodes.filter((node) => RING[node.kind] === 3), RADIUS[3]);
  return pos;
}

const cy = cytoscape({
  container: document.querySelector("#canvas"),
  elements: [
    ...data.nodes.map((n) => ({ data: { id: n.id, kind: n.kind, label: n.label } })),
    ...data.edges.map((e) => ({
      data: { id: `${e.source}~${e.rel}~${e.target}`, source: e.source, target: e.target, rel: e.rel },
    })),
  ],
  style: graphStyle(),
  layout: {
    name: "preset",
    positions: radialPositions(data.nodes, data.edges),
    padding: 34,
    fit: true,
  },
  // The floor must sit below the fit zoom of the smallest phones (~0.11 on a
  // 320px viewport), or fit() clamps and crops the graph instead of fitting it.
  minZoom: 0.1,
  maxZoom: 3,
});

function chip(edge, direction) {
  const button = document.createElement("button");
  button.className = "edge-chip";
  const rel = document.createElement("span");
  rel.className = "rel";
  rel.textContent = direction === "out" ? `${edge.rel} → ` : `← ${edge.rel} `;
  const target = document.createElement("span");
  const other = direction === "out" ? edge.target : edge.source;
  target.textContent = nodesById.get(other)?.label ?? other;
  button.append(rel, target);
  button.addEventListener("click", () => select(other));
  return button;
}

function edgeList(title, edges, direction) {
  if (edges.length === 0) return [];
  const heading = document.createElement("h4");
  heading.textContent = title;
  const list = document.createElement("div");
  list.className = "edge-list";
  for (const edge of edges) list.append(chip(edge, direction));
  return [heading, list];
}

function paragraph(text, className) {
  const p = document.createElement("p");
  if (className) p.className = className;
  p.textContent = text;
  return p;
}

function bullets(title, items) {
  if (items.length === 0) return [];
  const heading = document.createElement("h4");
  heading.textContent = title;
  const list = document.createElement("ul");
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item;
    list.append(li);
  }
  return [heading, list];
}

function showNode(id) {
  const node = nodesById.get(id);
  const parts = [paragraph(node.kind, "panel-type")];

  const name = document.createElement("h3");
  name.textContent = node.label;
  parts.push(name, paragraph(node.id, "panel-id"));

  // Labels in every language but the one already in the heading. The ontology
  // is bilingual by design; the panel should not quietly hide half of it.
  const others = Object.entries(node.labels)
    .filter(([lang, text]) => text !== node.label && lang)
    .map(([lang, text]) => `${lang} · ${text}`);
  if (others.length) parts.push(paragraph(others.join(" · "), "panel-aside"));

  // A property's signature, including targets outside this graph. An absent
  // domain or range is no constraint at all, so it reads as "any" rather than
  // as a blank the reader has to interpret.
  if (node.domain || node.range) {
    const side = (values) => (values ?? ["any"]).join(", ");
    parts.push(paragraph(`${side(node.domain)} → ${side(node.range)}`, "panel-aside"));
  }

  const definition = node.definition.en ?? node.definition[""];
  if (definition) parts.push(paragraph(definition));
  const comment = node.comment.en ?? node.comment[""];
  if (comment) parts.push(paragraph(comment, "panel-note"));
  const note = node.note.en ?? node.note[""];
  if (note) parts.push(paragraph(note, "panel-note"));

  parts.push(
    ...bullets("sources", node.sources),
    ...edgeList("relations out", data.edges.filter((e) => e.source === id), "out"),
    ...edgeList("relations in", data.edges.filter((e) => e.target === id), "in"),
  );
  panel.replaceChildren(...parts);
}

// With nothing selected the panel reports what the graph is made of. The counts
// come from the data, so the breakdown grows with the ontology rather than
// describing the shape it had when this was written.
function showSummary() {
  const counts = new Map();
  for (const node of data.nodes) counts.set(node.kind, (counts.get(node.kind) ?? 0) + 1);
  const composition = Object.entries(KINDS)
    .filter(([kind]) => counts.has(kind))
    .map(([kind, { legend, plural }]) => {
      const n = counts.get(kind);
      return `${n} ${n === 1 ? legend.toLowerCase() : plural}`;
    });
  panel.replaceChildren(
    paragraph(
      `${data.nodes.length} terms bound by ${data.edges.length} relations: ${composition.join(", ")}.`,
      "panel-empty",
    ),
    paragraph("Select a term to read its definition and follow its relations.", "panel-empty"),
  );
}

function select(id) {
  cy.elements().unselect();
  const node = cy.$id(id);
  node.select();
  cy.animate({ center: { eles: node } }, { duration: 233 });
}

cy.on("select", "node", (e) => {
  showNode(e.target.id());
  e.target.connectedEdges().addClass("adjacent");
  // Every term gets a URL, so a definition can be cited rather than described.
  history.replaceState(null, "", `#${e.target.id()}`);
});

cy.on("unselect", "node", (e) => {
  e.target.connectedEdges().removeClass("adjacent");
  if (cy.$("node:selected").length === 0) {
    showSummary();
    history.replaceState(null, "", location.pathname + location.search);
  }
});

onThemeChange(() => cy.style(graphStyle()));

// Keep the graph fitted to its container across window resizes, orientation
// flips, and the portrait/landscape reflow that changes the canvas dimensions.
// A ResizeObserver on the canvas catches every size change, not just
// window-level ones, and fires once on attach so the initial layout is fitted
// to the settled box rather than whatever size it had mid-render.
const canvas = document.querySelector("#canvas");
let resizeTimer;
new ResizeObserver(() => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    cy.resize();
    cy.fit(undefined, 34);
  }, 120);
}).observe(canvas);

// A term URL should land on the term. On the first load the graph is scrolled
// into view as well, since the hash names no element the browser could reach.
function selectFromHash(scroll) {
  const id = decodeURIComponent(location.hash.slice(1));
  if (!nodesById.has(id)) {
    showSummary();
    return;
  }
  select(id);
  if (scroll) document.querySelector("#graph").scrollIntoView({ block: "start" });
}
window.addEventListener("hashchange", () => selectFromHash(false));
selectFromHash(true);

// The ontology is also explorable from the browser console.
window.cy = cy;
