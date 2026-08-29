// Search over the compiled ontology. Everything here is pure: it takes the
// same ontology-data.json the graph is drawn from and returns ranked results.
// No DOM, no network, no index shipped alongside the data — three hundred
// terms is small enough that building the index in the browser costs a few
// milliseconds, and one implementation of the tokenizer cannot drift from
// another the way a build-time index and a query-time parser would.
//
// Four layers, each answering a failure of the one before it:
//
//   lexical    BM25 over weighted fields, so a hit in a label outranks the
//              same word buried in a note.
//   fuzzy      prefix and bounded edit distance, because the corpus is full of
//              transliterations nobody spells the same way twice.
//   semantic   query expansion along terms that co-occur inside a node
//              (positive pointwise mutual information), so "rapture" reaches
//              Pīti and a German label reaches its English gloss. This is what
//              a vector store would approximate; on a corpus this size the
//              co-occurrence counts are the thing itself.
//   structural spreading activation over the graph, so a match on a capacity
//              also surfaces the practice said to yield it. The semantics of
//              this corpus are largely in its edges; ignoring them would throw
//              away the better half of the signal.

// Characters that carry no decomposition of their own. Everything else folds
// through NFD: Pīti and Piti, samādhi and samadhi, Körper and korper are the
// same query, which matters in a corpus transliterated out of six scripts.
const SPECIAL = new Map(Object.entries({
  "ß": "ss", "æ": "ae", "œ": "oe", "ø": "o", "ł": "l",
  "đ": "d", "ħ": "h", "ı": "i", "ŋ": "n", "þ": "th",
  "ð": "d", "ʼ": "", "'": "", "ʾ": "", "ʿ": "",
}));

const COMBINING = /[\u0300-\u036f]/g;

/**
 * Fold text to bare lowercase ASCII, keeping a map back to the original.
 * Folding changes length — ß becomes two characters, a combining macron
 * vanishes — so a highlight computed on the folded form needs the map to land
 * on the right characters of the text the reader actually sees.
 */
export function foldWithMap(text) {
  let folded = "";
  const map = [];
  for (let i = 0; i < text.length; i++) {
    const lower = text[i].toLowerCase();
    const out = SPECIAL.get(lower) ?? lower.normalize("NFD").replace(COMBINING, "");
    for (const ch of out) {
      folded += ch;
      map.push(i);
    }
  }
  map.push(text.length);
  return { folded, map };
}

export const fold = (text) => foldWithMap(text).folded;

/** Tokens of a text, each carrying its span in the original string. */
export function tokenize(text) {
  const { folded, map } = foldWithMap(text);
  const out = [];
  for (const match of folded.matchAll(/[a-z0-9]+/g)) {
    const start = map[match.index];
    const end = Math.max(map[match.index + match[0].length] ?? text.length, start + 1);
    out.push({ term: match[0], start, end });
  }
  return out;
}

/** PascalCase local names are compounds: AnapanasatiYieldsPiti is three words. */
export function splitCamel(name) {
  return name
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .replace(/([A-Z]+)([A-Z][a-z])/g, "$1 $2");
}

// Field weights. A label is what a term is called and a source is what a claim
// stands on; both are worth more than a word that happens to fall in a note.
export const FIELDS = {
  label: 9,
  name: 6,
  source: 4,
  type: 3,
  tradition: 3,
  definition: 3,
  note: 2,
};
const FIELD_NAMES = Object.keys(FIELDS);

const K1 = 1.2;
const B = 0.72;

const local = (curie) => curie.split(":").pop();
const values = (langMap) => [...new Set(Object.values(langMap ?? {}))];

// ---------------------------------------------------------------------------
// Index
// ---------------------------------------------------------------------------

/**
 * Build the searchable projection of the graph: one document per node, seven
 * fields per document, plus the two derived structures the semantic layers
 * need — term associations and an adjacency list.
 */
export function buildIndex(data) {
  const byId = new Map(data.nodes.map((node) => [node.id, node]));

  // Tradition membership and claim class live in edges and types; search wants
  // them as text on the node, so "theravada rapture" is one query rather than
  // two lookups and an intersection.
  const traditionOf = new Map();
  const degree = new Map(data.nodes.map((node) => [node.id, 0]));
  const adjacency = new Map(data.nodes.map((node) => [node.id, new Set()]));
  for (const edge of data.edges) {
    if (!byId.has(edge.source) || !byId.has(edge.target)) continue;
    degree.set(edge.source, degree.get(edge.source) + 1);
    degree.set(edge.target, degree.get(edge.target) + 1);
    adjacency.get(edge.source).add(edge.target);
    adjacency.get(edge.target).add(edge.source);
    if (edge.rel === "withinTradition") {
      if (!traditionOf.has(edge.source)) traditionOf.set(edge.source, []);
      traditionOf.get(edge.source).push(edge.target);
    }
  }

  const labelOf = (id) => byId.get(id)?.label ?? local(id);

  const docs = data.nodes.map((node) => {
    const traditions = [...(traditionOf.get(node.id) ?? [])];
    // A tradition belongs to itself; without this pmt:Theravada would fall out
    // of tradition:theravada, which is the one term that filter is about.
    if (node.kind === "tradition") traditions.push(node.id);
    const types = node.types.filter((type) => type.startsWith("pm:"));
    const text = {
      label: values(node.labels).join(" · ") || node.label,
      name: `${local(node.id)} ${splitCamel(local(node.id))}`,
      source: node.sources.join(" · "),
      type: types.map((type) => `${local(type)} ${labelOf(type)}`).join(" · "),
      tradition: traditions.map(labelOf).join(" · "),
      definition: values(node.definition).join(" ").trim(),
      note: [...values(node.note), ...values(node.comment)].join(" ").trim(),
    };
    const tokens = {};
    for (const field of FIELD_NAMES) tokens[field] = tokenize(text[field]);
    return {
      id: node.id,
      node,
      text,
      tokens,
      traditions,
      types,
      degree: degree.get(node.id) ?? 0,
      folded: { label: fold(node.label), name: fold(local(node.id)) },
    };
  });

  // Postings. One flat array per term beats nested maps here: the corpus is a
  // few thousand terms and every query walks the array end to end anyway.
  const postings = new Map();
  const documentFrequency = new Map();
  const totalLength = Object.fromEntries(FIELD_NAMES.map((field) => [field, 0]));
  docs.forEach((doc, index) => {
    const seen = new Set();
    for (const field of FIELD_NAMES) {
      totalLength[field] += doc.tokens[field].length;
      const counts = new Map();
      for (const { term } of doc.tokens[field]) counts.set(term, (counts.get(term) ?? 0) + 1);
      for (const [term, frequency] of counts) {
        if (!postings.has(term)) postings.set(term, []);
        postings.get(term).push({ doc: index, field, tf: frequency, length: doc.tokens[field].length });
        seen.add(term);
      }
    }
    for (const term of seen) documentFrequency.set(term, (documentFrequency.get(term) ?? 0) + 1);
  });

  const averageLength = Object.fromEntries(
    FIELD_NAMES.map((field) => [field, totalLength[field] / Math.max(docs.length, 1) || 1]),
  );

  const index = {
    docs,
    byId: new Map(docs.map((doc, position) => [doc.id, position])),
    postings,
    documentFrequency,
    vocabulary: [...postings.keys()],
    averageLength,
    adjacency,
    kinds: [...new Set(data.nodes.map((node) => node.kind))].sort(),
  };
  index.associations = buildAssociations(index);
  return index;
}

// A term in fewer nodes than this carries no reliable association; a term in
// more than this share is the corpus's own connective tissue — "tradition",
// "practice" — and would associate with everything.
const ASSOC_MIN_DF = 2;
const ASSOC_MAX_SHARE = 0.28;
const ASSOC_MIN_PAIR = 2;
const ASSOC_MIN_SCORE = 0.6;
const ASSOC_PER_TERM = 6;
const ASSOC_TERMS_PER_DOC = 44;

/**
 * Positive pointwise mutual information over co-occurrence inside a node.
 *
 * Two terms are associated when they keep turning up in the same node and are
 * each rare enough that this is not an accident. It is the counting method
 * word vectors were invented to compress; with a few hundred documents there
 * is nothing to compress, so the counts are used directly. The pay-off is
 * specific to this corpus: a node almost always states a term and its gloss
 * together, so the transliteration and the English word for the same thing
 * become neighbours without anyone writing a synonym list — and so do the
 * German and English labels of one term.
 */
function buildAssociations(index) {
  const { docs, documentFrequency } = index;
  const maxDocumentFrequency = Math.max(2, Math.floor(docs.length * ASSOC_MAX_SHARE));
  const pairs = new Map();

  for (const doc of docs) {
    const terms = new Set();
    for (const field of FIELD_NAMES) for (const { term } of doc.tokens[field]) terms.add(term);
    // Rarest first: what is informative about a node, not what it shares with
    // every other node.
    const kept = [...terms]
      .filter((term) => {
        const frequency = documentFrequency.get(term) ?? 0;
        return term.length >= 3 && frequency >= ASSOC_MIN_DF && frequency <= maxDocumentFrequency;
      })
      .sort((a, b) => documentFrequency.get(a) - documentFrequency.get(b))
      .slice(0, ASSOC_TERMS_PER_DOC)
      .sort();
    for (let i = 0; i < kept.length; i++) {
      for (let j = i + 1; j < kept.length; j++) {
        const key = `${kept[i]} ${kept[j]}`;
        pairs.set(key, (pairs.get(key) ?? 0) + 1);
      }
    }
  }

  const candidates = new Map();
  const offer = (from, to, score) => {
    if (!candidates.has(from)) candidates.set(from, []);
    candidates.get(from).push({ term: to, score });
  };
  for (const [key, together] of pairs) {
    if (together < ASSOC_MIN_PAIR) continue;
    const [a, b] = key.split(" ");
    const score = Math.log(
      (together * docs.length) / (documentFrequency.get(a) * documentFrequency.get(b)),
    );
    if (score < ASSOC_MIN_SCORE) continue;
    offer(a, b, score);
    offer(b, a, score);
  }

  // Normalised per term, so the expansion weight reads as "how strong for this
  // word" rather than "how rare the corpus happens to be".
  const associations = new Map();
  for (const [term, list] of candidates) {
    list.sort((x, y) => y.score - x.score);
    const top = list.slice(0, ASSOC_PER_TERM);
    const best = top[0].score;
    associations.set(term, top.map((entry) => ({ term: entry.term, weight: entry.score / best })));
  }
  return associations;
}

// ---------------------------------------------------------------------------
// Query language
// ---------------------------------------------------------------------------

export const FILTER_FIELDS = new Set(["kind", "tradition", "type", "class", "source", "has", "lang"]);

/**
 * Split a query into free terms, quoted phrases, negations and filters.
 *
 * The filters are what makes the corpus auditable rather than merely
 * browsable: `-has:source` lists every node that asserts something without
 * saying on what, and `tradition:daoist type:Yielding` answers how much of one
 * tradition's material has been brought into one claim form at all.
 */
export function parseQuery(input) {
  const query = {
    terms: [],
    phrases: [],
    negatedTerms: [],
    negatedPhrases: [],
    filters: [],
    raw: input ?? "",
  };
  const pattern = /(-?)(?:([A-Za-z]+):)?(?:"([^"]*)"|(\S+))/g;
  for (const match of (input ?? "").matchAll(pattern)) {
    const [, negated, field, quoted, bare] = match;
    const value = (quoted ?? bare ?? "").trim();
    if (!value) continue;
    if (field && FILTER_FIELDS.has(field.toLowerCase())) {
      query.filters.push({
        field: field.toLowerCase(),
        value: fold(value),
        negated: negated === "-",
      });
      continue;
    }
    // A prefix that names no filter is simply part of what was typed.
    const tokens = tokenize(field ? `${field} ${value}` : value).map((token) => token.term);
    if (!tokens.length) continue;
    if (quoted !== undefined && tokens.length > 1) {
      (negated ? query.negatedPhrases : query.phrases).push(tokens);
    }
    for (const token of tokens) (negated ? query.negatedTerms : query.terms).push(token);
  }
  return query;
}

/**
 * Does this text contain the filter value as a run of whole words, the last of
 * which may still be being typed? A plain substring test would let
 * `type:Testing` match Attesting, which is the opposite of what a filter is
 * for: filters answer questions about the corpus and have to be exact about
 * what they counted.
 */
function fieldMatches(text, value) {
  const wanted = tokenize(value).map((token) => token.term);
  if (!wanted.length) return false;
  const found = tokenize(text ?? "").map((token) => token.term);
  outer: for (let i = 0; i + wanted.length <= found.length; i++) {
    for (let j = 0; j < wanted.length; j++) {
      const last = j === wanted.length - 1;
      if (last ? !found[i + j].startsWith(wanted[j]) : found[i + j] !== wanted[j]) continue outer;
    }
    return true;
  }
  return false;
}

function matchesFilter(doc, filter, index) {
  const contains = (text) => fieldMatches(text, filter.value);
  const labelOfId = (id) => index.docs[index.byId.get(id)]?.node.label;
  switch (filter.field) {
    case "kind":
      return fold(doc.node.kind).startsWith(filter.value);
    case "tradition":
      // Three spellings of the same tradition: the local name as it stands in
      // the CURIE (PatanjalaYoga), the same name read as the compound it is
      // (Patanjala Yoga), and the label (Pātañjala Yoga). All three are things
      // a reader will type, and the matrix builds its queries from the first.
      return doc.traditions.some(
        (id) => contains(local(id)) || contains(splitCamel(local(id))) || contains(labelOfId(id)),
      );
    case "type":
    case "class":
      return contains(doc.text.type);
    case "source":
      return doc.node.sources.some((source) => contains(source));
    case "lang":
      return Object.keys(doc.node.labels).includes(filter.value);
    case "has":
      switch (filter.value) {
        case "source": return doc.node.sources.length > 0;
        case "definition": return Object.keys(doc.node.definition).length > 0;
        case "note":
          return Object.keys(doc.node.note).length > 0 || Object.keys(doc.node.comment).length > 0;
        case "tradition": return doc.traditions.length > 0;
        case "relation": return (index.adjacency.get(doc.id)?.size ?? 0) > 0;
        // Anything else reads as a language tag: has:de finds what has been
        // translated, -has:de what has not.
        default: return Object.keys(doc.node.labels).includes(filter.value);
      }
    default:
      return true;
  }
}

// ---------------------------------------------------------------------------
// Fuzzy expansion
// ---------------------------------------------------------------------------

/** Damerau-Levenshtein, abandoned as soon as every cell in a row exceeds the budget. */
export function editDistance(a, b, budget) {
  if (Math.abs(a.length - b.length) > budget) return budget + 1;
  let twoBack = null;
  let previous = Array.from({ length: b.length + 1 }, (_, index) => index);
  for (let i = 1; i <= a.length; i++) {
    const current = [i];
    let best = i;
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      let value = Math.min(current[j - 1] + 1, previous[j] + 1, previous[j - 1] + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
        value = Math.min(value, twoBack[j - 2] + 1);
      }
      current.push(value);
      best = Math.min(best, value);
    }
    if (best > budget) return budget + 1;
    twoBack = previous;
    previous = current;
  }
  return previous[b.length];
}

/** How much misspelling a query word of this length earns. */
export function fuzzyBudget(length) {
  if (length <= 3) return 0;
  if (length <= 6) return 1;
  return 2;
}

/**
 * Every index term a query word should reach, and what each is worth.
 * Exact beats prefix beats a typo beats an association, and the best route to
 * a given term wins — no term is counted twice for being reachable twice.
 */
export function expandTerm(index, word, { fuzzy = true, semantic = true } = {}) {
  const variants = new Map();
  const offer = (term, weight, how) => {
    const existing = variants.get(term);
    if (!existing || existing.weight < weight) variants.set(term, { term, weight, how });
  };

  if (index.postings.has(word)) offer(word, 1, "exact");

  const budget = fuzzy ? fuzzyBudget(word.length) : 0;
  for (const term of index.vocabulary) {
    if (term === word) continue;
    if (word.length >= 2 && term.startsWith(word)) {
      // A partial word is what typing looks like before it is finished; the
      // weight follows how much of the term the reader has committed to.
      offer(term, 0.55 + (0.4 * word.length) / term.length, "prefix");
      continue;
    }
    if (budget === 0) continue;
    const distance = editDistance(word, term, budget);
    if (distance <= budget) offer(term, distance === 1 ? 0.82 : 0.58, "fuzzy");
  }

  if (semantic) {
    for (const { term, weight } of index.associations.get(word) ?? []) {
      offer(term, 0.34 * weight, "related");
    }
  }
  return [...variants.values()];
}

// ---------------------------------------------------------------------------
// Ranking
// ---------------------------------------------------------------------------

function bm25(index, term, field, posting) {
  const frequency = index.documentFrequency.get(term) ?? 0;
  const idf = Math.log(1 + (index.docs.length - frequency + 0.5) / (frequency + 0.5));
  const average = index.averageLength[field] || 1;
  const saturation = posting.tf + K1 * (1 - B + (B * posting.length) / average);
  return (idf * posting.tf * (K1 + 1)) / saturation;
}

/** The first field in which these words occur as consecutive tokens. */
function hasPhrase(doc, phrase) {
  for (const field of FIELD_NAMES) {
    const tokens = doc.tokens[field];
    for (let i = 0; i + phrase.length <= tokens.length; i++) {
      let ok = true;
      for (let j = 0; j < phrase.length; j++) {
        if (tokens[i + j].term !== phrase[j]) {
          ok = false;
          break;
        }
      }
      if (ok) return field;
    }
  }
  return null;
}

const GRAPH_DAMPING = [0.3, 0.09];
const MIN_RELATIVE_SCORE = 0.02;

/**
 * Rank the corpus against a query.
 *
 * Every surviving document comes back with its score and the reason it scored:
 * which fields matched, whether a word had to be corrected or expanded, and
 * which already-matching node pulled it in over the graph. A result that
 * cannot say why it is a result is indistinguishable from a guess, and this
 * repository is in the business of telling those apart.
 */
export function search(index, input, options = {}) {
  const { limit = 80, fuzzy = true, semantic = true, structural = true } = options;
  const query = parseQuery(input);

  let candidates = index.docs.map((_, position) => position);
  for (const filter of query.filters) {
    candidates = candidates.filter(
      (position) => matchesFilter(index.docs[position], filter, index) !== filter.negated,
    );
  }

  const explanations = new Map();
  const reasonFor = (position) => {
    if (!explanations.has(position)) {
      explanations.set(position, {
        fields: new Set(),
        matched: new Set(),
        covered: new Set(),
        corrected: [],
        related: [],
        via: null,
        viaScore: 0,
      });
    }
    return explanations.get(position);
  };

  // A query of filters alone is a listing, not a search: order it by how
  // connected each term is, so the spine of the filtered set comes first.
  if (!query.terms.length && !query.phrases.length) {
    const listed = candidates
      .map((position) => index.docs[position])
      .sort((a, b) => b.degree - a.degree || a.node.label.localeCompare(b.node.label))
      .map((doc) => ({
        id: doc.id,
        doc,
        score: 1,
        reason: { fields: [], corrected: [], related: [], via: null },
        snippet: snippetFor(doc, new Set()),
      }));
    return { query, total: listed.length, results: listed.slice(0, limit), listing: true };
  }

  const allowed = new Set(candidates);
  const scores = new Map();
  const add = (position, amount) => scores.set(position, (scores.get(position) ?? 0) + amount);

  for (const word of query.terms) {
    for (const variant of expandTerm(index, word, { fuzzy, semantic })) {
      for (const posting of index.postings.get(variant.term) ?? []) {
        if (!allowed.has(posting.doc)) continue;
        add(posting.doc, FIELDS[posting.field] * variant.weight * bm25(index, variant.term, posting.field, posting));
        const reason = reasonFor(posting.doc);
        reason.fields.add(posting.field);
        reason.matched.add(variant.term);
        if (variant.how === "fuzzy" && !reason.corrected.includes(variant.term)) {
          reason.corrected.push(variant.term);
        }
        if (variant.how === "related") {
          if (!reason.related.includes(variant.term)) reason.related.push(variant.term);
        } else {
          reason.covered.add(word);
        }
      }
    }
  }

  for (const [position, score] of [...scores]) {
    const doc = index.docs[position];
    const reason = reasonFor(position);
    let factor = 1;

    // Every word accounted for is worth far more than one word accounted for
    // loudly — without going so far as to turn a query into a conjunction.
    const coverage = query.terms.length ? reason.covered.size / query.terms.length : 1;
    factor *= (0.3 + 0.7 * coverage) ** 2;

    // A phrase in quotes is a demand, not a hint.
    for (const phrase of query.phrases) {
      const field = hasPhrase(doc, phrase);
      if (field) {
        factor *= 1.7;
        reason.fields.add(field);
      } else {
        factor *= 0.12;
      }
    }
    for (const phrase of query.negatedPhrases) if (hasPhrase(doc, phrase)) factor = 0;
    for (const word of query.negatedTerms) {
      if ((index.postings.get(word) ?? []).some((posting) => posting.doc === position)) factor = 0;
    }

    // Someone typing a term's own name means that term.
    const typed = query.terms.join("");
    if (doc.folded.label === typed || doc.folded.name === typed) factor *= 3;
    else if (doc.folded.label.startsWith(typed) || doc.folded.name.startsWith(typed)) factor *= 1.6;

    // Ties go to the better connected term: in a graph, the hub is the one a
    // reader was more likely reaching for.
    factor *= 1 + 0.07 * Math.log1p(doc.degree);
    scores.set(position, score * factor);
  }

  for (const [position, score] of [...scores]) if (score <= 0) scores.delete(position);

  // Spreading activation. A node beside a strong match is worth showing even
  // when it shares no word with the query: that adjacency is the assertion the
  // graph was built to record. Both ends are normalised by degree, so a class
  // with two hundred instances hanging off it cannot flood the result set.
  if (structural && scores.size) {
    let frontier = new Map(scores);
    for (const damping of GRAPH_DAMPING) {
      const next = new Map();
      for (const [position, score] of frontier) {
        const neighbours = index.adjacency.get(index.docs[position].id) ?? new Set();
        if (!neighbours.size) continue;
        for (const neighbourId of neighbours) {
          const target = index.byId.get(neighbourId);
          if (target === undefined || !allowed.has(target)) continue;
          const targetDegree = index.adjacency.get(neighbourId)?.size || 1;
          const share = (damping * score) / Math.sqrt(neighbours.size * targetDegree);
          next.set(target, (next.get(target) ?? 0) + share);
          if (!scores.has(target)) {
            const reason = reasonFor(target);
            if (share > reason.viaScore) {
              reason.via = index.docs[position].id;
              reason.viaScore = share;
            }
          }
        }
      }
      for (const [position, amount] of next) add(position, amount);
      frontier = next;
    }
  }

  const results = [...scores]
    .filter(([, score]) => score > 0)
    .sort(
      (a, b) => b[1] - a[1] || index.docs[a[0]].node.label.localeCompare(index.docs[b[0]].node.label),
    )
    .map(([position, score]) => {
      const doc = index.docs[position];
      const reason = reasonFor(position);
      return {
        id: doc.id,
        doc,
        score,
        reason: {
          fields: [...reason.fields],
          corrected: reason.corrected,
          related: reason.related,
          via: reason.fields.size ? null : reason.via,
        },
        snippet: snippetFor(doc, reason.matched),
      };
    });

  // Scores are relative to the best hit, and everything under a fiftieth of it
  // is dropped. Expansion and spreading activation reach almost the whole graph
  // at some minute weight; reporting that as a result count would be a lie
  // about how much the corpus actually says on the question.
  const best = results[0]?.score || 1;
  for (const result of results) result.score /= best;
  const kept = results.filter((result) => result.score >= MIN_RELATIVE_SCORE);
  return { query, total: kept.length, results: kept.slice(0, limit), listing: false };
}

// ---------------------------------------------------------------------------
// Snippets
// ---------------------------------------------------------------------------

const SNIPPET_FIELDS = ["definition", "note", "source", "label"];
const SNIPPET_WIDTH = 190;

/**
 * The one passage worth showing under a result, and the spans to mark in it.
 * A field that actually contains a matched word wins; failing that, prose
 * before metadata, because a definition says what a term is and that is what a
 * reader scanning a list of results is deciding between.
 */
export function snippetFor(doc, matched) {
  const withHit = SNIPPET_FIELDS.map((field) => ({
    field,
    hits: doc.text[field] ? doc.tokens[field].filter((token) => matched.has(token.term)) : [],
  })).find((entry) => entry.hits.length);

  if (withHit) {
    const text = doc.text[withHit.field];
    const clipped = clip(text, Math.max(0, withHit.hits[0].start - 60));
    const ranges = withHit.hits
      .map((hit) => [hit.start - clipped.offset, hit.end - clipped.offset])
      .filter(([start, end]) => start >= 0 && end <= clipped.text.length);
    return { field: withHit.field, text: clipped.text, ranges };
  }

  for (const field of SNIPPET_FIELDS) {
    if (doc.text[field]) return { field, text: clip(doc.text[field], 0).text, ranges: [] };
  }
  return { field: "label", text: doc.node.label, ranges: [] };
}

/** A window of the text starting near `start`, cut at word boundaries. */
function clip(text, start) {
  let from = start;
  if (from > 0) {
    const space = text.lastIndexOf(" ", from);
    from = space > 0 ? space + 1 : from;
  }
  let body = text.slice(from, from + SNIPPET_WIDTH);
  if (from + SNIPPET_WIDTH < text.length) {
    const space = body.lastIndexOf(" ");
    if (space > SNIPPET_WIDTH * 0.6) body = body.slice(0, space);
    body += "…";
  }
  const lead = from > 0 ? "…" : "";
  return { text: lead + body, offset: from - lead.length };
}

/**
 * Openings for a reader with nothing typed yet. They are deliberately not
 * "popular searches": each one answers a question the repository says it cares
 * about, and the first of them reports where the corpus is unsourced.
 */
export function hints(index) {
  const tradition = index.docs.find((doc) => doc.node.kind === "tradition");
  return [
    { query: "type:Disputing", label: "where the witnesses disagree" },
    { query: "type:Converging", label: "where traditions meet" },
    { query: "type:Cautioning", label: "warnings a tradition gives about itself" },
    { query: "type:Testing", label: "claims someone has tried to examine" },
    { query: "kind:instance -has:source", label: "assertions standing on nothing" },
    tradition
      ? { query: `tradition:${local(tradition.id)}`, label: `everything under ${tradition.node.label}` }
      : null,
  ].filter(Boolean);
}
