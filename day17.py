from itertools import cycle


def tuple_add(first, second):
    """Add two 2-tuples component-wise."""
    return first[0] + second[0], first[1] + second[1]


def rock_overlaps(pos, rock, landscape):
    """Return whether a given rock at pos overlaps with older rocks."""
    return any(tuple_add(pos, dpos) in landscape for dpos in rock)


def day17(inp):
    # parse input characters into dx deltas
    dxs = cycle(-1 if c == '<' else 1 for c in inp.strip())

    # rock origin (bottom left) relative coordinate is (0, 0) = (x, y) = (horizontal, vertical)
    # world coordinates have (0, 0) in bottom left of screen, x in range(7), y grows upwards
    # rock starting position is (2, height + 3)

    rocks = cycle([
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ])

    height = 0
    landscape = set()  # set of sedimented rock positions
    for it in range(2022):
        rock = next(rocks)
        pos = (2, height + 3)  # position of rock origin (bottom left corner)
        for dx in dxs:
            # 1. move to the side if possible
            next_pos = pos[0] + dx, pos[1]
            next_pieces = {tuple_add(next_pos, dpos) for dpos in rock}
            max_x = max(next_piece[0] for next_piece in next_pieces)
            # check if wall or rock hit
            if 0 <= next_pos[0] <= max_x < 7 and not rock_overlaps(next_pos, rock, landscape):
                # valid move
                pos = next_pos

            # 2. move down if possible
            next_pos = pos[0], pos[1] - 1
            if next_pos[1] < 0 or rock_overlaps(next_pos, rock, landscape):
                # we hit the floor or rock below
                # take care to use (previous) pos instead of next_pos here
                new_pieces = {tuple_add(pos, dpos) for dpos in rock}
                landscape |= new_pieces
                height = max(height, max(new_piece[1] + 1 for new_piece in new_pieces))
                break
            # the way is free below
            pos = next_pos
    part1 = height

    return part1


if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    inp = open('day17.inp').read()
    print(day17(testinp))
    print(day17(inp))
