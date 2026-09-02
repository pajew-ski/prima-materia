# Contributing to prima-materia

Thank you for considering a contribution. The ontology is released under
CC0 1.0 — by submitting changes you agree that your contribution is
likewise dedicated to the public domain.

## Before You Open a Pull Request

1. Read `SPEC.md` end-to-end. It is the single source of truth. Where this
   file or `CLAUDE.md` conflict with `SPEC.md`, `SPEC.md` wins.
2. Run the local validation pipeline; it must pass before you push:
   ```bash
   pip install -r requirements.txt
   python scripts/validate.py
   pytest tests/
   ```
3. Keep commits small and atomic. Commit messages in the imperative mood.

## Ontology Conventions

- **Process, not substance.** Every new class is a gerund. Static-substance
  classes (`pm:Symbol`, `pm:Concept`, `pm:Entity`, `pm:Object`) are
  forbidden and will fail SHACL validation.
- **English identifiers.** URIs and class names stay in English; use
  `rdfs:label` with language tags (`@en`, `@de`, ...) for multilingual
  presentation.
- **Name the edition you read from.** Every source reference gives work,
  place and the edition or translation the writer actually used
  (`"Patañjali, Yogasūtra III.38 (trans. Bryant 2009)"`). Not because
  the witnesses are known to differ — that is known only after comparing
  them — but because a finding is relative to the search that produced
  it, and the edition is that relation. Where the reading is assembled
  from several editions, say so rather than smooth it over. See
  `SPEC.md §10`.
- **A file header may hold only what costs nothing when lost.** Turtle
  comments do not survive compilation. Structure of the file, a note for
  the next editor, the reason for the filing: fine. Any statement about
  the subject matter belongs on a node — as a `skos:note` on the
  tradition's `pmt:` instance if it concerns the file as a whole.
- **Sources are mandatory.** Every concept instance needs at least one
  `dcterms:source`, and it must name a work and the place in it that
  carries the claim. **No URLs of any
  kind**, DOI and open-access editions included — `pm:SourceIsLiteratureShape`
  rejects any value with an `http` prefix. Modern research never enters
  as `dcterms:source`; it belongs at `pm:evidenceFrom` on a `pm:Testing`
  node, where a DOI is admissible as a work identifier. See `SPEC.md §10`.
- **Tradition membership is mandatory.** Every concept instance needs
  `pm:withinTradition`.
- **Labels and definitions.** Every class needs `rdfs:label` and
  `skos:definition`.
- **Independence must be grounded.** A `pm:Converging` node that asserts
  `pm:independentAttestation` needs `pm:independenceGround`: when the
  testimony it relies on was fixed or gathered, and against which
  publication or route that date stands. Where the corpus comes from
  fieldwork, the ground also states the gathering situation, because
  feedback inside a single enquiry precedes any publication and no date
  catches it. See `SPEC.md §14`.
- **Reception is not a demotion.** A documented `pm:transmissionPath`
  does not devalue a correspondence; it only forbids counting the same
  statement twice. What is worth looking for in a chain is what a later
  station *added* — a term, a consequence, a caution, a sign, a condition
  of failure. That is `pm:Reworking`, and `pm:addedElement` must point at
  the node carrying the addition.

## Quellenführung (Source Discipline)

Do not reproduce copyrighted primary texts verbatim. Paraphrase and cite.
Cite the work and the place in it, never a link. Videos, blogs, wikis and
forum posts are a way into a search, never a citation: trace them back to
the work, then cite the work.

## Behauptungen einreichen

Du musst keine Recherche mitliefern und in keiner Tradition stehen, um
eine Behauptung beizutragen. **Öffne ein Issue.** Eine Behauptung, die
der vorhandene Korpus noch nicht beantwortet, wird mitrecherchiert,
sobald ihr Korpus an der Reihe ist.

Ein brauchbares Behauptungs-Issue enthält:

1. Die Behauptung in einem entscheidbaren Satz. „Der Atem trägt die
   Energie" ist entscheidbar, „Atem ist wichtig" nicht.
2. Woher sie stammt, falls bekannt — ein Buch, eine Schule, ein
   Methodenentwurf, eine eigene Beobachtung.
3. Falls schon gesucht wurde: wo, und mit welchem Ergebnis.

Das Issue bleibt offen, bis ein Knoten die Behauptung trägt. Der
vollständige Lebenslauf steht in `SPEC.md §13`.

### Label-Vokabular

Aus dieser Liste übernehmen, nicht aus dem Gedächtnis schreiben: GitHub
legt einen unbekannten Labelnamen stillschweigend als neues Label an,
statt den Aufruf abzuweisen, und erzeugt so ein zweites Bündel, das
niemandem auffällt.

| Label | Bedeutung |
|---|---|
| `behauptung` | Behauptung, keine Repo-Arbeit. Jedes Behauptungs-Issue trägt es |
| `strittig` | zwei **Quellen** widersprechen einander; Ziel ist ein `pm:Disputing`-Knoten. Nicht, wenn eine Quelle einem Methodenentwurf widerspricht — ein Entwurf ist keine Seite |
| `unbelegt` | Schließgrund: plausible Korpora erschöpft, keine Stelle gefunden |
| `nicht-graphfaehig` | Schließgrund: gegen keine Überlieferung entscheidbar |
| `entwurf:strom` | Herkunft: Methodenentwurf „Der Strom" |

Dazu je ein `korpus:`-Label pro geprüftem oder zu prüfendem Korpus. Sie
kumulieren und sind damit zugleich das Protokoll der Suchabdeckung:

- `korpus:daoistisch`
- `korpus:upanisadisch`
- `korpus:patanjala`
- `korpus:hathayoga`
- `korpus:saiva-sakta`
- `korpus:tibetisch`
- `korpus:theravada`
- `korpus:dramaturgie`
- `korpus:henochisch`
- `korpus:sefer-yetzirah`
- `korpus:platonisch`
- `korpus:graeco-roman`
- `korpus:eleusis`
- `korpus:stoisch`
- `korpus:hesychasmus`
- `korpus:wuestenvaeter`
- `korpus:unterscheidung`
- `korpus:sufismus`
- `korpus:neuplatonisch`
- `korpus:kabbalistisch`
- `korpus:islamisch`
- `korpus:inkubation`
- `korpus:orientalistik` (H. H. Wilson, Sellon, Barth, Monier-Williams und
  die übrige britische Indienwissenschaft des 19. Jh.)
- `korpus:theosophisch` (Blavatsky und die theosophische Publizistik)
- `korpus:lhp-milieu` (Temple of Set, Dragon Rouge, LaVey, Flowers und die
  Selbstdarstellungen dieses Milieus)
- `korpus:thelema` (Crowley und die thelemische Literatur)
- `korpus:ra-material` (das gechannelte Law-of-One-Korpus, 1981–1984)
- `korpus:madhyamaka` (Nāgārjuna und die Madhyamaka-Kommentatoren)
- `korpus:jung` (C. G. Jung, insbesondere Septem Sermones und Liber Novus)
- `korpus:gurdjieff` (Gurdjieff und Ouspensky)
- `korpus:gnostisch` (Nag Hammadi, Irenäus als Referent, valentinianische
  und sethianische Systeme)
- `korpus:modern` (für Behauptungen, deren Ort `pm:evidenceFrom` an einem
  `pm:Testing`-Knoten ist)
- `korpus:maori` (Shortland, Grey/Te Rangikāheke, White, Best, Ngā Mōteatea und
  die übrige verschriftlichte Māori-Überlieferung)
- `korpus:zuni` (Bunzel und die Zuni-Texte der Bureau-of-American-Ethnology-Berichte)
- `korpus:navajo` (Matthews, Wyman und die aufgezeichneten Diné-Zeremonialtexte)
- `korpus:midewiwin` (Hoffman, Dewdney, Angel und die Birkenrindenrollen der
  Anishinaabe-Medizingesellschaft)
- `korpus:inuit` (Rasmussen, Report of the Fifth Thule Expedition, Bände VII und
  VIII, und die übrigen aufgezeichneten Inuit-Zeugnisse)
- `korpus:ifa` (das Odù-Korpus und die Literatur zur Yoruba-Divination: Ellis
  1894, Johnson und Cole in Dennetts Anhang von 1906, Bascom, Abimbola,
  Maupoil für das Fon-Fa)
- `korpus:geomantie` (ʿilm al-raml und die von ihm abhängige oder mit ihm
  strittig verwandte Literatur: die arabische Sandkunst, die europäische
  Geomantie, das madagassische sikidy)
- `korpus:nahua` (Sahagún, Ruiz de Alarcón, Jacinto de la Serna, Ponce, die
  Codices und die übrige aufgezeichnete zentralmexikanische Überlieferung)
- `korpus:dogon` (Griaule, Masques dogons und Dieu d'eau; Griaule und
  Dieterlen, Un système soudanais de Sirius und Le renard pâle; Dieterlen,
  Les âmes des Dogon — die Feldwiederholungen gehören nicht dazu und gehen
  als `pm:evidenceFrom` ein, nie als Quelle)
- `korpus:azande` (Evans-Pritchard, Witchcraft, Oracles and Magic among the
  Azande; de Calonne-Beaufaict, Azande; Larken, An account of the Zande;
  Lagae, Les Azande ou Niam-Niam; Schweinfurth, The Heart of Africa, Bd. II,
  als frühester Zeuge — die Rationalitätsdebatte um Winch, Horton und Gluckman
  gehört nicht dazu und geht als `pm:evidenceFrom` ein, nie als Quelle)
- `korpus:andin` (Arriaga, Extirpación de la idolatría del Pirú; Molina,
  Relación de las fábulas y ritos de los incas; Guaman Poma de Ayala, Nueva
  corónica y buen gobierno; das Huarochirí-Manuskript und seine Übersetzungen;
  Polo de Ondegardo; Cobo, Historia del Nuevo Mundo, Buch XIII — die moderne
  Andinistik geht als `pm:evidenceFrom` ein, nie als Quelle)

Die Werte dieses Blocks benennen Korpora, für die noch keine Datei
existiert. Das ist beabsichtigt: nach `SPEC.md §14` ist ein solches Label
bereits die Nachfragemeldung, und ein zweites Verzeichnis dafür wird
nicht geführt.

Ein neuer `korpus:`-Wert wird hier eingetragen, bevor er vergeben wird.
Er benennt den Korpus, den man aufschlägt, nicht die Datei, in der er
später landet.

Er kommt als **neue Zeile ans Ende der Liste**, und keine bestehende Zeile
wird dabei angefasst. Deshalb trägt auch kein Eintrag ein abschließendes
Satzzeichen: solange die Liste in einem fortlaufenden Satz stand, musste
jeder Lauf den Punkt des letzten Eintrags in ein Komma verwandeln, und damit
schrieben zwei gleichzeitig laufende Traditionsläufe zwangsläufig auf
dieselbe Zeile. Der zweite Merge konfliktierte dann jedes Mal, obwohl sich
die neuen Werte inhaltlich nie ausschlossen. Ein reines Anhängen an
verschiedene Zeilen führt git dagegen ohne Handzusammenführung zusammen.

## Offline Reproducibility

Scripts in `scripts/` must remain offline-reproducible. No network calls.

## Distribution Repository

Never edit `pajew-ski/prima-materia-dist` directly — it is auto-generated
by the `distribute.yml` GitHub Action on each push to `main`.

## Scope

Phase 0 and Phase 1 are delivered. New traditions are not added by plan
any more: `SPEC.md §14` sets out the two entrances and the three
decisions that precede a new file. If a change goes beyond that, raise an
issue first. Ask rather than guess.
