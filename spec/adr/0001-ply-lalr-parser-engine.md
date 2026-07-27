# ADR-0001: Use ply (LALR(1)) as the parser engine

## Status

accepted

## Context

The spec (`spec/spec.md`) calls for parsing arithmetic expressions over
`+ - * / //` into an AST, using a rules-based method (no ML/LLM). During Spec
Planning we weighed three engine strategies:

- **(a)** a hand-written recursive-descent / precedence-climbing parser in
  pure Python — no dependency, and genuinely "recursive descent";
- **(b)** a PEG / combinator library (`lark`, `pyparsing`, `parsimonious`);
- **(c)** `ply`, a lex/yacc toolkit that generates a bottom-up **LALR(1)**
  parser.

The original request named both "recursive descent" *and* `ply`. Those cannot
both hold: `ply`'s `yacc` module produces LALR(1) parsers, not recursive-descent
ones. The choice had to be resolved explicitly. Relevant constraints: the
grammar is small and well-understood (a classic expression grammar with
precedence and associativity), and the standards discourage adding
dependencies without cause.

## Decision

Implement the parser with `ply` — `ply.lex` for tokenizing and `ply.yacc` for
an LALR(1) grammar — adding `ply` as a runtime dependency. We accept that the
result is bottom-up LALR(1), not recursive descent.

## Consequences

**Easier.** The grammar stays declarative — production rules plus a single
precedence table — instead of hand-threaded control flow. Precedence and
left-associativity for `+ - * / //` are expressed once in `ply`'s precedence
declaration. `ply` is mature, and its yacc-style conflict reporting surfaces
grammar ambiguities at build time rather than as silent mis-parses.

**Harder / costs.** A new third-party runtime dependency to vet and keep
current (via `dependabot`). `ply` generates parser tables and by default writes
`parser.out` / `parsetab.py` artifacts that must be suppressed or git-ignored.
`ply` ships no type hints, so `mypy` (strict-ish here) will need a scoped
`ignore_missing_imports` for the module rather than a blanket relaxation.
LALR shift/reduce conflicts are less intuitive to debug than hand-written
recursion, and good error messages for cases like `parse("1 +")` require a
deliberate `p_error` handler translating into the spec's `ParseError` — they
do not fall out of the engine for free.

**Forecloses.** It commits the grammar to what LALR(1) can express;
context-sensitive or heavily backtracking constructs (unlikely for this DSL,
but relevant if the language later grows) would fight the engine. Reversing
this later means rewriting the parser internals — but because the public
contract is `parse(text) -> Node` over fixed AST node types, such a swap is
contained to the parser module and does **not** change the public API. That
containment is why this is recorded as a notable-but-reversible decision, not
an irreversible one.
