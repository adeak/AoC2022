from itertools import takewhile

def day05(inp, part2=False):
    layout, moves = inp.rstrip().split('\n\n')

    # parse layout
    *layout_lines, label_line = layout.splitlines()
    n_buckets = len(label_line.split())
    hanoi = [
        list(takewhile(lambda c: c != ' ', [line[4 * i + 1] for line in layout_lines[::-1]]))
        for i in range(n_buckets)
    ]

    # parse moves
    for move in moves.splitlines():
        words = move.split()
        count, source, target = map(int, words[1::2])
        # watch out for 1-based indices
        source -= 1
        target -= 1
        substack = hanoi[source][-count:]
        if not part2:
            substack = substack[::-1]
        hanoi[target].extend(substack)
        hanoi[source] = hanoi[source][:-count]

    apices = ''.join([tower[-1] for tower in hanoi])

    return apices


if __name__ == "__main__":
    inp = open('day05.inp').read()
    print(day05(inp))
    print(day05(inp, part2=True))
