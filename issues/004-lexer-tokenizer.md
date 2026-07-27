---
title: Implement the expression tokenizer (ply.lex)
---

## Purpose
Tokenize an input string into the fixed token set for the grammar, treating
whitespace between tokens as insignificant.

## Acceptance criteria
- A `ply.lex` lexer recognizes integer-literal tokens (one or more digits),
  carrying an `int` value.
- It recognizes the operator tokens `+`, `-`, `*`, `/`, and `//`, with `//`
  tokenized as a single distinct token rather than two consecutive `/` tokens.
- It recognizes left `(` and right `)` parenthesis tokens.
- Whitespace (spaces and tabs) between tokens is skipped and yields no tokens,
  so `"1+2"` and `"  1  +  2 "` produce the same token sequence.
- A character outside the token set (e.g. `&`) is detected/flagged as illegal
  by the lexer.

## Notes
- Tokens only — this issue does NOT build the grammar or any AST nodes.
- Translating an illegal character (or any lexer/parser failure) into a
  `ParseError` raised to the caller is the parse-error-handling issue's job;
  here the lexer only needs to detect the illegal character.
- Integer token values are `int` so the grammar can wrap them in `Number`.
