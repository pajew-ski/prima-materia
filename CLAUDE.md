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

### Der Maßstab ist Auffindbarkeit, nicht Nummerierung

Eine Quellenangabe muss so genau sein, dass ein Leser die Stelle **im benannten Werk findet**. Sie muss keine Nummer tragen, wenn das Werk keine hat oder wenn die Zählung zwischen Ausgaben schwankt.

- ✅ `"Philokalia I, Hesychios of Sinai, On Watchfulness and Holiness"`
- ✅ `"John Climacus, The Ladder of Divine Ascent, steps 1-30"`
- ✅ `"Athenian decree concerning Eleusis, IG I³ 6, face C"`

Zitiergenauigkeit mit Zitierbarkeit zu verwechseln kostet mehr, als es schützt. Ein Befund, der wegen einer fehlenden Kapitelnummer draußen bleibt, obwohl das Werk und der Traktat benannt sind, ist unnötig verloren. **Wo die Zählung zwischen Ausgaben schwankt, gehört das in eine `skos:note`, nicht in eine Weglassung.**

### Die Rezension gehört in die Angabe

Wo Textzeugen inhaltlich auseinandergehen, nennt `dcterms:source` die Rezension und die Ausgabe, und die abweichenden Fassungen stehen als getrennte Knoten. Eine Angabe wie `"1 Henoch 8:3"` behauptet einen einheitlichen Text, den es nicht gibt.

- ✅ `"1 Enoch 8:3 (Ethiopic; Charles 1912)"` neben `"1 Enoch 8:3 (Aramaic/Greek reconstruction; Nickelsburg 2001)"`

Ein gemittelter Knoten meldet einen Text, den kein Zeuge gibt. Wo die Ausgaben nur in Datierung oder Lesung streiten, ohne dass zwei Fassungen entstehen, gehört das in einen `pm:Disputing`-Knoten.

### Evidenz ist nicht Quelle

Ein moderner Forschungsartikel ist **nie** Zeuge einer Tradition und erscheint **nie** als `dcterms:source` an einem Traditionsknoten. Er trägt zu einer Behauptung von außen bei und gehört an `pm:evidenceFrom` eines `pm:Testing`-Knotens. Genau diese Trennung erlaubt es, Forschung überhaupt aufzunehmen, ohne die Quellenregel aufzuweichen.

Dort ist auch der DOI wieder zulässig, weil `doi:10.1371/...` eine Werkkennung ist und keine Ortsangabe. `pm:EvidenceIsLiteratureShape` weist auch hier `http`-Präfixe ab.

## Behauptungsklassen: welche wofür

Material aus einer Tradition kommt in sehr verschiedenen Formen. Die falsche Klasse zu wählen verzerrt die Behauptung, noch bevor sie geprüft werden kann.

| Form der Aussage | Klasse | Pflichtangaben |
|---|---|---|
| „X lehrte Y" — ein Vermögen wird einer Figur zugeschrieben | `pm:Attributing` | `pm:ascribedCapacity`, `pm:attestedBy`, Quelle |
| „Praxis P bringt Vermögen C hervor" | `pm:Yielding` | `pm:byPractice`, `pm:yieldsCapacity`, `pm:attestedBy`, Quelle |
| „B ist ohne A nicht zu erreichen" | `pm:Presupposing` | `pm:dependentStep`, `pm:priorStep`, `pm:prerequisiteStrength`, `pm:attestedBy`, Quelle |
| „Hütet euch vor C" | `pm:Cautioning` | `pm:cautionsAbout`, Quelle |
| Jemand hat geordnet, was das Material nicht ordnete | `pm:Systematizing` | `pm:compiledBy`, `dcterms:date` |
| Zwei Seiten streiten über eine Behauptung | `pm:Disputing` | `pm:disputedClaim`, **zwei** Quellen, `pm:attestedBy` |
| Eine Übereinstimmung über Traditionen hinweg | `pm:Converging` | Übertragungsweg **oder** unabhängige Bezeugung |
| Ein Prüfprotokoll zu einer Behauptung | `pm:Testing` | `pm:examinationState`, `pm:examinedBy`, `pm:protocolUpdated` |

**Behauptungen sind Knoten, keine Kanten.** Sobald eine Aussage eine eigene Quelle, einen eigenen Bezeugungsmodus, eine eigene Stärke oder ein eigenes Prüfprotokoll tragen muss, ist sie zu reifizieren. Auf einer Kante sehen ein zitierfähiger Notwendigkeitssatz und eine Kapitelreihenfolge gleich aus. Kommt ein neuer Behauptungstyp hinzu, gilt dieselbe Regel, bevor der erste Knoten geschrieben wird.

Beim Reifizieren fallen zirkuläre Aussagen auf, die als Kante durchgehen: eine Praxis bringt nicht hervor, was sie ist. Die Zirkulation des Qi bringt kein Qi hervor, die Kanalreinigung keine Kanäle.

## Die Skalen benutzen, statt zu schweigen

Zwei kontrollierte Vokabulare tragen die schwachen Fälle. Sie existieren, damit schwaches Material eingetragen werden kann, nicht damit es draußen bleibt.

`pm:PrerequisiteStrength`: `pm:statedNecessity` nur, wenn sich zitieren lässt, was der Text als Folge des Überspringens nennt — sonst weist `pm:StatedNecessityShape` ab. `pm:prescribedOrder` für eine Anweisung ohne Folgenangabe. `pm:presentationOrder` für „der Text ordnet sein Material so an, mehr sagt er nicht".

`pm:ExaminationState`: `pm:noProcedureDevised` ist die häufigste Lage und keine Schwäche der Behauptung, sondern eine Aussage über die Reichweite der Prüfmittel.

**Ein Befund gehört auf die Stufe, die er verdient, nicht in den Papierkorb.** Etwas unter `pm:presentationOrder` einzutragen behauptet keine Notwendigkeit; es hält fest, dass die Anordnung existiert, und genau das braucht ein späterer Leser, um zu sehen, wo ein modernes System eine Notwendigkeit hineingelesen hat. Wer solche Befunde weglässt, verliert nicht Vorsicht, sondern den Vergleichsmaßstab.

## Negative Befunde gehören in den Bestand

Ein Rechercheergebnis der Form „das steht so nicht im Grundtext" ist wertvoller als ein weiterer positiver Knoten und geht am leichtesten verloren.

- Eine Ordnung, die erst der Kommentar oder die Moderne hergestellt hat → `pm:Systematizing` mit `pm:compilerInference` und benanntem Kompilator.
- Ein Streit zwischen Grundtext und Lesern → `pm:Disputing`.
- Eine Warnung der Tradition gegen ihre eigenen Vermögen → `pm:Cautioning`.
- Eine Behauptung, die sich nicht bis zu einer Stelle zurückverfolgen ließ → **Issue in diesem Repo**, mit der geprüften Kandidatenstelle und dem Grund des Scheiterns. Sonst prüft der nächste Agent dieselbe Behauptung und scheitert genauso.

Datierungswarnungen gehören an den Knoten, nicht in eine Fußnote: wo eine Stufenfolge jünger ist als die Werke, denen sie zugeschrieben wird, sagt das die `skos:note` des Knotens.

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

**Ein neuer Datenordner muss an vier Stellen nachgezogen werden**, sonst wird er still nicht kompiliert und nicht validiert: `DEFAULT_INPUTS` in `scripts/compile.py`, `DEFAULT_INPUTS` in `scripts/publish.py`, `DEFAULT_DATA_DIRS` in `scripts/validate.py`, `SCAN_DIRS` in `tests/test_no_substance_classes.py`. Nichts schlägt fehl, wenn eine davon vergessen wird; die Dateien erscheinen einfach nicht.

**Jedes neue Shape braucht einen Fixture, der zeigt, dass es feuert.** Ein Wächter, von dem nie gezeigt wurde, dass er auslöst, ist nicht als funktionierend bekannt. Hat das Shape eine Ausnahme, braucht es zusätzlich einen positiven Fixture für die Ausnahme, sonst ist unbekannt, ob die Ausnahme greift.

**Kein Vokabular auf Vorrat.** Eine Klasse oder Property entsteht, wenn Material sie erzwingt, und mit ihrem ersten belegten Knoten im selben PR. Unbelegtes Vokabular ist derselbe Fehler wie ein unbelegter Knoten, eine Ebene höher.

**Kein Prüfknoten-Stub pro Behauptung.** `pm:Testing` entsteht, wenn jemand die Prüfung aufnimmt. Das Fehlen eines Knotens sagt bereits, was ein Knoten mit Stand „ungeprüft" sagen würde, und kostet nichts.

**Löst eine Validierung aus, wird sie gemeldet, nicht umformuliert.** Das gilt für SHACL, für die Tests und für jeden vorgeschalteten Wächter im Schreibweg. Hat ein Wächter falsch ausgelöst, ist das ein Befund über den Wächter und gehört berichtet, damit er repariert wird. Eine Umgehung, die nicht auffällt, repariert nichts und kostet das Vertrauen in genau die Vorrichtung, die den Menschen am Merge entlasten soll. Ob der Alarm berechtigt war, entscheidet nicht, wer schreiben will.

## Repositories

- **Source (dieses Repo):** `pajew-ski/prima-materia` — manuell editieren
- **Distribution:** `pajew-ski/prima-materia-dist` — auto-generiert, nie manuell anfassen

## Manuelle User-Aktionen (nicht Agent-automatisierbar)

- Aktivieren von GitHub Pages: **Settings → Pages → Source: GitHub Actions**. Der Workflow kann die Quelle nicht selbst umstellen.
- Setzen des `DIST_REPO_TOKEN`-Secrets im Source-Repo (Personal Access Token mit Write-Access auf `prima-materia-dist`)
- Anlage des `prima-materia-dist`-Repos in GitHub
- jsDelivr-Cache-Purge bei Bedarf

Bei diesen Schritten den User explizit auffordern und warten.

## Lizenz

CC0 1.0 — Code, Ontologie und Spezifikation. Public-Domain-Dedication für maximale maschinelle Nachnutzbarkeit.
