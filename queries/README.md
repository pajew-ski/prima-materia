# queries

Die Abfragen, aus denen SPEC seine Warteschlangen ableitet, statt sie zu führen.

SPEC §13 verbietet, eine Frage als Issue einzutragen, die aus dem Zustand des Bestands folgt: sie wird abgefragt. §13, §14 und §16 nennen solche Warteschlangen namentlich; welche es gibt, sagt die Tabelle unten. Bis hierher stand nirgends, wie man sie abfragt, und es gab keinen Endpunkt dafür. Dieser Ordner trägt die Abfragen; der Endpunkt kommt getrennt.

## Ausführen

Gegen den kompilierten Graphen, ohne Server:

```bash
curl -sL -o prima-materia.ttl \
  https://cdn.jsdelivr.net/gh/pajew-ski/prima-materia-dist@main/prima-materia.ttl
python3 -c "
from rdflib import Graph
g = Graph(); g.parse('prima-materia.ttl', format='turtle')
for row in g.query(open('queries/coverage-queue.rq').read()): print(row)
"
```

Gegen einen SPARQL-Endpunkt, der den Graphen geladen hat, unverändert.

## Was hier liegt

| Datei | Frage | SPEC |
|---|---|---|
| `coverage-queue.rq` | welche registrierten Überlieferungen sind noch nicht erschlossen, und auf welchem Kontaktweg | §14 |
| `untested-generalizations.rq` | welche Verallgemeinerungen trägt kein Prüfknoten, geordnet nach der Zahl ihrer Belege | §16 |
| `exhibited-gaps.rq` | wo wurde gesucht und nichts gefunden | §13 |
| `unopened-works.rq` | welche Werke im Korpus einer erschlossenen Überlieferung trägt noch keine eingetragene Stelle | §14 |
| `work-migration-backlog.rq` | welche erschlossenen Überlieferungen führen ihren Korpus noch nicht als Werkbezeichner | §14 |

## Zwei Lesehilfen

**Der Nenner zählt mit.** Eine Häufigkeit über die Traditionen hinweg misst zuerst die Werkauswahl der bisherigen Läufe. Sie wird erst gegen den `pm:coverageState` der registrierten Traditionen aussagekräftig, sonst meldet der Bestand seine eigene Abdeckung als Struktur der Überlieferung.

**Abwesenheit ist eine Aussage.** Kein Prüfknoten heißt, dass niemand die Prüfung aufgenommen hat, und nicht, dass geprüft und nicht gestützt wurde. Dieselbe Unterscheidung trägt `pm:searchYieldedNode`: eine Suche ohne Fund ist ein ausgestellter Leerbefund, eine nie geführte Suche ist gar nichts.
