from collections import deque
from itertools import count, cycle
from math import prod

def day11(inp, part2=False):
    blocks = inp.rstrip().split('\n\n')

    # parse monkeys
    items = []  # list of deques for each monkey
    ops = []  # list of callables for each monkey
    moduli = []  # list of int (moduli) for each monkey
    successors = []  # list of (int, int) tuples for each monkey
    for i, block in enumerate(blocks):
        header, itemline, opline, testline, *if_true_false = block.splitlines()

        # sanity check for monkey index
        assert int(header.split()[-1][:-1]) == i
        items.append(deque(map(int, itemline.replace(',', '').split()[2:])))
        # sanity check for operation kind
        assert opline.split()[-2] in '*+'

        args = opline.split()[-3:]
        def op(val, args=args):
            """Determine new value if this monkey looks at an item."""
            ops = [
                int(arg) if arg.isdigit() else val
                for arg in args[::2]
            ]
            return prod(ops) if args[1] == '*' else sum(ops)
        ops.append(op)
        moduli.append(int(testline.split()[-1]))
        successors.append(tuple(int(line.split()[-1]) for line in if_true_false))
    n_monkeys = len(items)

    # simulate rounds
    inspections = [0] * n_monkeys
    it = 0
    n_rounds = 20
    for monkey in cycle(range(n_monkeys)):
        for item in items[monkey]:
            inspections[monkey] += 1
            new_val = ops[monkey](item) // 3
            successor_options = successors[monkey]
            if new_val % moduli[monkey]:
                # not divisible
                successor = successor_options[1]
            else:
                successor = successor_options[0]
            items[successor].append(new_val)
        items[monkey] = deque()

        if monkey == n_monkeys - 1:
            # end of a round
            it += 1

        if it == n_rounds:
            monkey_business = prod(sorted(inspections)[-2:])
            break

    return monkey_business


def day11b(inp, part2=False):
    blocks = inp.rstrip().split('\n\n')

    # parse monkeys
    # numbers in part2 too large to keep track of; instead of tracking each "worth" value, only
    # keep track of the modulus of each value with respect to every possible modulus (from every
    # monkey)
    items = []  # list of deques for each monkey; deque items are a dict of remainders eventually
    ops = []  # list of callables for each monkey
    moduli = []  # list of int (moduli) for each monkey
    successors = []  # list of (int, int) tuples for each monkey
    for i, block in enumerate(blocks):
        header, itemline, opline, testline, *if_true_false = block.splitlines()

        # sanity check for monkey index
        assert int(header.split()[-1][:-1]) == i
        # collect raw int items initially, postprocess into dict of remainders later
        items.append(deque(map(int, itemline.replace(',', '').split()[2:])))
        # sanity check for operation kind
        assert opline.split()[-2] in '*+'

        args = opline.split()[-3:]
        def op(val, args=args):
            """Determine new value if this monkey looks at an item."""
            ops = [
                int(arg) if arg.isdigit() else val
                for arg in args[::2]
            ]
            return prod(ops) if args[1] == '*' else sum(ops)
        ops.append(op)
        moduli.append(int(testline.split()[-1]))
        successors.append(tuple(int(line.split()[-1]) for line in if_true_false))
    n_monkeys = len(items)

    # replace each raw item with a modulus -> remainder mapping
    items = [
        deque(
            {modulus: raw_value % modulus for modulus in moduli}
            for raw_value in item
        )
        for item in items
    ]

    # simulate rounds
    inspections = [0] * n_monkeys
    it = 0
    n_rounds = 10_000
    for monkey in cycle(range(n_monkeys)):
        op = ops[monkey]  # operates on a single value (remainder)
        for old_remainders in items[monkey]:
            inspections[monkey] += 1
            # for each modulus of interest, use monkey op to compute new remainder and re-apply mod
            new_remainders = {
                modulus: op(old_remainder) % modulus
                for modulus, old_remainder in old_remainders.items()
            }
            successor_options = successors[monkey]
            # pick out relevant modulus of interest for this monkey
            if new_remainders[moduli[monkey]]:
                # not divisible
                successor = successor_options[1]
            else:
                successor = successor_options[0]
            items[successor].append(new_remainders)
        items[monkey] = deque()

        if monkey == n_monkeys - 1:
            # end of a round
            it += 1

        if it == n_rounds:
            monkey_business = prod(sorted(inspections)[-2:])
            break

    return monkey_business


if __name__ == "__main__":
    testinp = open('day11.testinp').read()
    print(day11(testinp), day11b(testinp))
    inp = open('day11.inp').read()
    print(day11(inp), day11b(inp))
