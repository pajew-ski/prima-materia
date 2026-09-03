# CLAUDE.md

Werkzeug- und Konventionsdetails für Claude Code an diesem Repository.

**Zuerst `AGENTS.md` lesen, vor allem anderen.** Dort stehen die Regeln der Arbeit: Recherche, Ernte, Quellen, Prüfung, der stehende Auftrag, die Abschlussbedingung der Sitzung. Diese Datei setzt sie voraus und wiederholt sie nicht. Vollständige Spezifikation in `SPEC.md`; bei Konflikten gilt `SPEC.md`.

Die Wiederholung ist entfernt, weil sie eine Kostenstelle war und weil sie driftete. Der Bootstrap las vier Dateien vollständig, 177244 Zeichen, bevor die erste Recherche begann; am 2026-09-03 sind drei Läufe in dieser Vorlast an Kapazitätsfehlern abgebrochen, bevor irgendetwas im Repo stand. Und die Kopie war bereits falsch: die Behauptungsklassentabelle in dieser Datei führte `pm:Reworking` und `pm:Situating` nicht, die in `SPEC.md` §3 Parameter 5 seit Tagen stehen. Fall in prima-materia#446, dieselbe Begründung wie für das entfernte Workflow-Listing in `SPEC.md` §7.

## Wo welche Regel steht

Kein Eintrag dieser Tabelle ist hier ausgeführt. Wer die Regel braucht, liest sie dort.

| Regel | Kanonische Stelle |
|---|---|
| Wozu das Repo da ist, Torkriterium | `SPEC.md` §0, `AGENTS.md` „Was dieses Repo ist" |
| Die vier Sätze der Recherche | `AGENTS.md` „Die Recherche-Regel", vollständig `SPEC.md` §15 |
| Die zwei Rechercheestufen, Erreichbarkeit, Unerreichbarkeitsgründe | `AGENTS.md` „Die Recherche hat zwei Stufen, und beide sind zu führen" |
| Ernte am geöffneten Werk, die vier geschuldeten Arten, Erntenotiz | `AGENTS.md` ebenda, vollständig `SPEC.md` §15 |
| Ernteläufe koordinieren, Lease, Branchname, Bezeichnerbildung | `AGENTS.md` „Ernteläufe koordinieren" |
| Was „gegroundet" heißt | `AGENTS.md` „Was „gegroundet" heißt und was nicht" |
| Quellenführung, Auffindbarkeit, Rezension, Vermittlungsmodus | `SPEC.md` §10, kurz `AGENTS.md` „Quellen" |
| Evidenz ist nicht Quelle, Gegensuchpflicht | `SPEC.md` §3 Parameter 5 |
| Behauptungsklassen, welche wofür, Bezeugungsmodi, die zwei Skalen | `SPEC.md` §3 Parameter 5 |
| Die Kette Behauptung, Überschneidung, Verallgemeinerung, Prüfung | `SPEC.md` §16, kurz `AGENTS.md` „Die Kette, auf die alles hinausläuft" |
| Die Bewusstseinsachsen und die Skalenfamilien | `SPEC.md` §17 |
| Negative Befunde, Befund auf die Suche relativiert | `SPEC.md` §13 „Befunde sind auf die Suche relativiert, nicht auf den Bestand" |
| Issues, Lebenslauf, Schließgründe, Issue-Nummer als Identität | `SPEC.md` §13, kurz `AGENTS.md` „Behauptungen liegen in Issues" |
| Label-Vokabular | `CONTRIBUTING.md` „Label-Vokabular" |
| Die vier Eingänge, mit denen der Korpus wächst | `SPEC.md` §14 |
| Designprinzipien, Prozess statt Substanz, Sphoṭa, Pronomenspektrum | `SPEC.md` §3 |
| Was der Agent nicht tun soll, verbotene Klassen, Turtle-Kommentar | `SPEC.md` §11 |
| Fixture-Pflicht je Shape, Ordnerregel für neue Datenordner | `SPEC.md` §9 |
| Batch statt nacheinander, ein Branch je Strang, Frage mit Empfehlung | `AGENTS.md` „Der stehende Auftrag" |
| Prüfung vor dem PR, Abgleich Klon gegen Branch | `AGENTS.md` „Prüfung, Läufe und der Abgleich vor dem PR" |
| Die Sitzung trägt sich selbst, die sechs Abschlussbedingungen | `AGENTS.md` „Die Sitzung trägt sich selbst" |
| Ausgelöste Validierung melden, nicht umformulieren | `SPEC.md` §11, `AGENTS.md` „Vor dem ersten Schreibzugriff" |

Was hier steht, steht nirgends sonst: Kommandos, die Konventionen von `site/`, die Kopiervorlagen, die Werkzeug-Fehlalarme.

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

`site/` enthält die handgeschriebenen Assets der GitHub-Pages-Seite (`index.html`, `style.css`, `ontology.js`, `theme.js`, `search.js`, `layouts.js`, `matrix.js`, `ontology/index.html`). `scripts/publish.py` kopiert sie nach `build/site/` und legt die aus dem Graphen abgeleiteten Daten (`ontology-data.json`) sowie die Serialisierungen daneben. Der `Pages`-Workflow deployt das bei jedem Push auf `main`.

- Die Seite wird **komplett aus dem kompilierten Graphen** gespeist. Neue Klassen, Properties und Instanzen erscheinen ohne Code-Änderung; Zähler, Legende, Panel, Suchindex, Anordnungen und Matrix leiten sich aus den Daten ab.
- **Jedes Literal erreicht die Seite, nicht nur die benannten sechs.** `_statements()` in `scripts/publish.py` trägt jedes literalwertige Prädikat außer Label, altLabel, Definition, Note, Comment und Source unter dem Namen der Property, die es aussagt. Eine neue Datatype-Property steht damit am selben Tag im Panel und im Suchindex, an dem sie in `ontology/` steht. Wer hier eine feste Liste einführt, verliert genau die Angaben, die eine Behauptung tragen: `pm:consequenceOfSkipping`, `pm:transmissionPath`, `pm:evidenceFrom`, `pm:compiledBy`, `pm:circulatesAs`. `test_every_literal_reaches_the_site` schlägt dann fehl.
- `pm:evidenceFrom` wird **nie** mit `dcterms:source` zusammengelegt — die Trennung, die Forschung überhaupt aufnehmbar macht, muss auch in der Darstellung halten.
- Design-Vorbild ist `pajew-ski/temet-nosce`: achromatische oklch-Tokens, φ-basierte Spacing- und Typo-Leiter, Canvas/Panel im Verhältnis φ:1, Cytoscape über jsDelivr.
- Neue Node-Art im Graphen → `KINDS` in `site/ontology.js` erweitern (Shape, Legenden-Name, Plural) und in `_kind()` in `scripts/publish.py` klassifizieren.
- **Landmarken sind eine Eigenschaft der Zeichnung, nicht der Art.** `ctx.isLandmark()` in `site/layouts.js` markiert, was eine Region *benennt*: Wurzel, Klassen und Traditionen, unter denen etwas steht. Eine nur registrierte Überlieferung benennt nichts, weil nichts neben ihr steht — als das noch an der Art hing, trug jede der 128 registrierten ein großes Label und drückte den Abstand der wirklich benennenden Terme unter die Kollisionsgrenze. Eine Anordnung mit eigenen Überschriften ergänzt sie über `landmarks` im `VIEWS`-Eintrag; `landmarksFor()` setzt die Klasse pro Ansicht.
- **Der Erschließungsstand ist eine eigene Achse.** Die Claim-Form-Matrix trägt nur die bezeugenden Traditionen und nennt in der Caption, wie viele registrierte sie auslässt; die Registertabelle (`registerTab()`) kreuzt `pm:CoverageState` gegen `pm:ContactRoute`. Eine leere Zeile pro unerschlossener Überlieferung wäre kein Befund, sondern `pm:corpusNamed` hundertfach wiederholt — und würde die Zellen zudecken, die etwas heißen: gelesen und trotzdem ohne diese Behauptungsform.
- **Skalenreihenfolge steht in `COVERAGE_SCALE` und `CONTACT_SCALE`** (`site/layouts.js`). Der Graph sagt, was jeder Term bedeutet, aber nicht, in welcher Folge sie stehen — und die Folge ist die ganze Lesart. Ein später hinzukommender Term erscheint hinten angehängt statt zu verschwinden; das ist der einzige Fehler, den diese Listen haben dürfen.
- **Aufteilung.** `search.js` (Suche), `layouts.js` (Anordnungen), `matrix.js` (Kreuztabelle) sind DOM-frei und rein; `ontology.js` verdrahtet sie mit Cytoscape und dem Panel. Das ist der Grund, warum sie testbar sind — beim Ändern nicht aufweichen.
- Neue Anordnung → Eintrag in `VIEWS` in `site/layouts.js` mit `question`: dem Satz, der sagt, welche Frage dieses Bild beantwortet. Eine Anordnung ohne beantwortete Frage ist Dekoration und gehört nicht in die Liste.
- **Getestet wird JavaScript mit JavaScript.** `tests/site.test.mjs` läuft über `tests/test_site_modules.py` in `pytest tests/` mit, gegen einen Mini-Korpus und gegen den echten kompilierten Graphen. Ohne `node` wird übersprungen, nicht stillschweigend weggelassen.
- **Cytoscape ist optional, alles andere nicht.** Ein fehlgeschlagener CDN-Load kostet die Zeichnung, nicht die Suche, das Panel oder die Matrix. Wer `ontology.js` erweitert, hält `cy === null` am Leben.

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
| „Praktiken dieser Art bringen diese Wirkung hervor" — aus mehreren bezeugten Behauptungen gebildet, von keiner Quelle gesagt | `pm:Generalizing` | `pm:generalizedStatement`, **zwei** `pm:generalizedFrom`, `pm:attestedBy pm:compilerInference`; **kein** `dcterms:source`, **keine** `pm:withinTradition` |
| „Diese Überlieferung nennt ein Wesen so und hält es für dies" — Engel, Wächter, Dämon, Gott, Geist | `pm:Naming` | `pm:nameForm` (Schreibung der zitierten Ausgabe), `pm:nameRole` (Term der Tradition selbst), `pm:attestedBy`, `pm:withinTradition`, Quelle |

Zu `pm:Naming` drei Dinge, die im Ablauf entscheiden. **Der Träger ist jetzt adressierbar:** wo `pm:ascribedTo` an einem `pm:Attributing` ein benanntes Wesen meint, zeigt es auf eine `pm:Naming`-Instanz. Die Property behält bewusst keine `rdfs:range`, weil sie auch auf die Menschheit vor einem Ereignis oder eine unbenannte Gattung zeigen muss. **Die operative Behauptung bleibt getrennt:** dass eine Anrufung unter diesem Namen etwas bewirkt, ist ein `pm:Yielding` mit der Anrufung als Praxis, nicht ein Feld am Namen — sie braucht ihre eigene Misslingensbedingung. **`pm:nameRole` ist ein Literal und keine Skala:** ein festes Vokabular müsste entscheiden, ob ein griechischer Daimon ein Engel oder ein Dämon ist, und diese Entscheidung gehört keiner Tradition im Bestand.

**Behauptungen sind Knoten, keine Kanten.** Sobald eine Aussage eine eigene Quelle, einen eigenen Bezeugungsmodus, eine eigene Stärke oder ein eigenes Prüfprotokoll tragen muss, ist sie zu reifizieren. Auf einer Kante sehen ein zitierfähiger Notwendigkeitssatz und eine Kapitelreihenfolge gleich aus. Kommt ein neuer Behauptungstyp hinzu, gilt dieselbe Regel, bevor der erste Knoten geschrieben wird.

Beim Reifizieren fallen zirkuläre Aussagen auf, die als Kante durchgehen: eine Praxis bringt nicht hervor, was sie ist. Die Zirkulation des Qi bringt kein Qi hervor, die Kanalreinigung keine Kanäle.

## Die Kette, auf die alles hinausläuft

Vollständig in `SPEC.md` §16. Vier Sätze, die im Ablauf entscheiden.

**Eine Behauptung ist, was eine Überlieferung sagt**, mit Werk und Stelle. Wo eine Anweisung „Hypothese" sagt, meint sie einen Issue und keine Klasse: eine Vermutung ohne gelesene Stelle gehört in den Tracker und nie in den Graphen.

**Eine Überschneidung wird nicht gefunden, sie wird behauptet.** `pm:Converging` trägt immer `pm:compilerInference`, und sie entsteht aus dem Beifang der Einzelrecherche — also während der ersten Stufe und nicht in einem späteren Durchgang, auf den zu warten wäre. Sie ist außerdem noch keine prüfbare Aussage: dass zwei Begriffe einander entsprechen, kann an keinem Ergebnis scheitern.

**Prüfbar wird es erst als Verallgemeinerung.** `pm:Generalizing` hält den Satz, den keine Quelle sagt, gebildet aus mindestens zwei bezeugten Behauptungen, auf die `pm:generalizedFrom` zeigt. Er trägt Herleitung statt Herkunft. Ein Satz aus einem Methodenentwurf hat keine bezeugten Vorgänger und kommt so nicht hinein; der Richtungssinn bleibt unangetastet.

**Die Warteschlange für die Prüfung ist damit abfragbar:** die Verallgemeinerungen, auf die kein `pm:Testing` zeigt, geordnet nach der Zahl ihrer Vorgänger und der Streuung von deren Traditionen. Bewusst kein Shape — ein Wächter, der zu jeder Verallgemeinerung ein Protokoll verlangte, machte die Warteschlange unschreibbar, und genau daran scheitert `pm:Positing` für diesen Zweck. Ein Lauf, der keine Prüfung aufnimmt, kann sich aber nicht mehr darauf berufen, dass keine anstand.

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
- Eine Behauptung, die der Korpus noch nicht beantwortet → **Issue in diesem Repo**, mit den geprüften Kandidatenstellen und dem Grund des Scheiterns. Sonst prüft der nächste Agent dieselbe Behauptung und scheitert genauso.

Datierungswarnungen gehören an den Knoten, nicht in eine Fußnote: wo eine Stufenfolge jünger ist als die Werke, denen sie zugeschrieben wird, sagt das die `skos:note` des Knotens.

**Ein Turtle-Kommentar ist kein Ort für einen Befund.** Kommentare fallen beim Kompilieren weg; der ausgelieferte Graph weiß von einer Prüfung nichts, die nur im Dateikopf steht. Was eine Prüfung ergeben hat, gehört in einen Knoten, in eine `skos:note` oder in ein Issue.

## Behauptungen, Issues, Labels

Vollständig in `SPEC.md` Abschnitt 13 und 14. Operativ:

**Der Issue-Tracker hält jede Behauptung, die der Bestand noch nicht beantwortet** — nicht nur die gescheiterten. Jeder darf einreichen, ohne Recherche und ohne in einer Linie zu stehen; das beseitigt dasselbe Tor wie CC0. Ein Issue lebt genau so lange, wie kein Knoten die Behauptung trägt. Schließen als `completed` mit Nennung des Knotens, oder als `not_planned` mit `unbelegt` beziehungsweise `nicht-graphfaehig`. Wiedereröffnung bei neuem Fund ist der Normalfall.

**Die Issue-Nummer ist die Identität der Behauptung.** Kein zweites Nummernschema. Rückverweis vom Knoten in einer `skos:note` als `prima-materia#42`, nie in `dcterms:source`.

**Recherchiert wird nach `korpus:`-Label gebündelt**, nicht nach Herkunftsabschnitt: die Arbeit folgt dem Text, den man aufschlägt. Die Labels kumulieren und sind damit das Protokoll der Suchabdeckung — „in diesem Korpus nicht gefunden" ist etwas anderes als „unbelegbar". Vokabular in `CONTRIBUTING.md`, von dort übernehmen: ein unbekannter Labelname wird stillschweigend als neues Label angelegt.

**Jedes Issue trägt entweder `behauptung` oder `befund`.** `befund` ist das Komplement und zugleich das Dachlabel für `befund:werkzeug`, `befund:ontologie`, `befund:bestand` und `befund:verfahren`, die kumulieren. Ein Befund trägt kein `korpus:`-Label — der `korpus:`-Wert zählt Suchabdeckung, und an einem Werkzeugbefund zählt er eine, die nie stattgefunden hat. `is:issue is:open no:label` muss leer bleiben; als das Label eingeführt wurde, standen dort 61 von 287 offenen Issues.

**Jeder Befund ist auf Korpus und Datum relativiert.** Gegroundet übersteht einen Gegenfund und wird zu `pm:Disputing`; wegen Gegenbezeugung verworfen kippt beim ersten stützenden Zeugen zurück in strittig. Eine Verwerfung, die auf einer einzigen Tradition beruht, ist ein einseitiger Streitfall und hat zu nennen, worauf sie beruht.

**Der Korpus wächst über vier Eingänge.** Drei setzen eine bereits gestellte Frage voraus und ordnen nur, welche zuerst drankommt: Prüfbarkeit — die Überlieferungen, die Anzeichen, Fristen, Kautelen und Misslingensbedingungen nennen — hat Vorrang, dann Unabhängigkeit, dann Bedarf aus offenen Issues. Zur Unabhängigkeit: eine weitere indische Datei erhöht die Dateizahl, nicht die Zeugenzahl. Vor jeder neuen Datei stehen Kontaktweg, Rezension und die Zahl der zitierbaren Stellen fest. `traditions/daoist.ttl` ist mit Absicht dünn und ist das Modell.

**Der vierte kommt ohne Frage aus, und nur er bricht die Prägung.** Ein Werk wird geöffnet, weil es zu einer registrierten Tradition mit dünnem Bestand gehört, nicht weil eine Behauptung darauf zeigt. Die Warteschlange ist der Registrierungsstand selbst — `pm:coverageState pm:corpusNamed`, sortiert nach der Zahl der bisher getragenen Knoten —, und ein zweites Verzeichnis wird auch hier nicht geführt. Der Ertrag sind Behauptungen, nach denen niemand gefragt hat, und nur die liefern eine Kategorie, die der Bearbeiter vorher nicht hatte. Was mit einer Frage gesucht wird, findet Übereinstimmungen, deren Begriff schon im Suchbegriff steckte, und eine solche Übereinstimmung bestätigt die Frage, bevor sie etwas über die Überlieferung sagt.

Beide Richtungen laufen im Batch nebeneinander, in eigenen Branches, und keine ersetzt die andere: der strukturelle Strang liefert Masse ohne Prioritätsordnung, die offenen Behauptungen liefern die Ordnung ohne Masse.

### Ernteläufe koordinieren

Sobald mehrere Agenten parallel ernten, gilt:

- **Die Arbeitseinheit ist ein Werk, kein Anspruch.** Teuer ist das Öffnen; eine weitere Stelle im offenen Text kostet fast nichts.
- **Der Lease ist ein Issue.** Je Werk ein Issue `Ernte: <Werk>` mit `ernte`; wer es nimmt, setzt `in-arbeit` und trägt sich als Assignee ein. Ein Zustand im Graphen wäre erst nach dem Merge sichtbar und als Reservierung zu langsam. Bricht ein Lauf ab, fällt das Label weg.
- **Der Branchname trägt den Werkslug**, `claude/ernte-<werk-slug>`. Damit zeigt `gh_branches` die laufenden Ernten, bevor ein Label gesetzt ist, und ein abgestürzter Lauf hinterlässt eine sichtbare Spur statt eines stillen Lochs.
- **Ein PR je Werk**, mit der Erntenotiz im Body und den Bezeichnern der geschriebenen Knoten namentlich. Kein Sammel-PR über mehrere Werke.
- **Der Lease verhindert nur gleichzeitige Doppelarbeit.** Gegen spätere hilft allein, dass derselbe Sachverhalt bei zwei unabhängigen Läufen denselben Bezeichner ergibt: `tests/test_identifier_uniqueness.py` meldet gleiche Bezeichner in zwei Dateien sofort und verschiedene Bezeichner für dieselbe Sache nie. Bezeichner werden deshalb aus dem Gegenstand gebildet — Tradition plus normalisierter Terminus in der Originalsprache —, nie aus der deutschen oder englischen Übersetzung, weil zwei Bearbeiter dort verschieden übersetzen und derselbe Gegenstand auseinanderfällt.

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
- Bei mehrdeutiger Spezifikation: **fragen, nicht raten** — und die Frage trägt eine Empfehlung, siehe unten
- Bei Scope-Erweiterung über Phase 0/1 hinaus: **vorher mit User abklären**

**Ein Branch und ein PR je unabhängigem Strang.** Was nicht dieselbe Datei anfasst, wartet nicht aufeinander: jeder Strang zweigt von `main` ab und wird einzeln vorgelegt. Gestapelt wird nur bei echter Dateiüberschneidung, und der PR sagt das im ersten Absatz. Drei kleine PR sind einzeln annehmbar und einzeln zurückweisbar; ein großer ist es nicht.

**Bis zum PR wird nicht innegehalten.** Keine Zwischenberichte, keine Bestätigungsfragen, keine Freigabe vor dem Schreiben. Geprüft wird am Merge.

**Jede Frage kommt mit einer Empfehlung.** Optionen, ihre Kosten, und welche empfohlen wird, mit Grund. Eine Frage ohne Empfehlung schiebt Arbeit weiter, die schon getan ist, und zwingt den Leser, sich denselben Fall ein zweites Mal zu erarbeiten. Das gilt auch, wo die Entscheidung ausdrücklich beim Menschen liegt: die Zuständigkeit für die Entscheidung ist nicht die Zuständigkeit für ihre Vorbereitung.

**Die Sitzung trägt sich selbst.** Sie darf offen lassen, was sie nicht schafft, aber nichts davon darf nur in ihr stehen: der nächste Lauf beginnt am Repo und sieht den Verlauf nicht. Fünf Bedingungen, geprüft und nicht erinnert — `no:label` leer; jeder PR nennt sein Issue; jedes Issue, dessen Gegenstand im Bestand steht, ist geschlossen; jede Recherche hat ihre Erntenotiz; jede offene Entscheidung liegt als Frage mit Empfehlung vor. Vollständig in `AGENTS.md`.

Die dritte ist die, die reißt. Ob ein Issue erledigt ist, steht im Bestand und nicht im Issue, also hilft nur Nachsehen. Ein erledigtes und offenes Issue ist teurer als ein fehlendes: es bindet Aufmerksamkeit an eine getilgte Schuld, und die abhängigen Issues führen sich weiter als blockiert.

**Ein neuer Datenordner muss an fünf Stellen nachgezogen werden**, sonst wird er still nicht kompiliert und nicht validiert: `DEFAULT_INPUTS` in `scripts/compile.py`, `DEFAULT_INPUTS` in `scripts/publish.py`, `DEFAULT_DATA_DIRS` in `scripts/validate.py`, `SCAN_DIRS` in `tests/test_no_substance_classes.py` und `SCAN_DIRS` in `tests/test_identifier_uniqueness.py`. Nichts schlägt fehl, wenn eine davon vergessen wird; die Dateien erscheinen einfach nicht. Die fünfte ist die teuerste: fällt sie aus, verschmelzen zwei Knoten mit demselben Bezeichner beim Kompilieren zu einem, und jede SHACL-Bedingung ist danach doppelt erfüllt, ohne dass etwas auffällt.

**Jedes neue Shape braucht einen Fixture, der zeigt, dass es feuert.** Ein Wächter, von dem nie gezeigt wurde, dass er auslöst, ist nicht als funktionierend bekannt. Hat das Shape eine Ausnahme, braucht es zusätzlich einen positiven Fixture für die Ausnahme, sonst ist unbekannt, ob die Ausnahme greift.

**Vollständiges Vokabular, belegte Knoten.** Eine Klasse behauptet nichts über die Welt, sie stellt eine Unterscheidung bereit; eine Quelle zu verlangen, wo nichts behauptet wird, wäre ein Kategorienfehler. Das Vokabular darf und soll der Sache vorauslaufen: es ist billiger, eine Unterscheidung vorzuhalten, die niemand braucht, als eine zu spät einzuführen und jeden Knoten umschreiben zu müssen, der inzwischen in der falschen Klasse gelandet ist. Was eine neue Klasse schuldet, ist keine Quelle, sondern eine `skos:definition`, die sagt, was als Instanz gelten würde. Ohne die ist sie kein Vorrat, sondern eine leere Stelle.

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

Nicht mehr auf dieser Liste: **Änderungen an `.github/workflows/*`.** Der Vermerk, das Agenten-Token trage keinen `workflows`-Scope und jeder Schreibversuch ende mit `403`, galt bis zum 2026-09-02 und ist überholt. Die beiden Änderungen aus prima-materia#352 (`validate.yml` läuft nicht mehr beim bloßen Anlegen eines Branches) und prima-materia#353 (`distribute.yml` bekommt eine serialisierende `concurrency`-Gruppe) sind vom Agenten geschrieben. Das Soll steht weiter in `SPEC.md` §7, und eine Änderung am eigenen Prüflauf gehört ausdrücklich in die PR-Begründung: eine Lockerung an `validate.yml` fällt niemandem auf, weil danach alles grün ist.

Bei diesen Schritten den User explizit auffordern und warten.

## Bekannte Fehlalarme der Werkzeuge

- Der Substanzklassen-Wächter im Schreibweg prüft **jede** TTL-Schreibung auf die vier verbotenen Namen, auch in `shapes/`. Dort müssen sie vorkommen, weil `pm:NoSubstanceClassesShape` sie verbietet, indem sie sie benennt; der zugehörige Test scannt `shapes/` folgerichtig nicht. Der Wächter ist an dieser Stelle strenger als die Regel, die er durchsetzt. **Melden, nicht umgehen** — siehe Workflow-Hygiene.

- **Ein grüner PR trägt ein rotes Kreuz, wenn von seinem Kopf abgezweigt wurde.** Beim gestapelten Arbeiten erbt der neue Branch anfangs den Kopf-SHA des PR darunter; das Anlegen des Refs startet einen `validate`-Lauf, der erste echte Commit bricht ihn ab, und GitHub rollt alle Check-Runs eines SHA am PR zusammen, gleich von welchem Ref sie stammen. Das Kreuz markiert nicht den defekten PR, sondern den, auf dem der nächste aufsitzt. `prima_repo_check` meldet in diesem Fall grün und hat recht; die Checks-Seite des PR zeigt den abgebrochenen Lauf mit dem fremden Branchnamen. Fall und Patch in prima-materia#352.

## Lizenz

CC0 1.0 — Code, Ontologie und Spezifikation. Public-Domain-Dedication für maximale maschinelle Nachnutzbarkeit.
