---
title: Implement core grammar — literals, binary operators, precedence, associativity
---

## Purpose
Provide the public `parse(text: str) -> Node` entry point that builds ASTs for
integer literals and the five binary operators with correct precedence and
left-associativity.

## Acceptance criteria
- `parse("42")` returns `Number(value=42)`.
- `parse("1+2")` and `parse("  1  +  2 ")` return equal ASTs (whitespace
  insignificant).
- `parse("1 + 2")` returns `BinaryOp(operator="+", left=Number(1), right=Number(2))`.
- `parse("6 - 2")`, `parse("6 * 2")`, `parse("6 / 2")`, and `parse("7 // 2")`
  each return a `BinaryOp` over `Number` leaves whose `operator` is `"-"`,
  `"*"`, `"/"`, and `"//"` respectively.
- `parse("1 + 2 * 3")` groups as `1 + (2 * 3)`: root is `BinaryOp("+")` whose
  `right` is `BinaryOp("*")`.
- `parse("1 * 2 + 3")` groups as `(1 * 2) + 3`: root is `BinaryOp("+")` whose
  `left` is `BinaryOp("*")`.
- `parse("8 // 4 * 2")` groups left-to-right as `(8 // 4) * 2` (`//` shares the
  precedence of `*` and `/`).
- `parse("8 - 3 - 2")` groups as `(8 - 3) - 2` and `parse("16 // 4 // 2")`
  groups as `(16 // 4) // 2` (all four binary operators are left-associative).

## Notes
- Assumes the AST node types, the tokenizer, and `ply` already exist (existence
  only — no dependency on their internals).
- Happy-path parsing only: error handling / `ParseError` is a separate issue.
- Parentheses and unary minus are a separate issue; this grammar need not yet
  handle `(`/`)` or a leading `-`.
- `parse` is the single public entry point defined by the spec.
