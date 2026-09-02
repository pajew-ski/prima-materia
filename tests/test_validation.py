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


def test_undiscriminating_verdict_without_named_outcomes_is_rejected() -> None:
    # The verdict that a claim says nothing is cheap to reach and hard to
    # contest. Requiring the pair of outcomes it fails to separate is what
    # keeps the state a finding rather than an opinion.
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:VagueVerdict a pm:Testing ;
        pm:examinationState pm:claimDoesNotDiscriminate ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:claimDoesNotDiscriminate without pm:undividedOutcomes must fail."
    assert "treats alike" in report


def test_undiscriminating_verdict_with_named_outcomes_conforms() -> None:
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:NamedVerdict a pm:Testing ;
        pm:examinationState pm:claimDoesNotDiscriminate ;
        pm:undividedOutcomes "The threshold rising and the threshold falling." ;
        pm:counterSearch pm:counterSearchFoundNothing ;
        pm:counterSearchNote "Searched; nothing found." ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A named pair of undivided outcomes must conform.\n{report}"


def test_other_states_need_no_undivided_outcomes() -> None:
    # The guard must not spread to the four older states, whose protocols
    # have no such pair to name.
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:OrdinaryProtocol a pm:Testing ;
        pm:examinationState pm:casesWithoutDeviation ;
        pm:counterSearch pm:counterSearchFoundNothing ;
        pm:counterSearchNote "Searched; nothing found." ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"An ordinary protocol must not be caught by the new guard.\n{report}"


def test_evidence_without_counter_search_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:UnopposedEvidence a pm:Testing ;
        pm:examinationState pm:procedureWithoutCases ;
        pm:evidenceFrom "Some study, in some journal, 2020" ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:evidenceFrom without pm:counterSearch must fail."
    assert "opposing work" in report


def test_counter_search_without_note_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:BareState a pm:Testing ;
        pm:examinationState pm:procedureWithoutCases ;
        pm:evidenceFrom "Some study, in some journal, 2020" ;
        pm:counterSearch pm:counterSearchFoundNothing ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:counterSearch without pm:counterSearchNote must fail."
    assert "what was searched" in report


def test_cases_without_carried_counter_search_are_rejected() -> None:
    # The shape that carries the weight: a protocol may report cases only if
    # somebody looked for the work that would unsettle them.
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:UncheckedCases a pm:Testing ;
        pm:examinationState pm:casesWithoutDeviation ;
        pm:evidenceFrom "Some study, in some journal, 2020" ;
        pm:counterSearch pm:counterSearchNotCarried ;
        pm:counterSearchNote "Nobody looked." ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "Cases reported without a carried counter-search must fail."
    assert "must have carried the counter-search" in report


def test_cases_with_carried_counter_search_conform() -> None:
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:CheckedCases a pm:Testing ;
        pm:examinationState pm:casesWithoutDeviation ;
        pm:evidenceFrom "Some study, in some journal, 2020" ;
        pm:counterSearch pm:counterSearchFoundNothing ;
        pm:counterSearchNote "Searched for replications and for critiques; none found." ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A carried counter-search must permit a case-bearing state.\n{report}"


def test_protocol_without_evidence_needs_no_counter_search() -> None:
    # The guard must not spread to protocols that cite nothing.
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:NoEvidence a pm:Testing ;
        pm:examinationState pm:procedureWithoutCases ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-02" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A protocol citing no evidence must not be caught.\n{report}"


def test_mediated_attestation_without_intermediary_is_rejected() -> None:
    # Declaring a claim second-hand costs nothing unless the second hand is
    # named. The mode exists so that an unreachable source can enter at its
    # true strength, not so that a node can wear a weaker label and stay vague
    # about whose reading it rests on.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:UnnamedIntermediary a pm:Attributing ;
        pm:attestedBy pm:mediatedAttestation ;
        dcterms:source "Some unreachable work, some passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:mediatedAttestation without pm:readVia must fail SHACL."
    assert "read in with pm:readVia" in report


def test_url_intermediary_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:LinkedIntermediary a pm:Attributing ;
        pm:attestedBy pm:mediatedAttestation ;
        pm:readVia "https://example.org/some-quotation" ;
        dcterms:source "Some unreachable work, some passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:readVia holding a URL must fail SHACL."
    assert "never a URL" in report


def test_mediated_attestation_with_named_intermediary_conforms() -> None:
    # The permitted shape: the work that carries the claim stays in
    # dcterms:source, because that is what a later reader must obtain; the
    # work actually read stands beside it and says so.
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:HonestlyMediated a pm:Attributing ;
        pm:attestedBy pm:mediatedAttestation ;
        pm:readVia "Some Editor, Some Study (1970), where the passage is quoted" ;
        dcterms:source "Some unreachable work, some passage" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A mediated claim naming its intermediary must conform.\n{report}"


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


def test_origination_without_circulating_ascription_is_rejected() -> None:
    # The ascription a claim circulates under is what makes the node a finding.
    # Without it the record holds a bibliography entry and calls it a discovery.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:BareOrigination a pm:Originating ;
        pm:originatedBy "Some Author" ;
        dcterms:date "1995" ;
        dcterms:source "Some Author, Some Book (1995)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "An origination without pm:circulatesAs must fail SHACL."
    assert "ascription the claim circulates under" in report


def test_origination_without_author_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:AnonymousOrigination a pm:Originating ;
        pm:circulatesAs "Ancient wisdom." ;
        dcterms:date "1995" ;
        dcterms:source "Some Book (1995)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "An origination without pm:originatedBy must fail SHACL."
    assert "author with whom the claim begins" in report


def test_positing_with_a_source_is_rejected() -> None:
    # A posited claim witnesses nothing. Letting it carry a source would make
    # an examined claim indistinguishable from a transmitted one at the point
    # where somebody reads the graph.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmp:     <https://pajew.ski/prima-materia/practices/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:SourcedPosit a pm:Positing ;
        pm:positedIn "prima-materia#13" ;
        dcterms:source "Some work, some passage" .

    pmp:SomeProtocol a pm:Testing ;
        pm:tests pmc:SourcedPosit ;
        pm:examinationState pm:noProcedureDevised ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-08-29" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Positing carrying dcterms:source must fail SHACL."
    assert "claims no source" in report


def test_positing_with_a_tradition_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmc:TraditionedPosit a pm:Positing ;
        pm:positedIn "prima-materia#13" ;
        pm:withinTradition pmt:Placeholder .

    pmp:AnotherProtocol a pm:Testing ;
        pm:tests pmc:TraditionedPosit ;
        pm:examinationState pm:noProcedureDevised ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-08-29" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Positing assigned to a tradition must fail SHACL."
    assert "belongs to no tradition" in report


def test_positing_without_an_examination_is_rejected() -> None:
    # The lock that keeps the class from becoming the channel through which an
    # unpublished draft enters the record. No object of examination without an
    # examination pointing at it.
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .

    pmc:UnexaminedPosit a pm:Positing ;
        pm:positedIn "prima-materia#13" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Positing with no pm:Testing pointing at it must fail SHACL."
    assert "no business in the graph" in report


def test_examined_posit_conforms() -> None:
    # The permitted shape, and the only one: a claim with no source and no
    # tradition, held solely because a protocol addresses it.
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmc:ExaminedPosit a pm:Positing ;
        pm:positedIn "prima-materia#13" .

    pmp:ItsProtocol a pm:Testing ;
        pm:tests pmc:ExaminedPosit ;
        pm:examinationState pm:noProcedureDevised ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-08-29" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A posited claim with an examination pointing at it must conform.\n{report}"


def test_convergence_claiming_independence_without_ground_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:UngroundedConvergence a pm:Converging ;
        pm:independentAttestation pmt:Placeholder ;
        pm:attestedBy pm:compilerInference ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A convergence asserting independence without a ground must fail."
    assert "independenceGround" in report


def test_convergence_on_a_transmission_path_alone_is_accepted() -> None:
    """The exception the shape allows: reception is a finding and needs no ground."""
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:ReceptionOnlyConvergence a pm:Converging ;
        pm:transmissionPath "A documented route (fixture)" ;
        pm:attestedBy pm:compilerInference ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A convergence resting on a transmission path alone must pass.\n{report}"


def test_reworking_without_added_element_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:EmptyReworking a pm:Reworking ;
        pm:reworkedClaim pmc:PlaceholderClaim ;
        pm:receivedFrom pmt:PlaceholderSource ;
        pm:attestedBy pm:textualAttestation ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A reworking that points at no addition must fail."
    assert "added" in report.lower()


def test_complete_reworking_is_accepted() -> None:
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:CompleteReworking a pm:Reworking ;
        pm:reworkedClaim pmc:PlaceholderClaim ;
        pm:receivedFrom pmt:PlaceholderSource ;
        pm:addedElement pmc:PlaceholderAddition ;
        pm:attestedBy pm:textualAttestation ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A complete reworking must pass.\n{report}"


def test_generalization_without_statement_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:SilentGeneralization a pm:Generalizing ;
        pm:attestedBy pm:compilerInference ;
        pm:generalizedFrom pmc:AttestedOne, pmc:AttestedTwo .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    pmc:AttestedTwo dcterms:source "Another work, another passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A generalization without pm:generalizedStatement must fail."
    assert "state the claim it makes" in report


def test_generalization_from_a_single_claim_is_rejected() -> None:
    # One claim generalized is one claim restated, and it would enter the
    # record without the source the original carried.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:ThinGeneralization a pm:Generalizing ;
        pm:generalizedStatement "Practices of a kind produce an effect of a kind." ;
        pm:attestedBy pm:compilerInference ;
        pm:generalizedFrom pmc:AttestedOne .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A generalization resting on one claim must fail."
    assert "one claim restated" in report.lower()


def test_generalization_claiming_textual_attestation_is_rejected() -> None:
    # The inversion of pm:CompilerInferenceScopeShape: here the compiler's
    # step is the only admissible attestation, because no source says it.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:OverclaimedGeneralization a pm:Generalizing ;
        pm:generalizedStatement "Practices of a kind produce an effect of a kind." ;
        pm:attestedBy pm:textualAttestation ;
        pm:generalizedFrom pmc:AttestedOne, pmc:AttestedTwo .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    pmc:AttestedTwo dcterms:source "Another work, another passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A generalization attested as textual must fail."
    assert "by nothing else" in report


def test_generalization_with_a_source_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:SourcedGeneralization a pm:Generalizing ;
        pm:generalizedStatement "Practices of a kind produce an effect of a kind." ;
        pm:attestedBy pm:compilerInference ;
        pm:generalizedFrom pmc:AttestedOne, pmc:AttestedTwo ;
        dcterms:source "Some work, some passage" .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    pmc:AttestedTwo dcterms:source "Another work, another passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A generalization carrying dcterms:source must fail."
    assert "claims no source" in report


def test_generalization_with_a_tradition_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:TraditionedGeneralization a pm:Generalizing ;
        pm:generalizedStatement "Practices of a kind produce an effect of a kind." ;
        pm:attestedBy pm:compilerInference ;
        pm:generalizedFrom pmc:AttestedOne, pmc:AttestedTwo ;
        pm:withinTradition pmt:Placeholder .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    pmc:AttestedTwo dcterms:source "Another work, another passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A generalization assigned to a tradition must fail."
    assert "belongs to no tradition" in report


def test_generalization_from_unattested_claims_is_rejected() -> None:
    # The lock. Without it the class would be the route by which an
    # unpublished method draft enters the record after all: a derivation whose
    # terms name no work is an assertion with a chain drawn around it.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:GroundlessGeneralization a pm:Generalizing ;
        pm:generalizedStatement "Practices of a kind produce an effect of a kind." ;
        pm:attestedBy pm:compilerInference ;
        pm:generalizedFrom pmc:AttestedOne, pmc:DraftSentence .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A generalization resting on an unattested node must fail."
    assert "must itself name a work" in report


def test_complete_generalization_conforms() -> None:
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:CompleteGeneralization a pm:Generalizing ;
        pm:generalizedStatement "Practices of a kind produce an effect of a kind." ;
        pm:attestedBy pm:compilerInference ;
        pm:generalizedFrom pmc:AttestedOne, pmc:AttestedTwo .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    pmc:AttestedTwo dcterms:source "Another work, another passage" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A generalization carrying its derivation must conform.\n{report}"


def test_generalization_without_an_examination_conforms() -> None:
    # The deliberate asymmetry against pm:Positing, and the reason this class
    # exists. A posited claim may live only where a protocol already points at
    # it; a generalization must be writable before anyone has taken the
    # examination up, because the set of generalizations without a pm:Testing
    # *is* the queue. A shape requiring the protocol here would make the queue
    # presuppose the work it exists to order.
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:UnexaminedGeneralization a pm:Generalizing ;
        pm:generalizedStatement "Practices of a kind produce an effect of a kind." ;
        pm:attestedBy pm:compilerInference ;
        pm:generalizedFrom pmc:AttestedOne, pmc:AttestedTwo .

    pmc:AttestedOne dcterms:source "Some work, some passage" .
    pmc:AttestedTwo dcterms:source "Another work, another passage" .
    """
    conforms, report = _validate(permitted)
    assert conforms, (
        "A generalization with no pm:Testing pointing at it must conform; "
        f"it is the queue for stage three.\n{report}"
    )


def test_naming_without_a_form_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:FormlessNaming a pm:Naming ;
        pm:nameRole "watcher" ;
        pm:attestedBy pm:textualAttestation ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "Some work, some passage (some edition)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A naming without pm:nameForm must fail SHACL."
    assert "as the cited edition spells it" in report


def test_naming_without_a_role_is_rejected() -> None:
    # A bearer without the term its own tradition uses has already been
    # harmonised by whoever left it out.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:RolelessNaming a pm:Naming ;
        pm:nameForm "Some Name" ;
        pm:attestedBy pm:textualAttestation ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "Some work, some passage (some edition)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A naming without pm:nameRole must fail SHACL."
    assert "takes the bearer to be" in report


def test_naming_without_a_tradition_is_rejected() -> None:
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:UnhousedNaming a pm:Naming ;
        pm:nameForm "Some Name" ;
        pm:nameRole "spirit" ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Some work, some passage (some edition)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A naming without pm:withinTradition must fail SHACL."
    assert "belongs to whoever gave it" in report


def test_complete_naming_conforms() -> None:
    # The shape a watcher node takes: the form as the cited edition spells
    # it, the term that edition's tradition uses, and the passage.
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:SomeNaming a pm:Naming ;
        pm:nameForm "Some Name" ;
        skos:altLabel "Another Transliteration" ;
        pm:nameRole "watcher" ;
        pm:attestedBy pm:textualAttestation ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "Some work, some passage (some edition)" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A complete naming must conform.\n{report}"
