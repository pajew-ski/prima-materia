#!/usr/bin/env python3
"""Assemble the static GitHub Pages site from the compiled ontology.

Copies the hand-written assets in site/ into the output directory, derives
the visualization data from the merged graph, and places the distributable
serialisations next to it so the namespace host also serves the ontology
itself. No network calls: everything is read from the working tree.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from rdflib import OWL, RDF, RDFS, SKOS, Graph, Literal, Namespace, URIRef
from rdflib.term import Node

import compile as compile_script
import transmute as transmute_script

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ASSETS = REPO_ROOT / "site"
DEFAULT_INPUTS = (
    REPO_ROOT / "ontology",
    REPO_ROOT / "traditions",
    REPO_ROOT / "convergences",
    REPO_ROOT / "examinations",
    REPO_ROOT / "originations",
    REPO_ROOT / "generalizations",
)
DEFAULT_CONTEXT = REPO_ROOT / "context" / "prima-materia-context.jsonld"
DEFAULT_OUTPUT = REPO_ROOT / "build" / "site"

PM = Namespace("https://pajew.ski/prima-materia/ontology#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

# The namespace host is where the ontology is both named and served, so the
# discovery file points there and not at a mirror. A mirror can move; the
# namespace cannot.
SITE_BASE = "https://pajew.ski/prima-materia/"
SOURCE_REPO = "https://github.com/pajew-ski/prima-materia"

# Selective loading. The graph has three layers, and the namespaces already
# mark them: pm: is vocabulary, pmt:/pmc:/pmp: is content. A cut by tradition
# alone would not be a partition — the nodes that belong to no tradition are
# the convergences, disputes, orderings and examinations, which is the yield of
# the project and not a remainder. So the cut is vocabulary, one part per
# tradition, and one part for everything that belongs to none.
PARTS_DIR = "parts"
VOCABULARY_BASE = "https://pajew.ski/prima-materia/ontology"

# Prefixes the site renders as CURIEs. Longest IRI first so pm: never swallows
# a pmt:/pmc: term by accident.
PREFIXES: tuple[tuple[str, str], ...] = (
    ("pmt", "https://pajew.ski/prima-materia/traditions/"),
    ("pmc", "https://pajew.ski/prima-materia/concepts/"),
    ("pmp", "https://pajew.ski/prima-materia/practices/"),
    ("pm", "https://pajew.ski/prima-materia/ontology#"),
    ("owl", "http://www.w3.org/2002/07/owl#"),
    ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
    ("skos", "http://www.w3.org/2004/02/skos/core#"),
    ("dcterms", "http://purl.org/dc/terms/"),
)

# Structural predicates get an explicit label; every other pm: object property
# is rendered under its own name, so new relations appear without a code change.
STRUCTURAL_EDGES: tuple[tuple[URIRef, str], ...] = (
    (RDFS.subClassOf, "subClassOf"),
    (RDFS.domain, "domain"),
    (RDFS.range, "range"),
)

PROPERTY_TYPES = (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty)


def curie(iri: Node) -> str:
    """Shorten a known IRI to prefix:local, leaving anything else verbatim."""
    text = str(iri)
    for prefix, base in PREFIXES:
        if text.startswith(base):
            return f"{prefix}:{text[len(base):]}"
    return text


def _langs(graph: Graph, subject: Node, predicate: URIRef) -> dict[str, str]:
    """Language-tagged literals as {tag: text}; untagged values land under ''."""
    values: dict[str, str] = {}
    for obj in graph.objects(subject, predicate):
        if isinstance(obj, Literal):
            values.setdefault(obj.language or "", str(obj))
    return values


def _plain(graph: Graph, subject: Node, predicate: URIRef) -> list[str]:
    return sorted(str(obj) for obj in graph.objects(subject, predicate))


# The literal-valued predicates the node record already carries under a name of
# its own. Every other literal on a subject is carried as a statement, so a
# property added to the ontology is on the page the same day rather than on the
# day someone remembers to name it here.
NAMED_LITERALS = frozenset(
    {RDFS.label, SKOS.altLabel, SKOS.definition, SKOS.note, RDFS.comment, DCTERMS.source}
)


def _property_label(graph: Graph, predicate: URIRef) -> str:
    """What to call a predicate in the panel: its own label, or its name read out."""
    labels = _langs(graph, predicate, RDFS.label)
    named = labels.get("en") or labels.get("")
    if named:
        return named
    local = curie(predicate).split(":", 1)[-1]
    return re.sub(r"(?<!^)(?=[A-Z])", " ", local).lower()


def _statements(graph: Graph, subject: URIRef) -> list[dict]:
    """Everything else the graph says about a subject in literals.

    These carry the evidential weight of a claim and were the part the site
    dropped: what a text says follows from skipping a step, the contact route
    behind a convergence, the research an examination rests on, who compiled an
    ordering, and what a modern claim is commonly taken for. A definition
    without them reads as a report; with them it reads as a claim with a case.
    """
    predicates = {p for p in graph.predicates(subject, None) if isinstance(p, URIRef)}
    out: list[dict] = []
    for predicate in sorted(predicates - NAMED_LITERALS, key=str):
        values = sorted(
            str(obj) for obj in graph.objects(subject, predicate) if isinstance(obj, Literal)
        )
        if values:
            out.append(
                {
                    "property": curie(predicate),
                    "label": _property_label(graph, predicate),
                    "values": values,
                }
            )
    return out


def _kind(graph: Graph, subject: URIRef) -> str | None:
    """Classify a subject into one of the shapes the visualization draws."""
    types = set(graph.objects(subject, RDF.type))
    if OWL.Class in types:
        return "root" if subject == PM.Process else "class"
    if types & set(PROPERTY_TYPES):
        return "property"
    if PM.Tradition in types:
        return "tradition"
    if types & set(graph.subjects(RDF.type, OWL.Class)):
        return "instance"
    return None


def _node(graph: Graph, subject: URIRef, kind: str) -> dict:
    labels = _langs(graph, subject, RDFS.label)
    node = {
        "id": curie(subject),
        "iri": str(subject),
        "kind": kind,
        # Instances carry the class they instantiate; classes and properties
        # carry their OWL type. Either way the panel has one line of provenance.
        "types": sorted(
            curie(t) for t in graph.objects(subject, RDF.type) if isinstance(t, URIRef)
        ),
        "label": labels.get("en") or labels.get("") or curie(subject).split(":", 1)[-1],
        "labels": labels,
        # An alternate spelling is what a reader who met the name elsewhere will
        # type. Kept beside the labels rather than among the statements below,
        # because for search it is a name and not a remark.
        "altLabels": _plain(graph, subject, SKOS.altLabel),
        "definition": _langs(graph, subject, SKOS.definition),
        "note": _langs(graph, subject, SKOS.note),
        "comment": _langs(graph, subject, RDFS.comment),
        "sources": _plain(graph, subject, DCTERMS.source),
        "statements": _statements(graph, subject),
    }

    # A property's signature is shown even where it points outside this
    # ontology — pm:assertedIn has rdf:Statement as its domain, which is
    # vocabulary rather than a node the graph draws.
    if kind == "property":
        for predicate, key in ((RDFS.domain, "domain"), (RDFS.range, "range")):
            values = sorted(
                curie(o) for o in graph.objects(subject, predicate) if isinstance(o, URIRef)
            )
            if values:
                node[key] = values
    return node


def _object_properties(graph: Graph) -> list[URIRef]:
    return sorted(
        (s for s in graph.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, URIRef)),
        key=str,
    )


def build_data(graph: Graph) -> dict:
    """Derive nodes and edges for the visualization from the merged graph."""
    subjects = sorted(
        {s for s in graph.subjects() if isinstance(s, URIRef)}, key=str
    )
    nodes: list[dict] = []
    kinds: dict[URIRef, str] = {}
    for subject in subjects:
        kind = _kind(graph, subject)
        if kind is None:
            continue
        kinds[subject] = kind
        nodes.append(_node(graph, subject, kind))

    edges: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    def add(source: Node, rel: str, target: Node) -> None:
        if source not in kinds or target not in kinds or source == target:
            return
        key = (curie(source), rel, curie(target))
        if key in seen:
            return
        seen.add(key)
        edges.append({"source": key[0], "rel": rel, "target": key[2]})

    for predicate, rel in STRUCTURAL_EDGES:
        for source, target in graph.subject_objects(predicate):
            add(source, rel, target)

    # rdf:type only counts as an edge when it points at a class of this
    # ontology — owl:Class and owl:ObjectProperty are vocabulary, not content.
    for source, target in graph.subject_objects(RDF.type):
        if (target, RDF.type, OWL.Class) in graph:
            add(source, "instanceOf", target)

    # Every pm: object property that is actually used becomes an edge under its
    # own name, so pm:withinTradition and later relations need no special case.
    for predicate in _object_properties(graph):
        for source, target in graph.subject_objects(predicate):
            add(source, curie(predicate).split(":", 1)[-1], target)

    return {
        "meta": {
            "title": "prima-materia",
            "triples": len(graph),
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            # Set by CI so the footer can point at the exact source commit.
            "commit": os.environ.get("PRIMA_MATERIA_COMMIT", ""),
        },
        "nodes": nodes,
        "edges": sorted(edges, key=lambda e: (e["source"], e["rel"], e["target"])),
    }


def _slug(subject: URIRef) -> str:
    """pmt:SaivaSakta -> saiva-sakta."""
    local = curie(subject).split(":", 1)[-1]
    return re.sub(r"(?<!^)(?=[A-Z])", "-", local).lower()


def _is_vocabulary(subject: Node) -> bool:
    return str(subject).startswith(VOCABULARY_BASE)


def _is_content(subject: Node) -> bool:
    """A term of this project that is not vocabulary: a tradition, a concept, a practice.

    Terms of owl:, rdfs: and skos: are neither. They are not carried by any
    part and need no stub, because a client that reads RDF at all already has
    them.
    """
    return str(subject).startswith(SITE_BASE) and not _is_vocabulary(subject)


def _stub(graph: Graph, subject: URIRef) -> list[tuple]:
    """Just enough of a foreign node that a reference does not dangle.

    A part carries whole nodes for what it is about and a name for what it
    points at. Without this a convergence in one part names six concepts that
    are nowhere in the file, and a client reading that part alone sees edges
    into nothing.
    """
    out = []
    for predicate in (RDF.type, RDFS.label, PM.withinTradition):
        for obj in graph.objects(subject, predicate):
            out.append((subject, predicate, obj))
    return out


def split_graph(graph: Graph) -> dict[str, Graph]:
    """Cut the graph into independently loadable parts.

    Returns {name: graph}: "vocabulary", "findings", and one entry per
    tradition under its slug. Every part is a subset of the whole graph, so a
    client that loads several never sees a triple the full serialisation does
    not have.
    """
    members: dict[str, set[URIRef]] = {"vocabulary": set(), "findings": set()}
    slugs: dict[URIRef, str] = {}

    for subject in graph.subjects(RDF.type, PM.Tradition):
        if isinstance(subject, URIRef):
            slug = _slug(subject)
            slugs[subject] = slug
            members[slug] = {subject}

    for subject in {s for s in graph.subjects() if isinstance(s, URIRef)}:
        if _is_vocabulary(subject):
            members["vocabulary"].add(subject)
            continue
        if subject in slugs:
            continue
        traditions = [
            o for o in graph.objects(subject, PM.withinTradition) if o in slugs
        ]
        if traditions:
            for tradition in traditions:
                members[slugs[tradition]].add(subject)
        else:
            members["findings"].add(subject)

    parts: dict[str, Graph] = {}
    for name, subjects in members.items():
        part = Graph()
        for prefix, base in PREFIXES:
            part.bind(prefix, Namespace(base))
        for subject in subjects:
            for predicate, obj in graph.predicate_objects(subject):
                part.add((subject, predicate, obj))
        # A stub names its own tradition, and that tradition then needs a name
        # too. Two rounds settle it, but the loop is written to a fixed point
        # rather than to the number two, because the next property that points
        # from one content node to another would silently break a count.
        named = set(subjects)
        while True:
            foreign = {
                o
                for o in part.objects()
                if isinstance(o, URIRef) and _is_content(o) and o not in named
            }
            if not foreign:
                break
            for subject in foreign:
                for triple in _stub(graph, subject):
                    part.add(triple)
            named |= foreign
        parts[name] = part
    return parts


def build_llms_txt(graph: Graph) -> str:
    """The discovery file an agent reads before it fetches anything.

    The list of traditions is derived from the graph and not from the
    directory: a file is a unit of the repository and not of the subject, two
    traditions can sit in one file, and a hand-kept list names files that stop
    existing. What a client wants to know is which transmissions the graph
    carries, and that question is answered by the pm:Tradition instances.
    """
    traditions = sorted(
        (subject for subject in graph.subjects(RDF.type, PM.Tradition) if isinstance(subject, URIRef)),
        key=lambda subject: str(subject),
    )

    lines = [
        "# prima-materia",
        "",
        "> Open-data ontology of magical and esoteric knowledge, built under a",
        "> consciousness-first design principle. It is an assay office and not a",
        "> collection: it holds no truths, only claims with an origin, and keeps a",
        "> claim separate from what attests it. Released under CC0 1.0.",
        "",
        "## Ontology Files",
        "",
        f"- [Full ontology (Turtle)]({SITE_BASE}prima-materia.ttl): the compiled graph",
        f"- [Full ontology (JSON-LD)]({SITE_BASE}prima-materia.jsonld): the same graph, JSON-LD serialisation",
        f"- [JSON-LD Context]({SITE_BASE}context.jsonld): standalone context for embedding in client systems",
        "",
        "## How to read a claim",
        "",
        "- Every claim carries at least one `dcterms:source` naming a received work,",
        "  the passage that bears it, and the edition it was read from. Never a URL.",
        "- `pm:attestedBy` says by which route the claim entered the record.",
        "  `pm:compilerInference` attests an ordering act, never the claim being ordered.",
        "- `pm:Converging` is a reading made by a compiler. A documented",
        "  `pm:transmissionPath` does not devalue the agreement — it says how the claim",
        "  travelled — but it bars counting the same statement twice.",
        "  `pm:independentAttestation` marks the witnesses that may be counted, and",
        "  carries `pm:independenceGround` saying when they were fixed or gathered.",
        "- `pm:Reworking` marks a station that took a claim over and added something the",
        "  exemplar does not have. That is what separates a chain of copies from a",
        "  series of attempts, and it is where a falsifying condition usually comes from.",
        "- The absence of a `pm:Testing` node means nobody has taken the examination up.",
        "  It does not mean the claim was examined and found wanting.",
        "",
        "## Loading less than the whole graph",
        "",
        "The graph is cut into parts that can be loaded on their own. Each part is",
        "a subset of the full serialisation, and each carries a name and a type for",
        "the nodes it points at but does not contain, so no reference dangles.",
        "",
        f"- [Vocabulary]({SITE_BASE}{PARTS_DIR}/vocabulary.ttl): the classes, properties and scales. Load this with any other part; without it the rest is not interpretable.",
        f"- [Findings]({SITE_BASE}{PARTS_DIR}/findings.ttl): every node that belongs to no single tradition — the convergences, the disputes, the examinations, and the orderings held as modern. This is what the project is for, and a cut by tradition alone would drop all of it.",
        "- One part per tradition, linked in the list below.",
        "",
        "Turtle is listed; the same parts exist as `.jsonld` beside them.",
        "",
        "## Traditions",
        "",
    ]

    for subject in traditions:
        labels = _langs(graph, subject, RDFS.label)
        label = labels.get("en") or labels.get("") or curie(subject).split(":", 1)[-1]
        definitions = _langs(graph, subject, SKOS.definition)
        definition = definitions.get("en") or definitions.get("")
        entry = f"- [{label}]({SITE_BASE}#{curie(subject)})"
        part = f" [[part]({SITE_BASE}{PARTS_DIR}/{_slug(subject)}.ttl)]"
        lines.append((f"{entry}: {definition}" if definition else entry) + part)

    lines += [
        "",
        "## Optional",
        "",
        f"- [Source repository]({SOURCE_REPO})",
        f"- [Specification]({SOURCE_REPO}/blob/main/SPEC.md)",
        f"- [Claims not yet answered by the graph]({SOURCE_REPO}/issues)",
        "",
    ]
    return "\n".join(lines)


def publish(
    assets: Path,
    inputs: Iterable[Path],
    context: Path,
    output: Path,
) -> dict:
    graph = compile_script.compile_graph(inputs)
    data = build_data(graph)

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(assets, output)

    (output / "ontology-data.json").write_text(
        json.dumps(data, indent=2, sort_keys=False, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # The distributable serialisations ship with the site so that the namespace
    # host answers for the ontology it names, not just for the page about it.
    turtle = output / "prima-materia.ttl"
    graph.serialize(destination=turtle, format="turtle")
    transmute_script.transmute(turtle, context, output / "prima-materia.jsonld")
    shutil.copy(context, output / "context.jsonld")

    parts = output / PARTS_DIR
    parts.mkdir(parents=True, exist_ok=True)
    for name, part in split_graph(graph).items():
        part_turtle = parts / f"{name}.ttl"
        part.serialize(destination=part_turtle, format="turtle")
        transmute_script.transmute(part_turtle, context, parts / f"{name}.jsonld")

    (output / "llms.txt").write_text(build_llms_txt(graph), encoding="utf-8")

    # GitHub Pages serves through Jekyll unless told otherwise; the marker keeps
    # it from filtering files and directories whose names start with an
    # underscore, and skips a build step the site does not need.
    (output / ".nojekyll").write_text("", encoding="utf-8")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--assets",
        type=Path,
        default=DEFAULT_ASSETS,
        help="Directory with the hand-written site assets (default: site/).",
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        nargs="+",
        default=list(DEFAULT_INPUTS),
        help="Files or directories whose .ttl contents are merged (default: ontology/ traditions/).",
    )
    parser.add_argument(
        "--context",
        type=Path,
        default=DEFAULT_CONTEXT,
        help="JSON-LD context file (default: context/prima-materia-context.jsonld).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output directory for the generated site (default: build/site).",
    )
    args = parser.parse_args(argv)

    data = publish(args.assets, args.inputs, args.context, args.output)
    print(
        f"Wrote {len(data['nodes'])} nodes and {len(data['edges'])} edges "
        f"from {data['meta']['triples']} triples to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
