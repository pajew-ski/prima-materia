"""Scan TTL files for forbidden static-substance class names."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = (REPO_ROOT / "ontology", REPO_ROOT / "traditions")

FORBIDDEN_LOCAL_NAMES = ("Symbol", "Concept", "Entity", "Object")
FORBIDDEN_FULL_IRI = "https://pajew-ski.github.io/prima-materia/ontology#"

# Matches `pm:Symbol` (token boundaries) or the full IRI form, but only when
# followed by whitespace/punctuation that suggests a subject position — i.e.
# not inside longer identifiers like pm:Symbolizing or pm:ConceptInstanceShape.
_PM_PREFIX_PATTERN = re.compile(
    r"\bpm:(" + "|".join(FORBIDDEN_LOCAL_NAMES) + r")\b(?!\w)"
)
_FULL_IRI_PATTERN = re.compile(
    r"<" + re.escape(FORBIDDEN_FULL_IRI) + r"(" + "|".join(FORBIDDEN_LOCAL_NAMES) + r")>"
)


def _collect_ttl() -> list[Path]:
    files: list[Path] = []
    for directory in SCAN_DIRS:
        if directory.exists():
            files.extend(sorted(directory.rglob("*.ttl")))
    return files


@pytest.mark.parametrize("ttl_path", _collect_ttl(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_no_forbidden_substance_classes(ttl_path: Path) -> None:
    text = ttl_path.read_text(encoding="utf-8")
    prefix_hits = _PM_PREFIX_PATTERN.findall(text)
    iri_hits = _FULL_IRI_PATTERN.findall(text)
    offenders = sorted(set(prefix_hits) | set(iri_hits))
    assert not offenders, (
        f"{ttl_path.name} references forbidden substance class names: {offenders}. "
        "Use the process form (pm:Symbolizing, pm:Conceptualizing, ...) instead."
    )
