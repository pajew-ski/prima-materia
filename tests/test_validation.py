"""SHACL validation tests for the seed ontology."""
from __future__ import annotations

from pathlib import Path

from pyshacl import validate
from rdflib import Graph

import validate as validate_script

REPO_ROOT = Path(__file__).resolve().parent.parent
SHAPES = REPO_ROOT / "shapes" / "prima-materia.shapes.ttl"
ONTOLOGY_DIR = REPO_ROOT / "ontology"


def _validate(data_ttl: str) -> tuple[bool, str]:
    data_graph = Graph()
    data_graph.parse(data=data_ttl, format="turtle")
    shapes_graph = Graph().parse(SHAPES, format="turtle")
    conforms, _, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="none",
        advanced=True,
        meta_shacl=False,
    )
    return conforms, report_text


def test_seed_ontology_conforms() -> None:
    conforms, report = validate_script.run(SHAPES, [ONTOLOGY_DIR])
    assert conforms, f"Seed ontology must conform to SHACL shapes.\n{report}"


def test_substance_class_is_rejected() -> None:
    offending = """
    @prefix pm:   <https://pajew-ski.github.io/prima-materia/ontology#> .
    @prefix owl:  <http://www.w3.org/2002/07/owl#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    pm:Symbol a owl:Class ;
        rdfs:label "Symbol"@en ;
        skos:definition "A static substance class; forbidden."@en .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:Symbol declared as owl:Class must fail SHACL."
    assert "Static substance classes" in report


def test_concept_instance_without_source_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew-ski.github.io/prima-materia/ontology#> .
    @prefix pmc: <https://pajew-ski.github.io/prima-materia/concepts/> .
    @prefix pmt: <https://pajew-ski.github.io/prima-materia/traditions/> .

    pmc:OrphanConcept a pm:Conceptualizing ;
        pm:withinTradition pmt:Placeholder .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Conceptualizing instance without dcterms:source must fail."
    assert "dcterms:source" in report


def test_concept_instance_without_tradition_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew-ski.github.io/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew-ski.github.io/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:FloatingConcept a pm:Conceptualizing ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Conceptualizing instance without pm:withinTradition must fail."
    assert "tradition" in report.lower()


def test_class_without_definition_is_rejected() -> None:
    offending = """
    @prefix pm:   <https://pajew-ski.github.io/prima-materia/ontology#> .
    @prefix owl:  <http://www.w3.org/2002/07/owl#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    pm:Whatevering a owl:Class ;
        rdfs:subClassOf pm:Process ;
        rdfs:label "Whatevering"@en .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A class without skos:definition must fail SHACL."
    assert "skos:definition" in report
