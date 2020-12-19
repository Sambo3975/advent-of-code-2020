"""
This isn't the way you should normally use Lark, but this is what I wrote while following the first tutorial on it. To
see an example of more proper usage, see part_2.py.
"""
from lark import Lark, Tree
parser = Lark(open('expr.lark').read())


def load_file(file_name):
    with open(file_name) as f:
        return [x[:-1] for x in f.readlines()]


def run_instruction(t):
    if t.data == 'expr':
        lhs, op, rhs = t.children
        if isinstance(lhs, Tree):
            lhs = run_instruction(lhs)
        if isinstance(rhs, Tree):
            rhs = run_instruction(rhs)
        return {
            '+': lambda x, y: x + y,
            '*': lambda x, y: x * y,
        }[op](lhs, rhs)

    elif t.data == 'token':
        token = t.children[0]
        if isinstance(token, Tree):
            token = run_instruction(token)
        return int(token)

    else:
        raise SyntaxError(f"Invalid expression.")


def run_expr(expr):
    parse_tree = parser.parse(expr)

    return run_instruction(parse_tree.children[0])


if __name__ == '__main__':
    expressions = load_file('input.txt')
    print(f"Sum of all evaluations: {sum([run_expr(e) for e in expressions])}")
