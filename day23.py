from collections import defaultdict, deque, Counter
from itertools import count


def get_adjacents(elf, board):
    neighb_tiles = {
        (elf[0] + di, elf[1] + dj)
        for di in range(-1, 2)
        for dj in range(-1, 2)
        if not di == dj == 0
    }
    return neighb_tiles & board


def ground_covered(board):
    extents = [0, 0, 0, 0]
    for elf in board:
        extents[0] = min(extents[0], elf[0])  # xmin
        extents[1] = max(extents[1], elf[0])  # xmax
        extents[2] = min(extents[2], elf[1])  # ymin
        extents[3] = max(extents[3], elf[1])  # ymax
    return (extents[1] - extents[0] + 1) * (extents[3] - extents[2] + 1) - len(board)


def day23(inp):
    lines = inp.rstrip().splitlines()
    board = {
        (i, j)
        for i, line in enumerate(lines)
        for j, c in enumerate(line)
        if c == '#'
    }
    steps = deque([
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ])

    for it in count(1):
        step_plans_by_elf = {}  # planned next position for each elf
        step_plans_by_tile = Counter()  # "to" -> number of "from" mapping for a given tile

        # first half round
        for elf in board:
            adjacents = get_adjacents(elf, board)
            if not adjacents:
                # elf stays put
                continue
            for di, dj in steps:
                if di == 0:
                    check_tiles = {(elf[0] + delta, elf[1] + dj) for delta in range(-1, 2)}
                else:
                    check_tiles = {(elf[0] + di, elf[1] + delta) for delta in range(-1, 2)}
                if not check_tiles & adjacents:
                    # tested tiles don't have any elves on them
                    elf_proposal = elf[0] + di, elf[1] + dj
                    break
            else:
                # all positions were blocked, stay put
                continue
            step_plans_by_elf[elf] = elf_proposal
            step_plans_by_tile[elf_proposal] += 1

        # second half round: collect elves that actually move
        valid_elves = {
            elf: target_tile
            for elf, target_tile in step_plans_by_elf.items()
            if step_plans_by_tile[target_tile] == 1
        }
        board -= valid_elves.keys()
        board |= set(valid_elves.values())

        # rotate strategy
        steps.rotate(-1)

        # check stop conditions
        if it == 10:
            part1 = ground_covered(board)
        if not valid_elves:
            part2 = it
            break

    return part1, part2


if __name__ == "__main__":
    testinp = open('day23.testinp').read()
    print(day23(testinp))
    inp = open('day23.inp').read()
    print(day23(inp))
