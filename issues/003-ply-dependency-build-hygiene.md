---
title: Add ply runtime dependency and parser-table build hygiene
---

## Purpose
Make `ply` available as the parser engine and keep its generated table
artifacts out of the repository and out of type-checking noise.

## Acceptance criteria
- `ply` is declared as a runtime dependency in `pyproject.toml` and installs
  via `uv sync`.
- `import ply.lex` and `import ply.yacc` succeed in the project environment.
- ply's generated `parser.out` and `parsetab.py` artifacts are git-ignored and
  never committed.
- `uv run mypy src` passes with a scoped `ignore_missing_imports` for the `ply`
  module only — not a blanket relaxation of missing-import checking.

## Notes
- Rationale is recorded in `spec/adr/0001-ply-lalr-parser-engine.md`.
- Scope is `ply` and its build/type-check configuration only; does NOT add any
  other dependency (e.g. `openwiki` remains a per-machine global CLI, never a
  project dependency).
