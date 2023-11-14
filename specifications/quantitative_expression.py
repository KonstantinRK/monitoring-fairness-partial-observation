from specifications.expression import Expression


class QuantitativeExpression(Expression):

    # Atom map, name in expression to atom class
    def __init__(self, name, expression, atoms, lower_bound=None, upper_bound=None):
        super().__init__(name, expression, atoms, lower_bound, upper_bound)

    