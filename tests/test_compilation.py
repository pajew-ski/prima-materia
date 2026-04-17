"""Compilation tests: every TTL fragment parses and merges cleanly."""
from __future__ import annotations

from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, Namespace, URIRef

import compile as compile_script

REPO_ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_DIR = REPO_ROOT / "ontology"
TRADITIONS_DIR = REPO_ROOT / "traditions"

PM = Namespace("https://pajew-ski.github.io/prima-materia/ontology#")


def test_every_fragment_parses() -> None:
    fragments = list(ONTOLOGY_DIR.rglob("*.ttl")) + list(TRADITIONS_DIR.rglob("*.ttl"))
    assert fragments, "Expected at least one TTL fragment under ontology/ or traditions/."
    for ttl in fragments:
        Graph().parse(ttl, format="turtle")


def test_compile_produces_nonempty_graph() -> None:
    graph = compile_script.compile_graph([ONTOLOGY_DIR, TRADITIONS_DIR])
    assert len(graph) > 0, "Compiled graph must contain triples."


def test_compile_contains_root_process_class() -> None:
    graph = compile_script.compile_graph([ONTOLOGY_DIR, TRADITIONS_DIR])
    assert (PM.Process, RDF.type, OWL.Class) in graph


def test_compile_contains_process_subclasses() -> None:
    graph = compile_script.compile_graph([ONTOLOGY_DIR, TRADITIONS_DIR])
    expected = {
        PM.Symbolizing,
        PM.Manifesting,
        PM.Perceiving,
        PM.Practicing,
        PM.Tradition,
        PM.Conceptualizing,
        PM.Relating,
    }
    for cls in expected:
        assert (URIRef(cls), RDFS.subClassOf, PM.Process) in graph, f"{cls} must subclass pm:Process"


def test_compile_writes_turtle(tmp_path: Path) -> None:
    output = tmp_path / "compiled.ttl"
    compile_script.main(["--inputs", str(ONTOLOGY_DIR), str(TRADITIONS_DIR), "--output", str(output)])
    assert output.exists() and output.stat().st_size > 0

    reloaded = Graph().parse(output, format="turtle")
    assert len(reloaded) > 0
