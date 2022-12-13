from functools import cmp_to_key
from json import loads
from math import prod


def compare_trees(first, second):
    """Compare two ints or lists.

    If first < second, return a negative int.
    If first == second, return 0.
    Otherwise return a positive int.
    """
    if isinstance(first, int) and isinstance(second, int):
        if first < second:
            return -1
        if first == second:
            return 0
        return 1

    # recurse into lists
    for lval, rval in zip(first, second):
        if isinstance(lval, int) and isinstance(rval, list):
            lval = [lval]
        elif isinstance(lval, list) and isinstance(rval, int):
            rval = [rval]
        subcomparison = compare_trees(lval, rval)
        if subcomparison != 0:
            # lval is smaller or larger
            return subcomparison

    # tied nested values: check list lengths
    return len(first) - len(second)


def day13(inp):
    blocks = inp.rstrip().split('\n\n')

    # part1
    sorted_pairs = 0
    for index, block in enumerate(blocks, start=1):
        first, second = map(loads, block.splitlines())
        if compare_trees(first, second) <= 0:
            sorted_pairs += index

    # part 2
    lines = '\n'.join(blocks + ['[[2]]\n[[6]]'])
    signals = map(loads, lines.splitlines())
    sorted_signals = sorted(signals, key=cmp_to_key(compare_trees))
    decoder_key = prod(
        index
        for index, value in enumerate(sorted_signals, start=1)
        if value in [[[2]], [[6]]]
    )

    return sorted_pairs, decoder_key


if __name__ == "__main__":
    testinp = open('day13.testinp').read()
    print(day13(testinp))
    inp = open('day13.inp').read()
    print(day13(inp))
