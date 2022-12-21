import graphlib
import sympy as sym


def day21(inp):
    lines = inp.rstrip().splitlines()

    # parse inputs into a toposorter graph
    toposorter = graphlib.TopologicalSorter()
    nums = {}  # monkey -> number or monkey -> (callable, name, other_name) mapping
    for line in lines:
        name, args = line.split(': ')
        words = args.split()
        if len(words) == 1:
            # number monkey
            if name == 'humn':
                # prepare for part 2
                HUMN_VALUE = words[0]
                nums[name] = 'x'
            else:
                nums[name] = int(words[0])
            toposorter.add(name)
        else:
            # math monkey
            arg1, opchar, arg2 = words
            if name == 'root':
                root_op = opchar
                opchar = 'ROOT_OP'
            nums[name] = (opchar, arg1, arg2)
            toposorter.add(name, arg1, arg2)  # depend on both arguments

    # walk the graph, build expression string, replace humn with variable
    for name in toposorter.static_order():
        if name == 'humn':
            nums[name] = 'x'
            continue
        if isinstance(nums[name], int):
            continue
        opchar, argname1, argname2 = nums[name]
        arg1, arg2 = nums[argname1], nums[argname2]
        if isinstance(arg1, int) and isinstance(arg2, int):
            # make work a bit easier by folding constants
            nums[name] = eval(f'{arg1} {opchar.replace("/", "//")} {arg2}')
        else:
            nums[name] = f'({arg1} {opchar} {arg2})'
        if name == 'root':
            # we're done building an evaluable expression
            expr = nums[name]
            # part 1:
            #    substitute x for original human value
            #    restore root operator
            #    replace truediv with floordiv
            #    evaluate
            part1 = eval(
                expr.replace('x', HUMN_VALUE).replace('ROOT_OP', root_op).replace('/', '//'),
                globals()
            )
            # part 2:
            #    replace '==' with '-' to turn 'f(x) == c' into 'f(x) - c' (== 0) for sympy
            root_expr = expr.replace('ROOT_OP', '-')  # part 2 (reduce equation to 0!)
            break

    # part 2: cheat
    part2 = sym.solve(root_expr, 'x')[0]
    return part1, part2


if __name__ == "__main__":
    testinp = open('day21.testinp').read()
    print(day21(testinp))
    inp = open('day21.inp').read()
    print(day21(inp))
