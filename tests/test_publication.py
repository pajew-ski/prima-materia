"""Publication tests: the site build derives a complete graph from the sources."""
from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, Namespace

import compile as compile_script
import publish as publish_script

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "site"
ONTOLOGY_DIR = REPO_ROOT / "ontology"
TRADITIONS_DIR = REPO_ROOT / "traditions"
CONTEXT = REPO_ROOT / "context" / "prima-materia-context.jsonld"

PM = Namespace("https://w3id.org/prima-materia/ontology#")

# Assets the page loads by name; a rename that misses one breaks the site
# silently, because a missing module logs to the console and nowhere else.
REQUIRED_ASSETS = ("index.html", "style.css", "ontology.js", "theme.js", "ontology/index.html")


def _data() -> dict:
    graph = compile_script.compile_graph([ONTOLOGY_DIR, TRADITIONS_DIR])
    return publish_script.build_data(graph)


def _by_id(data: dict) -> dict[str, dict]:
    return {node["id"]: node for node in data["nodes"]}


def test_assets_are_present() -> None:
    for name in REQUIRED_ASSETS:
        assert (ASSETS_DIR / name).is_file(), f"site/{name} is missing"


def test_every_declared_term_becomes_a_node() -> None:
    nodes = _by_id(_data())
    for term in ("pm:Process", "pm:Symbolizing", "pm:AwarenessContext", "pm:withinTradition",
                 "pm:WakingState", "pm:individualAwareness"):
        assert term in nodes, f"{term} is missing from the site data"


def test_kinds_are_classified() -> None:
    nodes = _by_id(_data())
    assert nodes["pm:Process"]["kind"] == "root"
    assert nodes["pm:Symbolizing"]["kind"] == "class"
    assert nodes["pm:withinTradition"]["kind"] == "property"
    assert nodes["pm:WakingState"]["kind"] == "instance"


def test_ontology_header_is_not_a_node() -> None:
    # The owl:Ontology declaration describes the file, not a term in it.
    assert "https://w3id.org/prima-materia/ontology" not in {
        node["iri"] for node in _data()["nodes"]
    }


def test_labels_and_definitions_survive_the_build() -> None:
    node = _by_id(_data())["pm:Symbolizing"]
    assert node["labels"]["en"] == "Symbolizing"
    assert node["labels"]["de"] == "Symbolisieren"
    assert node["definition"]["en"].startswith("The act of one form standing for another")


def test_sources_survive_the_build() -> None:
    node = _by_id(_data())["pm:WakingState"]
    assert node["sources"] == ["Māṇḍūkya Upaniṣad, verse 3"]


def test_structural_edges_are_derived() -> None:
    edges = {(e["source"], e["rel"], e["target"]) for e in _data()["edges"]}
    assert ("pm:Symbolizing", "subClassOf", "pm:Process") in edges
    assert ("pm:WakingState", "instanceOf", "pm:AwarenessContext") in edges
    assert ("pm:withinTradition", "range", "pm:Tradition") in edges


def test_property_signature_keeps_targets_outside_the_graph() -> None:
    # rdf:Statement is vocabulary, not a node the graph draws; the panel still
    # has to be able to state the domain of pm:assertedIn.
    node = _by_id(_data())["pm:assertedIn"]
    assert node["domain"] == ["rdf:Statement"]
    assert node["range"] == ["pm:AwarenessContext"]


def test_edges_only_connect_nodes_that_exist() -> None:
    data = _data()
    ids = {node["id"] for node in data["nodes"]}
    for edge in data["edges"]:
        assert edge["source"] in ids and edge["target"] in ids, f"dangling edge: {edge}"


def test_publish_writes_a_complete_site(tmp_path: Path) -> None:
    output = tmp_path / "site"
    publish_script.main(
        [
            "--assets", str(ASSETS_DIR),
            "--inputs", str(ONTOLOGY_DIR), str(TRADITIONS_DIR),
            "--context", str(CONTEXT),
            "--output", str(output),
        ]
    )

    for name in (*REQUIRED_ASSETS, "ontology-data.json", "prima-materia.ttl",
                 "prima-materia.jsonld", "context.jsonld", ".nojekyll"):
        assert (output / name).is_file(), f"{name} is missing from the built site"

    data = json.loads((output / "ontology-data.json").read_text(encoding="utf-8"))
    assert data["nodes"] and data["edges"]
    assert data["meta"]["triples"] == len(
        compile_script.compile_graph([ONTOLOGY_DIR, TRADITIONS_DIR])
    )

    # The serialisations shipped with the site must be the same graph.
    assert len(Graph().parse(output / "prima-materia.ttl", format="turtle")) == data["meta"]["triples"]
    assert len(Graph().parse(output / "prima-materia.jsonld", format="json-ld")) == data["meta"]["triples"]


def test_namespace_page_hands_over_to_the_site() -> None:
    # The ontology namespace IRI has to resolve to the page that documents it,
    # and a dereferenced term IRI has to land on that term.
    page = (ASSETS_DIR / "ontology" / "index.html").read_text(encoding="utf-8")
    assert "../#pm:${term}" in page
    assert 'href="../prima-materia.ttl"' in page


def test_publish_is_idempotent(tmp_path: Path) -> None:
    output = tmp_path / "site"
    for _ in range(2):
        publish_script.publish(ASSETS_DIR, [ONTOLOGY_DIR, TRADITIONS_DIR], CONTEXT, output)
    assert (output / "index.html").is_file()
