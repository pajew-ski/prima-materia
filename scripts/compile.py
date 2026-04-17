#!/usr/bin/env python3
"""Compile all .ttl fragments in ontology/ and traditions/ into one graph.

Writes a single Turtle file containing the union of every fragment. The
operation is idempotent and performs no network calls.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from rdflib import Graph
from rdflib.namespace import NamespaceManager

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUTS = (REPO_ROOT / "ontology", REPO_ROOT / "traditions")
DEFAULT_OUTPUT = REPO_ROOT / "build" / "prima-materia.ttl"

PREFIXES: dict[str, str] = {
    "pm": "https://pajew-ski.github.io/prima-materia/ontology#",
    "pmt": "https://pajew-ski.github.io/prima-materia/traditions/",
    "pmc": "https://pajew-ski.github.io/prima-materia/concepts/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",
    "sh": "http://www.w3.org/ns/shacl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def _iter_ttl(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from sorted(path.rglob("*.ttl"))
        elif path.is_file() and path.suffix == ".ttl":
            yield path


def compile_graph(inputs: Iterable[Path]) -> Graph:
    graph = Graph()
    nm: NamespaceManager = graph.namespace_manager
    for prefix, iri in PREFIXES.items():
        nm.bind(prefix, iri, override=True, replace=True)

    for ttl in _iter_ttl(inputs):
        graph.parse(ttl, format="turtle")
    return graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inputs",
        type=Path,
        nargs="+",
        default=list(DEFAULT_INPUTS),
        help="Files or directories whose .ttl contents are merged (default: ontology/ traditions/).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output TTL path (default: build/prima-materia.ttl).",
    )
    args = parser.parse_args(argv)

    graph = compile_graph(args.inputs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=args.output, format="turtle")
    print(f"Wrote {len(graph)} triples to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
