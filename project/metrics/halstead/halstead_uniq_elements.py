from .halstead_operators import get_operators
from .halstead_operands import get_operands


def calculate(node):
    operators = get_operators(node)
    operands = get_operands(node)

    n1 = len(set(operators))
    n2 = len(set(operands))

    print("n1: ",  operators, n1)
    print("n2: ",  operands, n2)


    return n1 + n2