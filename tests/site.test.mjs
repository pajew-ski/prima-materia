// Tests for the browser modules: the search engine, the arrangements, and the
// cross-tabulation. They are plain JavaScript because the code under test is,
// and running them through pytest keeps `pytest tests/` the one gate before a
// commit rather than adding a second thing to remember.
//
//   node --test tests/site.test.mjs
//
// With PRIMA_MATERIA_DATA pointing at a built ontology-data.json the file also
// runs the assertions that need the real corpus. tests/test_site_modules.py
// compiles the graph and sets it; without it those are skipped and the rest
// still runs against the fixture below.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import {
  buildIndex, editDistance, expandTerm, fold, fuzzyBudget, hints, parseQuery,
  search, snippetFor, splitCamel, tokenize,
} from "../site/search.js";
import { VIEWS, context, positionsFor, viewById } from "../site/layouts.js";
import { ACROSS, crosstab, queryFor } from "../site/matrix.js";

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
    node("pm:Tradition", "class", ["owl:Class"], "Tradition"),
    node("pm:withinTradition", "property", ["owl:ObjectProperty"], "within tradition"),
    node("pmt:Theravada", "tradition", ["pm:Tradition"], "Theravāda"),
    node("pmt:Daoist", "tradition", ["pm:Tradition"], "Daoist tradition"),
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
  ],
  edges: [
    edge("pm:Conceptualizing", "subClassOf", "pm:Process"),
    edge("pm:Practicing", "subClassOf", "pm:Process"),
    edge("pm:Yielding", "subClassOf", "pm:Process"),
    edge("pmt:Theravada", "instanceOf", "pm:Tradition"),
    edge("pmt:Daoist", "instanceOf", "pm:Tradition"),
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
    definition: {}, note: {}, comment: {}, sources: [],
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

test("filters match whole words, so type:Testing is not Attesting", () => {
  assert.deepEqual(ids(search(fixtureIndex, "type:Yielding")), ["pmc:AnapanasatiYieldsPiti"]);
  assert.deepEqual(ids(search(fixtureIndex, "kind:tradition")).sort(), ["pmt:Daoist", "pmt:Theravada"]);
  assert.deepEqual(ids(search(fixtureIndex, "tradition:daoist")).sort(), ["pmc:Qi", "pmt:Daoist"]);
  assert.deepEqual(ids(search(fixtureIndex, "source:nikaya")).sort(), [
    "pmc:AnapanasatiYieldsPiti",
    "pmp:Anapanasati",
  ]);
});

test("has: audits the corpus, and its negation is the interesting half", () => {
  const without = ids(search(fixtureIndex, "kind:instance -has:source"));
  assert.deepEqual(without, ["pmc:Qi"]);
  assert.ok(ids(search(fixtureIndex, "kind:instance has:source")).includes("pmc:Piti"));
  // A language tag falls through to the labels, so a gap in translation shows.
  assert.deepEqual(ids(search(fixtureIndex, "has:de")), ["pmc:Piti"]);
});

test("a negated word removes a term that would otherwise rank", () => {
  assert.ok(ids(search(fixtureIndex, "rapture")).includes("pmc:Piti"));
  assert.ok(!ids(search(fixtureIndex, "rapture -piti")).includes("pmc:Piti"));
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
    if (view.matrix) continue;
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
  assert.equal(matrix.total, 4); // Piti, Anapanasati, the pairing, Qi
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

test("a tradition that has contributed nothing still gets a row", () => {
  const barren = {
    ...FIXTURE,
    nodes: [...FIXTURE.nodes, node("pmt:Empty", "tradition", ["pm:Tradition"], "Empty tradition")],
  };
  const matrix = crosstab(barren, context(barren));
  const row = matrix.rows.find((entry) => entry.id === "pmt:Empty");
  assert.ok(row, "an absent row would read as an absent tradition");
  assert.equal(row.total, 0);
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
const onlyWithCorpus = { skip: corpus ? false : "set PRIMA_MATERIA_DATA to a built ontology-data.json" };

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
    assert.equal(Object.keys(positions).length, corpus.nodes.length, `${view.id} left a term unplaced`);
  }

  const matrix = crosstab(corpus, ctx);
  assert.equal(
    matrix.rows.reduce((sum, row) => sum + row.total, 0),
    matrix.total,
  );
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
