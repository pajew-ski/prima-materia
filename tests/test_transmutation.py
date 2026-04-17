"""Transmutation tests: TTL → JSON-LD round-trips via rdflib."""
from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, compare

import compile as compile_script
import transmute as transmute_script

REPO_ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_DIR = REPO_ROOT / "ontology"
TRADITIONS_DIR = REPO_ROOT / "traditions"
CONTEXT = REPO_ROOT / "context" / "prima-materia-context.jsonld"


def _build_ttl(tmp_path: Path) -> Path:
    output = tmp_path / "compiled.ttl"
    graph = compile_script.compile_graph([ONTOLOGY_DIR, TRADITIONS_DIR])
    graph.serialize(destination=output, format="turtle")
    return output


def test_transmute_writes_valid_jsonld(tmp_path: Path) -> None:
    ttl_path = _build_ttl(tmp_path)
    jsonld_path = tmp_path / "compiled.jsonld"

    transmute_script.transmute(ttl_path, CONTEXT, jsonld_path)

    assert jsonld_path.exists() and jsonld_path.stat().st_size > 0
    document = json.loads(jsonld_path.read_text(encoding="utf-8"))
    assert "@context" in document or "@graph" in document or isinstance(document, list)


def test_jsonld_roundtrips_back_to_ttl(tmp_path: Path) -> None:
    ttl_path = _build_ttl(tmp_path)
    jsonld_path = tmp_path / "compiled.jsonld"

    transmute_script.transmute(ttl_path, CONTEXT, jsonld_path)

    original = Graph().parse(ttl_path, format="turtle")
    reloaded = Graph().parse(jsonld_path, format="json-ld")

    iso_original = compare.to_isomorphic(original)
    iso_reloaded = compare.to_isomorphic(reloaded)
    assert iso_original == iso_reloaded, "TTL ↔ JSON-LD round-trip must preserve the graph."
