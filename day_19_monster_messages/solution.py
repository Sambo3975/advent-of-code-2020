import re
from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF
from multiprocessing import Process
import time


def rules_to_lark(rules, start_rule=None, substitute=False):
    if substitute:  # For part 2, two rules must be changed.
        rules = rules.replace("8: 42\n", "8: 42 | 42 8\n")
        rules = rules.replace("11: 42 31\n", "11: 42 31 | 42 11 31\n")
    # The rules are already almost valid Lark EBNF. I just need to precede each number with a letter so the rules
    # have valid names
    rules = re.sub(r"(\d+)", r"r\1", rules)
    # I also need to set the starting rule
    if start_rule is None:
        start_rule = rules[:rules.find(':')]  # Default to the first rule
    return Lark(rules, start=start_rule).parse


def load_file(file_name, start_rule=None, substitute=False):
    with open(file_name) as f:
        data = f.read().split('\n\n')
    return rules_to_lark(data[0], start_rule, substitute), data[1].split('\n')[:-1]


def parse_thread(substitute):
    parse, strings = load_file('input.txt', start_rule='r0', substitute=substitute)
    valid_count = len(strings)
    for x in strings:
        try:
            parse(x)
        except (UnexpectedCharacters, UnexpectedEOF):
            # The string caused an exception while parsing, so it isn't valid
            valid_count -= 1
    if substitute:
        print(f"There are {valid_count} valid strings when substituting rules 8 and 11.")
    else:
        print(f"There are {valid_count} valid strings when not substituting rules 8 and 11.")


if __name__ == '__main__':
    start = time.time()

    no_sub_thread = Process(target=parse_thread, args=(False,))
    sub_thread = Process(target=parse_thread, args=(True,))

    no_sub_thread.start()
    sub_thread.start()

    while no_sub_thread.is_alive():
        no_sub_thread.join()
    while sub_thread.is_alive():
        sub_thread.join()

    # This is about 3.5 seconds faster than without multiprocessing.
    # That makes sense, because the parse without substitution takes about the same amount of time.
    # I tested this on my Ryzen 7 3700x, which has 8 cores (16 threads)
    print(f"\nFinished after {time.time() - start} seconds")
