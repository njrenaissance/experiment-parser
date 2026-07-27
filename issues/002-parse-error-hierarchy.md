---
title: Add AppError base and ParseError exception
---

## Purpose
Establish the project's exception hierarchy with a `ParseError` type for
invalid parser input.

## Acceptance criteria
- An `errors` module (e.g. `src/<pkg>/errors.py`) defines `AppError(Exception)`
  as the single base of the hierarchy.
- `ParseError` is defined as a subclass of `AppError` (and therefore of
  `Exception`): `issubclass(ParseError, AppError)` is `True`.
- `ParseError` can be raised with a human-readable message that is recoverable
  via `str(err)`.
- The module raises and catches no bare `Exception`.

## Notes
- Follows `.claude/standards/error-handling.md` (single rooted hierarchy).
- Defines the exception types only. Actually raising `ParseError` from the
  parser is the parse-error-handling issue's responsibility, not this one.
