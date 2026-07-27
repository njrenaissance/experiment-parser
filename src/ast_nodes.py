"""Immutable AST node types for the expression parser.

Defines the three node types the parser produces — :class:`Number`,
:class:`BinaryOp`, and :class:`UnaryOp` — plus the :data:`Node` union so any
node can be referenced by a single type. Nodes are frozen dataclasses, giving
structural equality and immutability without hand-written ``__eq__`` or
attribute guards.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Number:
    """An integer-literal leaf."""

    value: int


@dataclass(frozen=True)
class BinaryOp:
    """A binary operation over two operands.

    ``operator`` is one of ``"+"``, ``"-"``, ``"*"``, ``"/"``, ``"//"``.
    """

    operator: str
    left: Node
    right: Node


@dataclass(frozen=True)
class UnaryOp:
    """A unary operation over a single operand (unary minus)."""

    operator: str
    operand: Node


type Node = Number | BinaryOp | UnaryOp
