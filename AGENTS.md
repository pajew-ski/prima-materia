# AGENTS.md

Anweisungen für jeden Agenten an diesem Repository, unabhängig vom Anbieter. Vollständige Spezifikation in `SPEC.md`; bei Konflikten gilt `SPEC.md`. `CLAUDE.md` enthält zusätzlich die Werkzeug- und Konventionsdetails für Claude Code.

## Was dieses Repo ist

**prima-materia ist eine Prüfstelle, keine Sammlung.** Eine Behauptung über ein magisches oder kontemplatives Vermögen wird aufgenommen, von ihrer Beglaubigung getrennt, und beide werden getrennt gehalten, damit sichtbar bleibt, worauf sie steht: auf einem überlieferten Text, auf einem modernen Bearbeiter, oder auf nichts.

Das Kriterium für jede Recherche, jede Fragestellung, jeden Eintrag:

> **Wertvoll ist, was ein Tor beseitigt.**

Der wertvollste Knoten ist nicht der gebrauchte, sondern der anderswo am zuverlässigsten falsch berichtete.

## Die Recherche-Regel

Diese vier Sätze sind der Kern der Arbeit. Wer sie verletzt, produziert Etiketten statt Befunde.

**1. Der Suchraum ist alles über das Internet erreichbare Wissen, nicht der Bestand.**

Der Bestand ist spärlich und wird es bleiben. Er ist rückwärts aus einem einzigen Methodenentwurf gewachsen: jede Datei existiert, weil sie etwas beantwortet, was ein moderner Text behauptet. Ihn als Prüfmaßstab zu nehmen misst nicht die Behauptung, sondern die bisherige Sammelrichtung. Ein vorhandener Knoten belegt nichts — er ist selbst nur eine früher eingetragene Behauptung mit Herkunft.

**2. Die erste Frage lautet: wo gibt es Quellen zu dieser Behauptung, die noch nicht im Bestand sind?**

Nicht: was sagt der Bestand dazu. Wer mit der zweiten Frage beginnt, hat den Ausgang der ersten vorweggenommen. Der Bestand liefert Hinweise, wo zu suchen wäre, und sonst nichts.

**3. Jede Recherche sucht die Behauptung und ihre Negation.**

Wer nur nach Bestätigung sucht, findet sie. Gesucht wird auch dort, wo das Gegenteil stehen könnte, und in Überlieferungen außerhalb der Sphäre, in der die Behauptung vermutet wird. `pm:Converging` und `pm:Disputing` entstehen nur so.

**4. Eine Recherche ist kein paar Suchanfragen nebenbei.**

Mindestumfang: der Fachterm in Originalsprache und gebräuchlichen Transliterationen; der Primärtext, mindestens zwei Übersetzungen und die Sekundärliteratur zur Stelle; die Datierung des frühesten Zeugen und die Frage, ob die Zuschreibung bestritten ist; die Gegensuche; mindestens eine Überlieferung außerhalb der erwarteten Sphäre.

## Die Recherche hat zwei Stufen, und beide sind zu führen

Diese Trennung ist keine Verfeinerung der vier Sätze oben, sondern die Bedingung, unter der sie überhaupt einzuhalten sind.

**Erste Stufe: die Landschaft.** Ein breiter Rechercheauftrag über den gesamten erreichbaren Suchraum, geführt mit dem Werkzeug, das viele Suchen parallel fährt. Er beantwortet die erste Frage aus Satz 2 — wo gibt es Quellen, die der Bestand nicht kennt —, findet die Sekundärliteratur für die Gegensuche, liefert Datierungen und Zuschreibungsstreit, und nennt Korpora, auf die man von selbst nicht käme. Ohne diese Stufe recherchiert der Agent dort, wo er ohnehin schon hinsah, und bestätigt die bisherige Sammelrichtung.

Der Auftrag an diese Stufe enthält: jede Behauptung einzeln und entscheidbar formuliert; die Pflicht zur Gegensuche je Behauptung; die Fachtermini in Originalsprache und Transliteration; die Frage nach Datierung und bestrittener Zuschreibung; die Pflicht, mindestens für einen Teil der Behauptungen eine Überlieferung außerhalb der erwarteten Sphäre zu befragen und für jede Übereinstimmung den Kontaktweg zu prüfen; und die Regel, dass Belege Werke mit Stellenangabe sind und niemals Links.

**Zweite Stufe: die Stelle.** Was die erste Stufe nennt, wird selbst aufgeschlagen, im Original, bevor daraus ein Knoten wird. Ein Bericht über eine Stelle ist keine Stelle. Ein Rechercheergebnis, das eine Stelle referiert, fällt unter dieselbe Regel wie jede andere sekundäre Zusammenfassung: es weist den Weg zum Werk und zählt nicht als Beleg.

**Die Aufteilung sagt, wohin ein Ergebnis gehört. Sie sagt nicht, ob die zweite Stufe geführt wird:**

| | |
|---|---|
| **In den Graphen** | nur, was die zweite Stufe überstanden hat: Stellen, deren Wortlaut gelesen wurde |
| **Ins Issue** | was die zweite Stufe **nicht überstanden hat**, ausdrücklich als nicht am Wortlaut geprüft gekennzeichnet, mit Werk und vermuteter Stelle, damit die nächste Runde dort ansetzt |

**Die zweite Stufe ist Pflicht und steht nicht zur Wahl.** Sie wird für jede Behauptung geführt, deren Werk erreichbar ist, und zwar in demselben Lauf. Ein Lauf, der die erste Stufe führt und die zweite auslässt, hat den Auftrag nicht erfüllt — auch dann nicht, wenn am Ende saubere Issues stehen. Die Zeile „ins Issue" ist der Ort für **gescheiterte** Prüfungen, nie für **unterlassene**. Wer sie für unterlassene benutzt, hat aus einer Schranke eine Erlaubnis gemacht.

**Erreichbar heißt erreichbar, nicht bequem.** Ein gemeinfreies Werk in einem Volltextarchiv ist erreichbar. Ein Band, dessen Volltext sich herunterladen und durchsuchen lässt, ist erreichbar, auch wenn er tausend Seiten hat. Umfang, Aufwand und die Schätzung, das brauche einen eigenen Lauf, sind keine Gründe — sie sind die Arbeit. Eine solche Schätzung ist außerdem fast immer falsch, weil sie vor dem Aufschlagen gemacht wird.

**Bleibt eine Prüfung aus, steht der Grund im Issue, und er ist eine Eigenschaft des Werkes:** nicht digitalisiert, urheberrechtlich gesperrt, ordensintern, nur als Druckausgabe vorhanden, Sprache nicht beherrscht. Fehlt der Grund, gilt die Prüfung als unterlassen und der Lauf als unvollständig.

Drei Fehler, alle gleich aussehend. Wer die erste Stufe für die ganze Recherche hält, trägt Referate als Belege ein. Wer sie überspringt, findet nur, was er schon kannte. Wer sie führt und dann aufhört, wirft sie weg: die erste Stufe erzeugt keine Befunde, sondern Adressen, und eine Adresse, an die niemand geht, ist nichts. Alle drei fallen erst auf, wenn jemand die Stelle aufschlägt. Ein dokumentierter Fall des dritten steht in prima-materia#76, mit drei Befunden, die beim Nachholen entstanden und von denen zwei den Issues widersprachen, die statt ihrer angelegt worden waren.

## Der stehende Auftrag

Eine Sitzung, die mit „prima materia weiter" oder Gleichwertigem beginnt, ist vollständig und autonom zu durchlaufen: Bestand lesen, Bündel nach `korpus:`-Label wählen, beide Recherchestufen führen, das Ergebnis sofort eintragen, alle dabei entstandenen Hypothesen und Nebenfunde noch im selben Lauf als Issues anlegen, PR öffnen, ohne Unterbrechung zum nächsten Bündel.

Keine Rückfragen zu Schritten, die `SPEC.md` und dieses Dokument bereits vorschreiben. Geprüft wird am Merge, nicht am Ablauf.

**Anlegen statt ankündigen.** Ein Satz der Form „das sollte noch ein Issue werden" ist bereits die Arbeit, die stattdessen zu tun war. Vollständigkeit geht vor Eleganz: lieber fünfzig knappe Issues als fünf ausformulierte und der Rest im Fließtext.

**Die Prüfung liegt vor dem PR, nicht danach.** `validate.yml` hört seit #32 auch auf `push` nach `claude/**`. Auf einem Arbeitsbranch entsteht damit ein echter Lauf, bevor ein PR offen ist: schreiben, `prima_repo_check` auf denselben Branch, und erst bei `gruen` den PR öffnen. Der frühere Vermerk an dieser Stelle — der Lauf entstehe erst mit dem PR, also PR zuerst — ist überholt und war der Grund, warum Fehler in TTL-Dateien vorher erst am offenen PR auffielen.

Zwei Dinge, die dabei aussehen wie ein Fehler und keiner sind. Eine `concurrency`-Gruppe mit `cancel-in-progress` bricht die Läufe überholter Zwischenstände ab, ein Branch mit vielen Commits sammelt also planmäßig `cancelled`-Läufe. Und `prima_repo_check` wertet seit #44 ausschließlich den Lauf des aktuellen Kopf-SHA; abgebrochene Läufe zählen in keinem Fall als Fehlschlag, ältere Läufe erscheinen nur noch als Zahl. Wer stattdessen die Lauf-Liste im Actions-Reiter überfliegt, sieht rote Kreuze, die nichts bedeuten.

**5. Beifang wird geerntet, aber nicht auf demselben Weg.**

Eine Recherche findet mehr, als die Frage verlangt, und dieser Beifang ist der Weg, auf dem der Bestand in die Breite wächst. Er darf den Maßstab aber nicht senken. Deshalb: ein nebenbei gefundener Befund wird nur dann Knoten, wenn er **selbst** die volle Prüfung durchlaufen hat — Stelle plus Gegensuche. Alles andere wird ein Issue mit `korpus:`-Label und den bereits geprüften Kandidatenstellen.

Der Unterschied ist keine Förmlichkeit. Ein im Vorbeigehen aufgesammelter Fund ist nicht geprüft, sondern begegnet. Läuft er als Knoten ein, ist der Bestand wieder eine Sammlung, und die Trennung von Behauptung und Beglaubigung, die dieses Repo ausmacht, ist an der billigsten Stelle durchbrochen.

Der Ertrag der Regel liegt beim Beifang, der schon im Bericht mit Vorbehalt kommt: Seitenzahlen aus Sekundärliteratur, gemeinfreie Altübersetzungen statt kritischer Ausgaben, bestrittene Zuschreibungen. Genau das wird Issue und nicht Knoten.

## Was „gegroundet" heißt und was nicht

| | |
|---|---|
| **Gegroundet** | Eine Stelle in einem Werk trägt die Behauptung, **und** die Gegensuche ist gelaufen. Die Stelle entscheidet den positiven Befund, sobald sie steht; die Erschöpfung des Suchraums ist dafür nicht Bedingung. |
| **Unbelegt** | Die teure Aussage: es gibt die Stelle nirgends. Trägt nur eine erschöpfende, dokumentierte Suche. Ein Durchgang ohne Fund reicht nicht. |
| **Nicht gegroundet** | Ein Knoten im Bestand. Eine Analogie in einer benachbarten Tradition. Eine Erinnerung des Modells an eine Stelle, die nicht aufgeschlagen wurde. |

## Behauptungen liegen in Issues

Der Issue-Tracker hält jede Behauptung, die noch nicht durch einen Knoten repräsentiert ist. Jeder darf einreichen, ohne Recherche und ohne in einer Tradition zu stehen; das beseitigt dasselbe Tor wie CC0.

- Ein Issue lebt genau so lange, wie kein Knoten die Behauptung trägt.
- Die Issue-Nummer ist die Identität der Behauptung. Kein zweites Nummernschema.
- Recherchiert wird nach `korpus:`-Label gebündelt: die Arbeit folgt dem Text, den man aufschlägt, nicht dem Abschnitt, aus dem die Behauptung stammt.
- Die `korpus:`-Labels kumulieren und sind der Nachweis der Suchabdeckung. „In diesem Korpus nicht gefunden" ist etwas anderes als „unbelegbar".
- Was eine Recherche ergeben hat, steht im Issue: geprüfte Korpora, verwendete Suchbegriffe samt Transliterationen, gefundene Stellen, Datum.

Vokabular der Labels in `CONTRIBUTING.md`, von dort übernehmen: GitHub legt einen unbekannten Labelnamen stillschweigend als neues an.

## Quellen

Jede Behauptung braucht mindestens ein `dcterms:source` als Referenz auf ein Werk mit der Stelle, die sie trägt (`"Patañjali, Yogasūtra III.38"`).

Nicht zulässig: URLs jeder Art, DOI und Open-Access-Editionen eingeschlossen (`pm:SourceIsLiteratureShape` weist sie ab); Videos, Blogs, Wikipedia, Foren als Beleg (als Einstieg brauchbar, dann bis zum Werk zurückverfolgen); unveröffentlichte eigene Texte und Methodenentwürfe; sekundäre Zusammenfassungen anstelle der Stelle, außer im Fall des nächsten Absatzes.

**Wenn das Werk nicht zu beschaffen ist, darf die Stelle aus zweiter Hand kommen — sichtbar.** Der Knoten trägt `pm:attestedBy pm:mediatedAttestation` und nennt mit `pm:readVia` das Werk, in dem gelesen wurde; `dcterms:source` nennt weiter das Werk, das die Behauptung trägt. `pm:MediatedAttestationShape` weist ab, wer den Modus setzt und den Vermittler verschweigt.

Der Modus hängt an der Unerreichbarkeit und nicht am Aufwand. Nicht digitalisiert, vergriffen, ordensintern, Sprache nicht beherrscht: ja. Umfangreich, unbequem, „wäre ein eigener Lauf": nein — was sich herunterladen und durchsuchen lässt, wird aufgeschlagen. Ein vermittelter Knoten ist ein offener Posten: sobald das Exemplar da ist, wird die Stelle nachgeprüft und der Modus gehoben, und das Issue bleibt bis dahin offen. Vollständig in `SPEC.md` §10.

Moderne Forschung betritt den Bestand ausschließlich über `pm:evidenceFrom` an einem `pm:Testing`-Knoten, nie als `dcterms:source` einer Tradition. Ein Aufsatz ist kein Zeuge einer Überlieferung.

## Der stehende Auftrag

Beginnt eine Sitzung mit „prima materia weiter" oder einer gleichwertigen Aufforderung, ist der vollständige Durchlauf gemeint. **Keine Rückfragen zu Schritten, die diese Datei und `SPEC.md` bereits vorschreiben.** Der Mensch prüft am Merge, nicht am Ablauf.

1. Bestand lesen: Dateibaum, offene Issues, Labels, letzte PRs.
2. Nächstes Bündel wählen. Vorrang hat der unabhängigkeitsgetriebene Eingang (SPEC §14) vor dem Bedarf aus offenen Issues; innerhalb dessen der Knoten, der anderswo am zuverlässigsten falsch berichtet wird.
3. Tiefe Recherche nach SPEC §15, **beide Stufen**, mit Gegensuche. Der Schritt ist erst beendet, wenn jede Behauptung mit erreichbarem Werk am Wortlaut geprüft ist.
4. Sofort integrieren: Knoten für vollgeprüfte Funde, Issues für alles andere.
5. Issue-Kommentar mit der Abdeckung, `korpus:`-Labels kumulieren, Schließen nur bei Erschöpfung.
6. PR öffnen, Validierung grün, dann liegen lassen. Der Mensch merged.
7. Ohne Unterbrechung zum nächsten Bündel.

**Jede im Lauf entstandene Hypothese wird noch im selben Lauf ein Issue.** Das gilt für den Zielbefund, für den Beifang, für jede Vermutung, die im Denken auftaucht, und für jeden Befund über das Repo oder die Werkzeuge. Eine Hypothese, die nur im Gesprächsverlauf steht, ist verloren, sobald die Sitzung endet — und der Gesprächsverlauf ist kein Speicher, sondern ein Fenster.

**Anlegen statt ankündigen.** Ein Satz der Form „das sollte noch ein Issue werden" ist bereits die Arbeit, die stattdessen zu tun war. Wer ihn schreibt, hat den Aufwand des Anlegens schon aufgewendet und das Ergebnis weggeworfen.

**Vollständigkeit vor Eleganz.** Lieber fünfzig knappe Issues mit Behauptung, geprüften Stellen und Labels als fünf ausformulierte und der Rest im Fließtext.

## Vor dem ersten Schreibzugriff

1. `SPEC.md` vollständig lesen. Bei mehrdeutiger Spezifikation fragen, nicht raten.
2. Prüfen, ob eine Datei fehlt, die diese Anweisungen voraussetzen. Fehlt sie, ist das zu melden und nicht stillschweigend zu übergehen.
3. Lokal `python scripts/validate.py && pytest tests/` grün, dann PR. Der Mensch merged.
4. Löst eine Validierung aus, wird sie gemeldet, nicht umformuliert. Ein Fehlalarm ist ein Befund über den Wächter.
