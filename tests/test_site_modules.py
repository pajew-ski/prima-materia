"""Run the browser modules' own tests, against the corpus this repository holds.

The search engine, the arrangements and the cross-tabulation are JavaScript,
because that is where they run. They are still covered by `pytest tests/`, the
one gate before a commit, rather than by a second command nobody remembers: this
module compiles the graph, hands node the same ontology-data.json the site is
built from, and reports what node found.

Where node is not installed the JavaScript tests are skipped rather than
silently dropped, and the skip says so.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

import compile as compile_script
import publish as publish_script

REPO_ROOT = Path(__file__).resolve().parent.parent
SUITE = REPO_ROOT / "tests" / "site.test.mjs"
ASSETS_DIR = REPO_ROOT / "site"

NODE = shutil.which("node")
requires_node = pytest.mark.skipif(NODE is None, reason="node is not installed")


@pytest.fixture(scope="module")
def corpus(tmp_path_factory) -> Path:
    """The site's data file, built from the sources exactly as publish.py does."""
    graph = compile_script.compile_graph(publish_script.DEFAULT_INPUTS)
    path = tmp_path_factory.mktemp("corpus") / "ontology-data.json"
    path.write_text(
        json.dumps(publish_script.build_data(graph), ensure_ascii=False),
        encoding="utf-8",
    )
    return path


@requires_node
def test_site_modules(corpus: Path) -> None:
    result = subprocess.run(
        [NODE, "--test", str(SUITE)],
        cwd=REPO_ROOT,
        env={**os.environ, "PRIMA_MATERIA_DATA": str(corpus)},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    # A suite that silently stopped running its assertions would still exit 0.
    assert "# fail 0" in result.stdout
    assert "# skipped 0" in result.stdout


def test_the_javascript_suite_is_not_orphaned() -> None:
    # Every module the suite covers has to be one the page actually loads, or
    # the tests drift into covering code nothing runs.
    page = (ASSETS_DIR / "index.html").read_text(encoding="utf-8")
    entry = (ASSETS_DIR / "ontology.js").read_text(encoding="utf-8")
    assert 'src="ontology.js"' in page
    for module in ("search.js", "layouts.js", "matrix.js", "theme.js"):
        assert f'"./{module}"' in entry, f"ontology.js does not import {module}"
        assert (ASSETS_DIR / module).is_file()
