# AGENTS.md

Anweisungen für jeden Agenten an diesem Repository. Vollständige Spezifikation in `SPEC.md`; bei Konflikt gilt `SPEC.md`. `CLAUDE.md` trägt Werkzeug- und Konventionsdetails. Issue-Nummern in Klammern sind Fallnachweise; die Begründung steht dort, nicht hier.

## Was dieses Repo ist

prima-materia ist eine Prüfstelle, keine Sammlung. Eine Behauptung über ein magisches oder kontemplatives Vermögen wird von ihrer Beglaubigung getrennt gehalten, damit sichtbar bleibt, worauf sie steht: auf einem überlieferten Text, auf einem modernen Bearbeiter, oder auf nichts.

> **Wertvoll ist, was ein Tor beseitigt.** Der wertvollste Knoten ist der anderswo am zuverlässigsten falsch berichtete.

## Recherche

Fünf Sätze, vollständig in `SPEC.md` §15.

1. **Der Suchraum ist alles Erreichbare, nicht der Bestand.** Ein vorhandener Knoten belegt nichts; er ist eine früher eingetragene Behauptung mit Herkunft.
2. **Erste Frage: wo gibt es Quellen, die der Bestand nicht kennt.** Nicht: was sagt der Bestand.
3. **Jede Recherche sucht Behauptung und Negation**, auch außerhalb der erwarteten Sphäre. Rezeption ist kein Ausschlussgrund, nur ein Verbot, dieselbe Aussage zweimal zu zählen; was eine spätere Station *hinzugefügt* hat, trägt `pm:Reworking`. Wer `pm:independentAttestation` setzt, schuldet `pm:independenceGround`.
4. **Mindestumfang:** Fachterm in Originalsprache und Transliterationen; Primärtext, zwei Übersetzungen, Sekundärliteratur zur Stelle; Datierung des frühesten Zeugen und Zuschreibungsstreit; Gegensuche; eine Überlieferung außerhalb der erwarteten Sphäre.
5. **Beifang wird Knoten nur mit gelesener Stelle**, sonst Issue mit `korpus:`-Label und den geprüften Kandidatenstellen. Die Schranke ist der gelesene Wortlaut, nicht die vollständige Prüfung (#76).

### Zwei Stufen, beide Pflicht

**Landschaft:** breiter Rechercheauftrag mit parallelen Suchen; liefert Adressen, nie Belege. **Stelle:** das Werk selbst, im Original, bevor daraus ein Knoten wird. In den Graphen kommt nur, was die zweite Stufe überstand; ins Issue, was sie **nicht überstand**, als nicht am Wortlaut geprüft gekennzeichnet. Die zweite Stufe für ein erreichbares Werk auszulassen macht den Lauf unvollständig, auch bei sauberen Issues.

**Erreichbar heißt erreichbar, nicht bequem.** Ein Volltext, der sich herunterladen und durchsuchen lässt, ist erreichbar, auch bei tausend Seiten. Bleibt eine Prüfung aus, steht der Grund am Werk, und er ist eine Eigenschaft des Werkes: nicht digitalisiert, gesperrt, ordensintern, nur Druck, Sprache nicht beherrscht. Vorher abgearbeitet: andere Kennung im selben Archiv, andere oder ältere Ausgabe, andere Umschrift, das Werk in einer Sammlung oder einem Kommentar, ein anderes Digitalisierungsvorhaben. Eine Sperre am Zugangsweg hängt nicht am Werk und verlangt einen anderen Weg (#76: vier von vier als unerreichbar geführte Werke lagen als Volltext vor).

### Die geprüften Zugangswege

Die Tabelle ist der Ort des Befunds. Wer einen Weg prüft, trägt ihn hier ein, im PR seines Bündels. Eine Sperre steht hier und nie am Werk.

| Weg | Stand |
|---|---|
| archive.org, `https://archive.org/download/<kennung>/<kennung>_djvu.txt` | Regelweg (#515, #584). Zeilenumbrüche fehlen, nach Zeichenbereich schneiden. Seitenzahl aus dem laufenden Kolumnentitel bilden (#546). Ausgabe vom Titelblatt im Volltext, nie aus den Katalogdaten (#153) |
| archive.org, Dateiname über `https://archive.org/metadata/<kennung>` | trägt, wo `_djvu.txt` mit 404 oder 503 antwortet (#700, #702) |
| archive.org, `503` auf eine Kennung | Sperre am Weg; andere Kennung desselben Werkes versuchen (#702) |
| archive.org, `503` auf **jede** Kennung, Körper 11832 Byte mit `<title>Internet Archive: Temporarily Offline</title>`, dazu `web.archive.org` ohne Antwort | Gesamtausfall des Archivs, keine Sperre an einer Kennung. Die Zeile darüber ist dann der falsche Zug und kostet den Lauf: eine zweite Kennung antwortet genauso. Erst Körpergröße und `<title>` prüfen, dann den Strang auf einen Weg ohne archive.org legen oder, wo keiner trägt, den Strang nicht als unerreichbares Werk führen, weil die Sperre am Weg hängt und nicht am Werk (2026-10-07) |
| archive.org, `500` bei vollständigen Metadaten, 170 Byte nginx | Drosselung, kein defektes Werk; zweite Kennung trug sofort (#788) |
| archive.org, `200`, Datei bricht nach den ersten Druckseiten ab | gefährlichste Klasse, sieht aus wie Negativbefund. Vor jedem Nichtfund die Kolumnentitelfolge bis zum Bandende prüfen (#796) |
| archive.org, Scan mit gemischter Schrift | ASCII-Buchstabenanteil je Block messen; unter 0,3 unbrauchbar (#767) |
| archive.org, griechischer, hebräischer oder syrischer Satz, ASCII-Anteil nahe 1,0 | OCR hat die zweite Schrift in lateinische Zeichen zerlesen. Zeichen je Unicode-Block zählen; null heißt: Originalsprache nicht vorhanden (#775) |
| archive.org, lateinischer Satz, ASCII-Buchstabenanteil **0,0** | der umgekehrte Fall, und er ist eine Eigenschaft des Uploads und nicht des Werkes: die OCR lief mit dem falschen Sprachmodell und hat englischen Druck Zeichen für Zeichen in Devanagari zerlesen, Umfang und Zeilenumbrüche stimmen, kein Wort ist lesbar. Nicht als unleserlicher Scan abbuchen, sondern eine andere Kennung desselben Werkes holen: am 2026-10-09 lagen Snellgroves Nine Ways of Bon und Reynolds Oral Tradition from Zhang Zhung unter je zwei Kennungen, eine mit 0,0 und eine mit 1,0. Der Anteil ist in einer Zeile zu messen, bevor gelesen wird, und er entscheidet die Kennungswahl (2026-10-09) |
| archive.org, zerlesene Ziffern im Kolumnentitel | Folge auf Monotonie prüfen; sonst nach kanonischem Schema zitieren und Seitenzahl weglassen (#829) |
| archive.org, Scanlücke | fehlende Seiten zeigen sich an der Kolumnentitelfolge (#576) |
| archive.org, Goldschmidts Talmud | Bände `derbabylonischet01unse` bis `08unse`, je Band eigener Verlag und Jahr vom Titelblatt; zweite Übersetzung `band-1` bis `band-12` mit anderer Paginierung (#826) |
| `https://<server>/fulltext/inside.php?item_id=&doc=&path=&q=` | trägt bis ans Bandende, absatzweise über ein Suchwort; Parameter aus `metadata`, braucht `indexed: true`. Findet nicht ohne Diakritika; Antworten kamen einmal unangekündigt übersetzt zurück, gilt dann als nicht gelesen (#797, #799) |
| Kanseki Repository, ein GitHub-Repo je Werk, eine Datei je juan | trägt für die chinesischen Klassiker und Sammelwerke; klonen statt abrufen. Einzelne juan können fremden Text tragen (#614, #676, #687) |
| Kanseki Repository, Kennung des Werkes | **nicht** über kanripo.org: die Seite antwortet auf jeden Pfad, Wurzel und Katalog eingeschlossen, mit `403`. Der Katalog liegt als GitHub-Repo daneben, `https://raw.githubusercontent.com/kanripo/KR-Catalog/master/KR/<klasse>.txt`, eine Datei je Siku-Klasse mit Zeilen der Form `*** KR3a0047 朱子語類-宋-黎靖德`; die Klassenliste steht in `README.org` desselben Repos. Erst dort suchen, dann `git clone https://github.com/kanripo/<kennung>.git`. Geraten wird nicht: KR3a0094 ist nicht das vermutete Werk, sondern das 格物通 (2026-10-10) |
| Kanseki Repository, Wenyuange-Satz, dasselbe Wort in zwei Zeichenformen | Der WYG-Satz schreibt Zeichen mit verkürztem Element neben der vollen Form und benutzt beide für dasselbe Wort im selben juan. Im 朱子語類 (KR3a0047) steht 靜坐 dreiunddreißigmal und 静坐 dreiundsechzigmal, in dreißig juan zusammen, und siebzehn juan erreicht nur die zweite Form; juan 12 trägt eine Stelle in der ersten und dreiundzwanzig in der zweiten. Eine Suche in einer Form allein ist hier keine Suche, sondern eine Aussage über diese Form, und der Lauf vom 2026-10-10 hätte in der ersten Form das einzige Methodenwort des Werkes, seine ganze bejahende Schicht und die Zweitbezeugung beider Fälle verfehlt und das Fehlen als Befund gemeldet. **Jede Suche über einen WYG-Text zählt beide Formen der Schlüsselzeichen und nennt beide Zahlen** (2026-10-10) |
| CBETA, Taishō-Kanon als TEI-P5 über `https://raw.githubusercontent.com/cbeta-org/xml-p5/master/T/T<band>/T<band>n<nummer>.xml` | Regelweg für den chinesischen buddhistischen Kanon, reiner GET, kein JS, eine Datei je Werk. Der kanonische Lokus steht als Zeilenbake `<lb n="0471b05"/>` darin: Seite plus Register, wie jede Ausgabe des Kanons ihn führt, also Stellenangabe ohne Umrechnung. `cbeta-git/xml-p5` liegt daneben und ist die ältere Fassung. Das ganze Repositorium zu klonen läuft in die Zeitgrenze, der Einzelabruf eines Werkes braucht eine Sekunde. Die Lesarten stehen als `<note place="foot">` im Fluss und sind vor dem Lesen zu entfernen, sonst stehen sie mitten im Satz (2026-10-10) |
| CBETA, `api.cbetaonline.cn` und `cbetaonline.dila.edu.tw/api/...` | beide unbenutzbar, und die zweite auf die gefährliche Weise: `api.cbetaonline.cn` antwortet durch den Agentproxy mit `502 Tunnel connection failed`, `cbetaonline.dila.edu.tw` dagegen auf **jeden** Pfad unter `/api/` mit `200` und der 64198 Byte großen JS-Hülle der Leseoberfläche. Ein stiller Treffer, der wie eine Antwort aussieht; Größe prüfen und den Weg der Zeile darüber nehmen (2026-10-10) |
| `https://api.digitale-sammlungen.de/ocr/<bsb-Kennung>/<Scannummer>` | hOCR einer Seite mit Kolumnentitel, bester Weg wo er greift; Scannummer-Offset je Digitalisat bestimmen. Nur BSB-Bestände (#797) |
| Persée | `web_fetch` gesperrt; Dokumentseite trägt in `data-content-url` je Druckseite den OCR-Text (#257). Die Dokumentkennung steht nicht über `/search`, das JS-getrieben ist und für ein `curl` leer zurückkommt, sondern im Klartext der Heftseite `https://www.persee.fr/issue/<reihe>_<issn>_<jahr>_num_<band>_<heft>`; ein Abruf je Druckseite, vierzig Seiten in gut einer Minute, Textschicht sauber samt kritischem Apparat (2026-10-07) |
| Gallica, Textlayer-Test `https://gallica.bnf.fr/services/ContentSearch?ark=ark:/12148/<id>&query=<wort>` | ein Band, der auch für ein triviales Wort null Treffer meldet, hat keine OCR, gleich wie vollständig das Digitalisat ist. Ein Abruf entscheidet, ob der Band als Wortlaut überhaupt in Frage kommt (Suchknoten `pmp:IbogaFirstDescriptionSearch`) |
| Gallica, `https://gallica.bnf.fr/RequestDigitalElement?O=<id>&E=ALTO&Deb=<view>` | seitenweises OCR-XML, trägt wo der Textlayer existiert, und antwortet `500` wo er fehlt. Druckseite aus der Kopfzeile, View-Offset je Digitalisat bestimmen. `/texteBrut` ist für Skripte durch eine Sicherheitsabfrage gesperrt (Suchknoten `pmp:IbogaFirstDescriptionSearch`) |
| Biodiversity Heritage Library | `403` hinter Cloudflare für jeden maschinellen Abruf, Seiten- wie Volltextweg; die Artikel-API von biostor.org läuft, deckt die alten Bulletinbände aber nicht (Suchknoten `pmp:IbogaFirstDescriptionSearch`) |
| archive.org, Zeitschriftenreihe heftweise | `https://archive.org/advancedsearch.php?q=identifier:<reihe>_<jahr>*&output=json` sagt in einem Abruf, ob der Jahrgang überhaupt liegt. Einzelne Jahrgänge fehlen, ohne dass die Reihe fehlt: Comptes rendus 1901 null Hefte, 1907 dreiundfünfzig (Suchknoten `pmp:IbogaFirstDescriptionSearch`) |
| Tote Adresse einer frei gestellten Datei | Wayback-Index `https://web.archive.org/cdx/search/cdx?url=<adresse>&output=text&limit=20`, dann `https://web.archive.org/web/<zeitstempel>id_/<adresse>`; ohne `id_` kommt die Rahmenseite (#730) |
| HathiTrust `pdus` | gesperrt, 403 hinter Cloudflare (#556, #702) |
| ctext.org, zh.wikisource.org, zysj.com.cn | 403 nach dem ersten Kapitel bzw. nicht abrufbar (#614) |
| HAL | Proof-of-Work-Abwehr, Browserweg offen (#565) |
| OAPEN | Proof-of-Work-Abwehr mit `200` und 4 KB Abwehrseite; Größe und `<title>` prüfen. DOAB, JSTOR-OA, Project MUSE ungeprüft (#814) |
| sacred-texts.com | drosselt, große PDF still gekürzt, HTML-Leseausgaben liefern Inhaltsangabe statt Wortlaut; für die Ernte unbrauchbar (#473, #796) |
| esotericarchives.com | das Urteil der Zeile darüber galt bis zum 2026-10-07 auch hier und ist für diese Adresse falsch: `juratus/juratus.htm` sind 745 KB in `cp1252` ohne Charset-Deklaration und tragen den lateinischen Wortlaut aus Sloane 3854 und die englische Übersetzung aus Royal 17 A. xlii nebeneinander, mit Kapitelzahlen nach Hedegård und Lesarten im Apparat. Eine Leseausgabe dieser Seite ist also vor dem Urteil an ihrer Größe zu messen, Inhaltsangaben liegen im Bereich einiger Zehn KB. Weiter gilt die Drosselung: ein Abruf, lokal ablegen, nicht erneut holen (2026-10-07) |
| archive.org, `_djvu.txt` bei neueren Uploads | der Dateiname ist der des Uploads, nicht die Kennung; `<kennung>_djvu.txt` antwortet dann mit 404. Erst `metadata` lesen und den echten Namen prozentkodieren. `access-restricted-item: true` in den Metadaten sagt 401 auf jeden Volltextabruf voraus und erspart den Versuch |
| hethport.net, Hethitologie-Portal Mainz | Regelweg für das hethitische Korpus, reiner GET, kein JS. Konkordanz je CTH `hetkonk/hetkonk_abfrage.php?c=<n>` mit Siglum, Join, Schriftdatierung und Bibliographie je Fragment; kritische Edition `txhet_besrit/intro.php?xst=CTH <n>` und `.../exemplar.php?xst=CTH <n>&expl=<A..D>&lg=&ed=` mit Transliteration, Paragraphen- und Zeilenloki; `TLHdig/tlh_xtx.php?d=<siglum>&o=CTH <n>` für Texte ohne kritische Edition, mit Interlinearglossierung. `translatio.php` ist für die meisten Texte eine leere Hülle von etwa 2,7 KB: keine Übersetzung veröffentlicht, nicht als Fehler lesen |
| hethport.uni-wuerzburg.de, alte Adresse | antwortet auf **jeden** Pfad mit `200` und einer Hinweisseite von 1744 Byte. Ein stiller 404, der wie ein Treffer aussieht; Größe prüfen und auf `hethport.net` wechseln |
| TLHdig als Massendatensatz, Zenodo 15459134, CC-BY | 64 MB ZIP, 22436 XML-Dateien, eine je Textzeuge, nach CTH-Ordnern. **Zwei Dateiarten:** glossierte Dateien tragen die Transliteration als Attribut `trans` am `<w>`-Element, unglossierte nur als Elementinhalt. Ein Extraktor, der nur `trans` liest, liefert für die unglossierten Dateien leere Zeilen — und darunter sind Hauptmanuskripte. Der Lauf vom 2026-10-06 hat damit eine Klausel nicht gefunden, die in der durchsuchten Datei stand. **Jede Suche über diesen Datensatz braucht eine Positivkontrolle:** eine bekannte Stelle mitsuchen und den Lauf verwerfen, wenn sie nicht kommt |
| sbl-site.org, Writings from the Ancient World | der Verlag stellt einzelne Bände selbst frei: `https://www.sbl-site.org/wp-content/uploads/<jahr>/<monat>/<Autor>.pdf`, mit Textschicht und echter Paginierung. Die Serienseite unter `/publications/` antwortet mit 403, die Datei darunter mit 200; vom 403 nicht auf den Band schließen |
| sites.dlib.nyu.edu, Ancient World Digital Library | frei gestellte Brill-Bände mit Textschicht: Betrachter `/viewer/books/<id>`, Datei `https://mc.dlib.nyu.edu/files/books/<id>/<id>_lo.pdf`. Trägt, wo die Verlagsseite gesperrt ist |
| hethport, freie StBoT-Bände `stbot/baende/StBoT<n>.pdf` | `200` und vollständig, aber **ohne Textschicht**: `pdftotext` gibt für zwölf Seiten zwölf Byte. Reines Bild, OCR nötig, und die erwartet denselben Diakritikaverlust wie ein archive.org-Scan. Frei nur bis Band 32 |

Bei beschädigter OCR ist ein Nichtfund des Fachterms kein Nachweis der Abwesenheit: nach der danebenstehenden Übersetzung suchen, Text auf Buchstaben normalisieren und über Positionsindex zurückrechnen (#702, #576).

## Ernte

**Die Arbeitseinheit ist ein Werk.** Teuer ist das Öffnen, billig die weitere Stelle im offenen Text. Geschuldet sind fünf Arten, vollständig in `SPEC.md` §15: **Vermögen** (streng vollständig; ein Rezept ist ein Vermögen), **Voraussetzungsketten**, **Warnungen** samt Selbstwarnungen, **Misslingensbedingungen** (daraus wird `pm:falsifiedBy`), **Gelingenszeichen** getrennt gezählt. Die Ernte braucht kein Issue vorher und ist keine Scope-Erweiterung.

**Aufnahme geht vor Vollständigkeit.** Aufnahmebedingung eines Bezeugungsknotens ist die gelesene Stelle mit Ausgabe. Ein `pm:Yielding` behauptet, dass diese Quelle die Wirkung behauptet; die Gegensuche gehört an den `pm:Testing`-Knoten. **Ein Issue ersetzt keinen Knoten, den die Stelle trägt** (#351, Kālikāpurāṇa 2026-09-09).

**Der Lease ist der Branch.** `claude/ernte-<werk-slug>`; `gh_branches` wird vor `prima_repo_base_sha` gelesen und zeigt laufende Ernten und abgestürzte Läufe. Kein Issue je Werk: der Branch reserviert, der Graph trägt, was geerntet ist (`pm:corpusWork`, `pm:fromWork`, `queries/unopened-works.rq`). Ein Branch ohne eigenen Commit wird mit `prima_repo_branch_delete` entfernt; einer mit ungemergten Commits gehört namentlich in den PR-Body des Laufs, der ihn fand, und bleibt dem Menschen (#573, #630).

**Ein PR je Werk, die Erntenotiz im PR-Body.** Sie nennt die geschriebenen Knoten mit Bezeichnern, aus der Lektüre geschrieben und nicht aus der Datei abgeschrieben, dazu was ungelesen blieb und was gesehen und mit Grund nicht aufgenommen wurde. Die Auslassung ist die Differenz zwischen Notiz und Branch (#351).

**Ein ungeöffnetes Werk ist ein Werkknoten, kein Issue.** Es wird als `pmw:`-Knoten an seiner Tradition deklariert (`pm:corpusWork`), ohne `pm:fromWork`; der Grund der Nichtöffnung steht als `skos:note` am Werk, wo er eine Eigenschaft des Werkes ist. `queries/unopened-works.rq` ist die Warteschlange. Ein vermittelter Knoten (`pm:mediatedAttestation`) trägt mit `pm:readVia` selbst, was fehlt; `queries/mediated-attestations.rq` listet ihn.

**Die Suchknoten eines Laufs stehen in einer eigenen Datei**, `examinations/searches-<korpus-slug>.ttl`, und nie durch Anhängen an `examinations/searches.ttl`. Der Grund ist mechanisch und kostet sonst einen Lauf: zwei Stränge, die an dieselbe Endposition derselben Datei anhängen, laufen nicht ohne Hand zusammen, und der stehende Auftrag verlangt zwei Stränge nebeneinander. Das Register ist die Klasse `pm:Searching` und nicht die Datei; `queries/exhibited-gaps.rq` fragt über alle (#703).

**Wer eine Traditionsdatei anfasst, führt ihren Korpus im selben Lauf als Werkbezeichner** (`pm:corpusWork`, `pm:fromWork`, `pmw:`); Rückstand in `queries/work-migration-backlog.rq` (#737).

**Bezeichner aus dem Gegenstand, nicht aus der Formulierung:** Tradition plus normalisierter Terminus der Originalsprache, bei Namen die Namensform der Leitumschrift der benutzten Ausgabe. Nie aus der Übersetzung. `tests/test_identifier_uniqueness.py` meldet gleiche Bezeichner in zwei Dateien, nie zwei Bezeichner für eine Sache.

## Prüfung vor dem PR

Alle Schreibvorgänge des Bündels, dann `prima_repo_check`; es stößt `validate.yml` per `workflow_dispatch` an und meldet `laeuft`, nach etwa einer Minute erneut aufrufen, PR erst bei `gruen`. Nicht nach jedem Schreibvorgang aufrufen. `cancelled`-Läufe und rote Kreuze an gestapelten PR sind kein Befund (#352, pajew-ski/data#337).

**Bei rot lokal reproduzieren statt raten:**

```
git clone --depth 1 --branch <branch> https://github.com/pajew-ski/prima-materia.git
pip install -r requirements.txt --break-system-packages
python scripts/validate.py && python -m pytest tests/ -q
```

**Der Branch ist die Quelle, der Klon das Abbild.** Vor dem PR `git fetch`; `git status --porcelain` und `git diff origin/<branch>` müssen leer sein, sonst ist das Bündel offen (#351).

**`prima_repo_write` legt nur an**; auf einen vorhandenen Pfad antwortet es mit einer Meldung ohne Pfad und Grund (#799). Bestehende Dateien ändert `prima_repo_replace`; große Umbauten stückweise anhängen, `alt` ist die letzte Zeile des vorigen Stücks. Nach `session expired` erst den Branch lesen, dann wiederholen (#829).

## Was „gegroundet" heißt

| | |
|---|---|
| **Gegroundet** | Stelle trägt die Behauptung **und** Gegensuche gelaufen |
| **Unbelegt** | die Stelle gibt es nirgends; trägt nur eine erschöpfende, dokumentierte Suche |
| **Nicht gegroundet** | ein Knoten im Bestand, eine Analogie, eine Erinnerung an eine nicht aufgeschlagene Stelle |
| **Aufnahmefähig** | die gelesene Stelle mit Ausgabe; weniger als gegroundet, genug für einen Knoten |

## Die Kette

Vollständig in `SPEC.md` §16. Eine Behauptung trägt Werk und Stelle; „Hypothese" meint ein Issue, keine Klasse. Eine Überschneidung wird behauptet, nicht gefunden (`pm:Converging` trägt `pm:compilerInference`), entsteht im Beifang und ist noch nicht prüfbar. Prüfbar wird es als `pm:Generalizing` aus mindestens zwei bezeugten Behauptungen, ohne `dcterms:source` und `pm:withinTradition`. Die Warteschlange der Prüfung ist `queries/untested-generalizations.rq`. **Die Gegensuche einer Verallgemeinerung läuft zuerst gegen den eigenen Bestand, bevor sie geschrieben wird** (#665, #667).

## Issues

Vollständig in `SPEC.md` §13. Der Tracker hält Behauptungen ohne gelesene Stelle und Befunde, die der Lauf nicht leisten kann. Jedes Issue trägt `behauptung` oder `befund`; `is:issue is:open no:label` bleibt leer. Labels aus `CONTRIBUTING.md`, nicht aus dem Gedächtnis.

**Vor jedem `issue_create`: folgt das aus einem Zustand im Graphen?** Dann ist es eine Abfrage und kein Issue. Registrierte Tradition ohne Knoten, ungeöffnetes Werk, ungeprüfte Verallgemeinerung, vermittelter Knoten, Prüfknoten ohne Fälle, Knoten ohne Verortung: alles in `queries/`.

**Ein Befund wird behoben oder als Regel geschrieben, bevor er ein Issue wird.** Nur was der Lauf nicht leisten kann, wird eines, und sein Body endet mit „Erledigt, wenn". Vor dem Anlegen nach einem offenen Befund zum selben Gegenstand suchen. Lücken im Werkzeugsatz gehören nach `pajew-ski/data`. Der PR, der einen Befund erledigt, nennt ihn; geschlossen wird ausdrücklich nach dem Merge, bis `Closes #<n>` an einem PR mit einer einzigen Zeile belegt ist (#815 hat mit 37 Zeilen nicht geschlossen).

**Behauptungen werden je Korpus gezogen, nicht als Liste gelesen.** `korpus:`-Labels kumulieren und sind der Nachweis der Suchabdeckung; was eine Recherche ergab, steht im Issue.

## Quellen

Jede Behauptung trägt `dcterms:source` als Werk mit Stelle und gelesener Ausgabe. Nie URLs, Videos, Blogs, Wikipedia, Foren, unveröffentlichte eigene Texte, Referate statt der Stelle. Unerreichbares Werk: `pm:mediatedAttestation` mit `pm:readVia`; der Modus hängt an der Unerreichbarkeit, nicht am Aufwand. Moderne Forschung nur über `pm:evidenceFrom` an `pm:Testing`, gelesen wie `dcterms:source`, mit `pm:counterSearch` (Shape erzwingt). Drei Prüfungen je Evidenzangabe: Werkangabe am Nachweis, stützt die Arbeit genau diese Aussage, an welcher Population (2026-09-02: alle drei an einem Knoten gerissen).

## Der stehende Auftrag

„prima materia weiter" meint den vollständigen Durchlauf. Keine Rückfragen zu Schritten, die diese Datei und `SPEC.md` vorschreiben; der Mensch prüft am Merge.

1. **Bestand lesen:** Dateibaum, `gh_branches`, letzte PRs, offene Befunde (`is:issue is:open label:befund`). Behauptungs-Issues erst je gewähltem Korpus (`label:behauptung label:korpus:<x>`), nicht als Ganzes. Wer eine Datei, einen Weg oder ein Werkzeug anfasst, über die ein Befund steht, erledigt oder kommentiert ihn im selben Lauf.
2. **Bündel wählen.** Vorrang prüfbarkeitsgetrieben (SPEC §14), dann unabhängigkeitsgetrieben, dann Bedarf aus Behauptungs-Issues. Daneben immer ein zweiter Strang ohne Frage: ein Werk einer Tradition auf `pm:corpusNamed` mit dünnem Bestand (`queries/coverage-queue.rq`); nur er erzeugt Behauptungen, nach denen niemand gefragt hat.
3. **Recherche**, beide Stufen, Gegensuche, bis jede Behauptung mit erreichbarem Werk am Wortlaut geprüft ist.
4. **Integrieren:** Knoten für Gelesenes, Werkknoten für Ungeöffnetes, Issues nur für Behauptungen ohne Stelle und aus keinem Zustand ableitbar. Befunde beheben oder als Regel schreiben.
5. `korpus:`-Labels kumulieren; Behauptungs-Issue schließen, sobald ein Knoten es trägt.
6. **PR öffnen** bei `gruen`, Erntenotiz im Body, liegen lassen.
7. Ohne Unterbrechung zum nächsten Bündel.

**Im Batch, nicht nacheinander.** Je unabhängiger Strang ein Branch von `main` und ein PR. Gestapelt nur bei Dateiüberschneidung, mit `base` auf den Branch darunter; wird die Überschneidung erst bei der Lektüre sichtbar, wird der spätere Strang auf den Kopf des früheren gesetzt (#475, #744). Nach dem Merge des unteren dessen Branch löschen, sonst zielt der obere weiter auf ihn.

**Jede Frage an den Menschen trägt ihre Empfehlung**, auch bei Entscheidungen nach §11 und §14: Optionen, Kosten, empfohlene Option mit Grund.

## Die Sitzung trägt sich selbst

Der Gesprächsverlauf ist kein Speicher. Abschlussbedingungen, geprüft statt erinnert:

1. `is:issue is:open -label:behauptung -label:befund` ist leer. Nicht `no:label`: das fängt nur „gar kein Label" und lässt ein Issue mit `korpus:` und sonst nichts durch, also genau den Zustand, den das Dachlabel verhindern soll (#698).
2. Jeder PR nennt seine Issues; jedes erledigte Issue ist geschlossen oder trägt einen Kommentar, was fehlt. **Ein Lauf am strukturgetriebenen Eingang hat planmäßig kein Issue** — die Warteschlange ist der Registrierungsstand und ein Issue daneben wäre die Kopie eines Zustands, die SPEC §13 verbietet. Sein PR nennt stattdessen den Zustand des Bestands, aus dem das Bündel gewählt wurde, und der offene Rest steht als `skos:note` an dem Knoten, den er betrifft, beim Register also an der Traditionsinstanz neben `pm:coverageState`; sonst findet ihn keine Abfrage (#779).
3. Jedes Issue, dessen Gegenstand im Bestand steht (Graph, diese Datei, `SPEC.md`, `CLAUDE.md`, `CONTRIBUTING.md`, Test, Workflow), ist als `completed` geschlossen, auch aus früheren Läufen.
4. Jede Recherche hat ihre Erntenotiz im PR.
5. Jede offene Entscheidung liegt als Frage mit Empfehlung vor.
6. Selbstcheck: welche Stufe wurde übersprungen, was nacheinander getan, was nebeneinander gehörte, wie steht Gerüst zu Bestand. Befunde daraus werden behandelt, nicht berichtet (#442, #443).

**Anlegen statt ankündigen.** Jede Hypothese des Laufs, die aus keinem Zustand ableitbar ist, wird im selben Lauf ein Issue. Und kein Issue, wo ein Knoten hingehört.

## Vor dem ersten Schreibzugriff

1. `SPEC.md` lesen. Bei Mehrdeutigkeit fragen, mit Empfehlung.
2. Fehlt eine Datei, die diese Anweisungen voraussetzen, melden.
3. Lokal `python scripts/validate.py && pytest tests/` grün.
4. Eine ausgelöste Validierung wird gemeldet, nicht umformuliert.
