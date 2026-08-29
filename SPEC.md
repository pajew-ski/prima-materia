# prima-materia — Project Specification

> **Agent-Hinweis:** Dieses Dokument ist die alleinige Quelle der Wahrheit (SSOT) für die Implementierung. Lies es vollständig, bevor du Code schreibst. Bei Konflikten zwischen diesem Dokument und deiner Trainingsintuition gilt dieses Dokument. Bei echten Unklarheiten frag nach — rate nicht.

## 0. Mission & Kontext

**prima-materia** ist eine Open-Data-Ontologie für magisches und esoterisches Wissen, eine **Prüfstelle, keine Sammlung**. Sie nimmt eine Behauptung über ein magisches oder kontemplatives Vermögen auf, trennt sie von ihrer Beglaubigung und hält beide getrennt, damit sichtbar bleibt, worauf sie steht: auf einem überlieferten Text, auf einem modernen Bearbeiter, oder auf nichts. Aus dem geprüften Bestand entsteht das eigentliche Werk, eine Karte, die durch Überlagerung der alten Traditionen zeigt, wo sie sich decken, wo sie sich widersprechen und was tatsächlich Wirkung erzielt, die sich messen lässt.

**Das Ziel dahinter.** Magie in ihren Konzepten verstehen und lehren können. Auf dem Weg dorthin die eigenen menschlichen und übermenschlichen Vermögen aktivieren oder zurückgewinnen. Und die Ergebnisse frei teilen, damit andere zu ihrem vollen Potenzial finden.

**Warum CC0 keine Lizenzentscheidung ist.** Magisches und kontemplatives Wissen war dreitausend Jahre lang durch Initiation, Linie, Geheimhaltung und Zahlung verschlossen. Dieser Verschluss wirkt wie Armut: er entscheidet über Entfaltung nach Zugehörigkeit statt nach Vermögen. Die Freigabe ins Gemeingut ist deshalb nicht die Vertriebsform des Projekts, sondern seine Maßnahme.

**Daraus das Kriterium, das jede Recherche, jede Fragestellung und jeden Eintrag trägt:**

> **Wertvoll ist, was ein Tor beseitigt.**

Die Unterscheidung von bezeugt und erschlossen beseitigt das Tor der Autorität: niemand braucht einen Lehrer, um zu wissen, worauf eine Behauptung steht. Die Voraussetzungsketten beseitigen das Tor der Reihenfolge, die Traditionen zurückgehalten haben. Die Prüfung beseitigt das Tor der unwiderlegbaren Behauptung. Die Konvergenz beseitigt das Tor der Linienzugehörigkeit, weil niemand in einer Tradition stehen muss, um zu sehen, was mehrere sagen.

Praktische Folge für die Priorisierung: der wertvollste Knoten ist nicht der, den der Betreiber gerade braucht, sondern der, der anderswo am zuverlässigsten falsch berichtet wird.

Das Projekt ist Teil einer übergeordneten Architektur — es ist die Basis, aus der die Methoden des **Opus Purum** (separates Projekt) extrahiert werden. Die Richtung läuft vom Entwurf über die Zerlegung und das Grounding zu dem, was übrig bleibt, und erst von dort zur Methode. Der Graph ist deshalb nicht die *undifferenzierte Ursubstanz*, als die frühere Fassungen dieses Dokuments ihn beschrieben haben. Die Ursubstanz ist der ungeprüfte Entwurf; dies hier ist die Probe auf seinen Gehalt.

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
│   ├── provenance.ttl           # Behauptungs- und Prüfklassen (siehe Abschnitt 3.5)
│   └── alignments.ttl           # Mappings zu SKOS, DCTerms, schema.org
├── traditions/                  # eine Datei je Tradition
│   └── *.ttl                    # enochic, patanjala-yoga, theravada, daoist, ...
├── convergences/                # Übereinstimmungen über Traditionen hinweg
│   └── *.ttl                    # gehören keiner Tradition, deshalb eigener Ordner
├── examinations/                # Prüfprotokolle zu einzelnen Behauptungen
│   └── *.ttl                    # nur angelegt, wo eine Prüfung aufgenommen wurde
├── site/                        # handgeschriebene Assets der GitHub-Pages-Seite
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

**Base Namespace:** `https://pajew.ski/prima-materia/ontology#`

Die Ontologie erscheint unter `https://pajew.ski/prima-materia/` und wird dort geprägt und ausgeliefert. Bezeichner und Auslieferungsort fallen bewusst zusammen: ein zweiter Name für dieselben Terme würde jeden Term verdoppeln, weil RDF-Identität keiner Umleitung folgt.

**Präfixe (in jeder TTL-Datei zu deklarieren):**

```turtle
@prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
@prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
@prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
@prefix pmp:     <https://pajew.ski/prima-materia/practices/> .
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

### Parameter 5: Behauptungen sind Knoten, keine Kanten

Der Graph hält Behauptungen mit Herkunft. Eine Behauptung, die ihre Quelle, ihren Bezeugungsmodus, ihre Stärke oder ein Prüfprotokoll tragen muss, kann keine Kante sein: auf einer Kante sähen ein zitierfähiger Notwendigkeitssatz und eine bloße Kapitelreihenfolge gleich aus. Alle Behauptungsformen werden deshalb reifiziert. Diese Regel gilt auch für jeden künftigen Behauptungstyp, und zwar bevor der erste Knoten geschrieben wird.

`ontology/provenance.ttl` enthält die Klassen:

| Klasse | Aussageform | Pflichtangaben zusätzlich zu `dcterms:source` |
|---|---|---|
| `pm:Attributing` | „X lehrte Y" | `pm:ascribedCapacity`, `pm:attestedBy` (nie `pm:compilerInference`) |
| `pm:Yielding` | „Praxis P bringt Vermögen C hervor" | `pm:byPractice`, `pm:yieldsCapacity`, `pm:attestedBy` |
| `pm:Presupposing` | „B ist ohne A nicht zu erreichen" | `pm:dependentStep`, `pm:priorStep`, `pm:prerequisiteStrength`, `pm:attestedBy` |
| `pm:Cautioning` | „Hütet euch vor C" | `pm:cautionsAbout` |
| `pm:Systematizing` | eine nachträglich hergestellte Ordnung | `pm:compiledBy`, `dcterms:date` |
| `pm:Disputing` | zwei Seiten streiten über eine Behauptung | `pm:disputedClaim`, **mindestens zwei** Quellen, `pm:attestedBy` |
| `pm:Converging` | Übereinstimmung über Traditionen hinweg | `pm:transmissionPath` **oder** `pm:independentAttestation` |
| `pm:Testing` | ein Prüfprotokoll | `pm:examinationState`, `pm:examinedBy`, `pm:protocolUpdated` |

**Bezeugungsmodi** (`pm:Attesting`): `pm:textualAttestation`, `pm:firstPersonReport`, `pm:protocolledPractice`, `pm:thirdPartyAscription`, `pm:compilerInference`. Der letzte bezeugt einen Ordnungsakt, nie die geordnete Behauptung; `pm:CompilerInferenceScopeShape` erzwingt das.

**Zwei kontrollierte Skalen tragen die schwachen Fälle.** Sie existieren, damit schwaches Material eingetragen werden kann, nicht damit es draußen bleibt. Ein Befund gehört auf die Stufe, die er verdient.

`pm:PrerequisiteStrength`: `pm:statedNecessity` nur mit zitierbarer `pm:consequenceOfSkipping`, sonst weist `pm:StatedNecessityShape` ab; `pm:prescribedOrder` für eine Anweisung ohne Folgenangabe; `pm:presentationOrder` für eine bloße Darstellungsreihenfolge.

`pm:ExaminationState`: `pm:noProcedureDevised`, `pm:procedureWithoutCases`, `pm:casesWithoutDeviation`, `pm:casesWithDeviation`. Der erste Stand darf nie mit dem dritten zusammenfallen. Eine Behauptung, für die niemand ein Prüfverfahren ersonnen hat, ist keine Behauptung, die geprüft und nicht gestützt wurde; wer beides gleich meldet, berichtet nicht über die Behauptungen, sondern über die Reichweite der eigenen Instrumente.

**Moderne Forschung** betritt den Bestand ausschließlich über `pm:evidenceFrom` an einem `pm:Testing`-Knoten, nie als `dcterms:source` einer Tradition. Ein Aufsatz ist kein Zeuge einer Überlieferung.

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

### Phase 1 — Seed Corpus (geliefert)

**Deliverables:**

1. Der Seed-Korpus steht. Er besteht aus den Traditionsdateien in `traditions/`, den traditionsübergreifenden Knoten in `convergences/` und dem ersten Prüfprotokoll in `examinations/`. Die früher an dieser Stelle genannten Dateien `traditions/valentinian.ttl` und `traditions/greek-cosmological.ttl` gehören nicht dazu und wurden nie angelegt. Die Planung ist hier hinter dem Bestand zurückgeblieben; maßgeblich ist der Dateibaum, nicht diese Liste. Wer sie noch anlegt, arbeitet gegen einen Plan statt gegen das Repo.
2. Von hier an wächst der Korpus nicht mehr nach Plan, sondern nach den zwei Eingängen in Abschnitt 14: dem Bedarf aus offenen Behauptungs-Issues und dem Engpass der unabhängigen Bezeugung.
3. ~~`traditions/opus-purum-axioms.ttl`~~ — **gestrichen.** Der Richtungssinn in Abschnitt 10 schließt das aus: prima-materia ist die Basis, aus der die Methoden des Opus Purum extrahiert werden. Die Axiome sind unveröffentlichtes eigenes Material und tragen keine Quelle im Sinne dieser Spezifikation. Ihre Bestandteile können einzeln eingehen, sobald sie gegen überliefertes Schrifttum gegroundet sind, dann aber unter der Tradition, aus der der Beleg stammt, nicht unter dem Namen des Entwurfs.
4. `prima-materia-dist`-Repository deployen — automatischer Build & Push via Action `distribute.yml`.
5. jsDelivr-CDN-Verifikation — Distribution-URLs sind via `https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/prima-materia.jsonld` abrufbar.

**Akzeptanzkriterien Phase 1:**

- [ ] Die Tradition-TTL-Dateien existieren und validieren gegen SHACL-Shapes
- [ ] Keine Verwendung verbotener statischer Substanzklassen (siehe Abschnitt 3, Parameter 1)
- [ ] Alle Konzepte tragen `dcterms:source` mit Primärquellen-Referenz
- [ ] Distribution-Repository wird auto-gebaut und gepusht
- [ ] jsDelivr-CDN liefert die JSON-LD-Datei mit korrekten CORS-Headern

### Phase 2 — Erweiterung & Integration (außerhalb des aktuellen Agent-Auftrags, hier nur referenziert)

Hermetik-Kernontologie, vollständige named-graph-Implementierung, llms.txt-Integration auf pajew.ski, Exocortex-n8n-Webhook-Pipeline.

## 5. SHACL Shapes (Validierungsregeln)

`shapes/prima-materia.shapes.ttl` enthält mindestens folgende Shapes:

```turtle
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
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

Ein Eintrag je Datei in `traditions/`, beim Bau aus dem Verzeichnis abgeleitet und nicht von Hand gepflegt. Eine fest verdrahtete Liste läuft dem Bestand hinterher und nennt irgendwann Dateien, die es nicht gibt.

## Optional

- [Source repository](https://github.com/pajew-ski/prima-materia)
- [Specification](https://github.com/pajew-ski/prima-materia/blob/main/SPEC.md)
```

## 9. Test-Strategie

Pytest-Tests in `tests/`:

- `test_validation.py` — verifiziert, dass die Seed-Ontologie SHACL-konform ist; verifiziert, dass ein deliberat ungültiges Test-TTL-Fragment fehlschlägt
- `test_compilation.py` — verifiziert, dass alle TTL-Fragmente parsen und mergen
- `test_transmutation.py` — verifiziert, dass JSON-LD-Output zurück nach TTL roundtripping ist (via rdflib)
**Fixture-Pflicht.** Jedes neue Shape braucht einen Negativfixture, der zeigt, dass es feuert. Ein Wächter, von dem nie gezeigt wurde, dass er auslöst, ist nicht als funktionierend bekannt. Hat das Shape eine Ausnahme, braucht es zusätzlich einen positiven Fixture für die Ausnahme.

**Ordnerregel.** Ein neuer Datenordner muss an vier Stellen nachgezogen werden, sonst wird er still nicht kompiliert und nicht validiert: `DEFAULT_INPUTS` in `scripts/compile.py`, `DEFAULT_INPUTS` in `scripts/publish.py`, `DEFAULT_DATA_DIRS` in `scripts/validate.py`, `SCAN_DIRS` in `tests/test_no_substance_classes.py`. Nichts schlägt fehl, wenn eine davon vergessen wird.

Ein Test, der gegen einen hartkodierten Namensraum vergleicht, hört bei einer Migration still auf zu prüfen und bleibt dabei grün. Solche Vergleiche gehören bei jeder Namensraumänderung mitgezogen.

- `test_no_substance_classes.py` — explizit: scannt alle TTL-Dateien auf Vorkommen verbotener Klassennamen (`pm:Symbol`, `pm:Concept`, `pm:Entity`, `pm:Object`) und fail wenn gefunden

## 10. Lizenzierung & Quellenführung

**Code & Ontologie:** CC0 1.0 Universal (Public Domain Dedication). Datei `LICENSE` enthält den vollständigen CC0-Text.

**Quellenführung.** Der Graph enthält keine Wahrheiten, sondern Behauptungen mit Herkunft. Die Herkunft zu prüfen ist die Kernaufgabe jedes Agenten an diesem Repo; der Mensch ist die letzte Instanz vor dem Merge, nicht die einzige.

Jede Behauptung **muss** mindestens ein `dcterms:source` tragen, und zwar als bibliographische Referenz auf ein überliefertes Werk mit der Stelle, die sie trägt: `"1 Henoch 8:1"`, `"Irenaeus, Adversus Haereses I.1"`, `"Patañjali, Yogasūtra III.16-49"`.

Ausgeschlossen sind:

- **URLs jeder Art**, DOI und Open-Access-Editionen eingeschlossen. Ein Link benennt einen Ort, der sich ändert und für den nur sein Betreiber einsteht; ein Werk benennt etwas, das ein Leser unabhängig von diesem Graphen beschaffen kann. `pm:SourceIsLiteratureShape` weist `dcterms:source`-Werte mit `http`-Präfix maschinell ab.
- **Videos, Blogs, Wikipedia, Foren.** Rechercheeinstieg, nie Beleg. Zurückverfolgen bis zum Werk, dann zählt das Werk.
- **Unveröffentlichte eigene Texte, Arbeitsfassungen, Methodenentwürfe**, auch die des Betreibers.
- **Sekundäre Zusammenfassungen** anstelle der Stelle, die sie zusammenfassen.

**Der Maßstab ist Auffindbarkeit, nicht Nummerierung.** Die Angabe muss so genau sein, dass ein Leser die Stelle im benannten Werk findet. Eine Nummer ist keine Bedingung, wo das Werk keine hat oder wo die Zählung zwischen Ausgaben schwankt: `"Philokalia I, Hesychios of Sinai, On Watchfulness and Holiness"` und `"John Climacus, The Ladder of Divine Ascent, steps 1-30"` sind zulässig. Schwankende Zählungen gehören in eine `skos:note`, nicht in eine Weglassung. Zitiergenauigkeit ist nicht Zitierbarkeit, und ein Befund, der an einer fehlenden Kapitelnummer scheitert, obwohl Werk und Traktat benannt sind, ist unnötig verloren.

**Die Rezension gehört in die Angabe.** Wo Textzeugen inhaltlich auseinandergehen, nennt `dcterms:source` Rezension und Ausgabe, und die abweichenden Fassungen stehen als getrennte Knoten: `"1 Enoch 8:3 (Ethiopic; Charles 1912)"` neben `"1 Enoch 8:3 (Aramaic/Greek reconstruction; Nickelsburg 2001)"`. Ein gemittelter Knoten meldet einen Text, den kein Zeuge gibt. Streiten die Ausgaben nur über Datierung oder Lesung, ohne dass zwei Fassungen entstehen, gehört das in einen `pm:Disputing`-Knoten.

**Negative Befunde gehören in den Bestand.** Eine Ordnung, die erst Kommentar oder Moderne hergestellt hat, wird ein `pm:Systematizing`-Knoten mit benanntem Kompilator; ein Streit zwischen Grundtext und Lesern ein `pm:Disputing`-Knoten; eine Behauptung, die der Korpus noch nicht beantwortet, ein Issue nach Abschnitt 13, mit den geprüften Kandidatenstellen und dem Grund des Scheiterns. Sonst prüft der nächste Agent dieselbe Behauptung und scheitert genauso.

**Ein Turtle-Kommentar ist kein Ort für einen Befund.** Kommentare fallen beim Kompilieren weg; der ausgelieferte Graph weiß von einer Prüfung nichts, die nur im Dateikopf steht. Was eine Prüfung ergeben hat, gehört in einen Knoten, in eine `skos:note` oder in ein Issue.

**Richtungssinn.** prima-materia ist die Basis, aus der die Methoden des Opus Purum extrahiert werden, nicht umgekehrt. Ein Methodenentwurf ist keine Quelle, sondern eine Menge von Behauptungen, die einzeln gegen überliefertes Schrifttum zu grounden sind. Was sich nicht grounden lässt, bleibt Entwurf und kommt nicht in den Graphen.

**Verboten:** Reproduktion urheberrechtlich geschützter Primärtexte. Konzept-Definitionen sind eigene Paraphrasen, niemals Direktzitate aus modernen Übersetzungen.

## 11. Was der Agent NICHT tun soll

- Keine `pm:Symbol`, `pm:Concept`, `pm:Entity`-Klassen erstellen (statische Substanz-Ontologie verboten)
- Keine externen Texte zitieren oder reproduzieren — nur paraphrasieren mit Quellenangabe
- Keine Network-Calls in den Skripten — alles muss offline reproduzierbar sein
- Keine eigenmächtige Erweiterung des Scopes über die in Phase 0/1 spezifizierten Tradition hinaus
- Kein automatisiertes Setzen von Repository-Secrets — den User explizit auffordern
- Keine Verwendung von `owl:NamedIndividual` ohne explizite Klassenzuweisung
- Keine deutschen Identifier in URIs/Klassennamen — englische Identifier mit deutschen `rdfs:label`-Tags
- **Keine ausgelöste Validierung umformulieren.** Löst SHACL, ein Test oder ein vorgeschalteter Wächter aus, wird das gemeldet. Ein Fehlalarm ist ein Befund über den Wächter und gehört berichtet, damit er repariert wird. Ob der Alarm berechtigt war, entscheidet nicht, wer schreiben will.
- **Keine Verwechslung von Vokabular mit Behauptung.** Eine Klasse behauptet nichts und braucht keine Quelle, sondern eine `skos:definition`, die sagt, was als Instanz gälte. Das Vokabular darf der Sache vorauslaufen; Knoten dürfen es nie.
- **Kein Prüfknoten-Stub pro Behauptung.** `pm:Testing` entsteht, wenn jemand die Prüfung aufnimmt; das Fehlen sagt bereits, was ein Knoten mit Stand „ungeprüft" sagen würde.
- **Keinen Befund weglassen, weil sich nur eine schwache Stärke setzen lässt.** Die Skalen tragen die schwachen Fälle; `pm:presentationOrder` behauptet keine Notwendigkeit, sondern hält fest, dass eine Anordnung existiert, und genau daran erkennt ein späterer Leser, wo ein modernes System eine Notwendigkeit hineingelesen hat.
- **Keine zirkuläre Wirkbehauptung.** Eine Praxis bringt nicht hervor, was sie ist; die Zirkulation des Qi bringt kein Qi hervor. Beim Reifizieren fällt das auf, auf einer Kante nicht.
- **Keine Umbenennung geprägter Bezeichner ohne zwingenden Grund.** Der Namensraum steht endgültig unter `https://pajew.ski/prima-materia/`. Eine Migration ist nur vollständig oder gar nicht auszuführen: RDF-Identität folgt keiner Umleitung, und ein halb migrierter Bestand ist ein still gespaltener Graph.
- **Keine zweite ID-Ebene für Behauptungen.** Issue-Nummern sind stabil, werden nicht wiederverwendet und sind aus Commits, PRs und `skos:note` referenzierbar. Ein zusätzliches Nummernschema aus einem Arbeitsdokument driftet gegen sie und ist nach dem ersten Umsortieren falsch.
- **Keinen Befund in einen Turtle-Kommentar schreiben.** Kommentare überstehen das Kompilieren nicht. Siehe Abschnitt 10.

## 12. Einstieg für den Agent

Phase 0 und Phase 1 sind geliefert. Ein frisch geklontes Repository läuft nach `pip install -r requirements.txt && python scripts/validate.py && pytest tests/` durch; wenn nicht, ist das ein Befund und die erste Aufgabe.

Die Arbeit beginnt nicht mehr an einem Plan, sondern am Issue-Tracker. Dort stehen die Behauptungen, die der Korpus noch nicht beantwortet. Der Ablauf:

1. Dieses Dokument vollständig lesen. Bei mehrdeutiger Spezifikation fragen, nicht raten.
2. Offene Issues mit `behauptung` ansehen und nach `korpus:`-Label bündeln. Recherchiert wird ein Bündel, nicht ein einzelnes Issue: die Arbeit folgt dem Text, den man aufschlägt, nicht dem Abschnitt, aus dem die Behauptung stammt.
3. Ergebnis eintragen — als Knoten, wenn eine Stelle trägt; als weiteres `korpus:`-Label am Issue, wenn dieser Korpus nichts hergibt.
4. Validierung und Tests grün, dann PR. Der Mensch merged.

## 13. Behauptungen als Issues

**Der Issue-Tracker ist der Ort jeder Behauptung, die der Bestand noch nicht beantwortet.** Das erweitert die frühere Regel, die Issues nur für gescheitertes Grounding vorsah. Die Erweiterung folgt dem Torkriterium aus Abschnitt 0: eine Behauptung einreichen zu können, ohne in einer Linie zu stehen und ohne die Recherche selbst zu führen, beseitigt dasselbe Tor wie CC0. Wer eine Behauptung hat, formuliert sie dort; sie wird mitrecherchiert, sobald ihr Korpus an der Reihe ist.

**Ein Issue existiert genau so lange, wie kein Knoten die Behauptung repräsentiert.** Daraus folgt sein Lebenslauf:

- **Offen**, solange die Behauptung ungeprüft oder in Prüfung ist.
- **Geschlossen als `completed`**, sobald ein Knoten sie trägt, mit Nennung des Knotens im Schließkommentar.
- **Geschlossen als `not_planned`** mit `unbelegt`, wenn die plausiblen Korpora erschöpft sind, oder mit `nicht-graphfaehig`, wenn die Behauptung gegen keine Überlieferung entscheidbar ist und es auch nach jeder Recherche nicht wäre. Beides bleibt über `reason:not-planned` auffindbar.
- **Wiedereröffnet**, sobald ein neuer Fund die Lage ändert. Das ist der Normalfall, kein Fehler.

**Die Identität der Behauptung ist die Issue-Nummer.** Kein zweites Nummernschema. Der Rückverweis von einem Knoten auf sein Issue steht in einer `skos:note` in der Form `prima-materia#42`, niemals in `dcterms:source`: ein Issue ist kein Werk, und `pm:SourceIsLiteratureShape` weist die URL ohnehin ab.

### Befunde sind auf die Suche relativiert, nicht auf den Bestand

Ein Befund lautet nie „gegroundet", sondern „gegroundet gegen diese Suche an diesem Tag". **Der Bestand ist dabei kein Maßstab.** Er ist selbst nur eine Menge früher eingetragener Behauptungen mit Herkunft; ein Knoten belegt nichts, er verweist auf eine Stelle. Eine Behauptung gegen den Bestand zu prüfen und das Ergebnis „gegroundet" zu nennen, ist ein Zirkelschluss mit Etikett. Was prüft, ist die Suche nach der Stelle, und ihr Raum ist Abschnitt 15.

Die beiden Ausgänge verhalten sich dabei unsymmetrisch:

- Ein **gegroundeter** Knoten übersteht einen späteren Gegenfund unbeschädigt. Er bekommt eine zweite Seite und wird zu einem `pm:Disputing`-Knoten.
- Ein wegen **Gegenbezeugung verworfener** Befund kippt beim ersten stützenden Zeugen zurück in strittig. Eine Verwerfung, die auf der Gegenbezeugung einer einzigen Tradition beruht, ist streng genommen keine Widerlegung, sondern ein einseitiger Streitfall, der auf seine zweite Seite wartet.

Deshalb trägt jede Verwerfung, worauf sie beruht: welche Stelle widerspricht, aus welcher Tradition, und ob außer ihr etwas geprüft wurde. Ohne das kann ein späterer Leser nicht entscheiden, ob sein Fund den Befund umstößt.

### Labels

Labels sind kein Zustandsduplikat — den Zustand trägt offen oder geschlossen. Sie tragen zwei Dinge: den Bündelungsschlüssel für die Recherche und das Protokoll der Suchabdeckung.

| Label | Bedeutung |
|---|---|
| `behauptung` | markiert das Issue als Behauptung, nicht als Repo-Arbeit. Ohne dieses Label ist der Tracker nach fünfzig Einträgen unlesbar |
| `korpus:<name>` | ein Korpus, der für diese Behauptung geprüft wurde oder zu prüfen ist |
| `strittig` | **zwei Quellen** widersprechen einander; Ziel ist ein `pm:Disputing`-Knoten. Nicht für den Fall, dass eine Quelle einem Methodenentwurf widerspricht: ein Entwurf ist keine Seite, und `pm:Disputing` verlangt zwei Quellen. Dieser Fall ist eine Behauptung ohne Zeugen, deren Gegenteil bezeugt ist |
| `unbelegt` | Schließgrund: plausible Korpora erschöpft, keine Stelle gefunden |
| `nicht-graphfaehig` | Schließgrund: gegen keine Überlieferung entscheidbar, etwa eine Dosierungsangabe |
| `entwurf:<name>` | Herkunft der Behauptung, wo sie aus einem Methodenentwurf stammt |

**Das `korpus:`-Label kumuliert.** Eine Behauptung, die in der Atemliteratur nicht gefunden wurde, ist nicht unbelegbar, sondern in diesem Korpus nicht gefunden. Sie behält das Label, bekommt beim nächsten Durchgang das nächste dazu, und wird erst geschlossen, wenn die plausiblen Korpora erschöpft sind. Damit ist die Labelmenge zugleich die Suchabdeckung, und ein späterer Fund lässt sich daran messen, ob er einen nie geprüften Korpus betrifft.

Die Labelnamen benennen den Korpus, den man aufschlägt, nicht die Datei, in der er später landet. Zwei Traditionen können in einer Datei stehen und zwei Dateien denselben Autor führen.

**Warnung zum Werkzeug:** Ein unbekannter Labelname wird von GitHub stillschweigend als neues Label angelegt, statt den Aufruf abzuweisen. Ein Tippfehler erzeugt also ein zweites Bündel, das niemandem auffällt. Das gültige Vokabular steht in `CONTRIBUTING.md` und wird von dort übernommen, nicht aus dem Gedächtnis geschrieben.

## 14. Erweiterung des Korpus

Der Korpus ist rückwärts aus einem Methodenentwurf gewachsen: jede Datei existiert, weil sie etwas beantwortet, was ein moderner Text behauptet. Das macht das Grounding in dem Maß zirkulär, in dem der Bestand nur dort nachschlägt, wo er ohnehin schon hinsah. Wer ihn allein entlang offener Behauptungen erweitert, vertieft diese Prägung. Deshalb zwei Eingänge, und der zweite hat Vorrang, wenn beide anstehen.

**Bedarfsgetrieben.** Ein `korpus:`-Label auf einer Behauptung, für die es noch keine Datei gibt, ist bereits die Nachfragemeldung. Offene Issues je fehlendem Label ergeben die geordnete Warteschlange; ein zweites Verzeichnis dafür wird nicht geführt.

**Unabhängigkeitsgetrieben.** Die Beweiskraft des ganzen Bestands hängt an `pm:independentAttestation`, und die steht dünn. Eine weitere indische oder buddhistische Datei erhöht die Dateizahl, nicht die Zeugenzahl: wo ein Kontaktweg belegt oder plausibel ist, zählt die Übereinstimmung als Rezeption und nicht als Befund. Gesucht sind Überlieferungen ohne plausible Kontaktroute zu den bereits vertretenen. Dort liegt der Zuwachs.

**Drei Entscheidungen vor dem Anlegen einer Datei, nicht danach:**

1. **Der Kontaktweg.** Sonst stellt sich hinterher heraus, dass der neue Zeuge Rezeption ist, und die Datei zählt für keine Konvergenz.
2. **Rezension und Ausgabe.** Abschnitt 10 verlangt sie in der Angabe; ein nachträglicher Wechsel fasst jeden Knoten der Datei an.
3. **Die Zahl der tatsächlich zitierbaren Stellen.** `traditions/daoist.ttl` ist mit Absicht dünn und ist das ehrliche Modell: gewachsen wird in Stellen, nicht in Traditionsnamen.

**Abgelehnte Aufnahmen bleiben sichtbar.** Was breit berichtet wird, sich aber auf keine Stelle zurückführen ließ, wird ein Issue mit demselben `korpus:`-Label und dem Schließgrund `unbelegt`. Nicht ein Kommentar im Dateikopf: der überlebt das Kompilieren nicht, und der nächste Bearbeiter führt dieselbe Prüfung noch einmal.

## 15. Recherche

### Der Suchraum ist alles Erreichbare

**Der Suchraum jeder Recherche ist das gesamte über das Internet erreichbare Wissen, nicht der Bestand.** Der Bestand ist der Ausgangspunkt der Frage und nie ihre Grenze. Er ist spärlich, er wird immer spärlich sein, und er ist rückwärts aus einem einzigen Entwurf gewachsen; ihn als Prüfmaßstab zu nehmen misst nicht die Behauptung, sondern die bisherige Sammelrichtung.

**Die erste Frage vor jeder Recherche lautet deshalb nicht „was sagt der Bestand dazu", sondern „wo gibt es Quellen zu dieser Behauptung, die noch nicht im Bestand sind".** Wer mit der zweiten Frage beginnt, hat den Ausgang der ersten schon vorweggenommen.

Einstiege in die Quellensuche, die außerhalb des Bestands liegen und regelmäßig gebraucht werden: digitalisierte Primärtextkorpora und ihre Suchmasken, kritische Editionen und ihre Apparate, Übersetzungen in mehrere Sprachen desselben Werks, Fachlexika und Handbücher der jeweiligen Philologie, Dissertationen und Aufsätze, die genau diese Frage behandeln, sowie die Fachliteratur, die der Behauptung widerspricht. Ein solcher Einstieg ist ein Weg zum Werk und wird nie selbst zum Beleg (Abschnitt 10).

### Jede Recherche sucht auch die Negation

Wer nur nach Bestätigung sucht, findet sie. Zu jeder Behauptung wird deshalb zweimal gesucht: nach der Stelle, die sie trägt, und nach der Stelle, die ihr widerspricht. Ohne die zweite Suche ist unbekannt, ob die Behauptung bestritten ist, und genau daran hängt, ob ein `pm:Disputing`-Knoten fehlt, den niemand vermisst.

Dasselbe gilt über die Traditionen hinweg: gesucht wird nicht nur dort, wo die Behauptung vermutlich steht, sondern auch dort, wo ihr Gegenteil stehen könnte. Der Wert des Bestands liegt in `pm:Converging` und `pm:Disputing`, und beide entstehen nur, wenn mehrere Überlieferungen zu derselben Frage befragt wurden.

### Was „gegroundet" heißt

Ein vorhandener Knoten groundet nichts. Eine Analogie in einer benachbarten Tradition groundet nichts. Beides ist ein Hinweis darauf, wo zu suchen wäre.

**Gegroundet ist eine Behauptung, wenn eine Stelle in einem Werk sie trägt und die Gegensuche gelaufen ist.** Die Stelle entscheidet den positiven Befund, sobald sie steht; die Erschöpfung des Suchraums ist dafür nicht Bedingung.

**Unbelegt ist die teure Aussage.** Sie behauptet, dass es die Stelle nirgends gibt, und das trägt nur eine erschöpfende Suche. Ein Issue schließt deshalb nicht als `unbelegt`, weil ein Durchgang nichts fand, sondern erst, wenn die plausiblen Korpora dokumentiert abgesucht sind. Die `korpus:`-Labels sind dieser Nachweis.

### Tiefe

**Eine Recherche ist kein paar Suchanfragen nebenbei.** Der Mindestumfang für eine Behauptung, die in den Graphen soll:

1. Der Fachterm in seiner Originalsprache und in den gebräuchlichen Transliterationen, nicht nur in der deutschen oder englischen Umschreibung.
2. Der Primärtext, mindestens zwei Übersetzungen, und die Sekundärliteratur, die die Stelle behandelt.
3. Die Datierung des frühesten Zeugen, und die Frage, ob die Zuschreibung an dieses Werk in der Fachliteratur bestritten ist.
4. Die Gegensuche nach 15.2.
5. Mindestens eine Überlieferung außerhalb der Sphäre, in der die Behauptung vermutet wird — sonst entsteht nie eine unabhängige Bezeugung.

**Was zurückkommt, gehört ins Issue, nicht in den Kopf des Agenten:** geprüfte Korpora, verwendete Suchbegriffe samt Transliterationen, gefundene und geprüfte Stellen, das Datum. Eine Recherche, deren Abdeckung nicht nachvollziehbar ist, muss beim nächsten Zweifel vollständig wiederholt werden und war damit umsonst.

---

**Document version:** 1.0
**Maintained by:** Michael Pajewski
**License:** CC0 1.0 (this specification document inclusive)
