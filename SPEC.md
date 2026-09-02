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
├── originations/                # moderne Behauptungen, die als alte zirkulieren
│   └── *.ttl                    # pm:Originating: ordnen keine Tradition und bezeugen keine
├── site/                        # handgeschriebene Assets der GitHub-Pages-Seite
├── shapes/
│   └── prima-materia.shapes.ttl # SHACL-Validierungsregeln
├── context/
│   └── prima-materia-context.jsonld  # JSON-LD Context-Definition
├── scripts/
│   ├── validate.py              # SHACL-Validierung
│   ├── compile.py               # TTL-Fragmente → kohärentes Modell
│   ├── transmute.py             # TTL → JSON-LD Konvertierung
│   └── publish.py               # Namensraum-Seite, Serialisierungen, llms.txt
├── tests/                       # eine Datei je Skript, plus die Wächtertests
└── .github/
    └── workflows/
        ├── validate.yml         # SHACL und pytest auf main und claude/**
        ├── pages.yml            # baut und deployt den Namensraum-Host
        └── distribute.yml       # Auto-Build & Push zu prima-materia-dist

prima-materia-dist/              # Distribution Repository (auto-generiert, nie manuell editieren)
├── README.md                    # Auto-generiert; verweist auf source repo
├── LICENSE                      # CC0 1.0
├── prima-materia.jsonld         # Vollständige kompilierte Ontologie als JSON-LD
├── prima-materia.ttl            # Vollständige kompilierte Ontologie als Turtle
├── context.jsonld               # JSON-LD Context (Kopie aus source/context/)
└── version.json                 # { "version": "...", "git_sha": "...", "built_at": "..." }
```

Die `llms.txt` und die Teilgraphen stehen auf dem Namensraum-Host und nicht im
Spiegel (Abschnitt 8). Das Distributionsrepo führt die vollständigen
Serialisierungen und sonst nichts.

### Selektives Laden

Der Bestand wächst mit jedem Lauf, und ein Client mit einer Frage an eine
einzelne Überlieferung soll dafür nicht den ganzen Graphen parsen müssen. Er
wird deshalb in Teile zerlegt, die einzeln geladen werden können; sie liegen
unter `parts/` neben der Seite.

Die frühere Fassung sah dafür „Pro-Tradition-Splits" vor, und das ist der
falsche Schnitt: eine Aufteilung nach Tradition ist keine Partition. Die
Inhaltsknoten ohne `pm:withinTradition` sind die Konvergenzen, die Streitfälle,
die Prüfungen und die als modern ausgewiesenen Ordnungen — der Ertrag des
Projekts und kein Rest. Wer nur nach Traditionen schneidet, liefert die
Sammlung aus und lässt die Prüfstelle liegen.

Der Schnitt folgt deshalb den drei Schichten, die die Namensräume ohnehin
markieren:

| Teil | Inhalt |
|---|---|
| `vocabulary` | alles im `pm:`-Namensraum: Klassen, Properties, Skalen, Bezeugungsmodi |
| `<tradition>` | die `pmt:`-Instanz und alles, was mit `pm:withinTradition` auf sie zeigt |
| `findings` | jeder Inhaltsknoten, der zu keiner Tradition gehört |

Zwei Bedingungen, die jeder Teil erfüllt und die die Tests sichern:

1. **Jeder Teil ist eine Teilmenge des ganzen Graphen.** Wer mehrere lädt, sieht
   nie ein Tripel, das die vollständige Serialisierung nicht hat.
2. **Kein Teil zeigt auf einen Knoten, den er nicht benennt.** Für Begriffe, die
   ein Teil referenziert und nicht enthält, trägt er einen Stub aus Typ, Label
   und Tradition. Sonst liest ein Client, der einen Teil allein lädt, Kanten ins
   Leere, und gerade die Konvergenzknoten zeigen quer über die Traditionen.

`vocabulary` ist ohne die übrigen Teile sinnvoll; die übrigen sind ohne
`vocabulary` nicht interpretierbar, weil dort steht, was `pm:attestedBy` und die
Skalen bedeuten. Die `llms.txt` sagt das dem Client.

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
| `pm:Converging` | Übereinstimmung über Traditionen hinweg | `pm:transmissionPath` **oder** `pm:independentAttestation`; bei letzterem zusätzlich `pm:independenceGround` |
| `pm:Reworking` | eine Tradition übernimmt eine Behauptung und fügt etwas hinzu | `pm:reworkedClaim`, `pm:receivedFrom`, `pm:addedElement`, `pm:attestedBy` |
| `pm:Testing` | ein Prüfprotokoll | `pm:examinationState`, `pm:examinedBy`, `pm:protocolUpdated` |

**Bezeugungsmodi** (`pm:Attesting`): `pm:textualAttestation`, `pm:firstPersonReport`, `pm:protocolledPractice`, `pm:thirdPartyAscription`, `pm:compilerInference`. Der letzte bezeugt einen Ordnungsakt, nie die geordnete Behauptung; `pm:CompilerInferenceScopeShape` erzwingt das.

**Zwei kontrollierte Skalen tragen die schwachen Fälle.** Sie existieren, damit schwaches Material eingetragen werden kann, nicht damit es draußen bleibt. Ein Befund gehört auf die Stufe, die er verdient.

`pm:PrerequisiteStrength`: `pm:statedNecessity` nur mit zitierbarer `pm:consequenceOfSkipping`, sonst weist `pm:StatedNecessityShape` ab; `pm:prescribedOrder` für eine Anweisung ohne Folgenangabe; `pm:presentationOrder` für eine bloße Darstellungsreihenfolge.

`pm:ExaminationState`: `pm:noProcedureDevised`, `pm:procedureWithoutCases`, `pm:casesWithoutDeviation`, `pm:casesWithDeviation`, `pm:claimDoesNotDiscriminate`. Der erste Stand darf nie mit dem vierten zusammenfallen. Eine Behauptung, für die niemand ein Prüfverfahren ersonnen hat, ist keine Behauptung, die geprüft und nicht gestützt wurde; wer beides gleich meldet, berichtet nicht über die Behauptungen, sondern über die Reichweite der eigenen Instrumente.

**Evidenz ist eine Partei, keine Instanz.** Eine Arbeit unter `pm:evidenceFrom` trägt eine eigene Behauptung, ein eigenes Verfahren und eigene Kritiker. Ein Protokoll, das sie ohne Suche nach Widerspruch aufnimmt, hat die Behauptung nicht gegen die Welt geprüft, sondern gegen einen Bericht über die Welt — derselbe Fehler wie die Prüfung einer Überlieferung gegen diesen Bestand statt gegen ihre Quelle, und leichter zu begehen, weil eine Studie wie ein Urteil aussieht.

Deshalb `pm:counterSearch` mit `pm:counterSearchNotCarried`, `pm:counterSearchFoundNothing`, `pm:counterSearchFoundOpposition`, dazu `pm:counterSearchNote` mit dem, wonach gesucht wurde und was kam. Pflicht, sobald `pm:evidenceFrom` gesetzt ist (`pm:CounterSearchRequiredShape`), und die Notiz ist Pflicht, sobald der Stand gesetzt ist (`pm:CounterSearchNoteRequiredShape`) — ohne sie wäre „nichts gefunden" von „niemand hat gesucht" nicht zu unterscheiden.

**Ein Stand, der Fälle meldet, setzt die geführte Gegensuche voraus** (`pm:CasesRequireCounterSearchShape`): `pm:casesWithoutDeviation`, `pm:casesWithDeviation` und `pm:claimDoesNotDiscriminate` sind mit `pm:counterSearchNotCarried` unvereinbar, und bis die Suche geführt ist, gilt `pm:procedureWithoutCases`. Das ist die Vorrichtung, nicht die Ermahnung: die Regel stand am 2026-09-02 als Prosa in `AGENTS.md` und wurde noch in derselben Sitzung gebrochen.

Der fünfte Stand ist keine mildere Fassung des dritten. Dort sagt die Behauptung etwas, und die Fälle bestätigen es; hier bestätigen die Fälle, weil die Behauptung nicht genug sagt, um an irgendetwas zu scheitern. Entscheidend ist nicht, wie stark die Evidenz ist, sondern ob es einen Ausgang gibt, den die Behauptung ausgeschlossen hätte — deckt sie ein Ergebnis und sein Gegenteil gleichermaßen, unterscheidet sie nichts. Wer diesen Stand setzt, muss über `pm:undividedOutcomes` die Ausgänge benennen, die die Behauptung gleich behandelt; das erzwingt `pm:UndividedOutcomesRequiredShape`. Ohne diese Pflicht würde der Stand zur bequemen Ablage für alles, was den Prüfenden nicht überzeugt hat, und der Bestand berichtete über dessen Geduld statt über die Behauptungen.

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

**Dieser Abschnitt beschreibt, was die Workflows leisten müssen, und nicht ihren Wortlaut.** Der Wortlaut steht in `.github/workflows/`. Ein wörtliches Listing hier war zweimal falsch, bevor es jemandem auffiel. Es ist auch dann überflüssig, wenn der Agent die Dateien schreiben kann: was zu gelten hat, steht hier, was gilt, steht dort, und zwei Fassungen desselben Wortlauts laufen auseinander.

**Der Scope-Vermerk an dieser Stelle ist überholt.** Bis zum 2026-09-02 trug das Agenten-Token keinen `workflows`-Scope, und Workflow-Änderungen waren zu beschreiben und von Hand einzuspielen. Der Versuch am 2026-09-02 ging durch; die beiden Änderungen aus prima-materia#352 und prima-materia#353 sind vom Agenten selbst geschrieben. Wer hier eine Änderung braucht, schreibt sie und begründet sie im PR wie jede andere. Das Recht, den eigenen Prüflauf zu ändern, verlangt dabei mehr Vorsicht als jede Datenänderung: eine Lockerung an `validate.yml` fällt niemandem auf, weil danach alles grün ist.

### `validate.yml`

Läuft auf `push` nach `main` und nach `claude/**` sowie auf `pull_request` gegen `main`, installiert die Abhängigkeiten und führt `scripts/validate.py` und `pytest tests/` aus.

Der Trigger auf `claude/**` ist die Bedingung dafür, dass die in `AGENTS.md` vorgeschriebene Reihenfolge überhaupt erfüllbar ist: auf dem Arbeitsbranch prüfen, dann den PR öffnen. Ohne ihn entsteht der erste Lauf mit dem PR, und ein Fehler in einer TTL-Datei fällt erst an der offenen Änderung auf.

Eine `concurrency`-Gruppe je Ereignistyp und Ref mit `cancel-in-progress: true` bricht die Läufe überholter Zwischenstände ab. Gewollte Nebenwirkung: ein Branch mit mehreren Commits sammelt `cancelled`-Läufe. Ein abgebrochener Lauf hat nichts festgestellt und ist kein Fehlschlag; `prima_repo_check` wertet deshalb ausschließlich den Lauf des aktuellen Kopf-SHA. Siehe #32 und #44.

**Kein Lauf beim bloßen Anlegen eines Branches.** Ein Push, der einen Ref erst erzeugt, prüft einen Commit, der auf seinem Ursprungsbranch bereits geprüft ist; der Lauf hat nie Aussagewert. Er hat aber eine Nebenwirkung, und sie ist teuer: bei gestapelten Branches trägt der neue Ref anfangs den Kopf-SHA des darunterliegenden PR. Der erste echte Commit auf dem neuen Branch bricht diesen Lauf ab, der abgebrochene Lauf bleibt an jenem SHA hängen, und GitHub rollt für einen PR alle Check-Runs am Kopf-SHA zusammen, gleich von welchem Ref sie stammen. Ergebnis: ein rotes Kreuz an einem grünen PR, und zwar ausgerechnet an dem, von dem abgezweigt wurde. Der Job trägt deshalb `if: ${{ !(github.event_name == 'push' && github.event.created) }}`; `github.event.created` ist genau dann wahr, wenn der Ref mit diesem Push entstanden ist, und ist bei `pull_request` null. Fall und Lauf-Nummern in prima-materia#352.

### `pages.yml`

Läuft auf `push` nach `main`, baut die Seite mit `scripts/publish.py` und deployt sie auf den Namensraum-Host. Braucht `pages: write` und `id-token: write`; nichts daran schreibt ins Repository zurück.

Die `concurrency`-Gruppe hier trägt ausdrücklich `cancel-in-progress: false`, anders als bei `validate.yml`. Ein abgebrochener Prüflauf kostet nichts; ein abgebrochenes Deployment kann ein halb hochgeladenes Artefakt zur Live-Seite machen, und die Live-Seite ist der Ort, an dem die Terme geprägt sind.

### `distribute.yml`

Läuft auf `push` nach `main` und auf `workflow_dispatch`, validiert, kompiliert, transmutiert und schiebt die Serialisierungen samt `version.json` nach `pajew-ski/prima-materia-dist`, wenn sich etwas geändert hat.

Der Spiegel ist ausdrücklich sekundär. Der Namensraum-Host liefert dieselben Dateien und ist der Ort, den die Bezeichner nennen; `distribute.yml` existiert für Abnehmer, die über jsDelivr laden wollen.

**Eine `concurrency`-Gruppe `distribute` mit `cancel-in-progress: false` serialisiert die Läufe.** Der Schreibschritt endet auf einem nackten `git push` ins Dist-Repo, ohne Retry. Zwei kurz hintereinander gemergte PR — der Normalfall bei einem gestapelten Lauf — starten sonst zwei Läufe, die dasselbe Dist-Repo zum selben Zeitpunkt ausgecheckt haben; der zweite scheitert non-fast-forward. Der Fehler ist still an der Stelle, an der er zählt: `main` ist grün, `version.json` im Spiegel zeigt einen älteren `git_sha`, und erst der nächste Push nach `main` repariert es zufällig mit. Abgebrochen werden darf hier nicht, aus demselben Grund wie bei `pages.yml`: ein abgebrochener Prüflauf kostet nichts, ein abgebrochener Publikationslauf lässt den Spiegel zurückstehen. Fall in prima-materia#353.

**Hinweis für den Agent:** Das `DIST_REPO_TOKEN`-Secret muss vom User manuell in den Repo-Settings gesetzt werden (Personal Access Token mit Write-Access auf prima-materia-dist). Das ist nicht vom Agent automatisierbar.

## 8. llms.txt

**Die `llms.txt` steht auf dem Namensraum-Host**, wird von `scripts/publish.py` erzeugt und mit der Seite ausgeliefert. Frühere Fassungen dieses Abschnitts setzten sie ins Distributionsrepo und verlinkten von dort auf jsDelivr; das macht den Spiegel zur Adresse. Nach Abschnitt 2 fallen Bezeichner und Auslieferungsort zusammen, und die Datei, die einem Agenten sagt, wo die Ontologie liegt, ist die letzte, die woandershin zeigen darf.

Inhalt: eine Kurzbeschreibung des Projekts, die drei Serialisierungen unter `https://pajew.ski/prima-materia/`, ein Abschnitt über das Lesen einer Behauptung, die Liste der Traditionen, und die Verweise auf Quellrepo, Spezifikation und Issue-Tracker.

Zwei Festlegungen dazu.

**Der Abschnitt „How to read a claim" ist kein Beiwerk.** Ein Client, der den Graphen ohne ihn lädt, liest Behauptungen als Aussagen: er sieht nicht, dass `pm:compilerInference` einen Ordnungsakt bezeugt und nie die geordnete Behauptung, dass eine Konvergenz mit `pm:transmissionPath` Rezeption ist und nichts belegt, und dass ein fehlender `pm:Testing`-Knoten „niemand hat die Prüfung aufgenommen" heißt und nicht „geprüft und nicht gestützt". Die Trennung von Behauptung und Beglaubigung ist der Zweck dieses Projekts; eine Discovery-Datei, die sie nicht mitliefert, gibt den Graphen als Sammlung heraus.

**Die Traditionsliste wird aus dem Graphen abgeleitet, nicht aus dem Verzeichnis.** Die frühere Fassung sagte „ein Eintrag je Datei in `traditions/`". Das ist falsch aus demselben Grund, aus dem Abschnitt 10 die Datei-Ebene im Graphen ablehnt: die Datei ist eine Einheit des Repos und keine der Sache. `traditions/greek-pneuma-hesychasm.ttl` trägt zwei Traditionen, und ein Client will wissen, welche Überlieferungen der Graph führt, nicht wie sie auf Dateien verteilt sind. Abgeleitet wird deshalb über die `pm:Tradition`-Instanzen, mit Label, Definition und einem Anker auf die Seite. Von Hand gepflegt wird nichts: eine fest verdrahtete Liste läuft dem Bestand hinterher.

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
- **Sekundäre Zusammenfassungen** anstelle der Stelle, die sie zusammenfassen — mit der einen Ausnahme, die der folgende Abschnitt regelt.

### Wenn das Werk nicht zu beschaffen ist

Das Grounding im Original hat Vorrang und behält ihn. Es gibt aber Werke, die nicht erreichbar sind: nicht digitalisiert, vergriffen, ordensintern, in einer Sprache, die der Bearbeiter nicht liest. Sie ganz draußen zu lassen kostet mehr, als es schützt — der Bestand berichtet dann nicht über die Überlieferung, sondern über die Beschaffungslage.

**Deshalb ist die Stelle in zweiter Hand zulässig, wenn die Vermittlung im Graphen steht.** Der Knoten trägt dann `pm:attestedBy pm:mediatedAttestation` und nennt mit `pm:readVia` das Werk, in dem der Bearbeiter die Stelle tatsächlich gelesen hat. `dcterms:source` nennt weiterhin das Werk, das die Behauptung trägt, denn das ist es, was ein späterer Leser beschaffen muss; `pm:readVia` nennt, was der Schreibende vor sich hatte. `pm:MediatedAttestationShape` weist einen Knoten ab, der den Modus setzt und den Vermittler verschweigt.

**Der Unterschied zwischen den beiden Angaben ist der ganze Punkt.** Eine Stelle in zweiter Hand trägt die Auswahl des Vermittlers, seine Übersetzung und sein Schweigen. Wer nicht sehen kann, dass sie aus zweiter Hand kommt, kann nichts davon abwägen — und genau diese Blindstelle entsteht, wenn man die Vermittlung in eine `skos:note` schreibt statt in ein Prädikat, nach dem sich abfragen lässt.

**Der Modus ist an die Unerreichbarkeit gebunden, nicht an den Aufwand.** Er existiert, damit unerreichbares Material in seiner wahren Stärke eingehen kann, nicht damit erreichbares billig eingeht. Ein Werk, das sich herunterladen und durchsuchen lässt, ist erreichbar (SPEC §15); wer es über ein Referat zitiert, verletzt die Regel, auch wenn er den Vermittler nennt. Der Grund für die Vermittlung gehört ins Issue und ist eine Eigenschaft des Werkes.

**Ein vermittelter Knoten bleibt ein offener Posten.** Er ist kein Abschluss, sondern der beste erreichbare Zwischenstand: sobald das Werk zugänglich wird, wird die Stelle nachgeprüft und der Modus auf `pm:textualAttestation` gehoben. Das zugehörige Issue bleibt offen und trägt, welches Exemplar fehlt.

**Der Maßstab ist Auffindbarkeit, nicht Nummerierung.** Die Angabe muss so genau sein, dass ein Leser die Stelle im benannten Werk findet. Eine Nummer ist keine Bedingung, wo das Werk keine hat oder wo die Zählung zwischen Ausgaben schwankt: `"Philokalia I, Hesychios of Sinai, On Watchfulness and Holiness"` und `"John Climacus, The Ladder of Divine Ascent, steps 1-30"` sind zulässig. Schwankende Zählungen gehören in eine `skos:note`, nicht in eine Weglassung. Zitiergenauigkeit ist nicht Zitierbarkeit, und ein Befund, der an einer fehlenden Kapitelnummer scheitert, obwohl Werk und Traktat benannt sind, ist unnötig verloren.

**Die Ausgabe gehört in jede Angabe, und zwar die, aus der gelesen wurde.** Die frühere Fassung dieser Regel verlangte die Ausgabe dort, „wo Textzeugen inhaltlich auseinandergehen". Das ist nicht anwendbar: ob sie auseinandergehen, weiß man erst nach dem Vergleich, und wer ihn nicht geführt hat, entscheidet die Frage durch Weglassen. Die Regel lautet deshalb umgekehrt und ist eine Aussage über die eigene Arbeit, die immer bekannt ist: `dcterms:source` nennt Werk, Stelle und die Ausgabe oder Übersetzung, aus der der Bearbeiter sie gelesen hat.

Das ist keine Formalie, sondern die Anwendung von Abschnitt 15 auf die Quellenangabe. Ein Befund ist auf die Suche relativiert, nicht auf den Bestand — und die Ausgabe *ist* diese Relativierung. Ohne sie behauptet ein Knoten eine Textkenntnis, die er nicht hat: er sagt „Haṭhayogapradīpikā III.73", wo er sagen müsste, dass er die Vulgata gelesen hat und nicht weiß, ob die kritische Edition dort ebenso zählt.

Wo die Kenntnis aus mehreren Ausgaben zusammengesetzt ist, wird das gesagt statt geglättet. Wo die Schwankung selbst der Befund ist, kommt zusätzlich ein `pm:Disputing`-Knoten; er ersetzt die Angabe nicht.

**Abweichende Fassungen stehen als getrennte Knoten:** `"1 Enoch 8:3 (Ethiopic; Charles 1912)"` neben `"1 Enoch 8:3 (Aramaic/Greek reconstruction; Nickelsburg 2001)"`. Ein gemittelter Knoten meldet einen Text, den kein Zeuge gibt. Streiten die Ausgaben nur über Datierung oder Lesung, ohne dass zwei Fassungen entstehen, gehört das in einen `pm:Disputing`-Knoten.

**Negative Befunde gehören in den Bestand.** Eine Ordnung, die erst Kommentar oder Moderne hergestellt hat, wird ein `pm:Systematizing`-Knoten mit benanntem Kompilator; ein Streit zwischen Grundtext und Lesern ein `pm:Disputing`-Knoten; eine Behauptung, die der Korpus noch nicht beantwortet, ein Issue nach Abschnitt 13, mit den geprüften Kandidatenstellen und dem Grund des Scheiterns. Sonst prüft der nächste Agent dieselbe Behauptung und scheitert genauso.

**Ein Turtle-Kommentar ist kein Ort für einen Befund.** Kommentare fallen beim Kompilieren weg; der ausgelieferte Graph weiß von einer Prüfung nichts, die nur im Dateikopf steht. Was eine Prüfung ergeben hat, gehört in einen Knoten, in eine `skos:note` oder in ein Issue.

Daraus die Regel für den Dateikopf: **er darf nur enthalten, was beim Verlust nichts kostet.** Aufbau der Datei, Hinweis für den nächsten Bearbeiter, Begründung der Ablage. Jede Aussage über die Sache gehört an einen Knoten — die Begründung einer Traditionsdatei als `skos:note` an ihre `pmt:`-Instanz, die es ohnehin gibt.

Eine Datei-Ebene im Graphen, die den Kopf als Aussage trüge, wird **nicht** eingeführt. Die Datei ist eine Einheit des Repos und keine der Sache: zwei Traditionen können in einer Datei stehen, und die `korpus:`-Label benennen ausdrücklich den Korpus und nicht die Datei. Ein Graph, der Dateien als Entitäten führt, bindet sich an eine Aufteilung, die sich beim nächsten Umsortieren ändert.

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
| `befund` | markiert das Issue als Repo-Arbeit, nicht als Behauptung. Das Komplement zu `behauptung` und das Dachlabel der vier folgenden |
| `befund:werkzeug` | Zugangsweg, Werkzeuggrenze, Umweg. Erledigt, wenn der Weg dokumentiert oder das Werkzeug geändert ist |
| `befund:ontologie` | Vokabular, Shape, fehlendes Prädikat. Erledigt, wenn die Ontologie geändert ist |
| `befund:bestand` | falsche, doppelte oder fehlende Daten im Graphen. Erledigt, wenn die Daten korrigiert sind |
| `befund:verfahren` | Regel in dieser Spezifikation, in `AGENTS.md`, in `CONTRIBUTING.md` oder in einem Workflow. Erledigt, wenn die Regel geändert ist |

**Jedes Issue trägt entweder `behauptung` oder `befund`.** Die Aufteilung stand von Anfang an in der Definition von `behauptung` — „nicht als Repo-Arbeit" —, aber die andere Hälfte hatte keinen Namen, und was keinen Namen hat, ist nicht als Menge abfragbar. Die Folge war messbar: bei der Einführung dieses Labels trugen 61 von 287 offenen Issues gar kein Label, und es waren fast genau die Repo-, Werkzeug-, Ontologie- und Verfahrensbefunde. Sie hatten stattdessen ein Ersatzvokabular in den Titeln gebildet — Werkzeugbefund, Werkzeuglücke, Werkzeugfalle, Werkzeugmechanik, Bestandsbefund, Ontologielücke —, also vier Namen für eine Klasse und keinen davon abfragbar.

Daraus folgt eine stehende Prüfung: **`is:issue is:open no:label` muss leer sein.** Ein Issue ohne Label ist kein neutraler Zustand, sondern eines, das in keiner Menge vorkommt.

Das Dachlabel neben den vier Verfeinerungen ist eine Eigenschaft des Werkzeugs und keine Redundanz: `label:` kennt keine Wildcards, `label:befund:*` gibt es nicht. Ohne `befund` an jedem einzelnen Issue macht jede neue Verfeinerung jede bestehende Oder-Abfrage still unvollständig — derselbe Fehler, den Abschnitt 13 für das zweite Nummernschema verbietet.

Die vier schneiden nicht nach Thema, sondern nach dem Zeitpunkt, zu dem sie gelesen werden: `befund:werkzeug` vor einem Lauf, weil dort steht, welche Zugangswege tragen; `befund:ontologie` blockiert Konvergenzknoten; `befund:bestand` sind Schulden gegen bereits gemergte Daten; `befund:verfahren` ändert Anweisungen. Sie kumulieren.

**Ein `befund` trägt kein `korpus:`-Label.** Der `korpus:`-Wert ist das Protokoll der Suchabdeckung einer Behauptung; an einem Werkzeugbefund zählt er eine Abdeckung mit, die nie stattgefunden hat.

**Das `korpus:`-Label kumuliert.** Eine Behauptung, die in der Atemliteratur nicht gefunden wurde, ist nicht unbelegbar, sondern in diesem Korpus nicht gefunden. Sie behält das Label, bekommt beim nächsten Durchgang das nächste dazu, und wird erst geschlossen, wenn die plausiblen Korpora erschöpft sind. Damit ist die Labelmenge zugleich die Suchabdeckung, und ein späterer Fund lässt sich daran messen, ob er einen nie geprüften Korpus betrifft.

Die Labelnamen benennen den Korpus, den man aufschlägt, nicht die Datei, in der er später landet. Zwei Traditionen können in einer Datei stehen und zwei Dateien denselben Autor führen.

**Warnung zum Werkzeug:** Ein unbekannter Labelname wird von GitHub stillschweigend als neues Label angelegt, statt den Aufruf abzuweisen. Ein Tippfehler erzeugt also ein zweites Bündel, das niemandem auffällt. Das gültige Vokabular steht in `CONTRIBUTING.md` und wird von dort übernommen, nicht aus dem Gedächtnis geschrieben.

## 14. Erweiterung des Korpus

Der Korpus ist rückwärts aus einem Methodenentwurf gewachsen: jede Datei existiert, weil sie etwas beantwortet, was ein moderner Text behauptet. Das macht das Grounding in dem Maß zirkulär, in dem der Bestand nur dort nachschlägt, wo er ohnehin schon hinsah. Wer ihn allein entlang offener Behauptungen erweitert, vertieft diese Prägung. Deshalb zwei Eingänge, und der zweite hat Vorrang, wenn beide anstehen.

**Bedarfsgetrieben.** Ein `korpus:`-Label auf einer Behauptung, für die es noch keine Datei gibt, ist bereits die Nachfragemeldung. Offene Issues je fehlendem Label ergeben die geordnete Warteschlange; ein zweites Verzeichnis dafür wird nicht geführt.

**Prüfbarkeitsgetrieben.** Knapp ist nicht die unabhängige Bezeugung, sondern die prüfbare Behauptung. Gesucht sind die Überlieferungen, die Anzeichen, Fristen, Kautelen und Misslingensbedingungen nennen — alles, woraus sich ein `pm:falsifiedBy` formen lässt. Eine Überlieferung, die sagt, woran ihr eigenes Scheitern zu erkennen wäre, bringt den Bestand weiter als eine, die nur geographisch weit weg liegt. Dieser Eingang hat Vorrang.

**Unabhängigkeitsgetrieben.** Weiter ein Eingang, aber nicht mehr der erste, und mit korrigierter Begründung. Eine weitere indische oder buddhistische Datei erhöht die Dateizahl, nicht die Zeugenzahl. Was ein belegter Kontaktweg verbietet, ist eine bestimmte Zählung — dieselbe Aussage zweimal zu zählen — und nicht die Aufnahme. Gesucht sind Überlieferungen ohne plausible Kontaktroute zu den bereits vertretenen, weil dort der Zuwachs an zählbaren Zeugen liegt.

### Rezeption ist ein Befund, keine Abwertung

Eine frühere Fassung dieses Dokuments ließ `pm:transmissionPath` die Übereinstimmung von Konvergenz auf Rezeption *herabstufen*. Das war eine Wertung in Definitionsgestalt und ist zurückgenommen. Ein Weg sagt, wie eine Behauptung gereist ist, nicht ob an ihr etwas dran war. Weitergabe über Jahrhunderte ist Selektion, denn die meisten Behauptungen überstehen sie nicht, und ein Bestand, der Überlieferung als Rauschen behandelt, wirft die einzige Evidenz weg, die er darüber hat, was immer wieder abzuschreiben sich lohnte. Stellt sich heraus, dass seit Jahrtausenden alle voneinander abgeschrieben haben, ist das ein Ergebnis und kein Scheitern: es zeigt, worüber sich alle aus irgendeinem Grund einig waren.

**Zwei Zahlen nebeneinander, und keine annulliert die andere.** Wie viele Überlieferungen eine Behauptung überhaupt tragen, und wie tief die Wege zwischen ihnen verzweigen. Viele Zeugen an einem Kabel ist eine andere Karte als viele Zeugen an drei, und beide sind lesbarer als der frühere Zustand, in dem der erste Fall gar nicht ausgewiesen wurde.

**Die Grenze, die bleibt:** Der Graph muss sagen können, welche der beiden Karten er zeigt. Dichte Überlieferung und starke Wirkung dürfen nicht gleich aussehen, sonst kehrt das Tor der Autorität in statistischer Verkleidung zurück. Deshalb bleibt `pm:independentAttestation` als eigene Angabe bestehen und wird durch `pm:independenceGround` begründungspflichtig.

**Unabhängigkeit ist außerdem ein schwächeres Instrument, als der Bestand lange tat.** Sie schützt gegen keine der drei häufigsten Quellen von Einigkeit: eine gemeinsame Physiologie, die dasselbe Erlebnis erzeugt, wo mit einem Körper dasselbe getan wird; eine strukturelle Notwendigkeit der Sache, an der jede brauchbare Fassung konvergiert; und die Form gestufter Institutionen, die einander ähneln, weil Institutionen mit Stufen einander ähneln. Was am Ende entscheidet, ist Reproduzierbarkeit; Unabhängigkeit sortiert dafür Kandidaten vor und spricht kein Urteil.

**Rezeption ist zweierlei, und der Unterschied ist zu modellieren.** Textliche Weitergabe heißt, dass jemand einen Satz abgeschrieben hat; das zeigt Überlieferung und sonst nichts. Operative Wiederaufnahme heißt, dass jemand die Anweisung genommen, ausgeführt und danach etwas geschrieben hat, das in der Vorlage nicht stand: eine Frist, eine Kautel, eine Korrektur, ein Anzeichen, eine Klage über eine Stelle, an der es nicht ging. Nur das Zweite unterscheidet eine Kopierkette von einer Versuchsreihe, und nur das Zweite ist gegen Rückkopplung immun. Der Dogon-Fall ist nicht schwach, weil er rezipiert ist, sondern weil an der zweiten Station nichts hinzukam, was nicht schon in der Frage steckte.

Die zu zählende Größe ist deshalb die Zahl der Stationen mit Bearbeitung, und dafür gibt es `pm:Reworking`. Die Klasse ist mit Absicht teuer: `pm:addedElement` zeigt auf einen Knoten, der Zusatz muss also eingetragen sein, bevor die Bearbeitung behauptet werden kann. Wie bei `pm:Testing` ist die Abwesenheit aussagekräftig und wird nicht durch Stubs gefüllt.

**Drei Entscheidungen vor dem ersten Knoten einer Tradition, nicht danach:**

1. **Der Kontaktweg.** Sonst stellt sich hinterher heraus, dass der neue Zeuge Rezeption ist, und die Datei zählt für keine Konvergenz.
2. **Rezension und Ausgabe.** Abschnitt 10 verlangt sie in der Angabe; ein nachträglicher Wechsel fasst jeden Knoten der Datei an.
3. **Die Zahl der tatsächlich zitierbaren Stellen.** `traditions/daoist.ttl` ist mit Absicht dünn und ist das ehrliche Modell: gewachsen wird in Stellen, nicht in Traditionsnamen.

### Registrierung und Bearbeitung sind zwei Akte

Die frühere Fassung band diese drei Entscheidungen an das Anlegen der Datei. Das war zu früh gesetzt und hatte eine Nebenwirkung, die niemand wollte: eine Überlieferung, für die der Kontaktweg noch nicht geklärt war, konnte im Graphen überhaupt nicht vorkommen. Der Bestand berichtete damit nicht über die Traditionen, sondern über die Reihenfolge, in der jemand Zeit für sie hatte, und eine Unterrepräsentation war von einer Nichtexistenz nicht zu unterscheiden.

**Eine Tradition wird deshalb registriert, bevor sie bearbeitet wird.** Eine Registrierung behauptet zweierlei und sonst nichts: dass diese Überlieferung besteht, und in welchen Werken sie im Wesentlichen liegt. Sie trägt `pm:principalCorpus` und steht auf `pm:coverageState pm:corpusNamed`. Sie trägt **kein** `dcterms:source`: eine Quelle nennt eine gelesene Stelle mit Ausgabe, und hier wurde nichts gelesen. `pm:principalCorpus` unterliegt derselben Literaturregel wie `dcterms:source`, benennt aber einen Korpus und keine Stelle.

**Was eine registrierte Tradition nicht darf.** Sie zählt für keine Konvergenz, sie ist keine unabhängige Bezeugung, und sie belegt nichts. Auf `pm:corpusNamed` bezeugt sie ausdrücklich nichts. Der Kontaktweg wird bei der Registrierung mit `pm:contactRoute` festgehalten, und `pm:contactRouteUndecided` ist dort der ehrliche Normalfall: die Entscheidung ist damit nicht gefallen, sondern sichtbar offen.

**Was sie einbringt.** Einen Nenner. Über- und Unterrepräsentation im Bestand werden zählbar, weil der Graph jetzt auch hält, was fehlt. Die Warteschlange dieses Abschnitts wird lesbar, ohne dass ein zweites Verzeichnis geführt wird: die geordnete Liste ist der Bestand selbst, gefiltert auf `pm:corpusNamed` und sortiert nach `pm:contactRoute`.

**Die Regel gegen dünne Dateien bleibt unverändert in Kraft.** Sie gilt jetzt an der Stelle, an die sie gehört: für die Bearbeitung. Eine Tradition, die vom Stand `pm:corpusNamed` heruntergeholt wird, wird an Stellen erschlossen und nicht an Namen, und die drei Entscheidungen oben fallen, bevor ihr erster Knoten geschrieben wird. Der Unterschied ist, dass sie bis dahin im Graphen steht und ihre eigene Leere ausweist, statt zu fehlen.

**Junge Traditionen sind Traditionen.** `pm:Tradition` ist ein fortlaufender Übertragungsakt, und das Alter gehört nicht zur Definition. Was Texte, Linien, Einweihungen und Nachfolger hat, wird als Tradition geführt. Behauptet eine junge Tradition Abstammung von einer alten, sind das zwei Behauptungen, und der Graph hält sie getrennt: die Übertragung wird registriert, die Abstammung wird ein `pm:Originating`- oder `pm:Disputing`-Knoten. Die Registrierung beglaubigt keinen Stammbaum.

**Die Grenze zur Wissenschaft verläuft nach Funktion, nicht nach Selbstbeschreibung.** Eine Tradition liefert Zeugnis: eine Stelle, an der jemand sagt, was der Fall ist. Eine Untersuchung liefert Evidenz: ein Verfahren mit einem Ausgang, der auch anders hätte ausfallen können. Evidenz betritt den Graphen ausschließlich über `pm:evidenceFrom` an einem `pm:Testing`-Knoten und nie als Quelle einer Tradition, weil ein Graph, der beides durch dasselbe Prädikat aufnimmt, das Geprüfte nicht mehr vom Prüfmittel unterscheiden kann. Ein Korpus, der beides liefert, geht zweimal ein, unter verschiedenen Prädikaten. Umgekehrt gilt dieselbe Regel: was sich Wissenschaft nennt und seine Ansprüche auf Zeugnis stützt statt auf ein Verfahren, ist eine Tradition und wird als solche geführt.

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

### Die zweite Stufe ist nicht abwählbar

Die Recherche hat zwei Stufen: die Landschaft, die findet, wo die Stellen liegen, und die Stelle selbst, die aufgeschlagen und gelesen wird. Nur die zweite trägt einen Knoten. **Daraus folgt nicht, dass sie entfallen darf.**

Die Trennung von bezeugt und erschlossen ist eine Schranke vor dem Graphen und keine Weiche im Ablauf. Wer aus „nur Gelesenes wird Knoten" schließt, es genüge, nichts zu lesen und alles als Issue abzulegen, hat aus einer Schranke eine Erlaubnis gemacht. Der Bestand wächst dann nie, und die erste Stufe ist verbraucht, ohne etwas zu tragen: sie erzeugt keine Befunde, sondern Adressen.

**Jede Behauptung, deren Werk erreichbar ist, wird im selben Lauf am Wortlaut geprüft.** Erreichbar ist ein Werk, das digitalisiert vorliegt und gelesen werden kann. Umfang und Aufwand ändern daran nichts; ein Volltextarchiv ist der Normalfall und nicht der Glücksfall, und ein tausendseitiger Band, der sich herunterladen und durchsuchen lässt, ist erreichbar. Die Schätzung, eine Prüfung brauche einen eigenen Lauf, ist kein Grund: sie wird vor dem Aufschlagen gemacht und ist deshalb keine Kenntnis, sondern eine Vermutung über die eigene Bequemlichkeit.

**Bleibt eine Prüfung aus, steht der Grund im Issue, und er ist eine Eigenschaft des Werkes** — nicht digitalisiert, urheberrechtlich gesperrt, nur intern verfügbar, nur als Druckausgabe vorhanden, Sprache nicht beherrscht. Fehlt er, ist die Prüfung unterlassen und der Lauf unvollständig, gleich wie sauber die Issues sind.

**Im ersten Anlauf nicht gefunden ist kein Grund.** Es ist eine Aussage über den Anlauf und keine über das Werk. Unerreichbarkeit wird festgestellt, nicht vermutet, und sie wird erst festgestellt, nachdem die Wege erschöpft sind, die es tatsächlich gibt:

- eine andere Kennung desselben Werkes im selben Archiv, denn dieselbe Ausgabe liegt dort oft mehrfach, einmal als Leihexemplar ohne Volltext und einmal mit
- eine andere Ausgabe oder Übersetzung desselben Werkes, auch eine ältere, gemeinfreie
- eine andere Umschrift des Titels oder des Autornamens, was bei nicht-lateinischen Schriften der häufigste Fehlschlag ist
- das Werk innerhalb einer Sammlung, einer Reihe oder eines Kommentars, der es vollständig abdruckt
- ein anderes Digitalisierungsvorhaben, eine Textsammlung des Fachs, eine Bibliothek mit eigenem Volltextzugang
- eine Sperre, die am Zugangsweg hängt und nicht am Werk, etwa eine Abwehr gegen automatisierte Abrufe: sie verlangt einen anderen Weg, keinen Verzicht

Nach welcher dieser Möglichkeiten gesucht wurde, gehört ins Issue. Erst wenn sie dort stehen und leer ausgegangen sind, trägt der Satz, das Werk sei nicht zu beschaffen.

Der Grund für diese Schärfe ist ein gezählter Fall und keine Vorsichtsregel: in einem einzigen Lauf wurden vier Werke als unerreichbar geführt, und alle vier lagen bei genauerem Suchen als Volltext vor. Die Fehlerquote der Vermutung lag damit bei vier von vier. Siehe prima-materia#76.

### Die Ernte am geöffneten Werk

Ein Werk, das für eine Behauptung geöffnet wurde, wird nicht für diese eine Behauptung wieder geschlossen. Der teure Schritt ist das Öffnen — Beschaffung, Wahl der Ausgabe, Prüfung des Textzustands, Lokalisierung der Stelle. Das Aufnehmen einer weiteren Stelle im schon offenen Text kostet fast nichts. Wer je Behauptung öffnet und schließt, zahlt den teuren Teil einmal je Behauptung statt einmal je Werk, und der Unterschied ist der Grund dieser Regel, nicht Gründlichkeit.

**Die Ernte ist keine Scope-Erweiterung, und sie braucht kein eigenes Issue vorher.** Das ist eine ausdrückliche Ausnahme von der Issue-Bindung des Laufs. Ohne sie ist ein Bearbeiter, der sich an die Regeln hält, gezwungen, gesehenes Wissen wegzuwerfen.

**Aufzunehmen ist, was der Graph tragen kann.** Vier Arten sind dabei nicht wahlfrei, sondern geschuldet:

- **Vermögen** — was an Zuständen, Fähigkeiten und Erreichungen als durch Übung erlangbar behauptet wird. Hier gilt Vollständigkeit im strengen Sinn: ein übergangenes Vermögen ist etwas, das zu lernen wäre und niemandem mehr auffällt.
- **Voraussetzungsketten** — was vor etwas anderem da sein muss, damit es überhaupt eintreten kann. Sie sind der Teil, den Zusammenfassungen zuerst verlieren, und der Teil, an dem eine Praxis scheitert.
- **Warnungen und Kautelen** — besonders die, die ihre eigene Verkennung mitnennen, und die Selbstwarnungen eines Textes gegen das, was er vorschreibt.
- **Prüfbares** — genannte Anzeichen, Kriterien, Fristen, Misslingensbedingungen; alles, woraus sich später ein `pm:falsifiedBy` formen lässt.

Erzählung, Lebenslauf, Polemik und kosmologisches Gerüst sind nicht geschuldet, sondern nach Ermessen, und nur soweit sie eines der vier tragen.

**Vollständigkeit heißt vollständig für das Geöffnete.** Wer fünf Passagen eines Werkes von vierhundert Seiten gelesen hat, hat nicht das Werk geerntet. Die Erntenotiz nennt daher beides: was aufgenommen wurde und welche Teile ungelesen blieben. Ein Anspruch auf Erschöpfung, der nicht stattgefunden hat, ist derselbe Fehler wie eine vermutete Unerreichbarkeit, nur an der anderen Achse.

**Die Erntenotiz steht im Issue, das den Lauf ausgelöst hat**, und sie nennt auch, was gesehen und bewusst nicht aufgenommen wurde, mit Grund. Das ist der wichtigere Teil: gesehen und stillschweigend fallengelassen ist von nie gesehen nicht zu unterscheiden, und ein späterer Bearbeiter kann einer Auslassung nur widersprechen, die dasteht.

**Die aufgenommene Seite wird namentlich geführt, nicht in Prosa.** Die Notiz listet die geschriebenen Knoten mit ihren Bezeichnern, und sie wird aus der Lektüre geschrieben, nicht aus der fertigen Datei. Der Grund ist die Umkehrung des Satzes darüber: solange die Notiz nur erzählt, was aufgenommen wurde, ist ein Knoten, der den Weg in den Bestand nicht gefunden hat, von einem nie gesehenen weiterhin nicht zu unterscheiden — die Notiz und die Datei sagen dann beide dasselbe Nichts. Steht die Liste da, ist die Auslassung die Differenz zwischen Notiz und Branch, also zählbar und von jedem prüfbar, der beides nebeneinanderlegt. Wird sie dagegen aus der fertigen Datei abgeschrieben, prüft sie nichts, weil sie dann per Konstruktion stimmt. Der dokumentierte Fall, in dem ein am Wortlaut geprüfter Fund nur die lokale Arbeitskopie erreichte, bei grünem PR und abgeschlossenem Lauf, steht in prima-materia#351.

**Die Ernte senkt keinen Maßstab.** Jede geerntete Behauptung braucht ihre eigene Stelle in derselben Ausgabe; eine gesehene, aber nicht lokalisierte Behauptung gehört ins Issue und nicht in den Graphen. Neue Traditionen und neues Vokabular bleiben Entscheidungen nach den Abschnitten 11 und 14 — die Ausnahme gilt für Knoten in bestehenden Ordnern, nicht für neue Überschriften.

**Und sie darf die Prüfschicht nicht abhängen.** Behauptungen sind billig geworden, Protokolle nicht. Wächst der Bestand an Behauptungen über mehrere Läufe, ohne dass `pm:Testing` und `pm:Disputing` mitwachsen, ist aus der Prüfontologie eine Zitatsammlung geworden, und das ist ein Befund für den nächsten Lauf und keine Nebensache.

Dieser Abschnitt steht hier und nicht nur in `AGENTS.md`, weil die Fehllesung eine Regel dieser Spezifikation betraf und weil eine Korrektur, die nur in der Agentendatei steht, bei deren nächster Umarbeitung verschwindet.

### Tiefe

**Eine Recherche ist kein paar Suchanfragen nebenbei.** Der Mindestumfang für eine Behauptung, die in den Graphen soll:

1. Der Fachterm in seiner Originalsprache und in den gebräuchlichen Transliterationen, nicht nur in der deutschen oder englischen Umschreibung.
2. Der Primärtext, mindestens zwei Übersetzungen, und die Sekundärliteratur, die die Stelle behandelt.
3. Die Datierung des frühesten Zeugen, und die Frage, ob die Zuschreibung an dieses Werk in der Fachliteratur bestritten ist.
4. Die Gegensuche nach 15.2.
5. Mindestens eine Überlieferung außerhalb der Sphäre, in der die Behauptung vermutet wird — sonst entsteht nie eine unabhängige Bezeugung.

**Was zurückkommt, gehört ins Issue, nicht in den Kopf des Agenten:** geprüfte Korpora, verwendete Suchbegriffe samt Transliterationen, gefundene und geprüfte Stellen, das Datum. Eine Recherche, deren Abdeckung nicht nachvollziehbar ist, muss beim nächsten Zweifel vollständig wiederholt werden und war damit umsonst.

### Beifang

Eine Recherche findet mehr, als die Frage verlangt. Dieser Beifang ist der Weg, auf dem der Bestand in die Breite wächst, und er ist ausdrücklich zu ernten — aber nicht auf demselben Weg wie der Zielbefund.

**Ein nebenbei gefundener Befund wird nur dann Knoten, wenn er selbst die volle Prüfung durchlaufen hat: Stelle plus Gegensuche.** Alles andere wird ein Issue mit `korpus:`-Label und den bereits geprüften Kandidatenstellen, damit die nächste Runde dort ansetzt, wo diese aufgehört hat.

Der Unterschied ist keine Förmlichkeit. Ein im Vorbeigehen aufgesammelter Fund ist nicht geprüft, sondern begegnet. Läuft er als Knoten ein, ist der Bestand wieder eine Sammlung, und die Trennung von Behauptung und Beglaubigung ist an der billigsten Stelle durchbrochen. Die Regel greift besonders dort, wo ein Rechercheergebnis seine eigenen Vorbehalte mitbringt: Seitenzahlen aus Sekundärliteratur, gemeinfreie Altübersetzungen statt kritischer Ausgaben, in der Forschung bestrittene Zuschreibungen. Solche Funde sind wertvoll und gehören festgehalten, aber als Issue.

**Der Beifang trägt die Konvergenzen.** Ein Befund, der zur gestellten Frage nichts beiträgt, kann für `pm:Converging` oder `pm:Disputing` entscheidend sein, weil beide erst entstehen, wenn mehrere Überlieferungen zu derselben Sache befragt wurden. Wer nur die eigene Frage protokolliert, wirft genau das Material weg, aus dem das eigentliche Werk besteht.

---

**Document version:** 1.0
**Maintained by:** Michael Pajewski
**License:** CC0 1.0 (this specification document inclusive)
