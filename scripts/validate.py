#!/usr/bin/env python3
"""SHACL validation of all .ttl files in ontology/ and traditions/.

Exits 0 on a conforming graph, 1 otherwise. The pyshacl validation report is
written to stderr on failure.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from pyshacl import validate
from rdflib import Graph

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SHAPES = REPO_ROOT / "shapes" / "prima-materia.shapes.ttl"
DEFAULT_DATA_DIRS = (REPO_ROOT / "ontology", REPO_ROOT / "traditions")


def _iter_ttl(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from sorted(path.rglob("*.ttl"))
        elif path.is_file() and path.suffix == ".ttl":
            yield path


def _load_graph(paths: Iterable[Path]) -> Graph:
    graph = Graph()
    for ttl in _iter_ttl(paths):
        graph.parse(ttl, format="turtle")
    return graph


def run(shapes_path: Path, data_paths: Iterable[Path]) -> tuple[bool, str]:
    shapes_graph = Graph().parse(shapes_path, format="turtle")
    data_graph = _load_graph(data_paths)

    conforms, _report_graph, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="none",
        advanced=True,
        meta_shacl=False,
        debug=False,
    )
    return conforms, report_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shapes",
        type=Path,
        default=DEFAULT_SHAPES,
        help="Path to the SHACL shapes file (default: shapes/prima-materia.shapes.ttl).",
    )
    parser.add_argument(
        "--data",
        type=Path,
        nargs="+",
        default=list(DEFAULT_DATA_DIRS),
        help="Files or directories with .ttl data to validate (default: ontology/ traditions/).",
    )
    args = parser.parse_args(argv)

    conforms, report_text = run(args.shapes, args.data)
    if conforms:
        print("SHACL validation: conforms")
        return 0

    print("SHACL validation: FAILED", file=sys.stderr)
    print(report_text, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
