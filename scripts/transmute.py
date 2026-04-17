#!/usr/bin/env python3
"""Transmute a compiled Turtle file into JSON-LD using a local context.

Reads the input TTL, emits JSON-LD serialised with the supplied context so
that consumers see stable, human-readable prefixes. No network calls.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "build" / "prima-materia.ttl"
DEFAULT_CONTEXT = REPO_ROOT / "context" / "prima-materia-context.jsonld"
DEFAULT_OUTPUT = REPO_ROOT / "build" / "prima-materia.jsonld"


def _load_context(context_path: Path) -> dict:
    with context_path.open("r", encoding="utf-8") as fh:
        document = json.load(fh)
    ctx = document.get("@context")
    if ctx is None:
        raise ValueError(f"{context_path} does not contain an @context entry")
    return ctx


def transmute(input_path: Path, context_path: Path, output_path: Path) -> None:
    graph = Graph()
    graph.parse(input_path, format="turtle")
    context = _load_context(context_path)

    serialized = graph.serialize(
        format="json-ld",
        context=context,
        auto_compact=True,
        indent=2,
        sort_keys=True,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        fh.write(serialized if isinstance(serialized, str) else serialized.decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Input TTL path (default: build/prima-materia.ttl).",
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
        help="Output JSON-LD path (default: build/prima-materia.jsonld).",
    )
    args = parser.parse_args(argv)

    transmute(args.input, args.context, args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
