"""Unit tests for the immutable AST node types."""

import dataclasses

import pytest

from ast_nodes import BinaryOp, Number, UnaryOp

pytestmark = pytest.mark.unit


def test_number_holds_int_value():
    value = 42
    assert Number(value=value).value == value


def test_equal_numbers_compare_equal():
    assert Number(value=42) == Number(value=42)


def test_different_numbers_compare_unequal():
    assert Number(value=1) != Number(value=2)


def test_binary_op_exposes_operator_and_children():
    node = BinaryOp(operator="+", left=Number(1), right=Number(2))

    assert node.operator == "+"
    assert node.left == Number(1)
    assert node.right == Number(2)


def test_equal_binary_ops_compare_equal():
    assert BinaryOp("+", Number(1), Number(2)) == BinaryOp("+", Number(1), Number(2))


@pytest.mark.parametrize(
    "other",
    [
        pytest.param(BinaryOp("-", Number(1), Number(2)), id="operator_differs"),
        pytest.param(BinaryOp("+", Number(9), Number(2)), id="left_differs"),
        pytest.param(BinaryOp("+", Number(1), Number(9)), id="right_differs"),
    ],
)
def test_binary_ops_differing_in_any_field_compare_unequal(other):
    assert BinaryOp("+", Number(1), Number(2)) != other


def test_unary_op_exposes_operator_and_operand():
    node = UnaryOp(operator="-", operand=Number(5))

    assert node.operator == "-"
    assert node.operand == Number(5)


def test_equal_unary_ops_compare_equal():
    assert UnaryOp("-", Number(5)) == UnaryOp("-", Number(5))


@pytest.mark.parametrize(
    "other",
    [
        pytest.param(UnaryOp("+", Number(5)), id="operator_differs"),
        pytest.param(UnaryOp("-", Number(9)), id="operand_differs"),
    ],
)
def test_unary_ops_differing_in_any_field_compare_unequal(other):
    assert UnaryOp("-", Number(5)) != other


def test_independently_built_nested_trees_compare_equal():
    left = BinaryOp("+", Number(1), BinaryOp("*", Number(2), Number(3)))
    right = BinaryOp("+", Number(1), BinaryOp("*", Number(2), Number(3)))

    assert left == right


def test_nested_trees_differing_deep_compare_unequal():
    left = BinaryOp("+", Number(1), BinaryOp("*", Number(2), Number(3)))
    right = BinaryOp("+", Number(1), BinaryOp("*", Number(2), Number(4)))

    assert left != right


@pytest.mark.parametrize(
    ("first", "second"),
    [
        pytest.param(Number(1), UnaryOp("-", Number(1)), id="number_vs_unary"),
        pytest.param(Number(1), BinaryOp("+", Number(1), Number(1)), id="number_vs_binary"),
        pytest.param(UnaryOp("-", Number(1)), BinaryOp("-", Number(1), Number(1)), id="unary_vs_binary"),
    ],
)
def test_different_node_types_compare_unequal(first, second):
    assert first != second


@pytest.mark.parametrize(
    "node",
    [
        pytest.param(Number(1), id="number"),
        pytest.param(BinaryOp("+", Number(1), Number(2)), id="binary_op"),
        pytest.param(UnaryOp("-", Number(5)), id="unary_op"),
    ],
)
def test_nodes_are_immutable(node):
    with pytest.raises(dataclasses.FrozenInstanceError):
        node.operator = "changed"  # type: ignore[misc]
