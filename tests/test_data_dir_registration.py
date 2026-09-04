"""Jeder Datenordner muss in allen fuenf Listen stehen.

SPEC §9 nennt fuenf Stellen, an denen ein neuer Datenordner nachzuziehen ist,
und bezeichnet die fuenfte als die teuerste: ohne sie prueft der
Kollisionswaechter den Ordner nicht, zwei Knoten mit demselben Bezeichner
verschmelzen beim Kompilieren zu einem, und jede SHACL-Bedingung ist danach
doppelt erfuellt, ohne dass etwas auffaellt.

Nichts schlaegt fehl, wenn eine der fuenf vergessen wird. Genau das ist mit
`generalizations/` passiert (prima-materia#426): der Ordner fehlte im
Kollisionswaechter, `generalizations/README.md` zaehlte die Verdrahtung auf und
zaehlte vier Stellen statt fuenf, und weil der Ordner leer war, fiel es nicht
auf. Die Auslassung stand als Liste da, und die Liste war so lang wie die
Pruefung, die jemand gegen sie gefuehrt haette.

Verglichen wird deshalb gegen den Dateibaum und ausdruecklich nicht gegen eine
sechste Liste. Eine sechste Liste waere dieselbe Fehlerklasse eine Ebene
hoeher.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import compile as compile_script
import publish as publish_script
import validate as validate_script

from tests.test_identifier_uniqueness import SCAN_DIRS as UNIQUENESS_DIRS
from tests.test_no_substance_classes import SCAN_DIRS as SUBSTANCE_DIRS

REPO_ROOT = Path(__file__).resolve().parent.parent

# Die fuenf Stellen aus SPEC §9, unter dem Namen, unter dem sie dort stehen.
REGISTRATIONS: dict[str, tuple[Path, ...]] = {
    "scripts/compile.py DEFAULT_INPUTS": tuple(compile_script.DEFAULT_INPUTS),
    "scripts/publish.py DEFAULT_INPUTS": tuple(publish_script.DEFAULT_INPUTS),
    "scripts/validate.py DEFAULT_DATA_DIRS": tuple(validate_script.DEFAULT_DATA_DIRS),
    "tests/test_no_substance_classes.py SCAN_DIRS": tuple(SUBSTANCE_DIRS),
    "tests/test_identifier_uniqueness.py SCAN_DIRS": tuple(UNIQUENESS_DIRS),
}

# shapes/ traegt .ttl und steht absichtlich in keiner der fuenf: es ist die
# Pruefvorschrift und keine Daten. build/ entsteht beim Kompilieren. Wer hier
# etwas eintraegt, nimmt einen Ordner aus der Pruefung und muss sagen warum.
EXEMPT = {"shapes", "build"}


def _data_dirs_in_tree() -> set[str]:
    found = set()
    for entry in REPO_ROOT.iterdir():
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if any(entry.rglob("*.ttl")):
            found.add(entry.name)
    return found - EXEMPT


@pytest.mark.parametrize("label", sorted(REGISTRATIONS))
def test_every_data_dir_is_registered(label: str) -> None:
    registered = {path.name for path in REGISTRATIONS[label]}
    missing = sorted(_data_dirs_in_tree() - registered)
    assert not missing, (
        f"{label} kennt diese Ordner mit .ttl-Dateien nicht: {missing}. "
        "SPEC §9 nennt fuenf Stellen; eine vergessene faellt sonst nirgends auf."
    )


@pytest.mark.parametrize("label", sorted(REGISTRATIONS))
def test_no_registration_names_a_vanished_dir(label: str) -> None:
    """Die Gegenrichtung: ein Eintrag, den es nicht mehr gibt.

    Er schadet nicht sofort, weil alle fuenf Stellen nicht existierende Pfade
    ueberspringen. Er laesst die Liste aber vollstaendig aussehen, wo sie es
    nicht ist, und beim naechsten Umsortieren zeigt sie ins Leere.
    """
    vanished = sorted(
        path.name for path in REGISTRATIONS[label] if not path.is_dir()
    )
    assert not vanished, f"{label} nennt Ordner, die es nicht gibt: {vanished}."


def test_the_guard_would_fire() -> None:
    """Negativfixture nach SPEC §9: eine Liste ohne einen vorhandenen Ordner."""
    tree = _data_dirs_in_tree()
    assert tree, "Der Dateibaum muss mindestens einen Datenordner haben."
    incomplete = {path.name for path in REGISTRATIONS["scripts/compile.py DEFAULT_INPUTS"]}
    incomplete.discard(sorted(tree)[0])
    assert tree - incomplete, (
        "Eine Liste, der ein vorhandener Datenordner fehlt, muss als unvollstaendig "
        "erkannt werden."
    )
