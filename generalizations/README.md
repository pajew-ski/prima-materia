# generalizations/

Instances of pm:Generalizing: statements formed from several attested claims
that no single source makes. They carry pm:generalizedFrom instead of
dcterms:source and belong to no tradition, which is why they live here and
not under traditions/.

One file per generalization. A generalization is only as good as the
derivation under it, and a reader has to be able to see the whole derivation
at once.

## The five places, and the one that was missing

SPEC §9 lists five places a new data folder must be wired into, and warns
that nothing fails if one is forgotten. This folder was wired into four:

- `DEFAULT_INPUTS` in `scripts/compile.py`
- `DEFAULT_INPUTS` in `scripts/publish.py`
- `DEFAULT_DATA_DIRS` in `scripts/validate.py`
- `SCAN_DIRS` in `tests/test_no_substance_classes.py`
- `SCAN_DIRS` in `tests/test_identifier_uniqueness.py` — **missing until the
  first file was written**

The earlier version of this README named the first four and called the wiring
complete. That is how the gap survived: the omission was written down as a
list, and the list was the same length as the check anybody would have run
against it.

The fifth is the one SPEC calls the most expensive. Without it the collision
guard does not scan this folder, two nodes with the same identifier merge into
one on compilation, and every SHACL condition is satisfied twice over while
nothing in the pipeline says a word. A generalization is a likely place for
that to happen, because its identifier is formed from an effect and not from a
term in a source language, so two runs generalizing the same material are more
likely to collide here than anywhere else. See prima-materia#426.
