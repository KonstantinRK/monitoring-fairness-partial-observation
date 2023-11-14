import ast
import operator
import numpy as np


def interval_addition(x, y):
    return x[0] + y[0], x[1] + y[1]


def interval_subtraction(x, y):
    return x[0] - y[1], x[1] - y[0]


def interval_negation(x):
    return -x[1], -x[0]


def interval_multiplication(x, y):
    v = [x[i] * y[j] for i in range(2) for j in range(2)]
    return np.min(v), np.max(v)


def interval_inverse(y):
    if y[0] <= 0 <= y[1]:
        if y[1] == 0 and y[0] == 0:
            return [np.infty, np.infty]
        if y[1] == 0:
            return [-np.infty, 1 / y[0]]
        if y[0] == 0:
            return [1 / y[1], np.infty]
        if y[0] < 0 < y[1]:
            return [np.infty, np.infty]
    else:
        return 1 / y[1], 1 / y[0]


def interval_division(x, y):
    return interval_multiplication(x, interval_inverse(y))


def eval_constant(node, variables):
    return [node.value, node.value]


def eval_name(node, variables):
    return variables[node.id]


def eval_binop(node, variables):
    OPERATIONS = {
        ast.Add: interval_addition,
        ast.Sub: interval_subtraction,
        ast.Mult: interval_multiplication,
        ast.Div: interval_division,
    }

    left_value = eval_node(node.left, variables)
    right_value = eval_node(node.right, variables)
    apply = OPERATIONS[type(node.op)]
    return apply(left_value, right_value)


def eval_unaryop(node, variables):
    OPERATIONS = {
        ast.USub: interval_negation,
    }

    operand_value = eval_node(node.operand, vars)
    apply = OPERATIONS[type(node.op)]
    return apply(operand_value)


def eval_expression(node, variables):
    return eval_node(node.body, variables)


def eval_node(node, variables):
    EVALUATORS = {
        ast.Expression: eval_expression,
        ast.Constant: eval_constant,
        ast.Name: eval_name,
        ast.BinOp: eval_binop,
        ast.UnaryOp: eval_unaryop,
    }

    for ast_type, evaluator in EVALUATORS.items():
        if isinstance(node, ast_type):
            return evaluator(node, variables)

    raise KeyError(node)
