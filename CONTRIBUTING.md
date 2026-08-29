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
  `dcterms:source`, and it must name a work and the place in it that
  carries the claim (`"Patañjali, Yogasūtra III.38"`). **No URLs of any
  kind**, DOI and open-access editions included — `pm:SourceIsLiteratureShape`
  rejects any value with an `http` prefix. Modern research never enters
  as `dcterms:source`; it belongs at `pm:evidenceFrom` on a `pm:Testing`
  node, where a DOI is admissible as a work identifier. See `SPEC.md §10`.
- **Tradition membership is mandatory.** Every concept instance needs
  `pm:withinTradition`.
- **Labels and definitions.** Every class needs `rdfs:label` and
  `skos:definition`.

## Quellenführung (Source Discipline)

Do not reproduce copyrighted primary texts verbatim. Paraphrase and cite.
Cite the work and the place in it, never a link. Videos, blogs, wikis and
forum posts are a way into a search, never a citation: trace them back to
the work, then cite the work.

## Behauptungen einreichen

Du musst keine Recherche mitliefern und in keiner Tradition stehen, um
eine Behauptung beizutragen. **Öffne ein Issue.** Eine Behauptung, die
der vorhandene Korpus noch nicht beantwortet, wird mitrecherchiert,
sobald ihr Korpus an der Reihe ist.

Ein brauchbares Behauptungs-Issue enthält:

1. Die Behauptung in einem entscheidbaren Satz. „Der Atem trägt die
   Energie" ist entscheidbar, „Atem ist wichtig" nicht.
2. Woher sie stammt, falls bekannt — ein Buch, eine Schule, ein
   Methodenentwurf, eine eigene Beobachtung.
3. Falls schon gesucht wurde: wo, und mit welchem Ergebnis.

Das Issue bleibt offen, bis ein Knoten die Behauptung trägt. Der
vollständige Lebenslauf steht in `SPEC.md §13`.

### Label-Vokabular

Aus dieser Liste übernehmen, nicht aus dem Gedächtnis schreiben: GitHub
legt einen unbekannten Labelnamen stillschweigend als neues Label an,
statt den Aufruf abzuweisen, und erzeugt so ein zweites Bündel, das
niemandem auffällt.

| Label | Bedeutung |
|---|---|
| `behauptung` | Behauptung, keine Repo-Arbeit. Jedes Behauptungs-Issue trägt es |
| `strittig` | zwei **Quellen** widersprechen einander; Ziel ist ein `pm:Disputing`-Knoten. Nicht, wenn eine Quelle einem Methodenentwurf widerspricht — ein Entwurf ist keine Seite |
| `unbelegt` | Schließgrund: plausible Korpora erschöpft, keine Stelle gefunden |
| `nicht-graphfaehig` | Schließgrund: gegen keine Überlieferung entscheidbar |
| `entwurf:strom` | Herkunft: Methodenentwurf „Der Strom" |

Dazu je ein `korpus:`-Label pro geprüftem oder zu prüfendem Korpus. Sie
kumulieren und sind damit zugleich das Protokoll der Suchabdeckung:

`korpus:daoistisch`, `korpus:upanisadisch`, `korpus:patanjala`,
`korpus:hathayoga`, `korpus:saiva-sakta`, `korpus:tibetisch`,
`korpus:theravada`, `korpus:dramaturgie`, `korpus:henochisch`,
`korpus:sefer-yetzirah`, `korpus:platonisch`, `korpus:graeco-roman`,
`korpus:eleusis`, `korpus:stoisch`, `korpus:hesychasmus`,
`korpus:wuestenvaeter`, `korpus:unterscheidung`, `korpus:sufismus`,
`korpus:kabbalistisch`, `korpus:islamisch`, `korpus:inkubation`,
`korpus:modern` (für Behauptungen, deren Ort `pm:evidenceFrom` an einem
`pm:Testing`-Knoten ist).

Die drei letztgenannten vor `korpus:modern` sind am 29.08.2026 an Issues
vergeben worden, bevor sie hier standen, und werden hier nachgetragen. Das
ist die Reihenfolge, die diese Regel gerade verhindern soll; sie steht
festgehalten, damit der Nachtrag nicht als Beleg dafür gilt, dass die
Reihenfolge beliebig wäre.

Ein neuer `korpus:`-Wert wird hier eingetragen, bevor er vergeben wird.
Er benennt den Korpus, den man aufschlägt, nicht die Datei, in der er
später landet.

## Offline Reproducibility

Scripts in `scripts/` must remain offline-reproducible. No network calls.

## Distribution Repository

Never edit `pajew-ski/prima-materia-dist` directly — it is auto-generated
by the `distribute.yml` GitHub Action on each push to `main`.

## Scope

Phase 0 and Phase 1 are delivered. New traditions are not added by plan
any more: `SPEC.md §14` sets out the two entrances and the three
decisions that precede a new file. If a change goes beyond that, raise an
issue first. Ask rather than guess.
