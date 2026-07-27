# spec.md

**Status:** draft

## Purpose

Parse a single arithmetic expression built from the operators `+ - * / //`
into an abstract syntax tree.

## Inputs / Outputs

**Input:** one expression as a `str` — e.g. `"1 + 2 * 3"`, `"(7 // 2) - -4"`.
Whitespace between tokens is insignificant.

**Output:** the root node of an immutable AST built from exactly three node
types, all supporting structural equality (so two ASTs parsed from
equivalent input compare equal):

- `Number(value: int)` — an integer-literal leaf.
- `BinaryOp(operator: str, left: Node, right: Node)` — a binary operation
  whose `operator` is one of `"+"`, `"-"`, `"*"`, `"/"`, `"//"`.
- `UnaryOp(operator: str, operand: Node)` — unary minus, `operator == "-"`.

**Public contract:** a single function `parse(text: str) -> Node` returning
the AST root. Invalid input raises `ParseError`, a subclass of the project's
`AppError` base (see `.claude/standards/error-handling.md`).

**Explicitly out of scope** (sharpens the contract; each is a candidate for a
later spec, not this one):

- No **evaluation** — the parser produces structure only, never a computed
  result. `/` vs `//` are distinct operator tokens in the AST; division is
  never performed, so division-by-zero cannot arise at parse time.
- **Integer literals only** — no floats, no scientific notation, no signs
  embedded in the literal (a leading `-` is a `UnaryOp`, not part of the
  `Number`).
- No variables, function calls, comparison/boolean operators, or
  exponentiation.
- One expression per call — no statement sequences or trailing input.

## What we produce

library

## Where we persist

stateless — `parse` returns an in-memory AST; nothing is written to a file
or a database. Callers persist the result if they wish.

## Method

rules — a deterministic LALR(1) grammar implemented with the `ply` library
(`ply.lex` for tokenizing, `ply.yacc` for the grammar). No classical ML, no
LLM. (`ply` is a new runtime dependency; it generates a bottom-up LALR(1)
parser, not a recursive-descent one.)

## Done criteria

Observable behaviors the TDD unit tests will assert.

**Literals & whitespace**

- `parse("42")` returns `Number(value=42)`.
- `parse("1+2")` and `parse("  1  +  2 ")` return equal ASTs (whitespace is
  insignificant).

**Binary operators**

- `parse("1 + 2")` returns `BinaryOp(operator="+", left=Number(1), right=Number(2))`.
- Each operator is recognized with the correct symbol: `parse("6 - 2")`,
  `parse("6 * 2")`, `parse("6 / 2")`, and `parse("7 // 2")` return `BinaryOp`
  nodes whose `operator` is `"-"`, `"*"`, `"/"`, and `"//"` respectively, each
  over `Number` leaves.

**Precedence**

- `parse("1 + 2 * 3")` groups as `1 + (2 * 3)` — the root is `BinaryOp("+")`
  whose `right` is `BinaryOp("*")`.
- `parse("1 * 2 + 3")` groups as `(1 * 2) + 3` — the root is `BinaryOp("+")`
  whose `left` is `BinaryOp("*")`.
- `//` shares the precedence of `*` and `/`: `parse("8 // 4 * 2")` groups
  left-to-right as `(8 // 4) * 2`.

**Associativity** (all four binary operators are left-associative)

- `parse("8 - 3 - 2")` groups as `(8 - 3) - 2` — the root's `left` is itself a
  `BinaryOp("-")`.
- `parse("16 // 4 // 2")` groups as `(16 // 4) // 2`.

**Parentheses**

- `parse("(1 + 2) * 3")` groups as `(1 + 2) * 3` — the root is `BinaryOp("*")`
  whose `left` is `BinaryOp("+")`.
- Parentheses never appear as nodes; they only change structure.

**Unary minus**

- `parse("-5")` returns `UnaryOp(operator="-", operand=Number(5))`.
- `parse("-3 + 2")` groups as `(-3) + 2` — the root is `BinaryOp("+")` whose
  `left` is `UnaryOp("-")`.
- Unary minus binds tighter than the binary operators: `parse("-2 * 3")`
  groups as `(-2) * 3`.

**Errors** (each raises `ParseError`; the message identifies the offending
token or position, not a bare failure)

- `parse("1 +")` — incomplete expression (operator with no right operand).
- `parse("+ 1")` — expression may not start with a binary operator.
- `parse("1 2")` — two adjacent literals with no operator between them.
- `parse("(1 + 2")` — unbalanced parenthesis.
- `parse("3 & 4")` — illegal character outside the token set.
- `parse("")` — empty input.
