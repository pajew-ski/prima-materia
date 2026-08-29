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
)
DEFAULT_CONTEXT = REPO_ROOT / "context" / "prima-materia-context.jsonld"
DEFAULT_OUTPUT = REPO_ROOT / "build" / "site"

PM = Namespace("https://pajew.ski/prima-materia/ontology#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

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
        "definition": _langs(graph, subject, SKOS.definition),
        "note": _langs(graph, subject, SKOS.note),
        "comment": _langs(graph, subject, RDFS.comment),
        "sources": _plain(graph, subject, DCTERMS.source),
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
