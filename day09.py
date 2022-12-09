def day09(inp, part2=False):
    lines = inp.rstrip().splitlines()

    n_knots = 10 if part2 else 2

    poses = [(0, 0)] * n_knots  # index 0 is head, -1 is tail
    visiteds = {poses[-1]}
    for line in lines:
        dir, count = line.split()
        count = int(count)
        for _ in range(count):
            # step
            i0, j0 = poses[0]
            if dir == 'L':
                i0 -= 1
            elif dir == 'R':
                i0 += 1
            elif dir == 'U':
                j0 -= 1
            elif dir == 'D':
                j0 += 1
            else:
                raise ValueError(f'Invalid direction {dir!r}.')
            poses[0] = i0, j0

            for knot_index, pos in enumerate(poses[1:], start=1):
                # step if necessary
                i0, j0 = poses[knot_index - 1]  # new position of previous knot
                i1, j1 = pos  # current position of this knot
                if max(abs(i0 - i1), abs(j0 - j1)) <= 1:
                    # nothing to do
                    continue
                if i0 == i1:
                    # step along y
                    j1 += (j0 - j1) // abs(j0 - j1)
                elif j0 == j1:
                    # step along x
                    i1 += (i0 - i1) // abs(i0 - i1)
                else:
                    # step diagonally
                    if abs(i0 - i1) == 1:
                        # distance is (+-1, +-2)
                        i1 = i0
                        j1 += (j0 - j1) // abs(j0 - j1)
                    elif abs(j0 - j1) == 1:
                        # distance is (+-2, +-1)
                        j1 = j0
                        i1 += (i0 - i1) // abs(i0 - i1)
                    else:
                        # distance is (+-2, +-2)
                        i1 += (i0 - i1) // abs(i0 - i1)
                        j1 += (j0 - j1) // abs(j0 - j1)
                poses[knot_index] = i1, j1  # update this knot

            # track positions
            visiteds.add(poses[-1])
    res = len(visiteds)

    return res


if __name__ == "__main__":
    testinp = open('day09.testinp').read()
    print(day09(testinp))
    testinp2 = open('day09.testinp2').read()
    print(day09(testinp2, part2=True))
    inp = open('day09.inp').read()
    print(day09(inp))
    print(day09(inp, part2=True))
