import string

def day03(inp):
    lines = inp.strip().splitlines()
    prios = dict(zip(string.ascii_lowercase + string.ascii_uppercase, range(1, 53)))

    score = 0
    for line in lines:
        first, second = line[:len(line)//2], line[len(line)//2:]
        score += prios[(set(first) & set(second)).pop()]

    return score


def day03b(inp):
    lines = inp.strip().splitlines()
    groups = zip(*[iter(lines)] * 3)  # iterator of line triples
    prios = dict(zip(string.ascii_lowercase + string.ascii_uppercase, range(1, 53)))

    score = 0
    for group in groups:
        common = set.intersection(*map(set, group))  # set(first) & set(second) & set(third)
        score += prios[common.pop()]

    return score


if __name__ == "__main__":
    inp = open('day03.inp').read()
    print(day03(inp))
    print(day03b(inp))
