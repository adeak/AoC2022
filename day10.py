def day10(inp):
    lines = inp.rstrip().splitlines()

    x = 1
    cycle = signal_strength = 0
    interesting_cycles = iter(range(20, 221, 40))  # part 1
    next_interesting = next(interesting_cycles)
    screen = [[] for _ in range(6)]  # part 2
    for line in lines:
        op, *args = line.split()
        if op == 'noop':
            n_cycles = 1
            delta = 0
        elif op == 'addx':
            n_cycles = 2
            delta = int(args[0])
        for _ in range(n_cycles):
            i, j = divmod(cycle, 40)
            cycle += 1
            screen[i].append('#' if abs(j - x) <= 1 else ' ')  # part 2
            if cycle == next_interesting:
                # part 1
                signal_strength += cycle * x
                next_interesting = next(interesting_cycles, None)
        x += delta
    part1 = signal_strength
    part2 = '\n'.join([''.join([c for c in row]) for row in screen])

    return part1, part2


if __name__ == "__main__":
    inp = open('day10.inp').read()
    print(*day10(inp), sep='\n')
