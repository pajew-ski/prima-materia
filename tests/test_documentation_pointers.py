"""Jeder dateiuebergreifende Verweis muss aufloesen.

Die Regeln dieses Repos stehen je einmal kanonisch; die anderen Dateien
zeigen darauf. Damit haengt die Verlaesslichkeit der Dokumentation an den
Verweiszielen. Ein Paragraph, der umnummeriert wird, oder eine Ueberschrift,
die umformuliert wird, macht den Zeiger still falsch: nichts schlaegt fehl,
und der Leser landet an keiner Stelle. Fall in prima-materia#446.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

DOCS = ["SPEC.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md"]

# `SPEC.md` §15  /  `SPEC.md §13`  /  `SPEC.md` Abschnitt 15
SECTION_REF = re.compile(
    r"`?(?P<file>SPEC|AGENTS|CLAUDE|CONTRIBUTING)\.md`?[ ]*"
    r"(?:\u00a7[ ]*|Abschnitt[ ]+)(?P<number>\d+)"
)

# `AGENTS.md` gefolgt von einem in Anfuehrungszeichen gesetzten Abschnittstitel.
# Gefangen wird bis zum letzten Anfuehrungszeichen der Tabellenzelle, damit ein
# Titel, der selbst Anfuehrungszeichen traegt, vollstaendig erfasst wird.
TITLE_REF = re.compile(
    r"`?(?P<file>SPEC|AGENTS|CLAUDE|CONTRIBUTING)\.md`?[ ]*"
    r"\u201e(?P<title>.+)[\u201c\"](?=[ ]*(?:\||$|[.,;]))"
)


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def numbered_sections(text: str) -> set[str]:
    """Nummern der nummerierten Abschnittsueberschriften."""
    return {m.group(1) for m in re.finditer(r"(?m)^##[ ]+(\d+)\.[ ]", text)}


def headings(text: str) -> set[str]:
    """Alle Ueberschriftentexte, Nummern- und Parameterpraefix zusaetzlich."""
    found = set()
    for m in re.finditer(r"(?m)^#{2,4}[ ]+(.+?)[ ]*$", text):
        title = m.group(1)
        found.add(title)
        found.add(re.sub(r"^\d+\.[ ]*", "", title))
        found.add(re.sub(r"^Parameter[ ]\d+:[ ]*", "", title))
    return found


@pytest.mark.parametrize("source", DOCS)
def test_section_numbers_resolve(source: str) -> None:
    text = read(source)
    broken = []
    for match in SECTION_REF.finditer(text):
        target = f"{match.group('file')}.md"
        number = match.group("number")
        if number not in numbered_sections(read(target)):
            broken.append(f"{source}: {target} Abschnitt {number}")
    assert not broken, "Verweis auf nicht existierenden Abschnitt: " + "; ".join(broken)


@pytest.mark.parametrize("source", DOCS)
def test_quoted_headings_resolve(source: str) -> None:
    text = read(source)
    broken = []
    for match in TITLE_REF.finditer(text):
        target = f"{match.group('file')}.md"
        title = match.group("title").strip()
        if title not in headings(read(target)):
            broken.append(f"{source}: {target} [{title}]")
    assert not broken, "Verweis auf nicht existierende Ueberschrift: " + "; ".join(broken)


def test_the_guard_would_fire() -> None:
    """Negativfixture: ein erfundener Verweis wird als gebrochen erkannt."""
    spec_sections = numbered_sections(read("SPEC.md"))
    assert "99" not in spec_sections
    match = SECTION_REF.search("siehe `SPEC.md` \u00a799 fuer den Rest")
    assert match is not None
    assert match.group("number") not in spec_sections

    agents_headings = headings(read("AGENTS.md"))
    match = TITLE_REF.search("siehe `AGENTS.md` \u201eDer erfundene Abschnitt\".")
    assert match is not None
    assert match.group("title") not in agents_headings
