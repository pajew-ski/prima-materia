# Methodenvergleich: §10 des Entwurfs gegen die Spezifikation dieses Bestands

Entstanden aus prima-materia#376. Der Methodenentwurf „Der Strom" trägt in §10 zehn Einträge, die als Behauptungen angelegt wurden. Sieben davon sind keine — sie sagen nicht, wie die Welt ist, sondern wie zu prüfen ist. Für eine Norm lässt sich kein `pm:falsifiedBy` formulieren, und ein Prüfprotokoll ohne Falsifikationsbedingung hätte keinen Gegenstand.

Dieses Blatt hält statt dessen fest, was der Vergleich der beiden Verfahren ergibt: welche Entwurfsregel im Bestand bereits als Vorrichtung existiert, welche nicht, und was das jeweils über die Spezifikation sagt.

## Vorbemerkung: die Einteilung war feiner als die erste Sichtung

prima-materia#376 hatte §10 pauschal als Prüfvorschriften eingeordnet. Das ist beim Nachlesen der einzelnen Einträge falsch. Drei von zehn sind sehr wohl prüfbar, und die Issues selbst sagen das bereits — 10-10 nennt von sich aus `pm:Systematizing` als mögliche Form und hält die Mehrdeutigkeit ausdrücklich fest, statt sie zu raten. Die Anlage war sorgfältiger als die Sichtung, die sie zusammenfasste.

| Kennung | Art | Ort |
| --- | --- | --- |
| 10-01 | Verfahrensregel | hier |
| 10-02 | Sachbehauptung | bleibt als Issue offen |
| 10-03 | Falsifikationsbedingung zu einer anderen Behauptung | hier |
| 10-04 | Sachbehauptung | bleibt als Issue offen |
| 10-05 | Verfahrensregel | hier |
| 10-06 | Verfahrensregel | hier |
| 10-07 | Verfahrensregel | hier |
| 10-08 | Verfahrensregel | hier |
| 10-09 | Setzung eines Schwellenwerts | hier |
| 10-10 | Zuordnung, kein Weltsatz | bleibt als Issue offen |

## Der Vergleich

### 10-01 — Zustand und Inhalt sind getrennt zu prüfen

**Im Bestand vorhanden, ohne Vorrichtung.** Die Regel wird befolgt und ist nirgends erzwungen. `pmc:AffectCouplingProtocol` trennt die schwache Lesart, dass die Kopplung den Träger verschiebt, von der starken, dass das Feld außerhalb des Trägers wirkt, und sagt in einer eigenen Notiz, dass nichts an der einen auf die andere zutrifft. `pmc:ParalysisIsTheRegularShutdown` und `pmc:ParalysisPrecedesItsNotice` sind aus demselben Grund getrennt, und dort hat sich die Trennung bezahlt: die eine hält der Prüfung stand, die andere nicht, auf derselben Evidenz.

Ein Wächter dagegen ist nicht denkbar. Ob zwei Behauptungen in einem Knoten stecken, ist keine Eigenschaft, die sich am Tripel ablesen lässt. Die Regel bleibt eine Sorgfaltspflicht, und der Bestand belegt, dass ihre Verletzung teuer ist.

### 10-03 — Ein benannter Falsifikator für die Wellenführung

**Kein Vergleichsfall, sondern ein fehlplatzierter Eintrag.** Was hier steht, ist eine Falsifikationsbedingung für eine Behauptung des §7.8, nicht eine eigene Behauptung. Im Bestand gehört so etwas an den Prüfknoten der betroffenen Behauptung, in `pm:falsifiedBy`, und nirgendwo sonst.

Das ist der einzige Punkt, an dem die Entwurfsgliederung selbst einen Fehler macht: sie führt die Bedingung als eigenen Satz, statt sie an ihren Gegenstand zu hängen. Der Bestand kann das gar nicht, weil `pm:FalsifierRequiredShape` die Bedingung am Protokoll erzwingt und ein freistehender Falsifikator keinen Ort hätte.

### 10-05 — Der Inhalt ist vor der Verifikation festzuhalten

**Nicht im Bestand, und aus einem Grund.** Die Regel richtet sich an jemanden, der selbst prüft und dabei der Versuchung ausgesetzt ist, seine Vorhersage im Nachhinein an den Ausgang anzupassen. Der Bestand prüft nicht selbst; er nimmt Prüfungen anderer über `pm:evidenceFrom` auf, und die Präregistrierung ist dort Sache der aufgenommenen Arbeit.

Der Fall ist trotzdem lehrreich: er markiert die Grenze zwischen einem Verzeichnis von Prüfungen und einem Prüfprotokoll. Wer den Bestand je um eigene Erhebungen erweitert, braucht diese Regel — und dann als Pflichtfeld, nicht als Vorsatz.

### 10-06 — Nicht bei jemandem verifizieren, dem man den Inhalt genannt hat

**Nicht im Bestand als Regel, aber als Begriff.** Der Bestand kennt genau diese Sorge unter anderem Namen: `pm:independenceGround` verlangt bei jeder behaupteten Unabhängigkeit zweier Zeugen die Tatsache, die sie prüfbar macht, und die Notiz dort begründet die umgekehrte Beweislast damit, dass eine Rückwirkung des veröffentlichten Berichts auf das beschriebene Feld sich fast nie nachweisen lässt.

Das ist dieselbe Struktur: eine Bestätigung ist wertlos, wenn der Bestätigende die Information von dem hat, der sich bestätigen lässt. Der Entwurf sagt es für den Einzelfall, der Bestand für Traditionszeugen. **Beide haben unabhängig dieselbe Kontaminationsfrage gefunden**, und keiner hat sie vom anderen.

### 10-07 — Nur der Überschuss über die Basisrate zählt

**Im Bestand als Vorrichtung.** `pm:baseRate` ist genau das, und es steht seit dem Anfang. `pmc:ParalysisUniversalityProtocol` trägt eine ausgerechnete Rate, `pmc:HeatWithoutBreathProtocol` eine Vergleichsbedingung an denselben Teilnehmern, `pmc:AzandePoisonOracleExamination` die Grundlage seiner Zählung.

Die Deckung ist vollständig und der Entwurf sagt nichts, was der Bestand nicht schon tut.

### 10-08 — Fehlschläge sind gleichgewichtig zu protokollieren

**Im Bestand als Vorrichtung, und schärfer als der Entwurf.** Dass beide Ausgänge gleich zu führen sind, liegt in der Existenz von `pm:casesWithDeviation` neben `pm:casesWithoutDeviation`. Der Bestand geht darüber hinaus: `SPEC.md` §13 verbietet ausdrücklich, dass ein ungeprüfter Stand mit einem geprüft-nicht-gestützten zusammenfällt, und `pm:noProcedureDevised` existiert allein dafür.

Die Verschärfung ist der Punkt. Der Entwurf verlangt, Fehlschläge nicht zu unterschlagen; der Bestand verlangt zusätzlich, ein Nichtwissen nicht als Fehlschlag zu buchen. Das ist die häufigere Fälschungsrichtung, und der Entwurf hat sie nicht.

### 10-09 — Dreißig Fälle ohne Abweichung falsifizieren den Maximalanspruch

**Nicht im Bestand, und die Abweichung ist beabsichtigt.** Der Bestand setzt keine Fallzahlschwelle. `pm:caseCount` zählt, `pm:examinationState` sagt, wie weit gezählt wurde, und keine Zahl kippt einen Stand automatisch.

Der Grund steht in der Sache: eine feste Schwelle über alle Behauptungen hinweg unterstellt, dass sie dieselbe Effektgröße und dieselbe Basisrate haben. Dreißig Fälle sind für einen seltenen Effekt nichts und für einen häufigen viel. Eine solche Zahl in die Ontologie zu schreiben hieße, eine statistische Annahme als Vokabular festzuschreiben, und das wäre nicht rückholbar, sobald Knoten daran hängen.

**Der Entwurf hat hier eine Regel, die der Bestand bewusst nicht will.** Das ist der Fall, um dessentwillen dieses Blatt geschrieben wurde: die Aufzählung sollte Lücken zeigen, und einer der Punkte ist keine Lücke, sondern eine Entscheidung.

## Was der Vergleich insgesamt ergibt

Von sieben Regeln sind zwei im Bestand als Vorrichtung erzwungen (10-07, 10-08), eine als Begriff in anderer Reichweite vorhanden (10-06), eine als Praxis ohne Vorrichtung befolgt (10-01), zwei nicht vorhanden mit nachvollziehbarem Grund (10-05, 10-09), und eine ist gar keine Regel, sondern ein fehlplatzierter Falsifikator (10-03).

**Keine Lücke der Spezifikation.** Kein Punkt aus §10 verlangt eine Vorrichtung, die dem Bestand fehlt und die er haben sollte. Zwei Stellen tragen die Regel nur als Sorgfalt statt als Wächter, und beide sind Fälle, in denen ein Wächter nicht baubar ist.

Und ein Nebenertrag, der mehr wiegt als die Bilanz: an drei Stellen — Kontamination durch Vorwissen, Überschuss über die Basisrate, Gleichbehandlung beider Ausgänge — sind zwei getrennt entstandene Texte auf dieselbe Regel gekommen. Das ist die Sorte Konvergenz, die der Bestand bei Traditionen protokolliert. Bei den eigenen Verfahren protokolliert er sie nicht, und dieses Blatt ist der Ersatz dafür.
