---
title: Define immutable AST node types with structural equality
---

## Purpose
Provide the three AST node types the parser produces — `Number`, `BinaryOp`,
and `UnaryOp` — as immutable, structurally-comparable data.

## Acceptance criteria
- A module exposes `Number`, `BinaryOp`, and `UnaryOp`, plus a single `Node`
  type (union or common base) so any node can be referenced by one type.
- `Number(value=42)` holds an `int` `value`; `Number(value=42) == Number(value=42)`
  and `Number(value=1) != Number(value=2)`.
- `BinaryOp(operator="+", left=Number(1), right=Number(2))` exposes
  `operator: str`, `left: Node`, `right: Node`; two `BinaryOp`s compare equal
  iff operator and both children are equal, and unequal if any field differs.
- `UnaryOp(operator="-", operand=Number(5))` exposes `operator: str` and
  `operand: Node`; structural equality holds on the same basis.
- Nested equality holds: two independently constructed identical trees (e.g.
  `BinaryOp("+", Number(1), BinaryOp("*", Number(2), Number(3)))`) compare equal.
- Instances are immutable — attempting to reassign an attribute raises.

## Notes
- Construction and equality only — no parsing, no evaluation, no `__call__`.
- Does NOT include the `parse()` function, the lexer, or the grammar.
