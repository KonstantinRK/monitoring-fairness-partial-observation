import ast
import operator

def eval_constant(node, variables):
    return node.value


def eval_name(node, variables):
    return variables[node.id]


def eval_binop(node, variables):
    OPERATIONS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    left_value = eval_node(node.left, variables)
    right_value = eval_node(node.right, variables)
    apply = OPERATIONS[type(node.op)]
    try:
        return apply(left_value, right_value)
    except ZeroDivisionError:
        return float("nan")


def eval_unaryop(node, variables) -> float:
    OPERATIONS = {
        ast.USub: operator.neg,
    }

    operand_value = eval_node(node.operand, vars)
    apply = OPERATIONS[type(node.op)]
    return apply(operand_value)


def eval_expression(node, variables) -> float:
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