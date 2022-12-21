import graphlib
from itertools import count
import operator as op


def do_work(lines, part2=False, initial_human=None):
    """Topologically sort monkeys, find root value.

    For part2, initial_human value can be passed to overwrite humn value.
    """
    toposorter = graphlib.TopologicalSorter()
    nums = {}  # monkey -> number or monkey -> (callable, name, other_name) mapping
    for line in lines:
        name, args = line.split(': ')
        words = args.split()
        if len(words) == 1:
            # number monkey
            if part2 and name == 'humn' and initial_human:
                nums[name] = initial_human
            else:
                nums[name] = int(words[0])
            toposorter.add(name)
        else:
            # math monkey
            arg1, opchar, arg2 = words
            opfun = dict(zip('+-*/', [op.add, op.sub, op.mul, op.floordiv]))[opchar]
            if part2 and name == 'root':
                opfun = op.eq
            nums[name] = (opfun, arg1, arg2)
            toposorter.add(name, arg1, arg2)  # depend on both arguments

    # walk the graph
    for name in toposorter.static_order():
        if isinstance(nums[name], int):
            # nothing to do
            continue
        opfun, arg1, arg2 = nums[name]
        nums[name] = opfun(nums[arg1], nums[arg2])
        if name == 'root':
            return nums[name]


def day21(inp):
    lines = inp.rstrip().splitlines()

    part1 = do_work(lines)
    for it in count():
        #for initial_human in -it, it:
        for initial_human in it,:
            this_is_it = do_work(lines, part2=True, initial_human=initial_human)
            if this_is_it:
                part2 = initial_human
                return part1, part2


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(day21(testinp))
    inp = open('day21.inp').read()
    print(day21(inp))
