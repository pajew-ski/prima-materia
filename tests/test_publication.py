"""Publication tests: the site build derives a complete graph from the sources."""
from __future__ import annotations

import json
from pathlib import Path

from rdflib import RDF, Graph, Literal, Namespace, URIRef

import compile as compile_script
import publish as publish_script

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "site"
ONTOLOGY_DIR = REPO_ROOT / "ontology"
TRADITIONS_DIR = REPO_ROOT / "traditions"
CONTEXT = REPO_ROOT / "context" / "prima-materia-context.jsonld"

PM = Namespace("https://pajew.ski/prima-materia/ontology#")

# Assets the page loads by name; a rename that misses one breaks the site
# silently, because a missing module logs to the console and nowhere else.
REQUIRED_ASSETS = (
    "index.html",
    "style.css",
    "ontology.js",
    "theme.js",
    "search.js",
    "layouts.js",
    "matrix.js",
    "ontology/index.html",
)


def _data() -> dict:
    graph = compile_script.compile_graph([ONTOLOGY_DIR, TRADITIONS_DIR])
    return publish_script.build_data(graph)


def _full_data() -> dict:
    """Every source directory the site is built from, not just the first two."""
    return publish_script.build_data(compile_script.compile_graph(publish_script.DEFAULT_INPUTS))


def _by_id(data: dict) -> dict[str, dict]:
    return {node["id"]: node for node in data["nodes"]}


def test_assets_are_present() -> None:
    for name in REQUIRED_ASSETS:
        assert (ASSETS_DIR / name).is_file(), f"site/{name} is missing"


def test_every_declared_term_becomes_a_node() -> None:
    nodes = _by_id(_data())
    for term in ("pm:Process", "pm:Symbolizing", "pm:SensoryAnchoring", "pm:withinTradition",
                 "pm:withdrawnAbsorption", "pm:individualAwareness"):
        assert term in nodes, f"{term} is missing from the site data"


def test_kinds_are_classified() -> None:
    nodes = _by_id(_data())
    assert nodes["pm:Process"]["kind"] == "root"
    assert nodes["pm:Symbolizing"]["kind"] == "class"
    assert nodes["pm:withinTradition"]["kind"] == "property"
    assert nodes["pm:withdrawnAbsorption"]["kind"] == "instance"


def test_ontology_header_is_not_a_node() -> None:
    # The owl:Ontology declaration describes the file, not a term in it.
    assert "https://pajew.ski/prima-materia/ontology" not in {
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


def test_every_literal_reaches_the_site() -> None:
    # The page is fed entirely from the graph, which has to mean every literal
    # and not just the six the record names. A property added to the ontology
    # must appear without an edit here; the ones below are only the witnesses.
    graph = compile_script.compile_graph(publish_script.DEFAULT_INPUTS)
    data = publish_script.build_data(graph)
    nodes = _by_id(data)

    carried = {
        (node["id"], statement["property"], value)
        for node in data["nodes"]
        for statement in node["statements"]
        for value in statement["values"]
    }
    named = publish_script.NAMED_LITERALS
    for subject, predicate, obj in graph:
        if predicate in named or not isinstance(obj, Literal):
            continue
        term = publish_script.curie(subject)
        if term not in nodes:
            continue  # the ontology header describes the file, not a term
        assert (term, publish_script.curie(predicate), str(obj)) in carried, (
            f"{term} {publish_script.curie(predicate)} is stated in the graph and dropped by the site"
        )


def test_statements_are_named_by_the_property_that_makes_them() -> None:
    nodes = _by_id(_full_data())
    statements = {s["property"]: s for s in nodes["pmc:HawkinsConsciousnessScale"]["statements"]}
    # The circulating ascription is the finding, not an addendum to it.
    assert statements["pm:circulatesAs"]["label"] == "circulates as"
    assert statements["pm:circulatesAs"]["values"][0].startswith("A perennial map")
    assert statements["pm:originatedBy"]["values"] == ["David R. Hawkins"]
    # A property with no label of its own is still named, from its own name.
    assert statements["dcterms:date"]["label"] == "date"


def test_evidence_is_never_folded_into_sources() -> None:
    # pm:evidenceFrom is a modern report contributing to a claim from outside;
    # dcterms:source is a witness of a tradition. Merging them on the page
    # would undo the separation the ontology draws to keep research admissible.
    node = _by_id(_full_data())["pmc:TummoHeatExamination"]
    evidence = [s for s in node["statements"] if s["property"] == "pm:evidenceFrom"]
    assert evidence and evidence[0]["values"]
    assert not any(value in node["sources"] for value in evidence[0]["values"])


def test_alternate_spellings_stay_with_the_labels() -> None:
    node = _by_id(_data())["pmc:Baraqel"]
    assert node["altLabels"] == ["Baraqijal"]
    assert not any(s["property"] == "skos:altLabel" for s in node["statements"])


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


def test_llms_txt_lists_every_tradition_in_the_graph() -> None:
    """The discovery file is derived, not kept by hand.

    A hand-kept list runs behind the corpus and eventually names transmissions
    that are not in the graph, or misses ones that are. It is derived from the
    pm:Tradition instances and not from the files in traditions/, because a
    file is a unit of the repository and not of the subject:
    greek-pneuma-hesychasm.ttl alone carries two traditions.
    """
    graph = compile_script.compile_graph(publish_script.DEFAULT_INPUTS)
    text = publish_script.build_llms_txt(graph)

    traditions = {
        publish_script.curie(subject)
        for subject in graph.subjects(RDF.type, publish_script.PM.Tradition)
        if isinstance(subject, URIRef)
    }
    assert traditions, "the fixture graph carries no tradition at all"
    for term in traditions:
        assert f"#{term}" in text, f"{term} is in the graph and missing from llms.txt"

    # The namespace host answers for the ontology it names. A discovery file
    # that sends a client to a mirror instead makes the mirror the address.
    assert "cdn.jsdelivr.net" not in text
    assert text.count(publish_script.SITE_BASE) >= 4


def test_publish_writes_the_discovery_file(tmp_path: Path) -> None:
    output = tmp_path / "site"
    publish_script.publish(ASSETS_DIR, [ONTOLOGY_DIR, TRADITIONS_DIR], CONTEXT, output)
    assert (output / "llms.txt").is_file()


def test_parts_partition_the_content_and_dangle_nothing() -> None:
    """The cut has to hold two things at once.

    Every content node lands in some part, so nothing is silently dropped —
    and in particular the nodes that belong to no tradition, which are the
    convergences, disputes, orderings and examinations this project exists to
    produce. A cut by tradition alone would leave exactly those behind.

    And no part points at a node it does not name. A part carries whole nodes
    for what it is about and a stub for what it references, because a client
    reading one part alone must not meet an edge into nothing.
    """
    graph = compile_script.compile_graph(publish_script.DEFAULT_INPUTS)
    parts = publish_script.split_graph(graph)

    assert "vocabulary" in parts and "findings" in parts
    for triple in (t for part in parts.values() for t in part):
        assert triple in graph, "a part carries a triple the whole graph does not"

    content = {
        s
        for s in graph.subjects()
        if isinstance(s, URIRef) and publish_script._is_content(s)
    }
    covered = {
        s
        for name, part in parts.items()
        if name != "vocabulary"
        for s in part.subjects()
        if isinstance(s, URIRef) and publish_script._is_content(s)
    }
    assert content <= covered, sorted(publish_script.curie(s) for s in content - covered)

    # The tradition-less nodes are the point of the findings part.
    tradition_less = {
        s
        for s in content
        if not any(graph.objects(s, publish_script.PM.withinTradition))
        and (s, RDF.type, publish_script.PM.Tradition) not in graph
    }
    assert tradition_less <= set(parts["findings"].subjects())

    for name, part in parts.items():
        named = set(part.subjects())
        for obj in part.objects():
            if isinstance(obj, URIRef) and publish_script._is_content(obj):
                assert obj in named, f"{name} points at {publish_script.curie(obj)} without naming it"


def test_publish_writes_the_parts(tmp_path: Path) -> None:
    output = tmp_path / "site"
    publish_script.publish(ASSETS_DIR, [ONTOLOGY_DIR, TRADITIONS_DIR], CONTEXT, output)
    parts = output / publish_script.PARTS_DIR
    assert (parts / "vocabulary.ttl").is_file()
    assert (parts / "findings.ttl").is_file()
    assert (parts / "vocabulary.jsonld").is_file()
