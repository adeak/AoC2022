def day02(inp, part2=False):
    lines = inp.strip().splitlines()
    shape_scores = dict(zip('XYZ', [1, 2, 3]))
    outcome_scores = dict(zip([-1, 0, 1], [0, 3, 6]))

    def outcome(theirs, ours):
        if (theirs, ours) in [('A', 'X'), ('B', 'Y'), ('C', 'Z')]:
            # draw
            return 0
        if (theirs, ours) in [('A', 'Y'), ('B', 'Z'), ('C', 'X')]:
            # we won
            return 1
        # we lost
        return -1

    shape_score = 0
    outcome_score = 0
    for line in lines:
        theirs, ours = line.split()
        if part2:
            # map to expected outcome
            if ours == 'X':
                ours = dict(zip('ABC', 'ZXY'))[theirs]
            elif ours == 'Y':
                ours = dict(zip('ABC', 'XYZ'))[theirs]
            else:
                ours = dict(zip('ABC', 'YZX'))[theirs]
        outcome_score += outcome_scores[outcome(theirs, ours)]
        shape_score += shape_scores[ours]
    score = shape_score + outcome_score

    return score


if __name__ == "__main__":
    inp = open('day02.inp').read()
    print(day02(inp))
    print(day02(inp, part2=True))
