"""
This code is based on the example calculator from https://github.com/lark-parser/lark/blob/master/examples/calc.py. This
is far simpler than that example, however, and it has a strange order of operations where '+' is before '*'.
"""
from lark import Lark, Transformer, v_args


def load_file(file_name):
    with open(file_name) as f:
        return [x[:-1] for x in f.readlines()]


@v_args(inline=True)
class CalculateTree(Transformer):
    # These have the same name as certain Tokens and will be applied to them during parsing
    # Trees with data field 'add' will have their contents replaced with the result of calling add() on those contents.
    from operator import add, mul
    # This makes it so tokens of type 'number' will be transformed into ints.
    number = int


parser = Lark(open('expr_ordered.lark').read(), parser='lalr', transformer=CalculateTree(), debug=True)
calc = parser.parse


if __name__ == '__main__':
    expr = load_file('input.txt')
    print(f"Sum of all evaluations: {sum([calc(x) for x in expr])}")
