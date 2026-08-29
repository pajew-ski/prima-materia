# prima-materia

Open-Data ontology of magical and esoteric knowledge, designed under a
**consciousness-first** design principle. Released into the public domain
under CC0 1.0.

## Overview

`prima-materia` provides a machine-readable semantic substrate for LLM agents
and knowledge-graph systems that need to reason about esoteric, mystical, and
magical knowledge across traditions. It is part of a larger architecture: it
is the *undifferentiated primordial substance* on which the separate **Opus
Purum** project operates.

The ontology models **processes instead of substances** (gerund-form classes),
embeds triples in `AwarenessContext` named graphs, and treats bounded
subgraphs (`MeaningCluster`) as the fundamental units of meaning — following
Bhartṛhari's Sphoṭa principle.

## Website

The ontology is published as a browsable page at
<https://pajew.ski/prima-materia/>: every class, property, and
instance drawn as the graph it is, with definitions, sources, and bilingual
labels. Selecting a term gives it a URL, so a definition can be cited rather
than described.

The page can be asked questions and can be redrawn. Search forgives the
spelling of a transliteration, follows the words a term keeps company with —
so *rapture* reaches Pīti and *Verzückung* reaches both — carries a match to
its neighbours over the graph, and says of every result why it is one.
Filters narrow the field and audit it: `type:Disputing` for where the
witnesses disagree, `tradition:Daoist`, `source:Visuddhimagga`,
`-has:source` for what asserts without saying on what. Seven arrangements
answer seven different questions — the vocabulary's strata, what stands under
which class, which tradition carries what, how far each kind of claim has got,
what the graph hangs on, what clusters unbidden, and a cross-tabulation of
traditions against claim forms whose empty cells are the finding. The
arrangement, the query and the term are all in the URL, so a particular
reading of the corpus can be sent rather than described.

The site is built from the same sources as the distribution artefacts and
deployed by the `Pages` workflow on every push to `main`. It also serves
`prima-materia.ttl`, `prima-materia.jsonld`, and `context.jsonld`, so the
namespace IRI resolves to the ontology it names: dereferencing
`https://pajew.ski/prima-materia/ontology#Symbolizing` lands on that term.

Build it locally with:

```bash
python scripts/publish.py --output build/site
python -m http.server -d build/site
```

Page assets are hand-written under `site/`; everything else in the output is
generated. Do not edit `build/site/` — it is rebuilt from scratch on every run.

## Repository Layout

- **Source (this repo):** `pajew-ski/prima-materia` — manually maintained
- **Distribution:** `pajew-ski/prima-materia-dist` — auto-generated, do not
  edit manually
- **CDN:** jsDelivr serves the distribution repo under
  `https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/`

See `SPEC.md` for the full specification and `CLAUDE.md` for the
operational constraints used by agent contributors.

## Quick Start

```bash
pip install -r requirements.txt

python scripts/validate.py
python scripts/compile.py --output build/prima-materia.ttl
python scripts/transmute.py \
    --input build/prima-materia.ttl \
    --context context/prima-materia-context.jsonld \
    --output build/prima-materia.jsonld
python scripts/publish.py --output build/site

pytest tests/
```

A freshly cloned repository must pass
`pip install -r requirements.txt && python scripts/validate.py && pytest tests/`
without errors.

## Manual Setup Steps (not agent-automatable)

- Create the `pajew-ski/prima-materia-dist` repository on GitHub.
- Enable GitHub Pages for this repository with **Settings → Pages → Source:
  GitHub Actions**. The `Pages` workflow cannot switch the source on.
- Set the `DIST_REPO_TOKEN` secret in this repository's settings (Personal
  Access Token with write access to `prima-materia-dist`).
- Purge the jsDelivr cache when a release needs to propagate immediately.

## Naming Conventions

- **Classes** — `PascalCase`, always gerund (process form):
  `pm:Symbolizing`, `pm:Manifesting`, `pm:Perceiving`.
- **Properties** — `camelCase`: `pm:assertedIn`, `pm:withinTradition`.
- **Tradition instances** — `pmt:` namespace, `PascalCase`:
  `pmt:ValentinianGnosis`.
- **Concept instances** — `pmc:` namespace, `PascalCase`: `pmc:Pleroma`.
- Identifiers are **English**; multilingual labels via
  `rdfs:label "..."@en, "..."@de`.

## License

CC0 1.0 Universal — public-domain dedication for code, ontology, and
specification. See `LICENSE`.
