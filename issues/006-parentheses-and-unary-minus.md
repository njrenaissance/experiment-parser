---
title: Add parentheses grouping and unary minus to the grammar
---

## Purpose
Extend the grammar so parentheses regroup subexpressions and a leading `-`
produces a `UnaryOp`.

## Acceptance criteria
- `parse("(1 + 2) * 3")` groups as `(1 + 2) * 3`: root is `BinaryOp("*")` whose
  `left` is `BinaryOp("+")`.
- Parentheses never appear as AST nodes; they only change tree structure.
- `parse("-5")` returns `UnaryOp(operator="-", operand=Number(5))`.
- `parse("-3 + 2")` groups as `(-3) + 2`: root is `BinaryOp("+")` whose `left`
  is `UnaryOp("-")`.
- `parse("-2 * 3")` groups as `(-2) * 3` — unary minus binds tighter than the
  binary operators.

## Notes
- Builds on the core grammar issue and uses the same `parse` entry point.
- The `-` symbol is shared between binary subtraction and unary minus; the AST
  distinguishes them by node type (`BinaryOp` vs `UnaryOp`), not by operator.
- Error handling for unbalanced parentheses (e.g. `"(1 + 2"`) belongs to the
  parse-error-handling issue, not here.
