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

**Rezeption ist dabei kein Ausschlussgrund.** Ein belegter Übertragungsweg wertet eine Übereinstimmung nicht ab, er verbietet nur, dieselbe Aussage zweimal als Zeugen zu zählen. Wie viele Überlieferungen etwas tragen und wie tief die Wege verzweigen, sind zwei Zahlen, und beide gehören in den Bestand. Zu suchen ist deshalb auch, was eine spätere Station der übernommenen Behauptung *hinzugefügt* hat — eine Frist, eine Kautel, ein Anzeichen, eine Misslingensbedingung. Das ist der Unterschied zwischen einer Kopierkette und einer Versuchsreihe, es trägt `pm:Reworking`, und es ist das Material, aus dem ein `pm:falsifiedBy` entsteht. Wer `pm:independentAttestation` setzt, schuldet `pm:independenceGround`: wann die tragende Bezeugung fixiert oder erhoben wurde und gegen welche Publikation oder Route dieses Datum steht.

**4. Eine Recherche ist kein paar Suchanfragen nebenbei.**

Mindestumfang: der Fachterm in Originalsprache und gebräuchlichen Transliterationen; der Primärtext, mindestens zwei Übersetzungen und die Sekundärliteratur zur Stelle; die Datierung des frühesten Zeugen und die Frage, ob die Zuschreibung bestritten ist; die Gegensuche; mindestens eine Überlieferung außerhalb der erwarteten Sphäre.

**5. Beifang wird geerntet, aber nicht auf demselben Weg.**

Eine Recherche findet mehr, als die Frage verlangt, und dieser Beifang ist der Weg, auf dem der Bestand in die Breite wächst. Er darf den Maßstab aber nicht senken. Deshalb: ein nebenbei gefundener Befund wird nur dann Knoten, wenn er **selbst** die volle Prüfung durchlaufen hat — Stelle plus Gegensuche. Alles andere wird ein Issue mit `korpus:`-Label und den bereits geprüften Kandidatenstellen.

Der Unterschied ist keine Förmlichkeit. Ein im Vorbeigehen aufgesammelter Fund ist nicht geprüft, sondern begegnet. Läuft er als Knoten ein, ist der Bestand wieder eine Sammlung, und die Trennung von Behauptung und Beglaubigung, die dieses Repo ausmacht, ist an der billigsten Stelle durchbrochen.

Der Ertrag der Regel liegt beim Beifang, der schon im Bericht mit Vorbehalt kommt: Seitenzahlen aus Sekundärliteratur, gemeinfreie Altübersetzungen statt kritischer Ausgaben, bestrittene Zuschreibungen. Genau das wird Issue und nicht Knoten.

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

**Im ersten Anlauf nicht gefunden ist kein solcher Grund**, sondern eine Aussage über den Anlauf. Vor der Feststellung der Unerreichbarkeit werden die Wege abgearbeitet, die es gibt: eine andere Kennung desselben Werkes im selben Archiv, eine andere oder ältere Ausgabe, eine andere Umschrift von Titel und Autor, das Werk innerhalb einer Sammlung oder eines es abdruckenden Kommentars, ein anderes Digitalisierungsvorhaben. Eine Sperre am Zugangsweg — etwa eine Abwehr gegen automatisierte Abrufe — hängt nicht am Werk und verlangt einen anderen Weg, keinen Verzicht. Was davon versucht wurde, steht im Issue.

Der Anlass ist gezählt: in einem Lauf wurden vier Werke als unerreichbar geführt, und alle vier lagen bei genauerem Suchen als Volltext vor. Vollständig in `SPEC.md` §15, Fall in prima-materia#76.

**Ist das Werk offen, wird geerntet, bevor es geschlossen wird.** Nicht nur die Behauptung, für die geöffnet wurde. Ausdrückliche Ausnahme von der Issue-Bindung: die Ernte braucht kein eigenes Issue vorher und gilt nicht als Scope-Erweiterung. Geschuldet sind vier Arten — **Vermögen** (hier Vollständigkeit im strengen Sinn), **Voraussetzungsketten**, **Warnungen** samt Selbstwarnungen eines Textes gegen das, was er vorschreibt, und **Prüfbares**, aus dem sich ein `pm:falsifiedBy` formen lässt. Erzählung und Polemik nur, soweit sie eines der vier tragen.

Vollständig heißt vollständig für das Geöffnete: die Erntenotiz im auslösenden Issue nennt, was aufgenommen wurde, welche Teile ungelesen blieben, und was gesehen und bewusst nicht aufgenommen wurde. Die aufgenommene Seite steht dabei namentlich, mit den Bezeichnern der geschriebenen Knoten, und wird aus der Lektüre geschrieben statt aus der fertigen Datei abgeschrieben — sonst stimmt sie per Konstruktion und prüft nichts. So ist eine Auslassung die Differenz zwischen Notiz und Branch und damit zählbar. Jede geerntete Behauptung braucht ihre eigene Stelle; neue Traditionen und neues Vokabular bleiben Entscheidungen nach §11 und §14. Verfahren in `SPEC.md` §15.

Drei Fehler, alle gleich aussehend. Wer die erste Stufe für die ganze Recherche hält, trägt Referate als Belege ein. Wer sie überspringt, findet nur, was er schon kannte. Wer sie führt und dann aufhört, wirft sie weg: die erste Stufe erzeugt keine Befunde, sondern Adressen, und eine Adresse, an die niemand geht, ist nichts. Alle drei fallen erst auf, wenn jemand die Stelle aufschlägt. Ein dokumentierter Fall des dritten steht in prima-materia#76, mit drei Befunden, die beim Nachholen entstanden und von denen zwei den Issues widersprachen, die statt ihrer angelegt worden waren.

## Prüfung, Läufe und der Abgleich vor dem PR

Der stehende Auftrag selbst steht weiter unten, in einem eigenen Abschnitt. Hier steht, was zwischen dem letzten Schreibvorgang eines Bündels und dem PR zu geschehen hat.

**Die Prüfung liegt vor dem PR, nicht danach.** `validate.yml` hört seit #32 auch auf `push` nach `claude/**`. Auf einem Arbeitsbranch entsteht damit ein echter Lauf, bevor ein PR offen ist: schreiben, `prima_repo_check` auf denselben Branch, und erst bei `gruen` den PR öffnen. Der frühere Vermerk an dieser Stelle — der Lauf entstehe erst mit dem PR, also PR zuerst — ist überholt und war der Grund, warum Fehler in TTL-Dateien vorher erst am offenen PR auffielen.

Drei Dinge, die dabei aussehen wie ein Fehler und keiner sind. Eine `concurrency`-Gruppe mit `cancel-in-progress` bricht die Läufe überholter Zwischenstände ab, ein Branch mit vielen Commits sammelt also planmäßig `cancelled`-Läufe. Und `prima_repo_check` wertet seit #44 ausschließlich den Lauf des aktuellen Kopf-SHA; abgebrochene Läufe zählen in keinem Fall als Fehlschlag, ältere Läufe erscheinen nur noch als Zahl. Wer stattdessen die Lauf-Liste im Actions-Reiter überfliegt, sieht rote Kreuze, die nichts bedeuten.

Das dritte ist neu und steht nicht im Actions-Reiter, sondern am PR: **bei gestapelten Branches trägt ein grüner PR ein rotes Kreuz, weil vom nächsten Branch abgezweigt wurde.** Das Anlegen eines Refs ist ein Push und startet einen Lauf auf dem geerbten Kopf-SHA; der erste echte Commit auf dem neuen Branch bricht ihn ab, und GitHub rollt alle Check-Runs eines SHA am PR zusammen, gleich von welchem Ref sie stammen. Das Kreuz markiert also nicht den defekten PR, sondern den, auf dem der nächste aufsitzt. `prima_repo_check` meldet in diesem Fall grün und hat recht. Behoben durch prima-materia#352: `validate.yml` läuft nicht mehr, wenn der Push den Ref erst erzeugt. Der Absatz bleibt stehen, weil das Muster in älteren PR sichtbar bleibt und weil ein `cancelled`-Lauf aus anderem Anlass dieselbe Anzeige erzeugt.

**Ein Bündel ist nicht fertig, solange der Klon und der Branch auseinandergehen.** Der Arbeitsweg hat zwei Schreibziele: der lokale Klon dient dazu, `python scripts/validate.py` und `pytest tests/` vor dem Schreiben laufen zu lassen, geschrieben wird aber über `prima_repo_write` auf den Branch. Zwischen beiden gibt es keinen automatischen Abgleich, und eine Änderung, die nach dem letzten Übertragen noch lokal entsteht, fällt lautlos heraus. SHACL, Tests und `prima_repo_check` bemerken das nicht: alle drei prüfen, was auf dem Branch steht, und dort steht sie ja gerade nicht. Das ist die schlimmste Fehlerklasse dieses Repos, weil ein fehlender Knoten von einer nie gelaufenen Recherche nicht zu unterscheiden ist, und sie ist eingetreten (prima-materia#351).

Die Regel dagegen ist keine Prüfung, sondern ein Schritt: **der Branch ist die Quelle, der Klon das Abbild.** Am Ende jedes Bündels, vor dem PR, `git fetch` und dann jede Datei, die im Arbeitsbaum vom Branch abweicht, per `prima_repo_write` schreiben. Damit ist die Übertragung der Diff und kein Urteil mehr, und ein Vergessen hat keinen Ort. Die Abschlussbedingung ist prüfbar: `git status --porcelain` und `git diff origin/<branch>` müssen beide leer sein. Sind sie es nicht, ist das Bündel offen, unabhängig davon, was der Prüflauf sagt.

Ein ungültiger Zwischenstand auf einem `claude/`-Branch ist dabei kein Schaden — dafür ist der Branch da, und die `concurrency`-Gruppe fängt die überholten Läufe ab. Ein unbemerkter Verlust ist einer.

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

**Jedes Issue trägt entweder `behauptung` oder `befund`.** Ein Befund über das Repo, die Ontologie, ein Werkzeug oder ein Verfahren ist keine Behauptung und bekommt kein `korpus:`-Label; er bekommt `befund` und dazu die zutreffenden Verfeinerungen `befund:werkzeug`, `befund:ontologie`, `befund:bestand`, `befund:verfahren`, die kumulieren. `is:issue is:open no:label` muss leer bleiben.

## Quellen

Jede Behauptung braucht mindestens ein `dcterms:source` als Referenz auf ein Werk mit der Stelle, die sie trägt (`"Patañjali, Yogasūtra III.38"`).

Nicht zulässig: URLs jeder Art, DOI und Open-Access-Editionen eingeschlossen (`pm:SourceIsLiteratureShape` weist sie ab); Videos, Blogs, Wikipedia, Foren als Beleg (als Einstieg brauchbar, dann bis zum Werk zurückverfolgen); unveröffentlichte eigene Texte und Methodenentwürfe; sekundäre Zusammenfassungen anstelle der Stelle, außer im Fall des nächsten Absatzes.

**Wenn das Werk nicht zu beschaffen ist, darf die Stelle aus zweiter Hand kommen — sichtbar.** Der Knoten trägt `pm:attestedBy pm:mediatedAttestation` und nennt mit `pm:readVia` das Werk, in dem gelesen wurde; `dcterms:source` nennt weiter das Werk, das die Behauptung trägt. `pm:MediatedAttestationShape` weist ab, wer den Modus setzt und den Vermittler verschweigt.

Der Modus hängt an der Unerreichbarkeit und nicht am Aufwand. Nicht digitalisiert, vergriffen, ordensintern, Sprache nicht beherrscht: ja. Umfangreich, unbequem, „wäre ein eigener Lauf": nein — was sich herunterladen und durchsuchen lässt, wird aufgeschlagen. Ein vermittelter Knoten ist ein offener Posten: sobald das Exemplar da ist, wird die Stelle nachgeprüft und der Modus gehoben, und das Issue bleibt bis dahin offen. Vollständig in `SPEC.md` §10.

Moderne Forschung betritt den Bestand ausschließlich über `pm:evidenceFrom` an einem `pm:Testing`-Knoten, nie als `dcterms:source` einer Tradition. Ein Aufsatz ist kein Zeuge einer Überlieferung.

## Der stehende Auftrag

Beginnt eine Sitzung mit „prima materia weiter" oder einer gleichwertigen Aufforderung, ist der vollständige Durchlauf gemeint. **Keine Rückfragen zu Schritten, die diese Datei und `SPEC.md` bereits vorschreiben.** Der Mensch prüft am Merge, nicht am Ablauf.

1. Bestand lesen: Dateibaum, offene Issues, Labels, letzte PRs.
2. Nächstes Bündel wählen. Vorrang hat der prüfbarkeitsgetriebene Eingang (SPEC §14) — die Überlieferungen, die Anzeichen, Fristen, Kautelen und Misslingensbedingungen nennen —, dann der unabhängigkeitsgetriebene, dann der Bedarf aus offenen Issues; innerhalb dessen der Knoten, der anderswo am zuverlässigsten falsch berichtet wird.

   **Dazu ein zweiter Strang, der keiner Frage folgt.** Neben dem Bündel aus offenen Behauptungen zieht jeder Lauf ein Werk aus dem Registrierungsstand: eine Tradition auf `pm:coverageState pm:corpusNamed`, deren Bestand dünn ist. Dieser Strang ist nicht nachrangig, sondern der einzige, der Behauptungen erzeugt, nach denen niemand gefragt hat — und nur solche können eine Kategorie liefern, die vorher niemand hatte. Was mit einer Frage gesucht wird, findet Übereinstimmungen, deren Begriff schon im Suchbegriff steckte. Die beiden Stränge laufen im Batch nebeneinander, in eigenen Branches, und keiner ersetzt den anderen.
3. Tiefe Recherche nach SPEC §15, **beide Stufen**, mit Gegensuche. Der Schritt ist erst beendet, wenn jede Behauptung mit erreichbarem Werk am Wortlaut geprüft ist.
4. Sofort integrieren: Knoten für vollgeprüfte Funde, Issues für alles andere.
5. Issue-Kommentar mit der Abdeckung, `korpus:`-Labels kumulieren, Schließen nur bei Erschöpfung.
6. PR öffnen, Validierung grün, dann liegen lassen. Der Mensch merged.
7. Ohne Unterbrechung zum nächsten Bündel.

**`pm:evidenceFrom` wird gelesen wie `dcterms:source`.** Beide sind Werkangaben, und die Regel aus §10 — keine Behauptung ohne Wortlaut — gilt für die moderne Arbeit genauso wie für den Traditionstext. Eine Studie, die nicht geöffnet wurde, ist keine Evidenz, sondern eine Erinnerung an eine Evidenz.

Daraus folgt der Prüfstand. `pm:casesWithoutDeviation` und `pm:casesWithDeviation` behaupten beide, **dass Fälle vorliegen und was sie zeigen**. Wer die Arbeit nicht gelesen hat, weiß das nicht; er weiß, was er über das Feld zu wissen glaubt. Ein Prüfstand jenseits von `pm:noProcedureDevised` und `pm:procedureWithoutCases` setzt die Lektüre voraus, und ohne sie ist der Knoten auf einen der beiden zurückzusetzen und die Adresse in ein Issue zu geben.

**Und die Gegensuche gehört dazu, erzwungen und nicht erinnert.** Eine Studie ist eine Partei, keine Instanz: sie hat Kritiker, Replikationen, die scheitern, und ein Feld, das sie heute anders liest. Wer sie aufnimmt, sucht nach dem Widerspruch und trägt den Stand ein — `pm:counterSearch` samt Notiz, Pflicht bei jeder Evidenzangabe, und ein Prüfstand mit Fällen ist mit `pm:counterSearchNotCarried` gar nicht erst validierbar. Diese Regel stand hier zuerst als Prosa und wurde noch in derselben Sitzung gebrochen; sie steht jetzt in den Shapes, weil eine Regel, die im Augenblick der Eile erinnert werden muss, im Augenblick der Eile versagt.

Drei Prüfungen, jede einzeln: **trägt die Werkangabe** — Band, Heft, Seiten, Kennung, und zwar am Nachweis und nicht aus dem Gedächtnis; **stützt die Arbeit die Aussage, für die sie steht**, oder eine benachbarte; **an welcher Population** wurde gemessen. Am 2026-09-02 sind an einem einzigen Knoten alle drei gerissen: eine DOI gehörte dem Nachbarartikel derselben Ausgabe, eine Interventionsstudie wurde für eine Wirkung der Kälte zitiert, die sie der Atemtechnik zuschreibt, und ein Rezeptorbefund aus dem Tiermodell stand ohne diesen Vermerk.

**Im Batch, nicht nacheinander.** Was in einem Lauf unabhängig voneinander bearbeitet werden kann, wird unabhängig voneinander bearbeitet: je Strang ein eigener Branch von `main`, ein eigener PR, eine eigene Begründung. Nicht gestapelt, wo nichts stapeln muss — gestapelt wird nur, wenn zwei Stränge dieselbe Datei anfassen, und dann sagt der PR es im ersten Absatz.

Der Grund ist nicht Geschwindigkeit, sondern Prüfbarkeit. Ein PR, der einen Wächter, eine Registrierung und einen Traditionsknoten zusammenfasst, ist als Ganzes anzunehmen oder abzulehnen; drei PR sind einzeln zu beurteilen und einzeln zurückzuweisen. Und ein Strang, der auf einen anderen wartet, obwohl er nicht muss, verlängert nur die Zeit, in der Arbeit im Gesprächsverlauf statt im Repo liegt.

**Bis zum PR wird nicht innegehalten.** Keine Zwischenberichte, keine Bestätigungsfragen, keine Freigabe vor dem Schreiben. Der Mensch prüft am Merge; alles davor ist der Auftrag, nicht die Verhandlung darüber.

**Jede Frage an den Menschen kommt mit einer Empfehlung.** Eine Entscheidung, die diese Datei und `SPEC.md` nicht abdecken, wird vorgelegt — aber nie als offene Frage allein. Vorzulegen sind: die Optionen, was jede kostet, und welche empfohlen wird, mit Grund. Wer die Alternativen kennt und die Empfehlung weglässt, schiebt die Arbeit weiter, die er schon getan hat; und eine Frage ohne Empfehlung zwingt den Menschen, sich den Fall ein zweites Mal zu erarbeiten, den der Agent gerade vor sich hatte.

Das gilt auch dort, wo die Entscheidung ausdrücklich beim Menschen liegt — bei Ontologieänderungen, beim Zuschnitt einer Klasse, bei allem nach §11 und §14. Die Zuständigkeit für die Entscheidung ist nicht die Zuständigkeit für ihre Vorbereitung.

## Die Sitzung trägt sich selbst

**Eine Sitzung ist in sich geschlossen.** Sie darf offen lassen, was sie nicht schafft — aber nichts davon darf nur in ihr stehen. Was am Ende offen ist, steht in einem Issue, das es trägt; was erledigt ist, ist geschlossen; was gesehen und nicht aufgenommen wurde, steht in einer Erntenotiz. Der Gesprächsverlauf ist kein Speicher, und das gilt nicht nur für Hypothesen, sondern für den Zustand der Arbeit selbst.

Der Grund ist derselbe wie bei prima-materia#351, eine Ebene höher: **ein Faden, der nur im Verlauf hängt, ist von einem nie aufgenommenen nicht zu unterscheiden.** Der nächste Lauf beginnt am Repo und sieht den Verlauf nicht. Was dort nicht steht, existiert für ihn nicht, unabhängig davon, wie klar es am Ende der Sitzung schien.

**Die Abschlussbedingung ist prüfbar und wird geprüft, nicht erinnert:**

1. `is:issue is:open no:label` ist leer.
2. Jeder in dieser Sitzung geöffnete PR nennt sein Issue, und jedes durch ihn erledigte Issue ist geschlossen oder trägt einen Kommentar, der sagt, was noch fehlt.
3. Jedes Issue, dessen Gegenstand im Bestand steht, ist als `completed` geschlossen — auch wenn die Arbeit in einem früheren Lauf geschah. Ein erledigtes und offenes Issue ist teurer als ein fehlendes: es bindet Aufmerksamkeit an eine Schuld, die getilgt ist, und die abhängigen Issues führen sich weiter als blockiert.
4. Jede Recherche des Laufs hat ihre Erntenotiz, mit den nicht aufgenommenen Funden und ihrem Grund.
5. Jede offene Entscheidung liegt als Frage mit Empfehlung vor, nicht als offene Frage.

Die dritte Bedingung ist die, die am häufigsten verletzt wird, und sie ist nicht durch Sorgfalt zu erfüllen, sondern nur durch Nachsehen: ob ein Issue erledigt ist, steht im Bestand und nicht im Issue. Am 2026-09-02 waren #23, #32 und #33 seit Tagen erledigt und offen, und drei weitere Issues führten sich deswegen als blockiert.

**Jede im Lauf entstandene Hypothese wird noch im selben Lauf ein Issue.** Das gilt für den Zielbefund, für den Beifang, für jede Vermutung, die im Denken auftaucht, und für jeden Befund über das Repo oder die Werkzeuge. Eine Hypothese, die nur im Gesprächsverlauf steht, ist verloren, sobald die Sitzung endet — und der Gesprächsverlauf ist kein Speicher, sondern ein Fenster.

**Anlegen statt ankündigen.** Ein Satz der Form „das sollte noch ein Issue werden" ist bereits die Arbeit, die stattdessen zu tun war. Wer ihn schreibt, hat den Aufwand des Anlegens schon aufgewendet und das Ergebnis weggeworfen.

**Vollständigkeit vor Eleganz.** Lieber fünfzig knappe Issues mit Behauptung, geprüften Stellen und Labels als fünf ausformulierte und der Rest im Fließtext.

## Vor dem ersten Schreibzugriff

1. `SPEC.md` vollständig lesen. Bei mehrdeutiger Spezifikation fragen, nicht raten.
2. Prüfen, ob eine Datei fehlt, die diese Anweisungen voraussetzen. Fehlt sie, ist das zu melden und nicht stillschweigend zu übergehen.
3. Lokal `python scripts/validate.py && pytest tests/` grün, dann PR. Der Mensch merged.
4. Löst eine Validierung aus, wird sie gemeldet, nicht umformuliert. Ein Fehlalarm ist ein Befund über den Wächter.
