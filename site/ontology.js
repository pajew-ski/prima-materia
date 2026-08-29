import { onThemeChange } from "./theme.js";
import { buildIndex, search, hints } from "./search.js";
import { VIEWS, DEFAULT_VIEW, viewById, context, positionsFor } from "./layouts.js";
import { crosstab, renderMatrix } from "./matrix.js";

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
        // Some arrangements pack three hundred terms tightly enough that every
        // label overlaps at fitted zoom. Rather than drop labels from those
        // views, let the zoom decide: illegible text is hidden until zooming in
        // has made room for it.
        "min-zoomed-font-size": 7,
      },
    },
    {
      selector: 'node[kind = "root"]',
      style: { width: 34, height: 34, "background-color": text, "border-color": text },
    },
    // Landmarks: the root process, the classes and the traditions. They are
    // forty terms out of three hundred, and they are the ones that name a
    // region of the drawing — a sector in the tradition view, a block in the
    // claim-form view. Their labels are set large enough to clear the zoom
    // floor at fitted zoom, so the arrangements stay readable as arrangements
    // instead of as three hundred anonymous squares.
    {
      selector: 'node[kind = "root"], node[kind = "class"], node[kind = "tradition"]',
      style: { "font-size": 15, "text-max-width": 130, color: text },
    },
    // A search result names itself for the same reason: the point of dimming
    // the rest is to be able to read what survived.
    {
      selector: "node.match",
      style: { "font-size": 13, "text-max-width": 110 },
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
    // A search result, marked in the graph itself. Reading a result list tells
    // you what matched; seeing the same matches land in one sector or scatter
    // across all of them tells you something the list cannot.
    {
      selector: "node.match",
      style: { "border-color": text, "border-width": 2, color: text, "background-color": bg },
    },
    {
      selector: ".dimmed",
      style: { opacity: 0.12, "text-opacity": 0 },
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
        "min-zoomed-font-size": 7,
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
const graphContext = context(data);

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

const canvas = document.querySelector("#canvas");
const matrixBox = document.querySelector("#matrix");
const viewNote = document.querySelector("#view-note");
const viewBar = document.querySelector("#views");

// Cytoscape comes off a CDN, and a CDN is a thing that can be blocked, cached
// wrong, or simply down. Everything else on this page — the search, the panel,
// the cross-tabulation, the term URLs — is served from the same origin as the
// data and has no reason to fail with it, so the drawing is treated as the one
// optional part rather than as the thing the rest hangs off.
const cy =
  typeof cytoscape === "function"
    ? cytoscape({
        container: canvas,
        elements: [
          ...data.nodes.map((n) => ({ data: { id: n.id, kind: n.kind, label: n.label } })),
          ...data.edges.map((e) => ({
            data: { id: `${e.source}~${e.rel}~${e.target}`, source: e.source, target: e.target, rel: e.rel },
          })),
        ],
        style: graphStyle(),
        layout: {
          name: "preset",
          positions: positionsFor(DEFAULT_VIEW, data, graphContext),
          padding: 34,
          fit: true,
        },
        // The floor must sit below the fit zoom of the smallest phones (~0.11 on
        // a 320px viewport), or fit() clamps and crops the graph instead of
        // fitting it.
        minZoom: 0.06,
        maxZoom: 3,
      })
    : null;

if (!cy) {
  const note = document.createElement("p");
  note.className = "stage-note";
  note.textContent =
    "The drawing needs a script that did not load. Search, the term panel and the matrix are unaffected.";
  canvas.replaceChildren(note);
}

// ---------------------------------------------------------------------------
// Views
// ---------------------------------------------------------------------------

const state = { view: DEFAULT_VIEW, query: "", selected: null, lastGraphView: DEFAULT_VIEW };

for (const view of VIEWS) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "view-button";
  button.dataset.view = view.id;
  button.textContent = view.name;
  button.title = view.question;
  button.addEventListener("click", () => setView(view.id));
  viewBar.append(button);
}

function setView(id, { rememberUrl = true } = {}) {
  const view = viewById(id);
  state.view = view.id;
  if (!view.matrix) state.lastGraphView = view.id;

  for (const button of viewBar.children) {
    button.setAttribute("aria-pressed", String(button.dataset.view === view.id));
  }
  viewNote.textContent = view.question;

  canvas.hidden = Boolean(view.matrix);
  matrixBox.hidden = !view.matrix;
  // The shape key belongs to the drawing. The matrix draws no shapes, so
  // leaving the key under it would promise a distinction the table is not
  // making.
  legend.hidden = Boolean(view.matrix);
  if (view.matrix) {
    renderMatrix(matrixBox, crosstab(data, graphContext), {
      onSelect: (query) => {
        input.value = query;
        runSearch();
        input.focus();
      },
    });
  } else if (cy) {
    const positions = positionsFor(view.id, data, graphContext);
    // The force layout is seeded from the ring positions rather than started at
    // random, so the same corpus settles the same way twice and a cluster a
    // reader noticed once can be found again.
    cy.layout({ name: "preset", positions, padding: 34, fit: !view.layout, animate: false }).run();
    if (view.layout) cy.layout({ ...view.layout, padding: 34, fit: true }).run();
    else cy.fit(undefined, 34);
  }
  if (rememberUrl) syncUrl();
}

// ---------------------------------------------------------------------------
// Search
// ---------------------------------------------------------------------------

const input = document.querySelector("#query");
const searchStatus = document.querySelector("#search-status");
const clearButton = document.querySelector("#search-clear");

// The index costs about a tenth of a second to build over the whole corpus.
// That is nothing to wait for once, and too much to spend before the graph has
// painted, so it is built when the browser is next idle or the moment someone
// touches the search box, whichever comes first.
let index = null;
function ensureIndex() {
  if (!index) index = buildIndex(data);
  return index;
}
(window.requestIdleCallback ?? ((fn) => setTimeout(fn, 400)))(() => ensureIndex());

let lastResults = null;
let activeResult = -1;
let debounce;

function runSearch({ rememberUrl = true } = {}) {
  const query = input.value.trim();
  state.query = query;
  clearButton.hidden = query === "";
  if (!query) {
    lastResults = null;
    activeResult = -1;
    markMatches(null);
    searchStatus.textContent = "";
    if (!state.selected) showSummary();
    if (rememberUrl) syncUrl();
    return;
  }
  const results = search(ensureIndex(), query);
  lastResults = results;
  activeResult = -1;
  searchStatus.textContent = results.total === 1 ? "1 term" : `${results.total} terms`;
  markMatches(results);
  showResults(results);
  if (rememberUrl) syncUrl();
}

input.addEventListener("input", () => {
  clearTimeout(debounce);
  debounce = setTimeout(runSearch, 110);
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    input.value = "";
    runSearch();
    return;
  }
  if (!lastResults?.results.length) return;
  if (event.key === "ArrowDown" || event.key === "ArrowUp") {
    event.preventDefault();
    const step = event.key === "ArrowDown" ? 1 : -1;
    activeResult = (activeResult + step + lastResults.results.length) % lastResults.results.length;
    select(lastResults.results[activeResult].id, { keepFocus: true });
  } else if (event.key === "Enter") {
    event.preventDefault();
    select(lastResults.results[Math.max(activeResult, 0)].id, { keepFocus: true });
  }
});

clearButton.addEventListener("click", () => {
  input.value = "";
  runSearch();
  input.focus();
});

// A slash reaches the search from anywhere on the page, the way it does in the
// tools this vocabulary is meant to be read alongside.
window.addEventListener("keydown", (event) => {
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName ?? "");
  if (typing || event.metaKey || event.altKey) return;
  if (event.key === "/" || (event.key === "k" && event.ctrlKey)) {
    event.preventDefault();
    input.focus();
    input.select();
  }
});

/** Mark the matching nodes in the graph and dim everything else. */
function markMatches(results) {
  if (!cy) return;
  cy.batch(() => {
    cy.elements().removeClass("match dimmed");
    if (!results) return;
    const matched = new Set(results.results.map((result) => result.id));
    for (const node of cy.nodes()) node.toggleClass(matched.has(node.id()) ? "match" : "dimmed", true);
    for (const edge of cy.edges()) {
      edge.toggleClass("dimmed", !matched.has(edge.source().id()) || !matched.has(edge.target().id()));
    }
  });
}

// ---------------------------------------------------------------------------
// Panel
// ---------------------------------------------------------------------------

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

const paragraph = (text, className) => element("p", className, text);

function chip(edge, direction) {
  const button = document.createElement("button");
  button.className = "edge-chip";
  const rel = element("span", "rel", direction === "out" ? `${edge.rel} → ` : `← ${edge.rel} `);
  const other = direction === "out" ? edge.target : edge.source;
  const target = element("span", null, nodesById.get(other)?.label ?? other);
  button.append(rel, target);
  button.addEventListener("click", () => select(other));
  return button;
}

function edgeList(title, edges, direction) {
  if (edges.length === 0) return [];
  const list = element("div", "edge-list");
  for (const edge of edges) list.append(chip(edge, direction));
  return [element("h4", null, title), list];
}

function bullets(title, items) {
  if (items.length === 0) return [];
  const list = document.createElement("ul");
  for (const item of items) list.append(element("li", null, item));
  return [element("h4", null, title), list];
}

function showNode(id) {
  const node = nodesById.get(id);
  const parts = [];

  // A term reached from a result list keeps the way back to it. Without this
  // the panel is a one-way door and every query has to be retyped.
  if (lastResults) {
    const back = element("button", "panel-back", `← ${lastResults.total} results`);
    back.type = "button";
    back.addEventListener("click", () => {
      state.selected = null;
      cy?.elements().unselect();
      showResults(lastResults);
      syncUrl();
    });
    parts.push(back);
  }

  parts.push(paragraph(node.kind, "panel-type"), element("h3", null, node.label), paragraph(node.id, "panel-id"));

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
  panel.scrollTop = 0;
}

/** A snippet with the matched words marked, built from spans rather than markup. */
function highlight(snippet) {
  const paragraph = element("p", "result-snippet");
  let cursor = 0;
  for (const [start, end] of snippet.ranges) {
    if (start < cursor) continue;
    paragraph.append(document.createTextNode(snippet.text.slice(cursor, start)));
    paragraph.append(element("mark", null, snippet.text.slice(start, end)));
    cursor = end;
  }
  paragraph.append(document.createTextNode(snippet.text.slice(cursor)));
  return paragraph;
}

/**
 * Why this term is in the list. A ranked result that cannot account for itself
 * asks to be trusted, and this repository is built on not doing that.
 */
function provenance(result) {
  const reasons = [];
  if (result.reason.fields.length) reasons.push(`matched in ${result.reason.fields.join(", ")}`);
  if (result.reason.corrected.length) reasons.push(`read as ${result.reason.corrected.join(", ")}`);
  if (result.reason.related.length) reasons.push(`related to ${result.reason.related.join(", ")}`);
  if (result.reason.via) reasons.push(`reached over the graph from ${result.reason.via}`);
  return reasons.length ? paragraph(reasons.join(" · "), "result-why") : null;
}

function showResults(results) {
  const parts = [];
  if (results.total === 0) {
    parts.push(paragraph(`Nothing in the corpus answers to “${results.query.raw}”.`, "panel-empty"));
    parts.push(
      paragraph(
        "Spelling is forgiven and words that keep company in the same term are followed, so a blank result usually means the corpus has not been asked this question yet.",
        "panel-empty",
      ),
    );
    parts.push(hintList());
    panel.replaceChildren(...parts);
    return;
  }

  const heading = results.listing
    ? `${results.total} terms match the filter`
    : `${results.total} terms, best first`;
  parts.push(paragraph(heading, "panel-type"));

  const list = element("div", "results");
  results.results.forEach((result, position) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "result";
    item.dataset.id = result.id;

    const head = element("div", "result-head");
    head.append(element("span", "result-label", result.doc.node.label));
    head.append(element("span", "result-kind", result.doc.node.kind));
    item.append(head);
    item.append(element("code", "result-id", result.id));
    item.append(highlight(result.snippet));
    const why = provenance(result);
    if (why) item.append(why);

    // A bar rather than a number: the useful fact is how far the second result
    // is behind the first, not that it scored 0.41.
    if (!results.listing) {
      const bar = element("span", "result-score");
      bar.style.setProperty("--score", result.score.toFixed(3));
      item.append(bar);
    }

    item.addEventListener("click", () => {
      activeResult = position;
      select(result.id);
    });
    list.append(item);
  });
  parts.push(list);
  if (results.total > results.results.length) {
    parts.push(paragraph(`Showing the first ${results.results.length}.`, "panel-empty"));
  }
  panel.replaceChildren(...parts);
  panel.scrollTop = 0;
}

function hintList() {
  const box = element("div", "hints");
  for (const hint of hints(ensureIndex())) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "hint";
    button.append(element("code", null, hint.query), element("span", null, hint.label));
    button.addEventListener("click", () => {
      input.value = hint.query;
      runSearch();
    });
    box.append(button);
  }
  return box;
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
    paragraph("Select a term to read its definition and follow its relations, or ask the corpus something.", "panel-empty"),
    hintList(),
  );
}

// ---------------------------------------------------------------------------
// Selection and address
// ---------------------------------------------------------------------------

function select(id, { keepFocus = false } = {}) {
  // Without a drawing there is nothing to select in, but the term still has a
  // definition to read and a URL to carry it.
  if (!cy) {
    state.selected = id;
    showNode(id);
    syncUrl();
    if (keepFocus) input.focus();
    return;
  }
  // A term selected out of the matrix has nothing to be selected in either: the
  // matrix draws no nodes. Fall back to the last graph view so the choice lands
  // somewhere it can be seen.
  if (viewById(state.view).matrix) setView(state.lastGraphView);
  cy.elements().unselect();
  const node = cy.$id(id);
  if (node.empty()) return;
  node.select();
  cy.animate({ center: { eles: node } }, { duration: 233 });
  if (keepFocus) input.focus();
}

function syncUrl() {
  const params = new URLSearchParams();
  if (state.view !== DEFAULT_VIEW) params.set("view", state.view);
  if (state.query) params.set("q", state.query);
  const queryString = params.toString();
  const hash = state.selected ? `#${state.selected}` : "";
  history.replaceState(null, "", `${location.pathname}${queryString ? `?${queryString}` : ""}${hash}`);
}

cy?.on("select", "node", (e) => {
  state.selected = e.target.id();
  showNode(state.selected);
  e.target.connectedEdges().addClass("adjacent");
  // Every term gets a URL, so a definition can be cited rather than described.
  syncUrl();
});

cy?.on("unselect", "node", (e) => {
  e.target.connectedEdges().removeClass("adjacent");
  if (cy.$("node:selected").length === 0) {
    state.selected = null;
    if (lastResults) showResults(lastResults);
    else showSummary();
    syncUrl();
  }
});

onThemeChange(() => cy?.style(graphStyle()));

// Keep the graph fitted to its container across window resizes, orientation
// flips, and the portrait/landscape reflow that changes the canvas dimensions.
// A ResizeObserver on the canvas catches every size change, not just
// window-level ones, and fires once on attach so the initial layout is fitted
// to the settled box rather than whatever size it had mid-render.
let resizeTimer;
new ResizeObserver(() => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (!cy || canvas.hidden) return;
    cy.resize();
    cy.fit(undefined, 34);
  }, 120);
}).observe(canvas);

/**
 * Restore whatever the address bar is asking for: a view, a query, a term.
 * All three are addressable, so a particular reading of the corpus — this
 * arrangement, this question, this term — can be sent to someone rather than
 * described to them.
 */
function readAddress({ scroll = false } = {}) {
  const params = new URLSearchParams(location.search);
  const view = params.get("view");
  if (view && viewById(view).id === view) setView(view, { rememberUrl: false });
  else setView(state.view, { rememberUrl: false });

  const query = params.get("q") ?? "";
  if (query !== input.value) {
    input.value = query;
    runSearch({ rememberUrl: false });
  }

  const id = decodeURIComponent(location.hash.slice(1));
  if (nodesById.has(id)) {
    select(id);
    if (scroll) document.querySelector("#graph").scrollIntoView({ block: "start" });
  } else if (!query) {
    showSummary();
  }
}

window.addEventListener("hashchange", () => readAddress());
readAddress({ scroll: true });

// The ontology is also explorable from the browser console: `cy` for the
// drawing, `pm.search("...")` for the corpus.
window.cy = cy;
window.pm = {
  data,
  cy,
  views: VIEWS,
  setView,
  crosstab: () => crosstab(data, graphContext),
  search: (query, options) => search(ensureIndex(), query, options),
};
