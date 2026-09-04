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


def test_undiscriminating_verdict_needs_no_counter_search() -> None:
    # The exception pm:CasesRequireCounterSearchShape now makes. The state
    # reports no cases: it says the wording of the claim excludes no outcome,
    # which is read off the claim and not off evidence, so there is nothing
    # for a counter-search to search. While the state was coupled to that
    # duty, a verdict actually reached had to be entered as
    # pm:procedureWithoutCases, and the record understated its own work. See
    # prima-materia#499.
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:VerdictOnTheWording a pm:Testing ;
        pm:examinationState pm:claimDoesNotDiscriminate ;
        pm:undividedOutcomes "The spirit answering and the spirit withdrawing." ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-04" .
    """
    conforms, report = _validate(permitted)
    assert conforms, (
        "A verdict on the wording of a claim must be writable without a "
        f"counter-search; there is no evidence for one to search.\n{report}"
    )


def test_undiscriminating_verdict_citing_evidence_still_needs_a_counter_search() -> None:
    # The decoupling reaches only as far as its reason. A protocol that cites
    # evidence is held to the counter-search by pm:CounterSearchRequiredShape
    # whatever its state, because there a report about the world has been
    # taken up and the search for the work that would unsettle it is owed.
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmp: <https://pajew.ski/prima-materia/practices/> .

    pmp:EvidenceWithoutSearch a pm:Testing ;
        pm:examinationState pm:claimDoesNotDiscriminate ;
        pm:undividedOutcomes "The threshold rising and the threshold falling." ;
        pm:evidenceFrom "Some study, in some journal, 2020" ;
        pm:falsifiedBy "Some stated condition." ;
        pm:examinedBy "Someone" ;
        pm:protocolUpdated "2026-09-04" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "Evidence cited without any counter-search state must still fail."
    assert "opposing work" in report


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


def test_field_attestation_without_a_record_is_rejected() -> None:
    # Where no earlier text exists, the gathering is all a later reader has.
    # A field claim that does not say who spoke, who wrote it down, when,
    # where and in which language cites a book and hides the distance between
    # that book and the speaker.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:BareFieldClaim a pm:Attributing ;
        pm:attestedBy pm:fieldAttestation ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "Some Recorder, Some Field Report (1929), some page" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:fieldAttestation without pm:fieldRecord must fail SHACL."
    assert "pm:fieldRecord" in report


def test_field_attestation_with_a_record_conforms() -> None:
    # The permitted shape, and the reason the mode exists: a transmission that
    # commits nothing to writing can now enter at its own strength instead of
    # staying at corpus named for want of a text behind the report.
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:HonestFieldClaim a pm:Attributing ;
        pm:attestedBy pm:fieldAttestation ;
        pm:fieldRecord "Told by a named speaker to the recorder at a named place in the winter of 1922, in the speaker's own language; the work carries the original wording beside the translation." ;
        pm:withinTradition pmt:Placeholder ;
        dcterms:source "Some Recorder, Some Field Report (1929), some page" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A field claim stating its gathering must conform.\n{report}"


def test_receiving_without_circumstances_is_rejected() -> None:
    # A node naming only receiver and claimed speaker repeats the title page.
    # What can be weighed is the proceeding.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:BareReceiving a pm:Receiving ;
        pm:receivedBy "Some Medium" ;
        pm:claimedSpeaker "Some Claimed Speaker" ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Some Editor, Some Collection (1981), session 41" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A pm:Receiving without pm:receptionCircumstance must fail SHACL."
    assert "circumstances of the receiving" in report


def test_claimed_speaker_as_a_reference_is_rejected() -> None:
    # The claim must not be able to make itself true by the form of its own
    # entry. Pointing the claimed speaker at a named being would put into the
    # graph as a bearer what the node exists to record as a claim.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:SpeakerAsBeing a pm:Receiving ;
        pm:receivedBy "Some Medium" ;
        pm:claimedSpeaker pmc:SomeNamedBeing ;
        pm:receptionCircumstance "Received in a state the work calls trance, questions put by a named questioner, taken down by a third party; tape recordings of the sittings are said to exist." ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Some Editor, Some Collection (1981), session 41" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:claimedSpeaker pointing at a resource must fail SHACL."
    assert "as a literal" in report


def test_complete_receiving_conforms() -> None:
    # The permitted shape. The source names the work a reader can obtain; who
    # spoke in it is the claim, and it stands here where it can be disputed
    # instead of riding inside a citation.
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:CompleteReceiving a pm:Receiving ;
        pm:receivedBy "Some Medium" ;
        pm:claimedSpeaker "Some Claimed Speaker, as the work gives the name" ;
        pm:receptionCircumstance "Received in a state the work calls trance, questions put by a named questioner, taken down by a third party; tape recordings of the sittings are said to exist." ;
        pm:attestedBy pm:textualAttestation ;
        dcterms:source "Some Editor, Some Collection (1981), session 41" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A complete receiving must conform.\n{report}"


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


def test_url_principal_corpus_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .

    pmt:Linked a pm:Tradition ;
        pm:principalCorpus "https://example.org/some-corpus" ;
        pm:coverageState pm:corpusNamed .
    """
    conforms, report = _validate(offending)
    assert not conforms, "pm:principalCorpus holding a URL must fail SHACL."
    assert "never a URL" in report


def test_registration_with_a_source_is_rejected() -> None:
    # At corpus named nothing has been read, so there is no passage and no
    # edition to name. A registration carrying a source would be
    # indistinguishable from a worked tradition, and the denominator the state
    # exists to provide would be unreadable again.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmt:PrematurelySourced a pm:Tradition ;
        pm:principalCorpus "Some corpus, named as literature" ;
        pm:coverageState pm:corpusNamed ;
        dcterms:source "Some work, some passage (some edition)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A registration carrying dcterms:source must fail SHACL."
    assert "claims no dcterms:source" in report


def test_registration_without_a_source_conforms() -> None:
    permitted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .

    pmt:HonestRegistration a pm:Tradition ;
        pm:principalCorpus "Some corpus, named as literature" ;
        pm:coverageState pm:corpusNamed ;
        pm:contactRoute pm:contactRouteUndecided .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A registration that names a corpus and no passage must conform.\n{report}"


def test_worked_tradition_may_carry_a_source() -> None:
    # The guard must not spread past the state it belongs to.
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmt:Worked a pm:Tradition ;
        pm:principalCorpus "Some corpus, named as literature" ;
        pm:coverageState pm:placesEntered ;
        dcterms:source "Some work, some passage (some edition)" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A tradition with passages read must be allowed its sources.\n{report}"


def test_registered_tradition_as_independent_attestation_is_rejected() -> None:
    # The most expensive mistake available in this holding, because it does
    # not look like one: pm:independentAttestation is the predicate that turns
    # an agreement into a countable witness, and a registration witnesses
    # nothing. The rule stood in ontology/coverage.ttl as a definition and was
    # enforced by nobody.
    offending = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmt:MerelyRegistered a pm:Tradition ;
        pm:principalCorpus "Some corpus, named as literature" ;
        pm:coverageState pm:corpusNamed .

    pmc:PrematureConvergence a pm:Converging ;
        pm:independentAttestation pmt:MerelyRegistered ;
        pm:independenceGround "Some ground (fixture)" ;
        pm:attestedBy pm:compilerInference ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A convergence resting on a registered tradition must fail SHACL."
    assert "witnesses nothing" in report


def test_worked_tradition_as_independent_attestation_conforms() -> None:
    permitted = """
    @prefix pm:      <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc:     <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt:     <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmt:Entered a pm:Tradition ;
        pm:principalCorpus "Some corpus, named as literature" ;
        pm:coverageState pm:placesEntered .

    pmc:AdmissibleConvergence a pm:Converging ;
        pm:independentAttestation pmt:Entered ;
        pm:independenceGround "Some ground (fixture)" ;
        pm:attestedBy pm:compilerInference ;
        dcterms:source "Test source (fixture)" .
    """
    conforms, report = _validate(permitted)
    assert conforms, f"A convergence on a worked tradition must conform.\n{report}"


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


#
# Negative fixtures for the scale guards, required by SPEC §9. Until these
# shapes existed, rdfs:range was the only statement of closure and constrained
# nothing: a misspelt or invented value passed every constraint in silence.
#


def test_invented_attestation_mode_is_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:LooseAttribution a pm:Attributing ;
        pm:ascribedCapacity pmc:Something ;
        pm:attestedBy pm:textualAttestaton ;
        pm:withinTradition pmt:Somewhere ;
        dcterms:source "A work, a place" .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A mode of attestation that no scale declares must fail SHACL."
    assert "declared mode of attestation" in report


def test_declared_attestation_mode_is_accepted() -> None:
    accepted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .

    pmc:SoundAttribution a pm:Attributing ;
        pm:ascribedCapacity pmc:Something ;
        pm:attestedBy pm:textualAttestation ;
        pm:withinTradition pmt:Somewhere ;
        dcterms:source "A work, a place" .
    """
    conforms, report = _validate(accepted)
    assert conforms, report


def test_scale_without_a_family_is_rejected() -> None:
    offending = """
    @prefix pm: <https://pajew.ski/prima-materia/ontology#> .

    pm:SomeNewScale a pm:Scale .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A scale that does not declare its family must fail SHACL."
    assert "which family it belongs to" in report


#
# Negative fixtures for the placement guards. A placement is the compiler's
# identification of a described condition with a coordinate, and the two
# things it must never be able to omit are the coordinate's declaration and
# the ground on which the identification rests.
#

_SITUATING_PREFIXES = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .
    @prefix dcterms: <http://purl.org/dc/terms/> .
"""


def test_situating_without_a_ground_is_rejected() -> None:
    offending = _SITUATING_PREFIXES + """
    pmc:BarePlacement a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:withdrawnAbsorption ;
        pm:attestedBy pm:compilerInference .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A placement without a ground must fail SHACL."
    assert "what in the source carries it" in report


def test_situating_with_an_undeclared_value_is_rejected() -> None:
    offending = _SITUATING_PREFIXES + """
    pmc:InventedCoordinate a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:trance ;
        pm:situationGround "The source says the practitioner is entranced."@en ;
        pm:attestedBy pm:compilerInference .
    """
    conforms, report = _validate(offending)
    assert not conforms, "A coordinate no axis declares must fail SHACL."
    assert "declared axis value" in report


def test_situating_on_two_axes_at_once_is_rejected() -> None:
    offending = _SITUATING_PREFIXES + """
    pmc:TwoCoordinatesInOne a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:withdrawnAbsorption, pm:embodiedLocus ;
        pm:situationGround "Two answers to two questions in one node."@en ;
        pm:attestedBy pm:compilerInference .
    """
    conforms, report = _validate(offending)
    assert not conforms, (
        "Two axis values in one placement must fail: two axes are two placements, "
        "and a node holding both cannot be disputed on one of them."
    )


def test_complete_situating_conforms() -> None:
    accepted = _SITUATING_PREFIXES + """
    pmc:GoodPlacement a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:sleepThreshold ;
        pm:situationGround "The passage describes sleep departing and waking beginning, with the eyes immobile."@en ;
        pm:attestedBy pm:compilerInference ;
        dcterms:source "A work, a place" .
    """
    conforms, report = _validate(accepted)
    assert conforms, report


def test_orientation_axes_accept_the_not_stated_value() -> None:
    # Positive fixture for the value added on the two older subject axes. The
    # case it records is the ordinary one: a handbook of technique that names
    # capacities and never places itself for or against the norm, or never
    # says what becomes of the self. Before the value existed, that source and
    # a source nobody had opened were entered identically.
    accepted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .

    pmt:Somewhere pm:methodOrientation pm:methodNotStated ;
        pm:telicOrientation pm:telosNotStated .
    """
    conforms, report = _validate(accepted)
    assert conforms, report


def test_orientation_axis_still_rejects_an_undeclared_value() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmt: <https://pajew.ski/prima-materia/traditions/> .

    pmt:Somewhere pm:methodOrientation pm:methodUnknown .
    """
    conforms, report = _validate(offending)
    assert not conforms, "An orientation value no scale declares must fail SHACL."
    assert "declared method orientation" in report


def test_the_split_persistence_axes_accept_their_values() -> None:
    # The axis these two replace held acquisition and duration between its two
    # ends, and fitted the Sufi material only because that material answers
    # both questions the same way. A capacity that is neither worked for nor
    # passing had no place on it at all.
    accepted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .

    pmc:NotWorkedFor a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:notByEffort ;
        pm:situationGround "Reported as a standing property and expressly not as the outcome of an exercise."@en ;
        pm:attestedBy pm:compilerInference .

    pmc:AndYetItLasts a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:abidingState ;
        pm:situationGround "A standing property of a person is not an episode."@en ;
        pm:attestedBy pm:compilerInference .
    """
    conforms, report = _validate(accepted)
    assert conforms, report


def test_the_retired_persistence_values_are_rejected() -> None:
    offending = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .

    pmc:OldCoordinate a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:occasionedState ;
        pm:situationGround "A coordinate that no longer exists."@en ;
        pm:attestedBy pm:compilerInference .
    """
    conforms, report = _validate(offending)
    assert not conforms, (
        "The values of the split axis must not survive as writable coordinates; "
        "a placement on a retired value would sit in the graph unread."
    )


def test_unbound_is_accepted_and_only_on_the_anchoring_axis() -> None:
    accepted = """
    @prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
    @prefix pmc: <https://pajew.ski/prima-materia/concepts/> .

    pmc:PrayedThroughout a pm:Situating ;
        pm:situatedNode pmc:Something ;
        pm:axisValue pm:anchoringUnbound ;
        pm:situationGround "Prescribed as continuous, through work and sleep alike."@en ;
        pm:attestedBy pm:compilerInference .
    """
    conforms, report = _validate(accepted)
    assert conforms, report

    offending = accepted.replace("pm:anchoringUnbound", "pm:locusUnbound")
    conforms, report = _validate(offending)
    assert not conforms, (
        "The unbound value exists only where a case in the holdings calls for "
        "it; an axis that has no such case has no such value."
    )


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
