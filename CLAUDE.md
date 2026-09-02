# CLAUDE.md

Permanent-Context für Claude Code. Enthält operative Constraints und Konventionen. Vollständige Spezifikation in `SPEC.md` — bei Konflikten gilt `SPEC.md`. `AGENTS.md` enthält dieselben Regeln anbieterneutral und kürzer; wer nur eine Datei liest, liest die.

## Recherche — vor allem anderen

Vollständig in `SPEC.md` Abschnitt 15. Vier Sätze, deren Verletzung Etiketten statt Befunde erzeugt:

**Der Suchraum ist alles über das Internet erreichbare Wissen, nicht der Bestand.** Der Bestand ist spärlich, bleibt es, und ist rückwärts aus einem einzigen Methodenentwurf gewachsen. Ein vorhandener Knoten belegt nichts; er ist selbst nur eine früher eingetragene Behauptung mit Herkunft. Eine Behauptung gegen den Bestand zu prüfen und das Ergebnis „gegroundet" zu nennen, ist ein Zirkelschluss mit Etikett.

**Die erste Frage lautet: wo gibt es Quellen zu dieser Behauptung, die noch nicht im Bestand sind?** Nicht: was sagt der Bestand dazu.

**Jede Recherche sucht die Behauptung und ihre Negation**, und sie sucht in mindestens einer Überlieferung außerhalb der Sphäre, in der die Behauptung vermutet wird. Wer nur nach Bestätigung sucht, findet sie.

**Eine Recherche ist kein paar Suchanfragen nebenbei.** Fachterm in Originalsprache und Transliterationen, Primärtext plus zwei Übersetzungen plus Sekundärliteratur, Datierung des frühesten Zeugen, Gegensuche. Was zurückkommt, steht im Issue: geprüfte Korpora, Suchbegriffe, Stellen, Datum.

**Die Recherche hat zwei Stufen, und beide sind zu führen.** Die erste ist die Landschaft: ein breiter Auftrag über den erreichbaren Suchraum, der findet, **wo** die Stellen liegen, welche Sekundärliteratur widerspricht, wie datiert wird und welche Korpora man von selbst nicht bedacht hätte. Die zweite ist die Stelle: das Werk wird aufgeschlagen und im Wortlaut gelesen.

**Nur die zweite trägt einen Knoten — daraus folgt nicht, dass sie entfallen darf.** Die Regel „in den Graphen nur, was gelesen wurde" ist eine Schranke vor dem Graphen, keine Weiche im Ablauf. Wer daraus schließt, es genüge, nichts aufzuschlagen und alles als Issue abzulegen, hat den Auftrag nicht erfüllt, auch wenn am Ende saubere Issues stehen. Die erste Stufe erzeugt keine Befunde, sondern Adressen; eine Adresse, an die niemand geht, ist nichts, und die teuerste Hälfte der Arbeit ist dann verbraucht.

**Jede Behauptung, deren Werk erreichbar ist, wird im selben Lauf am Wortlaut geprüft.** Erreichbar heißt digitalisiert und lesbar, nicht bequem: ein gemeinfreies Werk in einem Volltextarchiv ist erreichbar, auch mit tausend Seiten — herunterladen und durchsuchen ist der Normalweg, nicht der Ausnahmeweg. Umfang, Aufwand und die Schätzung „das braucht einen eigenen Lauf" sind keine Gründe, sondern die Arbeit; die Schätzung entsteht vor dem Aufschlagen und ist deshalb keine Kenntnis.

**Bleibt eine Prüfung aus, steht der Grund im Issue, und er ist eine Eigenschaft des Werkes:** nicht digitalisiert, urheberrechtlich gesperrt, nur intern verfügbar, nur als Druckausgabe vorhanden, Sprache nicht beherrscht. Fehlt er, gilt die Prüfung als unterlassen.

**„Im ersten Anlauf nicht gefunden" ist kein Grund, sondern der Beginn der Suche.** Vor jeder Feststellung von Unerreichbarkeit abzuarbeiten:

- andere Kennung desselben Werkes im selben Archiv — dieselbe Ausgabe liegt oft mehrfach, einmal ohne und einmal mit Volltext
- andere oder ältere Ausgabe, andere Übersetzung, gemeinfreie Vorgängerfassung
- andere Umschrift von Titel und Autornamen; bei nicht-lateinischen Schriften der häufigste Fehlschlag
- das Werk innerhalb einer Sammlung, Reihe oder eines Kommentars, der es abdruckt
- anderes Digitalisierungsvorhaben, Fachtextsammlung, Bibliothek mit eigenem Volltextzugang
- Sperren am Zugangsweg (Bot-Abwehr, Anmeldezwang) hängen nicht am Werk: anderer Weg, kein Verzicht

Was versucht wurde, steht im Issue. Der Anlass ist gezählt und keine Vorsicht: in einem Lauf galten vier Werke als unerreichbar, und alle vier lagen bei genauerem Suchen im Volltext vor — Fehlerquote der Vermutung vier von vier. Fall in `prima-materia#76`, vollständig in `SPEC.md` Abschnitt 15 und in `AGENTS.md`.

### Ist das Werk offen, wird geerntet

Ein Werk, das für eine Behauptung geöffnet wurde, wird nicht für diese eine wieder geschlossen. Das Öffnen ist der teure Schritt; eine weitere Stelle im offenen Text kostet fast nichts.

**Das ist eine ausdrückliche Ausnahme von der Issue-Bindung.** Die Ernte braucht kein eigenes Issue vorher und gilt nicht als eigenmächtige Scope-Erweiterung. Ohne diese Ausnahme wirft ein regeltreuer Bearbeiter gesehenes Wissen weg.

Geschuldet, nicht wahlfrei:

- **Vermögen** — was als durch Übung erlangbar behauptet wird. Vollständigkeit hier im strengen Sinn: ein übergangenes Vermögen ist etwas zu Lernendes, das niemandem mehr auffällt.
- **Voraussetzungsketten** — was vorher da sein muss, damit etwas eintreten kann. Der Teil, den Zusammenfassungen zuerst verlieren.
- **Warnungen und Kautelen** — besonders solche, die ihre eigene Verkennung mitnennen, und Selbstwarnungen eines Textes gegen das, was er vorschreibt.
- **Prüfbares** — Anzeichen, Kriterien, Fristen, Misslingensbedingungen, aus denen später ein `pm:falsifiedBy` wird.

Erzählung, Lebenslauf und Polemik nach Ermessen, nur soweit sie eines der vier tragen.

**Vollständig heißt vollständig für das Geöffnete.** Fünf gelesene Passagen sind nicht das Werk. Die Erntenotiz im auslösenden Issue nennt: was aufgenommen wurde, welche Teile ungelesen blieben, und was gesehen und bewusst nicht aufgenommen wurde, mit Grund — gesehen und stillschweigend fallengelassen ist von nie gesehen nicht zu unterscheiden.

**Kein Maßstab sinkt.** Jede geerntete Behauptung braucht ihre eigene Stelle in derselben Ausgabe; gesehen, aber nicht lokalisiert gehört ins Issue. Neue Traditionen und neues Vokabular bleiben Entscheidungen nach `SPEC.md` §11 und §14. Und wächst der Bestand an Behauptungen über mehrere Läufe, ohne dass `pm:Testing` und `pm:Disputing` mitwachsen, ist aus der Prüfontologie eine Zitatsammlung geworden — das ist ein Befund und keine Nebensache.

**Gegroundet** heißt: eine Stelle trägt die Behauptung, und die Gegensuche ist gelaufen. **Unbelegt** ist die teure Aussage und trägt nur eine erschöpfende, dokumentierte Suche; ein Durchgang ohne Fund reicht nicht.

## Wozu

Lies das vor allem anderen. Es entscheidet, was aufzunehmen sich lohnt, und ohne diesen Abschnitt arbeitet ein Agent korrekt an der falschen Sache.

**prima-materia ist eine Prüfstelle, keine Sammlung.** Eine Behauptung über ein magisches oder kontemplatives Vermögen wird aufgenommen, von ihrer Beglaubigung getrennt, und beide werden getrennt gehalten, damit sichtbar bleibt, worauf sie steht: auf einem überlieferten Text, auf einem modernen Bearbeiter, oder auf nichts. Aus dem geprüften Bestand entsteht das eigentliche Werk: eine Karte, die durch Überlagerung der alten Traditionen zeigt, wo sie sich decken, wo sie sich widersprechen und was tatsächlich Wirkung erzielt, die sich messen lässt.

**Das Ziel dahinter.** Magie in ihren Konzepten verstehen und lehren können. Auf dem Weg dorthin die eigenen menschlichen und übermenschlichen Vermögen aktivieren oder zurückgewinnen. Und die Ergebnisse frei teilen, damit andere zu ihrem vollen Potenzial finden. CC0 ist deshalb keine Lizenzwahl, sondern die Maßnahme: magisches Wissen war dreitausend Jahre durch Initiation, Linie, Geheimhaltung und Zahlung verschlossen, und dieser Verschluss entscheidet über Entfaltung nach Zugehörigkeit statt nach Vermögen.

**Das Kriterium für jede Recherche, jede Fragestellung, jeden Eintrag:**

> **Wertvoll ist, was ein Tor beseitigt.**

Bezeugt gegen erschlossen beseitigt das Tor der Autorität. Die Voraussetzungsketten beseitigen das Tor der zurückgehaltenen Reihenfolge. Die Prüfung beseitigt das Tor der unwiderlegbaren Behauptung. Die Konvergenz beseitigt das Tor der Linienzugehörigkeit.

Drei operative Folgen, die laufend Entscheidungen tragen:

**Der wertvollste Knoten ist nicht der gebrauchte, sondern der anderswo am zuverlässigsten falsch berichtete.** Unter CC0 und mit Auslieferung an Sprachmodelle propagieren nicht die Inhalte, sondern die Unterscheidungen. Ein Knoten, der eine moderne Konstruktion als moderne kenntlich macht, ist mehr wert als zehn korrekt abgeschriebene Stellen.

**`pm:Converging`, `pm:Disputing` und `pm:Testing` tragen das Ziel; alles andere ist Substrat für sie.** Überdeckung, Widerspruch, Wirkung sind wörtlich die drei Fragen. Wo diese drei Schichten dünner sind als die Traditionsdateien, arbeitet der Bestand an seinem Unterbau statt an seinem Zweck.

**Eine Recherche fragt nicht nur, was eine Tradition sagt.** Sie fragt, wo zwei dasselbe sagen ohne belegten Kontaktweg, wo sie einander widersprechen, und wo sich etwas messen lässt.

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
- ❌ **Sekundäre Zusammenfassungen** anstelle der Stelle, die sie zusammenfassen — außer im Fall direkt unten.

### Unerreichbares Werk: die Stelle aus zweiter Hand, aber sichtbar

Das Original hat Vorrang und behält ihn. Ist das Werk nicht zu beschaffen — nicht digitalisiert, vergriffen, ordensintern, Sprache nicht beherrscht —, darf die Stelle über ein Werk zitiert werden, das sie wiedergibt, **wenn die Vermittlung im Graphen steht**:

```turtle
pmc:SomeClaim a pm:Attributing ;
    pm:attestedBy pm:mediatedAttestation ;
    pm:readVia "Editor, Study (Jahr), wo die Stelle zitiert wird" ;
    dcterms:source "Das Werk, das die Behauptung trägt, mit der Stelle" .
```

`dcterms:source` nennt weiterhin das Werk, das ein Leser beschaffen muss; `pm:readVia` nennt, was der Schreibende vor sich hatte. Die beiden nicht zusammenziehen — der Unterschied ist der ganze Punkt, weil eine Stelle aus zweiter Hand die Auswahl, die Übersetzung und das Schweigen des Vermittlers mitträgt. `pm:MediatedAttestationShape` weist ab, wer den Modus setzt und den Vermittler verschweigt; `pm:ReadViaIsLiteratureShape` weist URLs ab.

**Der Modus hängt an der Unerreichbarkeit, nicht am Aufwand.** Was sich herunterladen und durchsuchen lässt, wird aufgeschlagen (siehe oben, zweite Recherchestufe). Ein vermittelter Knoten ist ein offener Posten: sobald das Exemplar vorliegt, wird nachgeprüft und der Modus auf `pm:textualAttestation` gehoben; das Issue bleibt bis dahin offen und nennt, welches Exemplar fehlt.

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
| „Praktiken dieser Art bringen diese Wirkung hervor" — aus mehreren bezeugten Behauptungen gebildet, von keiner Quelle gesagt | `pm:Generalizing` | `pm:generalizedStatement`, **zwei** `pm:generalizedFrom`, `pm:attestedBy pm:compilerInference`; **kein** `dcterms:source`, **keine** `pm:withinTradition` |

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

**Der Korpus wächst über zwei Eingänge, und der zweite hat Vorrang.** Bedarf aus offenen Issues ist der eine. Der andere ist der Engpass: die Beweiskraft hängt an `pm:independentAttestation`, und eine weitere indische Datei erhöht die Dateizahl, nicht die Zeugenzahl. Vor jeder neuen Datei stehen Kontaktweg, Rezension und die Zahl der zitierbaren Stellen fest. `traditions/daoist.ttl` ist mit Absicht dünn und ist das Modell.

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

**Ein neuer Datenordner muss an vier Stellen nachgezogen werden**, sonst wird er still nicht kompiliert und nicht validiert: `DEFAULT_INPUTS` in `scripts/compile.py`, `DEFAULT_INPUTS` in `scripts/publish.py`, `DEFAULT_DATA_DIRS` in `scripts/validate.py`, `SCAN_DIRS` in `tests/test_no_substance_classes.py`. Nichts schlägt fehl, wenn eine davon vergessen wird; die Dateien erscheinen einfach nicht.

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
