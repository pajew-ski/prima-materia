# CLAUDE.md

Permanent-Context für Claude Code. Enthält operative Constraints und Konventionen. Vollständige Spezifikation in `SPEC.md` — bei Konflikten gilt `SPEC.md`.

## Projekt

**prima-materia** — Open-Data-Ontologie für magisches/esoterisches Wissen, gestaltet nach einem **bewusstsein-ersten** Designprinzip. Source-Repo (manuell) → GitHub Actions (validate/compile/transmute) → Distribution-Repo (auto-generiert) → jsDelivr CDN.

## Kommandos

```bash
# Setup
pip install -r requirements.txt

# Validierung (SHACL)
python scripts/validate.py

# Vollständige Pipeline (lokal)
python scripts/compile.py --output build/prima-materia.ttl
python scripts/transmute.py --input build/prima-materia.ttl --context context/prima-materia-context.jsonld --output build/prima-materia.jsonld

# Tests (immer vor Commit)
pytest tests/
```

**Pre-Commit-Pflicht:** `python scripts/validate.py && pytest tests/` muss grün sein. Niemals committen wenn rot.

## Namespaces (in jeder neuen TTL-Datei)

```turtle
@prefix pm:      <https://pajew-ski.github.io/prima-materia/ontology#> .
@prefix pmt:     <https://pajew-ski.github.io/prima-materia/traditions/> .
@prefix pmc:     <https://pajew-ski.github.io/prima-materia/concepts/> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
```

## Naming-Konventionen

- **Klassen:** `PascalCase`, immer Gerundium (Prozess): `pm:Symbolizing`, `pm:Manifesting`, `pm:Perceiving`
- **Properties:** `camelCase`: `pm:assertedIn`, `pm:withinTradition`
- **Tradition-Instanzen:** `pmt:`-namespace, `PascalCase`: `pmt:ValentinianGnosis`
- **Konzept-Instanzen:** `pmc:`-namespace, `PascalCase`: `pmc:Pleroma`
- **Identifier sind englisch.** Mehrsprachige Labels via `rdfs:label "..."@en, "..."@de`

## Verboten (führt zu SHACL-Fail)

- ❌ Statische Substanz-Klassen: `pm:Symbol`, `pm:Concept`, `pm:Entity`, `pm:Object`
  - ✅ Stattdessen: `pm:Symbolizing`, `pm:Conceptualizing`, etc. (Prozess-Form)
- ❌ Konzept-Instanzen ohne `dcterms:source`
- ❌ Konzept-Instanzen ohne `pm:withinTradition`
- ❌ Klassen ohne `rdfs:label` und `skos:definition`
- ❌ Direktzitate aus modernen Übersetzungen urheberrechtlich geschützter Texte
- ❌ Deutsche Identifier in URIs/Klassennamen
- ❌ Network-Calls in `scripts/` — alles muss offline reproduzierbar sein
- ❌ Direkte Edits am Distribution-Repo (`prima-materia-dist`) — wird auto-generiert

## Quellenführung (verpflichtend)

Jede Konzept-Instanz braucht mindestens ein `dcterms:source` als:
- Bibliographische Referenz: `"Irenaeus, Adversus Haereses I.1 (c. 180 CE)"`
- DOI-URI: `<https://doi.org/...>`
- ISBN-URN: `<urn:isbn:978-...>`
- URL einer Open-Access-Edition

## Designprinzipien (kurz)

1. **Prozess statt Substanz** — Klassen als Gerundien
2. **AwarenessContext als First-Class** — `pm:assertedIn` taggt epistemischen Modus
3. **Sphoṭa** — Bedeutung in `pm:MeaningCluster`-Subgraphen, nicht in isolierten Triples
4. **Pronomenspektrum** — `pm:AwarenessSpace` (individual/dyadic/collective/universal) statt isoliertem Self/Other

Vollständige Begründung in `SPEC.md` Abschnitt 3.

## Workflow-Hygiene

- Neuer Code → Tests dafür schreiben (TDD bevorzugt)
- TTL-Änderungen → SHACL-Validierung lokal laufen lassen
- Commits klein und atomar, Messages im Imperativ
- Bei mehrdeutiger Spezifikation: **fragen, nicht raten**
- Bei Scope-Erweiterung über Phase 0/1 hinaus: **vorher mit User abklären**

## Repositories

- **Source (dieses Repo):** `pajew-ski/prima-materia` — manuell editieren
- **Distribution:** `pajew-ski/prima-materia-dist` — auto-generiert, nie manuell anfassen

## Manuelle User-Aktionen (nicht Agent-automatisierbar)

- Setzen des `DIST_REPO_TOKEN`-Secrets im Source-Repo (Personal Access Token mit Write-Access auf `prima-materia-dist`)
- Anlage des `prima-materia-dist`-Repos in GitHub
- jsDelivr-Cache-Purge bei Bedarf

Bei diesen Schritten den User explizit auffordern und warten.

## Lizenz

CC0 1.0 — Code, Ontologie und Spezifikation. Public-Domain-Dedication für maximale maschinelle Nachnutzbarkeit.
