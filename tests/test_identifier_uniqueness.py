"""Guard against identifier collisions across data files.

RDF has no notion of file membership: two blocks that happen to share an
identifier are merged into one node on compilation, with two labels, two
definitions and two traditions, and every SHACL constraint is still satisfied
because each of them holds twice. Nothing in the pipeline says a word. The one
occurrence in the holdings (prima-materia#275) was caught by accident, by a
JavaScript test over a cross-tabulation of the website.

The rule this enforces is not "a subject appears in one file". Twenty subjects
appear in two files on purpose: traditions/registry-established.ttl carries the
coverage assessment of the whole holding, deliberately kept in one place so
that a single act of assessment is not scattered across twenty-one files. Those
statements add predicates to subjects defined elsewhere and are correct.

The rule is "a subject is typed in one file". The class assignment fixes what a
node is; additions elsewhere are allowed. A guard on subjects would flag twenty
correct cases, and a guard that cries wolf twenty times gets switched off.
"""
from __future__ import annotations

import collections
from pathlib import Path

from rdflib import Graph, RDF, URIRef

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = (
    REPO_ROOT / "ontology",
    REPO_ROOT / "traditions",
    REPO_ROOT / "convergences",
    REPO_ROOT / "examinations",
    REPO_ROOT / "originations",
)

PM = "https://pajew.ski/prima-materia/ontology#"
INSTANCE_PREFIXES = (
    "https://pajew.ski/prima-materia/traditions/",
    "https://pajew.ski/prima-materia/concepts/",
    "https://pajew.ski/prima-materia/practices/",
)


def _collect_ttl() -> list[Path]:
    files: list[Path] = []
    for directory in SCAN_DIRS:
        if directory.exists():
            files.extend(sorted(directory.rglob("*.ttl")))
    return files


def _typed_subjects(path: Path) -> set[URIRef]:
    """Subjects that receive a pm: class assignment in this file."""
    graph = Graph()
    graph.parse(path, format="turtle")
    return {
        subject
        for subject, _, obj in graph.triples((None, RDF.type, None))
        if isinstance(subject, URIRef) and str(obj).startswith(PM)
    }


def _instance_subjects(path: Path) -> set[URIRef]:
    """Subjects in the instance namespaces, typed or not."""
    graph = Graph()
    graph.parse(path, format="turtle")
    return {
        subject
        for subject in graph.subjects()
        if isinstance(subject, URIRef)
        and str(subject).startswith(INSTANCE_PREFIXES)
    }


def _collisions(paths: list[Path]) -> dict[URIRef, list[str]]:
    homes: dict[URIRef, list[str]] = collections.defaultdict(list)
    for path in paths:
        for subject in _typed_subjects(path):
            homes[subject].append(path.name)
    return {
        subject: sorted(files) for subject, files in homes.items() if len(files) > 1
    }


def _orphans(paths: list[Path]) -> dict[URIRef, list[str]]:
    typed: set[URIRef] = set()
    mentioned: dict[URIRef, list[str]] = collections.defaultdict(list)
    for path in paths:
        typed |= _typed_subjects(path)
        for subject in _instance_subjects(path):
            mentioned[subject].append(path.name)
    return {
        subject: sorted(files)
        for subject, files in mentioned.items()
        if subject not in typed
    }


def test_no_identifier_is_typed_in_two_files() -> None:
    collisions = _collisions(_collect_ttl())
    assert not collisions, (
        "These identifiers carry a pm: class assignment in more than one file. "
        "On compilation they merge into a single node holding both sets of "
        "statements, and SHACL will not object because every constraint is "
        "satisfied twice: " + "; ".join(
            f"{subject} in {files}" for subject, files in sorted(collisions.items())
        )
    )


def test_every_instance_identifier_is_typed_somewhere() -> None:
    """The other direction, and the one the rule above newly permits.

    Since additions to a subject defined elsewhere are legitimate, a misspelt
    identifier now looks exactly like one: it carries predicates and no type,
    and nothing distinguishes it from a deliberate addition. Only a check
    across all files can tell the two apart.
    """
    orphans = _orphans(_collect_ttl())
    assert not orphans, (
        "These identifiers appear as subjects without ever receiving a pm: "
        "class assignment in any file. Either the class assignment is missing "
        "or the identifier is a typo for one that exists: " + "; ".join(
            f"{subject} in {files}" for subject, files in sorted(orphans.items())
        )
    )


#
# Negative fixtures, required by SPEC §9. A guard that has never been shown to
# fire is not known to work, and both of these guards permit a case that looks
# almost exactly like the one they forbid: a second file adding predicates to a
# known subject. The fixtures pin the difference.
#

_PREFIXES = """@prefix pm:  <https://pajew.ski/prima-materia/ontology#> .
@prefix pmt: <https://pajew.ski/prima-materia/traditions/> .
@prefix pmc: <https://pajew.ski/prima-materia/concepts/> .
"""


def _write(directory: Path, name: str, body: str) -> Path:
    path = directory / name
    path.write_text(_PREFIXES + body, encoding="utf-8")
    return path


def test_collision_guard_fires_on_a_subject_typed_twice(tmp_path: Path) -> None:
    first = _write(tmp_path, "a.ttl", "pmc:Shared a pm:Conceptualizing .\n")
    second = _write(tmp_path, "b.ttl", "pmc:Shared a pm:Practising .\n")
    assert _collisions([first, second]), (
        "The collision guard must fire when the same identifier is typed in two files."
    )


def test_collision_guard_is_silent_on_a_permitted_addition(tmp_path: Path) -> None:
    home = _write(tmp_path, "a.ttl", "pmt:Somewhere a pm:Tradition .\n")
    addition = _write(
        tmp_path, "registry.ttl", "pmt:Somewhere pm:coverageState pm:placesEntered .\n"
    )
    assert not _collisions([home, addition]), (
        "A file adding predicates to a subject typed elsewhere is the documented "
        "arrangement of traditions/registry-established.ttl and must not fire."
    )


def test_orphan_guard_fires_on_an_addition_to_a_misspelt_identifier(tmp_path: Path) -> None:
    home = _write(tmp_path, "a.ttl", "pmt:SomewhereElse a pm:Tradition .\n")
    typo = _write(
        tmp_path, "registry.ttl", "pmt:Somewhere pm:coverageState pm:placesEntered .\n"
    )
    assert _orphans([home, typo]), (
        "The orphan guard must fire when an addition names an identifier that is "
        "typed nowhere. This is the case the collision rule newly permits."
    )


def test_orphan_guard_is_silent_when_the_identifier_matches(tmp_path: Path) -> None:
    home = _write(tmp_path, "a.ttl", "pmt:Somewhere a pm:Tradition .\n")
    addition = _write(
        tmp_path, "registry.ttl", "pmt:Somewhere pm:coverageState pm:placesEntered .\n"
    )
    assert not _orphans([home, addition]), (
        "A correctly spelt addition must not fire the orphan guard."
    )
