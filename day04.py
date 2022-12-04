def day04(inp):
    lines = inp.strip().splitlines()

    contains = 0  # part1
    overlaps = 0  # part2
    for line in lines:
        first, second = line.split(',')
        nums = [tuple(map(int, substr.split('-'))) for substr in [first, second]]
        ranges = [range(pair[0], pair[1] + 1) for pair in nums]
        sets = list(map(set, ranges))
        if sets[0] & sets[1]:
            overlaps += 1
            if sets[0] <= sets[1] or sets[1] <= sets[0]:
                contains += 1

    return contains, overlaps


if __name__ == "__main__":
    inp = open('day04.inp').read()
    print(day04(inp))
