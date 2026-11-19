// Tests for the browser modules: the search engine, the arrangements, and the
// cross-tabulation. They are plain JavaScript because the code under test is,
// and running them through pytest keeps `pytest tests/` the one gate before a
// commit rather than adding a second thing to remember.
//
//   node --test tests/site.test.mjs
//
// With PRIMA_MATERIA_DATA pointing at the full page data (publish.build_data)
// and PRIMA_MATERIA_SKELETON at the graph.json cut from it, the file also runs
// the assertions that need the real corpus. tests/test_site_modules.py compiles
// the graph and sets both; without them those are skipped and the rest still
// runs against the fixture below.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import {
  absorbShard, buildIndex, editDistance, expandTerm, fold, fuzzyBudget, hints, missingShards,
  packIndex, parseQuery, search, shippedIndex, snippetFor, splitCamel, tokenize,
} from "../site/search.js";
import {
  CONTACT_SCALE, COVERAGE_SCALE, VIEWS, context, drawnEdges, positionsFor, viewById,
} from "../site/layouts.js";
import { PROSE, absorb, expand } from "../site/corpus.js";
import {
  ACROSS, INDEPENDENT, TRANSMITTED, UNSTATED, convergenceFacts, convergenceQueryFor, convergenceTab,
  crosstab, queryFor, registerQueryFor, registerTab,
} from "../site/matrix.js";

// A miniature corpus with the shape of the real one: two traditions, a claim
// that pairs a practice with a capacity, a transliterated term glossed in
// English, and a German label for the same thing.
const FIXTURE = {
  meta: { triples: 0, generated: "2026-01-01T00:00:00+00:00" },
  nodes: [
    node("pm:Process", "root", [], "Process"),
    node("pm:Conceptualizing", "class", ["owl:Class"], "Conceptualizing"),
    node("pm:Practicing", "class", ["owl:Class"], "Practicing"),
    node("pm:Yielding", "class", ["owl:Class"], "Yielding"),
    node("pm:Originating", "class", ["owl:Class"], "Originating"),
    node("pm:Tradition", "class", ["owl:Class"], "Tradition"),
    node("pm:CoverageState", "class", ["owl:Class"], "Coverage state"),
    node("pm:ContactRoute", "class", ["owl:Class"], "Contact route"),
    node("pm:corpusNamed", "instance", ["pm:CoverageState"], "Corpus named"),
    node("pm:workOpened", "instance", ["pm:CoverageState"], "Work opened"),
    node("pm:placesEntered", "instance", ["pm:CoverageState"], "Places entered"),
    node("pm:contactRouteDocumented", "instance", ["pm:ContactRoute"], "Contact route documented"),
    node("pm:contactRouteAbsent", "instance", ["pm:ContactRoute"], "Contact route absent"),
    node("pm:withinTradition", "property", ["owl:ObjectProperty"], "within tradition"),
    node("pmt:Theravada", "tradition", ["pm:Tradition"], "Theravāda"),
    node("pmt:Daoist", "tradition", ["pm:Tradition"], "Daoist tradition"),
    // Registered and unopened: named corpus, no passage read, nothing under it.
    node("pmt:Registered", "tradition", ["pm:Tradition"], "A registered transmission"),
    {
      ...node("pmc:Piti", "instance", ["pm:Conceptualizing"], "Pīti"),
      labels: { en: "Pīti", de: "Verzückung" },
      definition: { en: "Rapture as a bodily felt state, graded into five degrees." },
      sources: ["Buddhaghosa, Visuddhimagga IV.94ff. (trans. Ñāṇamoli 1956)"],
    },
    {
      ...node("pmp:Anapanasati", "instance", ["pm:Practicing"], "Ānāpānasati"),
      definition: { en: "Mindfulness of in-breath and out-breath." },
      sources: ["Majjhima Nikāya 118"],
    },
    {
      ...node("pmc:AnapanasatiYieldsPiti", "instance", ["pm:Yielding"], "Mindfulness of breathing yields rapture"),
      note: { en: "Rapture appears as a factor of absorption, not as something aimed at." },
      sources: ["Majjhima Nikāya 118"],
    },
    node("pmc:Qi", "instance", ["pm:Conceptualizing"], "Qi"),
    // A claim that begins with a named modern author and is afterwards
    // reported as ancient. What it is taken for is stated by a property, not
    // by the definition, and that statement is the finding.
    {
      ...node("pmc:ModernScale", "instance", ["pm:Originating"], "A modern ranking of the emotions"),
      statements: [
        { property: "pm:originatedBy", label: "originated by", values: ["A Named Author"] },
        {
          property: "pm:circulatesAs",
          label: "circulates as",
          values: ["A perennial map, reported as the agreement of the mystical traditions."],
        },
        { property: "dcterms:date", label: "date", values: ["1995"] },
      ],
    },
    // An angel of the Watchers, met elsewhere under another spelling.
    { ...node("pmc:Baraqel", "instance", ["pm:Conceptualizing"], "Baraqel"), altLabels: ["Baraqijal"] },
  ],
  edges: [
    edge("pm:Conceptualizing", "subClassOf", "pm:Process"),
    edge("pm:Practicing", "subClassOf", "pm:Process"),
    edge("pm:Yielding", "subClassOf", "pm:Process"),
    edge("pm:Originating", "subClassOf", "pm:Process"),
    edge("pmc:ModernScale", "instanceOf", "pm:Originating"),
    edge("pmc:Baraqel", "instanceOf", "pm:Conceptualizing"),
    edge("pmt:Theravada", "instanceOf", "pm:Tradition"),
    edge("pmt:Daoist", "instanceOf", "pm:Tradition"),
    edge("pmt:Registered", "instanceOf", "pm:Tradition"),
    edge("pmt:Theravada", "coverageState", "pm:placesEntered"),
    edge("pmt:Theravada", "contactRoute", "pm:contactRouteDocumented"),
    edge("pmt:Daoist", "coverageState", "pm:placesEntered"),
    edge("pmt:Daoist", "contactRoute", "pm:contactRouteAbsent"),
    edge("pmt:Registered", "coverageState", "pm:corpusNamed"),
    edge("pmt:Registered", "contactRoute", "pm:contactRouteAbsent"),
    edge("pmc:Piti", "instanceOf", "pm:Conceptualizing"),
    edge("pmp:Anapanasati", "instanceOf", "pm:Practicing"),
    edge("pmc:AnapanasatiYieldsPiti", "instanceOf", "pm:Yielding"),
    edge("pmc:Qi", "instanceOf", "pm:Conceptualizing"),
    edge("pmc:Piti", "withinTradition", "pmt:Theravada"),
    edge("pmp:Anapanasati", "withinTradition", "pmt:Theravada"),
    edge("pmc:AnapanasatiYieldsPiti", "withinTradition", "pmt:Theravada"),
    edge("pmc:Qi", "withinTradition", "pmt:Daoist"),
    edge("pmc:AnapanasatiYieldsPiti", "byPractice", "pmp:Anapanasati"),
    edge("pmc:AnapanasatiYieldsPiti", "yieldsCapacity", "pmc:Piti"),
  ],
};

function node(id, kind, types, label) {
  return {
    id, kind, types, label,
    iri: `https://example.invalid/${id}`,
    labels: { en: label },
    altLabels: [],
    definition: {}, note: {}, comment: {}, sources: [], statements: [],
  };
}

function edge(source, rel, target) {
  return { source, rel, target };
}

const fixtureIndex = buildIndex(FIXTURE);
const ids = (result) => result.results.map((entry) => entry.id);

// ---------------------------------------------------------------------------
// Folding and tokenizing
// ---------------------------------------------------------------------------

test("folding strips the diacritics the corpus is transliterated with", () => {
  assert.equal(fold("Pīti"), "piti");
  assert.equal(fold("samādhi"), "samadhi");
  assert.equal(fold("Ñāṇamoli"), "nanamoli");
  assert.equal(fold("Śaiva and Śākta"), "saiva and sakta");
  assert.equal(fold("Verzückung"), "verzuckung");
  assert.equal(fold("Fluß"), "fluss");
});

test("tokens keep the span they occupy in the unfolded text", () => {
  const text = "Pīti and Ānāpānasati";
  for (const token of tokenize(text)) {
    // The span has to name the word as the reader sees it, or a highlight
    // computed from the folded form marks the wrong characters.
    assert.equal(fold(text.slice(token.start, token.end)), token.term);
  }
});

test("PascalCase locals are read as the compounds they are", () => {
  assert.equal(splitCamel("AnapanasatiYieldsPiti"), "Anapanasati Yields Piti");
  assert.equal(splitCamel("IRIName"), "IRI Name");
});

// ---------------------------------------------------------------------------
// Fuzzy matching
// ---------------------------------------------------------------------------

test("edit distance counts substitutions, gaps and transpositions", () => {
  assert.equal(editDistance("piti", "pita", 2), 1);
  assert.equal(editDistance("piti", "pit", 2), 1);
  assert.equal(editDistance("piti", "piti", 2), 0);
  assert.equal(editDistance("tummo", "tumom", 2), 1); // one transposition
  assert.equal(editDistance("qi", "piti", 2), 3);     // gives up past the budget
});

test("short words earn no misspelling, long ones earn two", () => {
  assert.equal(fuzzyBudget(3), 0);
  assert.equal(fuzzyBudget(5), 1);
  assert.equal(fuzzyBudget(12), 2);
});

test("a query word reaches exact, prefix, corrected and related terms", () => {
  const routes = new Map(
    expandTerm(fixtureIndex, "rapture").map((variant) => [variant.term, variant]),
  );
  assert.equal(routes.get("rapture").how, "exact");
  assert.equal(routes.get("rapture").weight, 1);
  // Pīti is glossed as rapture in the same node, so the two keep company.
  assert.equal(routes.get("piti")?.how, "related");
  assert.ok(routes.get("piti").weight < routes.get("rapture").weight);
});

test("a misspelling still finds the term", () => {
  assert.deepEqual(ids(search(fixtureIndex, "anapanasat"))[0], "pmp:Anapanasati");
  assert.ok(ids(search(fixtureIndex, "visudhimaga")).includes("pmc:Piti"));
});

// ---------------------------------------------------------------------------
// The query language
// ---------------------------------------------------------------------------

test("filters, phrases and negations are read out of the query", () => {
  const query = parseQuery('kind:instance -has:source "mind made" -qi rapture');
  assert.deepEqual(
    query.filters,
    [
      { field: "kind", value: "instance", negated: false },
      { field: "has", value: "source", negated: true },
    ],
  );
  assert.deepEqual(query.phrases, [["mind", "made"]]);
  assert.deepEqual(query.negatedTerms, ["qi"]);
  assert.ok(query.terms.includes("rapture"));
});

test("a prefix that names no filter is part of what was typed", () => {
  const query = parseQuery("chapter:XII");
  assert.deepEqual(query.filters, []);
  assert.deepEqual(query.terms, ["chapter", "xii"]);
});

test("tradition:<local name> means that transmission, not every label with the word", () => {
  const index = buildIndex({
    meta: FIXTURE.meta,
    nodes: [
      node("pmt:Hermetic", "tradition", ["pm:Tradition"], "Hermetic transmission"),
      node("pmt:GoldenDawn", "tradition", ["pm:Tradition"], "Hermetic Order of the Golden Dawn"),
      node("pmc:Poimandres", "instance", ["pm:Conceptualizing"], "Poimandres"),
      node("pmc:Tattva", "instance", ["pm:Conceptualizing"], "Tattva"),
    ],
    edges: [
      edge("pmc:Poimandres", "withinTradition", "pmt:Hermetic"),
      edge("pmc:Tattva", "withinTradition", "pmt:GoldenDawn"),
    ],
  });
  assert.deepEqual(ids(search(index, "tradition:Hermetic")).sort(), ["pmc:Poimandres", "pmt:Hermetic"]);
  assert.deepEqual(ids(search(index, "tradition:golden dawn")).sort(), ["pmc:Tattva", "pmt:GoldenDawn"]);
});

test("filters match whole words, so type:Testing is not Attesting", () => {
  assert.deepEqual(ids(search(fixtureIndex, "type:Yielding")), ["pmc:AnapanasatiYieldsPiti"]);
  assert.deepEqual(ids(search(fixtureIndex, "kind:tradition")).sort(), [
    "pmt:Daoist", "pmt:Registered", "pmt:Theravada",
  ]);
  assert.deepEqual(ids(search(fixtureIndex, "tradition:daoist")).sort(), ["pmc:Qi", "pmt:Daoist"]);
  assert.deepEqual(ids(search(fixtureIndex, "source:nikaya")).sort(), [
    "pmc:AnapanasatiYieldsPiti",
    "pmp:Anapanasati",
  ]);
});

test("has: audits the corpus, and its negation is the interesting half", () => {
  const without = ids(search(fixtureIndex, "kind:instance -has:source"));
  assert.ok(["pmc:Baraqel", "pmc:ModernScale", "pmc:Qi"].every((id) => without.includes(id)));
  assert.ok(!without.includes("pmc:Piti"), "Piti cites a passage and is not a gap");
  assert.ok(ids(search(fixtureIndex, "kind:instance has:source")).includes("pmc:Piti"));
  // A language tag falls through to the labels, so a gap in translation shows.
  assert.deepEqual(ids(search(fixtureIndex, "has:de")), ["pmc:Piti"]);
});

test("a negated word removes a term that would otherwise rank", () => {
  assert.ok(ids(search(fixtureIndex, "rapture")).includes("pmc:Piti"));
  assert.ok(!ids(search(fixtureIndex, "rapture -piti")).includes("pmc:Piti"));
});

test("a negated word stays negated after the graph has had its say", () => {
  // Pīti is one edge from the pairing that yields it, so spreading activation
  // reaches it from any neighbour that matches. Excluding it has to survive
  // that, or the exclusion is only a suggestion.
  const result = search(fixtureIndex, "anapanasati -piti");
  assert.ok(result.total > 0);
  assert.ok(!ids(result).includes("pmc:Piti"));
  assert.ok(result.results.every((entry) => entry.id !== "pmc:AnapanasatiYieldsPiti"));
});

test("a negation on its own narrows a listing rather than being ignored", () => {
  const all = search(fixtureIndex, "kind:instance");
  const fewer = search(fixtureIndex, "kind:instance -qi");
  assert.ok(fewer.total < all.total);
  assert.ok(!ids(fewer).includes("pmc:Qi"));
});

test("a filter with no words is a listing, ordered by how connected each term is", () => {
  const result = search(fixtureIndex, "kind:class");
  assert.equal(result.listing, true);
  assert.ok(result.results.every((entry) => entry.score === 1));
  const degrees = result.results.map((entry) => entry.doc.degree);
  assert.deepEqual(degrees, [...degrees].sort((a, b) => b - a), "a listing leads with the spine");
});

// ---------------------------------------------------------------------------
// Ranking
// ---------------------------------------------------------------------------

test("a term's own name outranks a mention of it elsewhere", () => {
  assert.equal(ids(search(fixtureIndex, "piti"))[0], "pmc:Piti");
  assert.equal(ids(search(fixtureIndex, "qi"))[0], "pmc:Qi");
});

test("the semantic layer crosses from the gloss to the transliteration", () => {
  // "rapture" is nowhere in the label or the name of pmc:Piti in this fixture
  // beyond its definition; the point is that it also pulls in the node that
  // only shares the company the word keeps.
  const found = ids(search(fixtureIndex, "rapture"));
  assert.ok(found.includes("pmc:Piti"));
  assert.ok(found.includes("pmc:AnapanasatiYieldsPiti"));
});

test("a German query reaches an English node through the labels beside it", () => {
  assert.ok(ids(search(fixtureIndex, "Verzückung")).includes("pmc:Piti"));
});

test("the graph carries a match to its neighbours, and says that it did", () => {
  const result = search(fixtureIndex, "anapanasati");
  const capacity = result.results.find((entry) => entry.id === "pmc:Piti");
  assert.ok(capacity, "the capacity the practice is said to yield should surface");
  const reached = result.results.filter((entry) => entry.reason.via);
  assert.ok(reached.length > 0, "reaching over the graph has to be reported as such");
});

test("switching a layer off changes what comes back", () => {
  const withGraph = search(fixtureIndex, "anapanasati");
  const withoutGraph = search(fixtureIndex, "anapanasati", { structural: false, semantic: false });
  assert.ok(withGraph.total >= withoutGraph.total);
  assert.ok(withoutGraph.results.every((entry) => entry.reason.via === null));
});

test("every result accounts for itself", () => {
  for (const entry of search(fixtureIndex, "rapture").results) {
    const reason = entry.reason;
    assert.ok(
      reason.fields.length || reason.corrected.length || reason.related.length || reason.via,
      `${entry.id} came back without a reason`,
    );
  }
});

test("scores are relative to the best hit and never zero", () => {
  const result = search(fixtureIndex, "rapture");
  assert.equal(result.results[0].score, 1);
  assert.ok(result.results.every((entry) => entry.score > 0 && entry.score <= 1));
});

test("a query the corpus cannot answer comes back empty rather than padded", () => {
  const result = search(fixtureIndex, "zzzzqqqqxxxx");
  assert.equal(result.total, 0);
});

test("what a claim is taken for is searchable, not just its definition", () => {
  // pm:circulatesAs is where an origination says what it is commonly reported
  // as, and the ontology calls that the finding. A page that indexed only
  // labels, definitions and notes would drop exactly it.
  const found = ids(search(fixtureIndex, "perennial map"));
  assert.ok(found.includes("pmc:ModernScale"));
  assert.ok(ids(search(fixtureIndex, "A Named Author")).includes("pmc:ModernScale"));
  // The property's own name is a way in as well.
  assert.ok(ids(search(fixtureIndex, "circulates as")).includes("pmc:ModernScale"));
});

test("a statement can be the passage a result shows", () => {
  const result = search(fixtureIndex, "perennial");
  const entry = result.results.find((candidate) => candidate.id === "pmc:ModernScale");
  assert.equal(entry.snippet.field, "statement");
  assert.ok(entry.snippet.ranges.length > 0);
});

test("an alternate spelling finds the term at a label's weight", () => {
  assert.equal(ids(search(fixtureIndex, "Baraqijal"))[0], "pmc:Baraqel");
});

test("a node that states nothing extra still indexes", () => {
  // Older builds of ontology-data.json carry no statements or altLabels at
  // all; the page has to survive one rather than throw on the first node.
  const bare = {
    ...FIXTURE,
    nodes: FIXTURE.nodes.map(({ statements, altLabels, ...rest }) => rest),
  };
  const index = buildIndex(bare);
  assert.ok(search(index, "rapture").total > 0);
});

test("snippets mark the words that were matched", () => {
  const doc = fixtureIndex.docs[fixtureIndex.byId.get("pmc:Piti")];
  const snippet = snippetFor(doc, new Set(["rapture"]));
  assert.equal(snippet.field, "definition");
  assert.ok(snippet.ranges.length > 0);
  const [start, end] = snippet.ranges[0];
  assert.equal(fold(snippet.text.slice(start, end)), "rapture");
});

test("the openings offered are queries the engine can actually run", () => {
  for (const hint of hints(fixtureIndex)) {
    assert.doesNotThrow(() => search(fixtureIndex, hint.query));
  }
});

// ---------------------------------------------------------------------------
// Arrangements
// ---------------------------------------------------------------------------

test("every arrangement places every term exactly once", () => {
  const ctx = context(FIXTURE);
  for (const view of VIEWS) {
    if (view.matrix || view.subset) continue;
    const positions = positionsFor(view.id, FIXTURE, ctx);
    assert.equal(
      Object.keys(positions).length,
      FIXTURE.nodes.length,
      `${view.id} left a term unplaced`,
    );
    for (const [id, point] of Object.entries(positions)) {
      assert.ok(Number.isFinite(point.x) && Number.isFinite(point.y), `${view.id} put ${id} nowhere`);
    }
  }
});

test("no arrangement stacks two terms on the same point", () => {
  const ctx = context(FIXTURE);
  for (const view of VIEWS) {
    if (view.matrix) continue;
    const positions = positionsFor(view.id, FIXTURE, ctx);
    const seen = new Set();
    for (const [id, point] of Object.entries(positions)) {
      const key = `${point.x.toFixed(3)} ${point.y.toFixed(3)}`;
      assert.ok(!seen.has(key), `${view.id} stacked ${id} on another term`);
      seen.add(key);
    }
  }
});

// A convergence over the two traditions, a dispute inside one, and a test of
// the convergence: the three ways a finding reaches its claims.
const WITH_FINDINGS = {
  ...FIXTURE,
  nodes: [
    ...FIXTURE.nodes,
    node("pm:Converging", "class", ["owl:Class"], "Converging"),
    node("pmc:BreathMeetsQi", "instance", ["pm:Converging"], "Breath and qi converge"),
    node("pmc:PitiDisputed", "instance", ["pm:Disputing"], "Whether rapture is a factor"),
    node("pmc:BreathQiTested", "instance", ["pm:Testing"], "The convergence put to a test"),
  ],
  edges: [
    ...FIXTURE.edges,
    edge("pmc:BreathMeetsQi", "convergingConcept", "pmp:Anapanasati"),
    edge("pmc:BreathMeetsQi", "convergingConcept", "pmc:Qi"),
    edge("pmc:PitiDisputed", "disputedClaim", "pmc:AnapanasatiYieldsPiti"),
    edge("pmc:BreathQiTested", "tests", "pmc:BreathMeetsQi"),
  ],
};

test("the overlay draws the findings, what they rest on, and the traditions they reach", () => {
  const ctx = context(WITH_FINDINGS);
  const positions = positionsFor("overlay", WITH_FINDINGS, ctx);
  assert.deepEqual(
    Object.keys(positions).sort(),
    [
      "pmc:AnapanasatiYieldsPiti", "pmc:BreathMeetsQi", "pmc:BreathQiTested", "pmc:PitiDisputed",
      "pmc:Qi", "pmp:Anapanasati", "pmt:Daoist", "pmt:Theravada",
    ],
  );
  const distance = (id) => Math.hypot(positions[id].x, positions[id].y);
  // Two traditions reached sit nearer the centre than one; the claims and the
  // traditions sit outside every finding.
  assert.ok(distance("pmc:BreathMeetsQi") < distance("pmc:PitiDisputed"));
  assert.ok(distance("pmc:BreathQiTested") < distance("pmc:PitiDisputed"));
  for (const id of ["pmc:Qi", "pmp:Anapanasati", "pmt:Daoist", "pmt:Theravada"]) {
    assert.ok(distance(id) > distance("pmc:PitiDisputed"), `${id} is inside a finding`);
  }
  const seen = new Set(Object.values(positions).map((p) => `${p.x.toFixed(3)} ${p.y.toFixed(3)}`));
  assert.equal(seen.size, Object.keys(positions).length, "the overlay stacked two terms");
  // A corpus without findings draws nothing rather than failing.
  assert.deepEqual(positionsFor("overlay", FIXTURE, context(FIXTURE)), {});
});

test("a convergence shows its breadth and how it splits, never the breadth alone", () => {
  const data = {
    ...WITH_FINDINGS,
    edges: [...WITH_FINDINGS.edges, edge("pmc:BreathMeetsQi", "independentAttestation", "pmt:Daoist")],
  };
  const ctx = context(data);
  assert.deepEqual(convergenceFacts(data, ctx).get("pmc:BreathMeetsQi"), {
    breadth: 2, independent: 1, transmitted: 1, reworked: 0,
  });
  const table = convergenceTab(data, ctx);
  assert.deepEqual(table.rows, [{ id: "pmc:BreathMeetsQi", label: "Breath and qi converge", total: 2 }]);
  // No reworking yet, so no column promising one.
  assert.deepEqual(table.columns.map((c) => c.id), [INDEPENDENT, TRANSMITTED]);
  assert.equal(table.count("pmc:BreathMeetsQi", INDEPENDENT) + table.count("pmc:BreathMeetsQi", TRANSMITTED), 2);
  // The query a row offers finds that convergence first.
  const found = search(buildIndex(data), convergenceQueryFor("pmc:BreathMeetsQi"));
  assert.equal(found.results[0].id, "pmc:BreathMeetsQi");
});

test("the view the page opens on draws a selection, and says so", () => {
  assert.equal(VIEWS[0].id, "overlay");
  assert.ok(VIEWS[0].subset);
});

test("a claim's class, tradition and scale are not drawn as lines", () => {
  const drawn = drawnEdges(WITH_FINDINGS).map((e) => `${e.source} ${e.rel} ${e.target}`);
  assert.ok(drawn.includes("pmc:AnapanasatiYieldsPiti byPractice pmp:Anapanasati"));
  assert.ok(drawn.includes("pmc:BreathMeetsQi convergingConcept pmc:Qi"));
  // The vocabulary's own structure is relation, not attribute.
  assert.ok(drawn.includes("pm:Yielding subClassOf pm:Process"));
  for (const rel of ["instanceOf", "withinTradition", "coverageState", "contactRoute"]) {
    assert.ok(!drawn.some((line) => line.split(" ")[1] === rel), `${rel} is drawn`);
  }
});

// ---------------------------------------------------------------------------
// The skeleton and the prose
// ---------------------------------------------------------------------------

/** What publish.split_data does, in miniature, for the fixture. */
function skeletonOf(data, chunk) {
  const position = new Map(data.nodes.map((n, i) => [n.id, i]));
  const rels = [...new Set(data.edges.map((e) => e.rel))].sort();
  const chunks = [];
  const nodes = data.nodes.map((n, i) => {
    const { iri, ...rest } = n;
    const lean = Object.fromEntries(Object.entries(rest).filter(([k]) => !PROSE.includes(k)));
    const has = PROSE.filter((k) => (Array.isArray(n[k]) ? n[k].length : Object.keys(n[k]).length));
    if (has.length) lean.has = has;
    if (lean.label === n.labels.en) delete lean.label;
    const number = Math.floor(i / chunk);
    chunks[number] ??= {};
    chunks[number][n.id] = Object.fromEntries(has.map((k) => [k, n[k]]));
    return lean;
  });
  const edges = data.edges.map((e) => [position.get(e.source), rels.indexOf(e.rel), position.get(e.target)]);
  return { skeleton: { meta: { ...data.meta, chunk }, rels, nodes, edges }, chunks };
}

test("the skeleton and the prose put back together are the data", () => {
  const { skeleton, chunks } = skeletonOf(FIXTURE, 4);
  const data = expand(skeleton);
  assert.deepEqual(data.edges, FIXTURE.edges);
  const byId = new Map(data.nodes.map((n) => [n.id, n]));
  for (const chunk of chunks) absorb(byId, chunk);
  for (const original of FIXTURE.nodes) {
    const { iri, ...expected } = original;
    const { chunk, has, ...actual } = byId.get(original.id);
    assert.deepEqual(actual, expected, `${original.id} did not survive the cut`);
  }
});

test("the audit filters answer before any prose is loaded", () => {
  const lean = expand(skeletonOf(FIXTURE, 4).skeleton);
  const before = buildIndex(lean);
  for (const query of ["-has:source", "has:source", "has:definition", "has:note"]) {
    assert.deepEqual(
      ids(search(before, query, { limit: 1000 })).sort(),
      ids(search(fixtureIndex, query, { limit: 1000 })).sort(),
      `${query} needs the prose to answer`,
    );
  }
  // The openings need no index at all.
  assert.deepEqual(hints(lean), hints(fixtureIndex));
});

/** Load a shipped index the way the page does: round after round until nothing is missing. */
function loadFor(index, shards, query) {
  for (let missing = missingShards(index, query); missing.length; missing = missingShards(index, query)) {
    for (const key of missing) absorbShard(index, key, shards[key]);
  }
}

/** What a result list says, without the snippet, which needs the prose. */
const ranked = (result) => result.results.map((entry) => [entry.id, entry.score.toFixed(9), entry.reason]);

function assertShippedAgrees(data, built, queries) {
  const { meta, shards } = JSON.parse(JSON.stringify(packIndex(built)));
  const lean = expand(skeletonOf(data, 4).skeleton);
  const shipped = shippedIndex(lean, meta);
  for (const query of queries) {
    loadFor(shipped, shards, query);
    assert.deepEqual(ranked(search(shipped, query)), ranked(search(built, query)), `“${query}” ranks otherwise`);
  }
  return shipped;
}

test("the index shipped as files answers as the one built in the browser", () => {
  const queries = [
    "rapture", "piti", "pitti", "ana", "verzuckung", "mindfulness breath", "baraqijal", "-piti rapture",
    "tradition:theravada", "kind:instance -has:source", "type:Yielding rapture", "qi",
    ...hints(fixtureIndex).map((hint) => hint.query),
  ];
  const shipped = assertShippedAgrees(FIXTURE, fixtureIndex, queries);
  // It reads only the files a query needs.
  const fresh = shippedIndex(expand(skeletonOf(FIXTURE, 4).skeleton), packIndex(fixtureIndex).meta);
  assert.ok(missingShards(fresh, "rapture").every((key) => key === "ra"));
  assert.ok(shipped.loaded.size < packIndex(fixtureIndex).meta.keys.length);
});

test("a shipped document takes up prose that arrives after the index was made", () => {
  const { skeleton, chunks } = skeletonOf(FIXTURE, 4);
  const lean = expand(skeleton);
  const { meta, shards } = packIndex(fixtureIndex);
  const shipped = shippedIndex(lean, meta);
  loadFor(shipped, shards, "rapture");
  const before = search(shipped, "rapture").results.find((r) => r.id === "pmc:Piti");
  assert.equal(before.snippet.field, "label");
  absorb(new Map(lean.nodes.map((n) => [n.id, n])), chunks.flatMap((c) => Object.entries(c)).reduce((o, [k, v]) => ({ ...o, [k]: v }), {}));
  for (const doc of shipped.docs) doc.refresh();
  const after = search(shipped, "rapture").results.find((r) => r.id === "pmc:Piti");
  assert.equal(after.snippet.field, "definition");
  assert.throws(() => shippedIndex(FIXTURE, { ...meta, docs: 1 }), /other data/);
});

test("a rebuild handed the associations keeps them", () => {
  const rebuilt = buildIndex(FIXTURE, { associations: fixtureIndex.associations });
  assert.equal(rebuilt.associations, fixtureIndex.associations);
  assert.deepEqual(ids(search(rebuilt, "rapture")), ids(search(fixtureIndex, "rapture")));
});

test("every arrangement states the question it answers", () => {
  for (const view of VIEWS) {
    assert.ok(view.name && view.question, `${view.id} has no question`);
  }
  assert.equal(viewById("no-such-view").id, VIEWS[0].id);
});

// ---------------------------------------------------------------------------
// The matrix
// ---------------------------------------------------------------------------

test("the cross-tabulation counts every claim once and no vocabulary", () => {
  const matrix = crosstab(FIXTURE, context(FIXTURE));
  // Piti, Anapanasati, the pairing, Qi, the modern scale, Baraqel.
  assert.equal(matrix.total, 6);
  // The origination belongs to no tradition, so it lands in the row for
  // claims made across them rather than being dropped.
  assert.equal(matrix.count(ACROSS, "pm:Originating"), 1);
  assert.equal(
    matrix.rows.reduce((sum, row) => sum + row.total, 0),
    matrix.total,
  );
  assert.equal(
    matrix.columns.reduce((sum, column) => sum + column.total, 0),
    matrix.total,
  );
  // The classes and properties of the ontology are scaffolding, not claims.
  assert.ok(!matrix.columns.some((column) => column.id === "pm:Tradition"));
});

test("the claim table holds the traditions that witness, and counts the rest", () => {
  // A registered transmission carries nothing by definition, so a row for it
  // would repeat pm:corpusNamed once per claim form rather than report
  // anything. What is worth keeping is the number, which the caption states
  // and which is carried here.
  const matrix = crosstab(FIXTURE, context(FIXTURE));
  assert.ok(!matrix.rows.some((row) => row.id === "pmt:Registered"));
  assert.equal(matrix.registered, 1);
  assert.ok(matrix.rows.every((row) => row.id === ACROSS || row.total > 0));
});

test("the register table counts every tradition exactly once", () => {
  const matrix = registerTab(FIXTURE, context(FIXTURE), {
    coverageScale: COVERAGE_SCALE,
    contactScale: CONTACT_SCALE,
  });
  const traditions = FIXTURE.nodes.filter((entry) => entry.kind === "tradition").length;
  assert.equal(matrix.total, traditions);
  assert.equal(matrix.rows.reduce((sum, row) => sum + row.total, 0), traditions);
  assert.equal(matrix.columns.reduce((sum, column) => sum + column.total, 0), traditions);
  assert.equal(matrix.count("pm:corpusNamed", "pm:contactRouteAbsent"), 1);
  assert.equal(matrix.count("pm:placesEntered", "pm:contactRouteDocumented"), 1);
});

test("a step of the scale nobody has reached keeps its row", () => {
  const matrix = registerTab(FIXTURE, context(FIXTURE), {
    coverageScale: COVERAGE_SCALE,
    contactScale: CONTACT_SCALE,
  });
  const opened = matrix.rows.find((row) => row.id === "pm:workOpened");
  assert.ok(opened, "an absent row would read as an absent stage of the work");
  assert.equal(opened.total, 0);
  // The scale is read in its own order, not sorted by how full each step is.
  const scale = matrix.rows.map((row) => row.id).filter((id) => COVERAGE_SCALE.includes(id));
  assert.deepEqual(scale, COVERAGE_SCALE.filter((id) => scale.includes(id)));
});

test("a tradition neither scale was applied to is counted, not rounded away", () => {
  const partial = {
    ...FIXTURE,
    nodes: [...FIXTURE.nodes, node("pmt:Unstated", "tradition", ["pm:Tradition"], "Unstated")],
  };
  const ctx = context(partial);
  const matrix = registerTab(partial, ctx, {
    coverageScale: COVERAGE_SCALE,
    contactScale: CONTACT_SCALE,
  });
  assert.equal(matrix.count(UNSTATED, UNSTATED), 1);
  assert.equal(matrix.rows.reduce((sum, row) => sum + row.total, 0), matrix.total);
  assert.deepEqual(
    ids(search(buildIndex(partial), registerQueryFor(UNSTATED, UNSTATED))),
    ["pmt:Unstated"],
  );
});

test("both scales are askable by every spelling a reader might use", () => {
  for (const query of ["coverage:corpusNamed", 'coverage:"corpus named"', "coverage:corpusnamed"]) {
    assert.deepEqual(ids(search(fixtureIndex, query)), ["pmt:Registered"], query);
  }
  assert.deepEqual(ids(search(fixtureIndex, "contact:documented")), ["pmt:Theravada"]);
  assert.deepEqual(
    ids(search(fixtureIndex, "kind:tradition contact:absent")).sort(),
    ["pmt:Daoist", "pmt:Registered"],
  );
});

test("a registered transmission names nothing in the drawing", () => {
  // Landmarks carry a label the drawing keeps legible at fitted zoom. Deciding
  // that by kind put a large label on every registered transmission and
  // crowded out the terms that do name a region.
  const ctx = context(FIXTURE);
  assert.equal(ctx.isLandmark("pmt:Theravada"), true);
  assert.equal(ctx.isLandmark("pmt:Registered"), false);
  assert.equal(ctx.isLandmark("pm:Conceptualizing"), true);
  assert.equal(ctx.isLandmark("pmc:Piti"), false);
});

test("the register earns no sector in a view that sizes sectors by contribution", () => {
  const ctx = context(FIXTURE);
  const positions = positionsFor("traditions", FIXTURE, ctx);
  // It is still drawn — on the rim, outside what the graph is carried by —
  // so nothing is hidden; it simply claims no share of the circle.
  const radius = (id) => Math.hypot(positions[id].x, positions[id].y);
  assert.ok(radius("pmt:Registered") > radius("pmt:Theravada"));
});

test("a cell knows the query that would list what it counted", () => {
  assert.equal(queryFor("pmt:Theravada", "pm:Yielding"), "tradition:Theravada type:Yielding");
  assert.equal(queryFor(ACROSS, "pm:Converging"), "type:Converging -has:tradition");
  assert.equal(queryFor(null, "pm:Testing"), "type:Testing");
});

test("the query a cell offers returns exactly the cell's count", () => {
  const ctx = context(FIXTURE);
  const matrix = crosstab(FIXTURE, ctx);
  for (const row of matrix.rows) {
    for (const column of matrix.columns) {
      const result = search(fixtureIndex, queryFor(row.id, column.id));
      assert.equal(
        result.total,
        matrix.count(row.id, column.id),
        `${row.label} × ${column.label} promises a count the query does not return`,
      );
    }
  }
});

// ---------------------------------------------------------------------------
// Against the real corpus, when there is one
// ---------------------------------------------------------------------------

const dataPath = process.env.PRIMA_MATERIA_DATA;
const corpus = dataPath ? JSON.parse(readFileSync(dataPath, "utf8")) : null;
// A row and a column each, not every cell: the cells are checked against the
// built index below, and the same filters make up a row query and a cell.
function matrixQueries(matrix, queryFor) {
  return [
    ...matrix.rows.map((row) => queryFor(row.id, null)),
    ...matrix.columns.map((column) => queryFor(null, column.id)),
    queryFor(matrix.rows[0].id, matrix.columns[0].id),
  ];
}

function assertShippedAgreesOnCorpus(full, skeletonFile, built, queries) {
  const { meta, shards } = JSON.parse(JSON.stringify(packIndex(built)));
  const shipped = shippedIndex(expand(skeletonFile), meta);
  for (const query of queries) {
    loadFor(shipped, shards, query);
    assert.deepEqual(ranked(search(shipped, query)), ranked(search(built, query)), `“${query}” ranks otherwise`);
  }
}

const skeletonPath = process.env.PRIMA_MATERIA_SKELETON;
const skeleton = skeletonPath ? JSON.parse(readFileSync(skeletonPath, "utf8")) : null;
const onlyWithCorpus = {
  skip: corpus && skeleton ? false : "set PRIMA_MATERIA_DATA and PRIMA_MATERIA_SKELETON",
};

test("the whole corpus indexes, searches and arranges", onlyWithCorpus, () => {
  const index = buildIndex(corpus);
  const ctx = context(corpus);

  // Every term is reachable by its own name.
  for (const term of ["pm:Process", "pm:Symbolizing", "pm:withinTradition"]) {
    const label = corpus.nodes.find((entry) => entry.id === term).label;
    const found = search(index, label).results.map((entry) => entry.id);
    assert.ok(found.includes(term), `${term} cannot be found by its own label`);
  }

  for (const view of VIEWS) {
    if (view.matrix) continue;
    const positions = positionsFor(view.id, corpus, ctx);
    if (view.subset) {
      assert.ok(Object.keys(positions).length > 0, `${view.id} drew nothing`);
      for (const id of Object.keys(positions)) assert.ok(ctx.byId.has(id), `${view.id} placed ${id}`);
      continue;
    }
    assert.equal(Object.keys(positions).length, corpus.nodes.length, `${view.id} left a term unplaced`);
  }

  // The index the page loads as files has to answer every query the page
  // offers exactly as the one built here: the openings, and every cell of the
  // tables, which promise their own counts.
  const cellQueries = [
    ...hints(corpus).map((hint) => hint.query),
    ...matrixQueries(crosstab(corpus, ctx), queryFor),
    ...matrixQueries(registerTab(corpus, ctx, { coverageScale: COVERAGE_SCALE, contactScale: CONTACT_SCALE }), registerQueryFor),
    "rapture", "jhana", "verzuckung", "breath qi", "angel watcher", "-has:source kind:instance",
  ];
  assertShippedAgreesOnCorpus(corpus, skeleton, index, cellQueries);

  // The page reads the skeleton, not the data: it has to carry every term and
  // every edge, and answer the audit filters the matrix and the openings use.
  const lean = expand(skeleton);
  assert.equal(lean.nodes.length, corpus.nodes.length);
  assert.deepEqual(lean.edges, corpus.edges);
  for (const [position, original] of corpus.nodes.entries()) {
    const node = lean.nodes[position];
    assert.equal(node.id, original.id);
    assert.equal(node.label, original.label, `${original.id} lost its label`);
  }

  const convergences = convergenceTab(corpus, ctx);
  assert.ok(convergences.rows.length > 0, "the corpus has convergences and the table shows none");
  for (const row of convergences.rows) {
    assert.equal(
      convergences.count(row.id, INDEPENDENT) + convergences.count(row.id, TRANSMITTED),
      row.total,
      `${row.label}: the split does not add up to the breadth`,
    );
    assert.equal(search(index, convergenceQueryFor(row.id)).results[0]?.id, row.id, `${row.label} cannot be opened`);
  }

  const matrix = crosstab(corpus, ctx);
  assert.equal(
    matrix.rows.reduce((sum, row) => sum + row.total, 0),
    matrix.total,
  );

  // The register table has to account for every registered transmission, and
  // every cell of both tables has to return its own count when opened.
  const register = registerTab(corpus, ctx, {
    coverageScale: COVERAGE_SCALE,
    contactScale: CONTACT_SCALE,
  });
  const traditions = corpus.nodes.filter((entry) => entry.kind === "tradition").length;
  assert.equal(register.total, traditions);
  assert.equal(register.rows.reduce((sum, row) => sum + row.total, 0), traditions);
  for (const row of register.rows) {
    for (const column of register.columns) {
      assert.equal(
        search(index, registerQueryFor(row.id, column.id)).total,
        register.count(row.id, column.id),
        `${row.label} × ${column.label} promises a count the query does not return`,
      );
    }
  }
  for (const row of matrix.rows) {
    for (const column of matrix.columns) {
      assert.equal(
        search(index, queryFor(row.id, column.id)).total,
        matrix.count(row.id, column.id),
        `${row.label} × ${column.label} promises a count the query does not return`,
      );
    }
  }
});
