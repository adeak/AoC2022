def day02(inp, part2=False):
    lines = inp.strip().splitlines()
    shape_scores = dict(zip('ABC', [1, 2, 3]))
    outcome_scores = dict(zip([-1, 0, 1], [0, 3, 6]))  # -1: we lost
    beating_shapes = dict(zip('ABC', 'BCA'))  # A beaten by B etc.
    losing_shapes = dict(zip('ABC', 'CAB'))  # A beats C etc.
    translation = str.maketrans('XYZ', 'ABC')  # for part 1

    def outcome(theirs, ours):
        if theirs == ours:
            # draw
            return 0
        if ours == beating_shapes[theirs]:
            # we win
            return 1
        # we lose
        return -1

    shape_score = 0
    outcome_score = 0
    for line in lines:
        theirs, ours = line.split()
        if not part2:
            ours = ours.translate(translation)
        else:
            # map to expected outcome
            if ours == 'X':
                # need to lose
                ours = losing_shapes[theirs]
            elif ours == 'Y':
                # need to draw
                ours = theirs
            elif ours == 'Z':
                # need to win
                ours = beating_shapes[theirs]
            else:
                raise ValueError(f'Unexpected letter {ours}.')

        outcome_score += outcome_scores[outcome(theirs, ours)]
        shape_score += shape_scores[ours]

    score = shape_score + outcome_score

    return score


if __name__ == "__main__":
    inp = open('day02.inp').read()
    print(day02(inp))
    print(day02(inp, part2=True))
