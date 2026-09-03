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

Neuer Code bekommt Tests, TDD bevorzugt. Commits klein und atomar, Messages im Imperativ.

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
