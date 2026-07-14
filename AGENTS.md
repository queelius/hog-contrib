# Repository Guidelines

## Project Structure & Module Organization

`contributions.yaml` is the source of truth for every House of Graphs deposit or candidate. Byte-exact graph6 witnesses live in `graphs/`, while `manifests/` preserves the original JSON deposit-preparation records. `verify.py` contains the pure-Python graph6 codec and graph-property checks; `verify_witnesses.py` is the repository-wide verification gate. Read `LESSONS.md` before preparing deposits, and keep the human-facing summary in `README.md` aligned with material status changes.

## Build, Test, and Development Commands

This repository has no build step or third-party runtime dependencies. Run commands from the repository root:

```bash
python3 verify_witnesses.py
python3 -m py_compile verify.py verify_witnesses.py
```

The first command decodes every file in `graphs/`, checks its vertex and edge counts and round trip, then applies the relevant property checks. It must exit successfully before graph data is committed. The second command provides a quick syntax check while editing Python.

## Coding Style & Naming Conventions

Follow the existing Python style: four-space indentation, `snake_case` functions and variables, uppercase module constants such as `CASES`, concise docstrings, and standard-library imports only unless a dependency is clearly justified. Keep verification logic explicit and deterministic. Name witnesses after their invariant and parameters, for example `graphs/sat9_C6_12.g6` or `graphs/z9_10_34.g6`. Preserve graph6 files byte-for-byte; strings may contain a literal backtick.

## Testing Guidelines

There is no separate unit-test suite or coverage threshold. Treat `python3 verify_witnesses.py` as the required regression test. When adding a witness, add its metadata to `contributions.yaml`, its exact `.g6` file to `graphs/`, and a matching `CASES` entry in `verify_witnesses.py`. Add focused checks to `verify.py` when introducing a new invariant family.

## Commit & Pull Request Guidelines

History currently contains a single descriptive subject (`Initial commit: House of Graphs deposit tracker and portfolio`), so no formal convention is established. Use short, imperative subjects that identify the affected graph or verification rule. Pull requests should explain the invariant or status change, list modified witnesses, cite the backing certificate or DOI, and include verification output. Never mark an entry `deposited` without a confirmed live HoG ID; add a dated `LESSONS.md` entry for corrected claims.
