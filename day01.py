def day01(inp):
    blocks = inp.strip().split('\n\n')
    valses = [list(map(int, block.splitlines())) for block in blocks]
    sums = sorted(sum(vals) for vals in valses)

    part1 = sums[-1]
    part2 = sum(sums[-3:])
    return part1, part2


if __name__ == "__main__":
    inp = open('day01.inp').read()
    print(day01(inp))
