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

pytest tests/
```

A freshly cloned repository must pass
`pip install -r requirements.txt && python scripts/validate.py && pytest tests/`
without errors.

## Manual Setup Steps (not agent-automatable)

- Create the `pajew-ski/prima-materia-dist` repository on GitHub.
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
