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

# GitHub-Pages-Seite bauen und lokal ansehen
python scripts/publish.py --output build/site
python -m http.server -d build/site

# Tests (immer vor Commit)
pytest tests/
```

**Pre-Commit-Pflicht:** `python scripts/validate.py && pytest tests/` muss grün sein. Niemals committen wenn rot.

## Website

`site/` enthält die handgeschriebenen Assets der GitHub-Pages-Seite (`index.html`, `style.css`, `ontology.js`, `theme.js`, `ontology/index.html`). `scripts/publish.py` kopiert sie nach `build/site/` und legt die aus dem Graphen abgeleiteten Daten (`ontology-data.json`) sowie die Serialisierungen daneben. Der `Pages`-Workflow deployt das bei jedem Push auf `main`.

- Die Seite wird **komplett aus dem kompilierten Graphen** gespeist. Neue Klassen, Properties und Instanzen erscheinen ohne Code-Änderung; Zähler, Legende und Panel leiten sich aus den Daten ab.
- Design-Vorbild ist `pajew-ski/temet-nosce`: achromatische oklch-Tokens, φ-basierte Spacing- und Typo-Leiter, Canvas/Panel im Verhältnis φ:1, Cytoscape über jsDelivr.
- Neue Node-Art im Graphen → `KINDS` in `site/ontology.js` erweitern (Shape, Legenden-Name, Plural) und in `_kind()` in `scripts/publish.py` klassifizieren.

## Namespaces (in jeder neuen TTL-Datei)

```turtle
@prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
@prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
@prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
@prefix pmp:     <https://pajew.ski/prima-materia/practices/> .
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
- ❌ Direkte Edits an `build/site/` — wird bei jedem `publish.py`-Lauf neu erzeugt; Quelle ist `site/`
- ❌ Fakten über die Ontologie in `site/index.html` hart kodieren (Anzahl Terme, Klassenlisten) — aus `ontology-data.json` ableiten

## Quellenführung (verpflichtend)

**Der Graph enthält keine Wahrheiten, sondern Behauptungen mit Herkunft.** Diese Herkunft zu prüfen ist die Kernaufgabe jedes Agenten an diesem Repo, nicht eine Sorgfaltspflicht am Rand. Der Mensch ist die letzte Instanz vor dem Merge, nicht die erste und nicht die einzige.

Jede Behauptung braucht mindestens ein `dcterms:source` als bibliographische Referenz auf ein überliefertes Werk, mit der Stelle, die sie trägt:

- `"1 Henoch 8:1"`
- `"Irenaeus, Adversus Haereses I.1"`
- `"Patañjali, Yogasūtra III.16-49"`

Nicht zulässig, weder als Quelle noch als Ersatz:

- ❌ **URLs jeder Art**, auch DOI und Open-Access-Editionen. Ein Link benennt einen Ort, der sich ändert; ein Werk benennt etwas, das ein Leser unabhängig von diesem Graphen beschaffen kann. `pm:SourceIsLiteratureShape` weist jeden `dcterms:source`-Wert mit `http`-Präfix ab.
- ❌ **YouTube-Videos, Blogs, Wikipedia, Forenbeiträge.** Als Rechercheeinstieg brauchbar, als Beleg nie. Was dort steht, ist bis zum Werk zurückzuverfolgen, und dann zählt das Werk.
- ❌ **Unveröffentlichte eigene Texte, Arbeitsfassungen, Methodenentwürfe.** Auch die des Betreibers nicht.
- ❌ **Sekundäre Zusammenfassungen** anstelle der Stelle, die sie zusammenfassen.

Es geht um uraltes magisches Wissen, nicht um aktuelle Meinungen. Ein Beleg aus dem Jahr 2024 belegt, was 2024 jemand behauptet hat, und das ist selten das, was der Knoten aussagt.

**Richtungssinn.** prima-materia ist die Basis, aus der die Methoden des **Opus Purum** extrahiert werden, nicht umgekehrt. Ein Methodenentwurf ist kein Beleg, sondern eine Menge von Behauptungen, die einzeln gegen überliefertes Schrifttum zu grounden sind. Was sich nicht grounden lässt, kommt nicht in den Graphen und bleibt Entwurf.

**Vor jedem inhaltlichen PR:** für jede eingetragene Behauptung die Stelle im Werk benannt, die sie trägt, und `pm:attestedBy` gesetzt. Bei Unsicherheit über eine Zuschreibung nicht eintragen. Ein gemergter Fehler ist über `prima-materia-dist` und jsDelivr nicht privat und nicht zurückholbar.

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

**Löst eine Validierung aus, wird sie gemeldet, nicht umformuliert.** Das gilt für SHACL, für die Tests und für jeden vorgeschalteten Wächter im Schreibweg. Hat ein Wächter falsch ausgelöst, ist das ein Befund über den Wächter und gehört berichtet, damit er repariert wird. Eine Umgehung, die nicht auffällt, repariert nichts und kostet das Vertrauen in genau die Vorrichtung, die den Menschen am Merge entlasten soll. Ob der Alarm berechtigt war, entscheidet nicht, wer schreiben will.

## Repositories

- **Source (dieses Repo):** `pajew-ski/prima-materia` — manuell editieren
- **Distribution:** `pajew-ski/prima-materia-dist` — auto-generiert, nie manuell anfassen

## Manuelle User-Aktionen (nicht Agent-automatisierbar)

- Aktivieren von GitHub Pages: **Settings → Pages → Source: GitHub Actions**. Der Workflow kann die Quelle nicht selbst umstellen.
- **Registrierung des Namensraums bei w3id.org.** Pull Request gegen `perma-id/w3id.org` mit dem Verzeichnis `prima-materia/` und einer `.htaccess`, die den ganzen Teilbaum nach `https://pajew.ski/prima-materia/` umleitet. Bis dieser PR gemergt ist, sind die geprägten IRIs Bezeichner ohne Auflösung; die Daten liegen unverändert am Auslieferungsort. Ein Agent kann das nicht tun: Fremdrepos sind über `gh_*` nur lesbar.
- Setzen des `DIST_REPO_TOKEN`-Secrets im Source-Repo (Personal Access Token mit Write-Access auf `prima-materia-dist`)
- Anlage des `prima-materia-dist`-Repos in GitHub
- jsDelivr-Cache-Purge bei Bedarf

Bei diesen Schritten den User explizit auffordern und warten.

## Lizenz

CC0 1.0 — Code, Ontologie und Spezifikation. Public-Domain-Dedication für maximale maschinelle Nachnutzbarkeit.
