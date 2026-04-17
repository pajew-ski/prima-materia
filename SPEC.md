# prima-materia — Project Specification

> **Agent-Hinweis:** Dieses Dokument ist die alleinige Quelle der Wahrheit (SSOT) für die Implementierung. Lies es vollständig, bevor du Code schreibst. Bei Konflikten zwischen diesem Dokument und deiner Trainingsintuition gilt dieses Dokument. Bei echten Unklarheiten frag nach — rate nicht.

## 0. Mission & Kontext

**prima-materia** ist eine Open-Data-Ontologie für magisches und esoterisches Wissen, gestaltet als maschinenlesbares semantisches Substrat für LLM-Agenten und Knowledge-Graph-Systeme. Das Projekt ist Teil einer übergeordneten Architektur — es bildet die *undifferenzierte Ursubstanz*, auf der das **Opus Purum** (separates Projekt) operiert.

Die ontologische Besonderheit: prima-materia folgt einem **bewusstsein-ersten** Designprinzip (Consciousness-First Ontology). Die Klassen modellieren Prozesse statt Substanzen, die Triples werden in `AwarenessContext`-named-graphs eingebettet, und semantische Bedeutung emergiert aus Subgraph-Clustern (Sphoṭa-Prinzip), nicht aus isolierten Knoten.

## 1. Repository-Struktur

Zwei separate GitHub-Repositories:

```
prima-materia/                  # Source Repository (manuell gepflegt)
├── README.md
├── LICENSE                      # CC0 1.0
├── CONTRIBUTING.md
├── SPEC.md                      # Dieses Dokument
├── CLAUDE.md                    # Agent-Instruktionen (Kurzform von SPEC.md)
├── ontology/
│   ├── core.ttl                 # Meta-Ontologie (pm:Process, pm:AwarenessContext, etc.)
│   ├── consciousness.ttl        # Bewusstseinszustände (Jāgrat/Svapna/Suṣupti/Turīya)
│   └── alignments.ttl           # Mappings zu SKOS, DCTerms, schema.org
├── traditions/
│   ├── valentinian.ttl          # Valentinianische Gnosis
│   ├── greek-cosmological.ttl   # 13-Prinzipien-System (Kairos → Hen)
│   └── opus-purum-axioms.ttl    # Opus Purum als formale Klassen
├── shapes/
│   └── prima-materia.shapes.ttl # SHACL-Validierungsregeln
├── context/
│   └── prima-materia-context.jsonld  # JSON-LD Context-Definition
├── scripts/
│   ├── validate.py              # SHACL-Validierung
│   ├── compile.py               # TTL-Fragmente → kohärentes Modell
│   └── transmute.py             # TTL → JSON-LD Konvertierung
├── tests/
│   ├── test_validation.py
│   ├── test_compilation.py
│   └── test_transmutation.py
└── .github/
    └── workflows/
        ├── validate.yml         # CI auf jedem Push
        └── distribute.yml       # Auto-Build & Push zu prima-materia-dist

prima-materia-dist/              # Distribution Repository (auto-generiert, nie manuell editieren)
├── README.md                    # Auto-generiert; verweist auf source repo
├── LICENSE                      # CC0 1.0
├── prima-materia.jsonld         # Vollständige kompilierte Ontologie als JSON-LD
├── prima-materia.ttl            # Vollständige kompilierte Ontologie als Turtle
├── context.jsonld               # JSON-LD Context (Kopie aus source/context/)
├── llms.txt                     # LLM-Discovery-File (siehe Abschnitt 8)
├── version.json                 # { "version": "...", "git_sha": "...", "built_at": "..." }
└── traditions/                  # Pro-Tradition-Splits für selektives Laden
    ├── valentinian.jsonld
    ├── greek-cosmological.jsonld
    └── opus-purum-axioms.jsonld
```

## 2. Namespace & URI-Strategie

**Base Namespace:** `https://pajew-ski.github.io/prima-materia/ontology#`

**Präfixe (in jeder TTL-Datei zu deklarieren):**

```turtle
@prefix pm:      <https://pajew-ski.github.io/prima-materia/ontology#> .
@prefix pmt:     <https://pajew-ski.github.io/prima-materia/traditions/> .
@prefix pmc:     <https://pajew-ski.github.io/prima-materia/concepts/> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
```

**URI-Konventionen:**
- Klassen in `PascalCase`, immer als Prozess-Substantiv (Gerundium): `pm:Symbolizing`, `pm:Manifesting`
- Properties in `camelCase`: `pm:assertedIn`, `pm:analogueConcept`
- Tradition-Instanzen in `pmt:` namespace: `pmt:ValentinianGnosis`
- Konzept-Instanzen in `pmc:` namespace: `pmc:Pleroma`, `pmc:Hen`

## 3. Bewusstsein-erste Ontologie — Kern-Designprinzipien

Die Ontologie folgt vier formalen Parametern, abgeleitet aus E-Prime, Hopi-Aspektsystem, Pāṇinian-Generativität und Bhartṛharis Sphoṭa-Theorie:

### Parameter 1: Prozess statt Substanz

**Regel:** Jede Hauptklasse ist ein Gerundium (Prozess-Substantiv). Statische Substantiv-Klassen (`Symbol`, `Concept`, `Entity`) sind verboten.

**Beispiel:**

```turtle
# RICHTIG — Prozess-Klasse
pm:Symbolizing a owl:Class ;
    rdfs:label "Symbolizing"@en, "Symbolisieren"@de ;
    skos:definition "The act of one form standing for another within awareness."@en ;
    rdfs:subClassOf pm:Process .

# FALSCH — statische Substanz-Klasse
# pm:Symbol a owl:Class .   # NICHT VERWENDEN
```

**Kern-Prozessklassen (in `ontology/core.ttl`):**

| Klasse | Bedeutung |
|---|---|
| `pm:Process` | Wurzelklasse aller Prozesse |
| `pm:Symbolizing` | Repräsentations-Akt |
| `pm:Manifesting` | Hervortreten in Form |
| `pm:Perceiving` | Wahrnehmungs-Akt |
| `pm:Practicing` | Operative Prozedur |
| `pm:Tradition` | Wissenstradition als ongoing Übertragung |
| `pm:Conceptualizing` | Begriffsbildung |
| `pm:Relating` | Beziehungs-Akt zwischen Konzepten |

### Parameter 2: AwarenessContext als First-Class-Entität

Jeder Triple wird in einem benannten Graph (Named Graph) eingebettet, der den Bewusstseinszustand der Aussage trägt. Das ist keine Metadaten-Spielerei — es ist epistemische Sauberkeit.

**Implementierung über `pm:AwarenessContext`:**

```turtle
pm:AwarenessContext a owl:Class .

pm:WakingState        a pm:AwarenessContext ;
    rdfs:label "Waking state (Jāgrat)"@en .
pm:DreamingState      a pm:AwarenessContext ;
    rdfs:label "Dreaming state (Svapna)"@en .
pm:DeepSleepState     a pm:AwarenessContext ;
    rdfs:label "Deep sleep state (Suṣupti)"@en .
pm:TranscendentState  a pm:AwarenessContext ;
    rdfs:label "Transcendent state (Turīya)"@en .
pm:GnosticState       a pm:AwarenessContext ;
    rdfs:label "Gnostic state (operative consciousness)"@en .
pm:ScholarlyState     a pm:AwarenessContext ;
    rdfs:label "Scholarly state (philological/historical assertion)"@en .
```

**Property zur Triple-Kontextualisierung:**

```turtle
pm:assertedIn a owl:ObjectProperty ;
    rdfs:domain rdf:Statement ;
    rdfs:range pm:AwarenessContext ;
    skos:definition "The awareness context in which a statement is asserted."@en .
```

Für Phase 1 ist es ausreichend, wenn jede Tradition-Datei einen Default-Context per Datei-Header deklariert (typisch `pm:ScholarlyState`). Vollständige named-graph-Implementierung kommt in Phase 2.

### Parameter 3: Sphoṭa — Bedeutung in Subgraph-Clustern

Einzelne Triples tragen keine vollständige Bedeutung. Erst der **Subgraph-Cluster** ist die Bedeutungs-Einheit. Dafür brauchen wir eine Klasse, die Subgraphen als Einheiten markiert:

```turtle
pm:MeaningCluster a owl:Class ;
    rdfs:label "Meaning Cluster (Sphoṭa-Unit)"@en ;
    skos:definition "A bounded subgraph that carries emergent meaning irreducible to its individual triples. Designed for vector embedding as a unit."@en .

pm:hasClusterMember a owl:ObjectProperty ;
    rdfs:domain pm:MeaningCluster .
```

Beispiel-Anwendung: Das gesamte Aeon-System des Pleroma ist *ein* `pm:MeaningCluster` — embedded als Vektor in Qdrant, nicht als Summe seiner Aeonen-Triples.

### Parameter 4: Inklusiv-/Exklusiv-Pronominalstruktur

Statt isolierter `Self`/`Other`-Knoten verwenden wir ein Spektrum:

```turtle
pm:AwarenessSpace a owl:Class .

pm:individualAwareness a pm:AwarenessSpace .
pm:dyadicAwareness     a pm:AwarenessSpace .   # ich + du, exklusiv
pm:collectiveAwareness a pm:AwarenessSpace .   # gruppenbasiert
pm:universalAwareness  a pm:AwarenessSpace .   # alle Bewusstsein
```

Diese Klasse wird in Phase 2 für Praxis-Modellierung relevant (rituelle Akte spezifizieren ihre Awareness-Space-Reichweite).

## 4. Phasen-Implementierungsplan

### Phase 0 — Infrastruktur (Agent-Ziel: vollständig in einer Session lieferbar)

**Deliverables:**

1. Beide Repositories anlegen (oder das Source-Repo, falls Distribution per Action erst später deployed wird)
2. README.md, LICENSE (CC0 1.0), CONTRIBUTING.md initialisieren
3. Repository-Struktur gemäß Abschnitt 1 anlegen (leere Platzhalter-Dateien wo nötig)
4. `ontology/core.ttl` — Meta-Ontologie aus Abschnitt 3
5. `ontology/consciousness.ttl` — AwarenessContext-Instanzen
6. `context/prima-materia-context.jsonld` — JSON-LD Context-Definition
7. `shapes/prima-materia.shapes.ttl` — initiale SHACL-Shapes (siehe Abschnitt 5)
8. Python-Toolchain (`scripts/validate.py`, `scripts/compile.py`, `scripts/transmute.py`) — siehe Abschnitt 6
9. `requirements.txt` mit `rdflib`, `pyshacl`, `pytest`
10. GitHub Actions Workflows (siehe Abschnitt 7)
11. Pytest-Tests für die drei Skripte (siehe Abschnitt 9)

**Akzeptanzkriterien Phase 0:**

- [ ] `python scripts/validate.py` läuft fehlerfrei auf der core+consciousness-Ontologie durch
- [ ] `python scripts/compile.py` produziert eine valide kombinierte TTL-Datei
- [ ] `python scripts/transmute.py` produziert eine valide JSON-LD-Datei
- [ ] `pytest tests/` läuft grün
- [ ] GitHub Action `validate.yml` läuft grün auf Push to main

### Phase 1 — Seed Corpus

**Deliverables:**

1. `traditions/valentinian.ttl` — Valentinianische Gnosis als Prozess-Ontologie. Migration der bestehenden Neo4j-Ontologie (Aeonen, Syzygies, Pleroma, Sophia-Fall, etc.) in die `pm:`-Klassenstruktur. Konkret: bestehende `Aeon`-Knoten werden zu `pm:Conceptualizing`-Instanzen mit `pm:withinTradition pmt:ValentinianGnosis`.
2. `traditions/greek-cosmological.ttl` — 13-Prinzipien-System (Kairos durch Hen) inklusive der hierarchischen Struktur und der existierenden SVG-Sigil-Referenzen via `pm:hasSymbolicForm`.
3. `traditions/opus-purum-axioms.ttl` — die fünf Axiome des Opus Purum als formale `pm:Axiom`-Subklasse, plus die sieben Kapitel als `pm:Practice`-Instanzen.
4. `prima-materia-dist`-Repository deployen — automatischer Build & Push via Action `distribute.yml`.
5. jsDelivr-CDN-Verifikation — Distribution-URLs sind via `https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/prima-materia.jsonld` abrufbar.

**Akzeptanzkriterien Phase 1:**

- [ ] Drei Tradition-TTL-Dateien existieren und validieren gegen SHACL-Shapes
- [ ] Keine Verwendung verbotener statischer Substanzklassen (siehe Abschnitt 3, Parameter 1)
- [ ] Alle Konzepte tragen `dcterms:source` mit Primärquellen-Referenz
- [ ] Distribution-Repository wird auto-gebaut und gepusht
- [ ] jsDelivr-CDN liefert die JSON-LD-Datei mit korrekten CORS-Headern

### Phase 2 — Erweiterung & Integration (außerhalb des aktuellen Agent-Auftrags, hier nur referenziert)

Hermetik-Kernontologie, vollständige named-graph-Implementierung, llms.txt-Integration auf pajew-ski.github.io, Exocortex-n8n-Webhook-Pipeline.

## 5. SHACL Shapes (Validierungsregeln)

`shapes/prima-materia.shapes.ttl` enthält mindestens folgende Shapes:

```turtle
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix pm:  <https://pajew-ski.github.io/prima-materia/ontology#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

# Jeder Prozess-Subclass muss von pm:Process abstammen
pm:ProcessShape a sh:NodeShape ;
    sh:targetSubclassOf pm:Process ;
    sh:property [
        sh:path rdfs:label ;
        sh:minCount 1 ;
        sh:datatype rdf:langString ;
        sh:message "Every process class requires at least one labeled language tag."
    ] ;
    sh:property [
        sh:path skos:definition ;
        sh:minCount 1 ;
        sh:message "Every process class requires a skos:definition."
    ] .

# Jede Konzept-Instanz braucht eine Quellenreferenz
pm:ConceptInstanceShape a sh:NodeShape ;
    sh:targetClass pm:Conceptualizing ;
    sh:property [
        sh:path dcterms:source ;
        sh:minCount 1 ;
        sh:message "Every concept instance requires at least one dcterms:source."
    ] ;
    sh:property [
        sh:path pm:withinTradition ;
        sh:minCount 1 ;
        sh:message "Every concept must be situated within at least one tradition."
    ] .

# Verbot statischer Substanzklassen — explizite Blacklist
pm:NoSubstanceClassesShape a sh:NodeShape ;
    sh:targetNode pm:Symbol, pm:Concept, pm:Entity, pm:Object ;
    sh:not [
        sh:property [
            sh:path rdf:type ;
            sh:hasValue owl:Class ;
        ]
    ] ;
    sh:message "Static substance classes (pm:Symbol, pm:Concept, pm:Entity, pm:Object) are forbidden. Use process classes instead (pm:Symbolizing, pm:Conceptualizing, etc.)." .
```

## 6. Python-Toolchain — Skript-Spezifikationen

### `scripts/validate.py`

```python
"""SHACL validation of all .ttl files in ontology/ and traditions/."""
# Verwendet pyshacl
# CLI: python scripts/validate.py [--shapes shapes/prima-materia.shapes.ttl] [--data ontology/ traditions/]
# Exit code 0 wenn valid, 1 wenn invalid; druckt Validierungsreport auf stderr.
```

### `scripts/compile.py`

```python
"""Compile all .ttl fragments in ontology/ and traditions/ into a single graph."""
# Verwendet rdflib
# CLI: python scripts/compile.py --output build/prima-materia.ttl
# Lädt rekursiv alle .ttl in ontology/ und traditions/, mergeded in einen rdflib.Graph,
# serialisiert nach Turtle.
```

### `scripts/transmute.py`

```python
"""Transmute compiled TTL to JSON-LD."""
# Verwendet rdflib + context-file
# CLI: python scripts/transmute.py --input build/prima-materia.ttl --context context/prima-materia-context.jsonld --output build/prima-materia.jsonld
# Verwendet den JSON-LD-Context für stabile Kürzel.
```

**Wichtig:** Alle Skripte müssen idempotent sein und dürfen keine Network-Calls machen.

## 7. GitHub Actions

### `.github/workflows/validate.yml`

```yaml
name: Validate

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: python scripts/validate.py
      - run: pytest tests/
```

### `.github/workflows/distribute.yml`

```yaml
name: Distribute

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout source
        uses: actions/checkout@v4
        with:
          path: source
      - name: Checkout dist
        uses: actions/checkout@v4
        with:
          repository: pajew-ski/prima-materia-dist
          path: dist
          token: ${{ secrets.DIST_REPO_TOKEN }}
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - working-directory: source
        run: |
          pip install -r requirements.txt
          python scripts/validate.py
          python scripts/compile.py --output build/prima-materia.ttl
          python scripts/transmute.py --input build/prima-materia.ttl --context context/prima-materia-context.jsonld --output build/prima-materia.jsonld
      - name: Sync to dist
        run: |
          cp source/build/prima-materia.ttl dist/
          cp source/build/prima-materia.jsonld dist/
          cp source/context/prima-materia-context.jsonld dist/context.jsonld
          # version.json mit git_sha und timestamp generieren
          cd dist && git add -A
          if git diff --cached --quiet; then
            echo "No changes to publish"
          else
            git -c user.name="prima-materia bot" -c user.email="bot@pajewski.net" commit -m "Auto-build from source@${{ github.sha }}"
            git push
          fi
```

**Hinweis für den Agent:** Das `DIST_REPO_TOKEN`-Secret muss vom User manuell in den Repo-Settings gesetzt werden (Personal Access Token mit Write-Access auf prima-materia-dist). Das ist nicht vom Agent automatisierbar — vermerke das in der README und im Setup-Schritt.

## 8. llms.txt Integration

Das Distribution-Repository enthält eine `llms.txt`, die LLM-Agenten Discovery erlaubt:

```
# prima-materia

> Open-Data ontology of magical and esoteric knowledge, structured under a consciousness-first design principle. Released under CC0 1.0.

## Ontology Files

- [Full ontology (JSON-LD)](https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/prima-materia.jsonld): Complete compiled ontology with embedded JSON-LD context
- [Full ontology (Turtle)](https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/prima-materia.ttl): Turtle serialization
- [JSON-LD Context](https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/context.jsonld): Standalone context for embedding in client systems

## Traditions

- [Valentinian Gnosis (JSON-LD)](https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/traditions/valentinian.jsonld)
- [Greek Cosmological 13-Principles (JSON-LD)](https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/traditions/greek-cosmological.jsonld)
- [Opus Purum Axioms (JSON-LD)](https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/traditions/opus-purum-axioms.jsonld)

## Optional

- [Source repository](https://github.com/pajew-ski/prima-materia)
- [Specification](https://github.com/pajew-ski/prima-materia/blob/main/SPEC.md)
```

## 9. Test-Strategie

Pytest-Tests in `tests/`:

- `test_validation.py` — verifiziert, dass die Seed-Ontologie SHACL-konform ist; verifiziert, dass ein deliberat ungültiges Test-TTL-Fragment fehlschlägt
- `test_compilation.py` — verifiziert, dass alle TTL-Fragmente parsen und mergen
- `test_transmutation.py` — verifiziert, dass JSON-LD-Output zurück nach TTL roundtripping ist (via rdflib)
- `test_no_substance_classes.py` — explizit: scannt alle TTL-Dateien auf Vorkommen verbotener Klassennamen (`pm:Symbol`, `pm:Concept`, `pm:Entity`, `pm:Object`) und fail wenn gefunden

## 10. Lizenzierung & Quellenführung

**Code & Ontologie:** CC0 1.0 Universal (Public Domain Dedication). Datei `LICENSE` enthält den vollständigen CC0-Text.

**Quellenführung:** Jede Konzept-Instanz **muss** mindestens ein `dcterms:source` mit einer der folgenden Formen tragen:

- Bibliographische Referenz als Plain-String: `"Irenaeus, Adversus Haereses I.1 (c. 180 CE)"`
- DOI als URI: `<https://doi.org/...>`
- ISBN-URN: `<urn:isbn:978-...>`
- URL einer Open-Access-Edition

**Verboten:** Reproduktion urheberrechtlich geschützter Primärtexte. Konzept-Definitionen sind eigene Paraphrasen, niemals Direktzitate aus modernen Übersetzungen.

## 11. Was der Agent NICHT tun soll

- Keine `pm:Symbol`, `pm:Concept`, `pm:Entity`-Klassen erstellen (statische Substanz-Ontologie verboten)
- Keine externen Texte zitieren oder reproduzieren — nur paraphrasieren mit Quellenangabe
- Keine Network-Calls in den Skripten — alles muss offline reproduzierbar sein
- Keine eigenmächtige Erweiterung des Scopes über die in Phase 0/1 spezifizierten Tradition hinaus
- Kein automatisiertes Setzen von Repository-Secrets — den User explizit auffordern
- Keine Verwendung von `owl:NamedIndividual` ohne explizite Klassenzuweisung
- Keine deutschen Identifier in URIs/Klassennamen — englische Identifier mit deutschen `rdfs:label`-Tags

## 12. Erste Aufgabe für den Agent

Beginne mit Phase 0. Lies dieses Dokument vollständig. Erstelle einen Implementierungsplan mit Todo-Liste. Stelle Klärungsfragen, falls eine Spezifikation mehrdeutig ist. Implementiere Schritt für Schritt mit Commits pro Deliverable. Führe nach jedem Skript-Update die Tests aus.

Erfolgskriterium für Phase 0: Ein frisch geklontes Repository soll nach `pip install -r requirements.txt && python scripts/validate.py && pytest tests/` fehlerfrei durchlaufen.

---

**Document version:** 1.0
**Maintained by:** Michael Pajewski
**License:** CC0 1.0 (this specification document inclusive)
