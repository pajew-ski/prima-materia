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
    @prefix pm:   <https://pajew.ski/prima-materia/ontology#> .
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
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .

    pmc:OrphanConcept a pm:Conceptualizing ;
        pm:withinTradition pmt:Placeholder .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Conceptualizing instance without dcterms:source must fail."
    assert "dcterms:source" in report


def test_concept_instance_without_tradition_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:FloatingConcept a pm:Conceptualizing ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Conceptualizing instance without pm:withinTradition must fail."
    assert "tradition" in report.lower()


def test_class_without_definition_is_rejected() -> None:
    offending = """
    @prefix pm:   <https://pajew.ski/prima-materia/ontology#> .
    @prefix owl:  <http://www.w3.org/2002/07/owl#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    pm:Whatevering a owl:Class ;
        rdfs:subClassOf pm:Process ;
        rdfs:label "Whatevering"@en .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A class without skos:definition must fail SHACL."
    assert "skos:definition" in report


def test_url_source_is_rejected() -> None:
    # Sources are literature, not links. A guard that has never been shown to
    # fire is not known to work, so the rule gets a fixture rather than trust.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:LinkedConcept a pm:Conceptualizing ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "https://example.org/some-page" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A dcterms:source that is a URL must fail SHACL."
    assert "never a URL" in report


def test_attribution_without_attestation_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:UnattestedAscription a pm:Attributing ;
        dcterms:source "1 Henoch 8:1" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "An attribution without pm:attestedBy must fail SHACL."
    assert "how it entered the record" in report


def test_compiler_inference_cannot_attest_an_attribution() -> None:
    # An order may belong to the compiler; the claim being ordered may not.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:InferredAscription a pm:Attributing ;
        pm:attestedBy pm:compilerInference ;
        dcterms:source "1 Henoch 8:1" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "Compiler inference must not attest an attribution."
    assert "ordering act" in report


def test_test_without_falsifier_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:UnfalsifiableProtocol a pm:Testing ;
        pm:caseCount 30 .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Testing node without pm:falsifiedBy must fail."
    assert "falsifying condition" in report


def test_test_without_examination_state_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:StatelessProtocol a pm:Testing ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-08-28" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Testing node without pm:examinationState must fail."
    assert "how far the examination has been carried" in report


def test_unexamined_claim_may_omit_the_falsifier() -> None:
    # The one permitted absence, and the reason the state vocabulary exists:
    # a claim nobody has devised a way to examine must be recordable as such,
    # and must not be forced to look like a claim that was examined and left
    # unsupported.
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:UnexaminedClaim a pm:Testing ;
        pm:examinationState pm:noProcedureDevised ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-08-28" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A protocol declared as having no devised procedure must conform.\n{report}"


def test_url_evidence_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:LinkedEvidence a pm:Testing ;
        pm:examinationState pm:noProcedureDevised ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-08-28" ;
        pm:evidenceFrom "https://example.org/some-study" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:evidenceFrom holding a URL must fail SHACL."
    assert "never a URL" in report


def test_prerequisite_without_strength_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:VagueOrdering a pm:Presupposing ;
        pm:dependentStep pmc:Later ;
        pm:priorStep pmc:Earlier ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Some work, some passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A prerequisite claim without pm:prerequisiteStrength must fail."
    assert "how firmly the source sets it" in report


def test_stated_necessity_without_consequence_is_rejected() -> None:
    # Claiming that a source sets a necessity obliges the claimant to say what
    # the source says goes wrong without it. Otherwise an order read as a
    # necessity would enter the record wearing the stronger label.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:UnsupportedNecessity a pm:Presupposing ;
        pm:dependentStep pmc:Later ;
        pm:priorStep pmc:Earlier ;
        pm:prerequisiteStrength pm:statedNecessity ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Some work, some passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:statedNecessity without pm:consequenceOfSkipping must fail."
    assert "consequence of skipping" in report


def test_prescribed_order_may_omit_the_consequence() -> None:
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:PlainOrdering a pm:Presupposing ;
        pm:dependentStep pmc:Later ;
        pm:priorStep pmc:Earlier ;
        pm:prerequisiteStrength pm:prescribedOrder ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Some work, some passage" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"An order that states no consequence must conform.\n{report}"


def test_dispute_with_one_source_is_rejected() -> None:
    # A disagreement reported from one side only is a position. Admitting it
    # as a dispute would let the record settle the matter by which side it
    # happened to have read.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:OneSidedDispute a pm:Disputing ;
        pm:disputedClaim pmc:SomeClaim ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Only one work, one passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A dispute citing a single source must fail SHACL."
    assert "one for each side" in report
