# Contributing to prima-materia

Thank you for considering a contribution. The ontology is released under
CC0 1.0 — by submitting changes you agree that your contribution is
likewise dedicated to the public domain.

## Before You Open a Pull Request

1. Read `SPEC.md` end-to-end. It is the single source of truth. Where this
   file or `CLAUDE.md` conflict with `SPEC.md`, `SPEC.md` wins.
2. Run the local validation pipeline; it must pass before you push:
   ```bash
   pip install -r requirements.txt
   python scripts/validate.py
   pytest tests/
   ```
3. Keep commits small and atomic. Commit messages in the imperative mood.

## Ontology Conventions

- **Process, not substance.** Every new class is a gerund. Static-substance
  classes (`pm:Symbol`, `pm:Concept`, `pm:Entity`, `pm:Object`) are
  forbidden and will fail SHACL validation.
- **English identifiers.** URIs and class names stay in English; use
  `rdfs:label` with language tags (`@en`, `@de`, ...) for multilingual
  presentation.
- **Sources are mandatory.** Every concept instance needs at least one
  `dcterms:source` (bibliographic string, DOI URI, ISBN URN, or
  open-access URL).
- **Tradition membership is mandatory.** Every concept instance needs
  `pm:withinTradition`.
- **Labels and definitions.** Every class needs `rdfs:label` and
  `skos:definition`.

## Quellenführung (Source Discipline)

Do not reproduce copyrighted primary texts verbatim. Paraphrase and cite.
Prefer primary-source references or open-access editions.

## Offline Reproducibility

Scripts in `scripts/` must remain offline-reproducible. No network calls.

## Distribution Repository

Never edit `pajew-ski/prima-materia-dist` directly — it is auto-generated
by the `distribute.yml` GitHub Action on each push to `main`.

## Scope

If a change expands the scope beyond the Phase 0 / Phase 1 deliverables in
`SPEC.md §4`, raise an issue first. Ask rather than guess.
