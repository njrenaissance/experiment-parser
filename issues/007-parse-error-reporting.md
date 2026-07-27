---
title: Raise ParseError with informative messages for invalid input
---

## Purpose
Translate every invalid-input case into a `ParseError` whose message identifies
the offending token or position rather than failing bare.

## Acceptance criteria
Each of the following raises `ParseError` (a subclass of `AppError`), and the
message names the offending token or position, not a generic failure:

- `parse("1 +")` — incomplete expression (operator with no right operand).
- `parse("+ 1")` — expression may not start with a binary operator.
- `parse("1 2")` — two adjacent literals with no operator between them.
- `parse("(1 + 2")` — unbalanced parenthesis.
- `parse("3 & 4")` — illegal character outside the token set.
- `parse("")` — empty input.

Additionally:
- The raised exception is an instance of `ParseError` (and therefore of
  `AppError`); no bare `Exception` escapes `parse`.

## Notes
- Requires the `ParseError` type, the lexer's illegal-character detection, and
  the full grammar (including parentheses and unary minus) to exist.
- Implemented via ply's `p_error` handler (and the lexer's `t_error`)
  translating engine failures into `ParseError`, per ADR-0001; message quality
  is part of the contract, not incidental.
- No evaluation is performed, so division-by-zero cannot arise — `/` and `//`
  remain purely structural.
