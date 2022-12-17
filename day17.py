from itertools import count, cycle


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
    last_complete_row = None  # last height where there was a full row
    complete_row_deltas = {}  # complete row distance -> rock count when achieved
    heights = []  # history of heights
    period = None  # to be determined empirically
    for it in count():
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
        heights.append(height)

        # for part 2: there has to be periodicity
        #             so let's compute the period from how often the distance between
        #             two consecutive filled rows repeats
        for y in range(0 if last_complete_row is None else last_complete_row + 1, height):
            if all((x, y) in landscape for x in range(7)):
                # we have a new complete row
                if last_complete_row is not None:
                    # we have a delta
                    delta = y - last_complete_row
                    last_complete_row = y
                else:
                    last_complete_row = y
                    continue

                # check if there's repetition
                if delta in complete_row_deltas:
                    # we have the period
                    prev_it = complete_row_deltas[delta]
                    period = it - prev_it
                    # keep heights only within a period
                    heights_in_period = heights[prev_it:]
                    deltas_in_period = [h2 - h1 for h1, h2 in zip(heights_in_period, heights_in_period[1:])]
                    break
                else:
                    # have to keep looking for period
                    complete_row_deltas[delta] = it
        if period is not None:
            # we're also done for part 2
            break

    # now we have a period of at worst `period` ranging from prev_it to it
    # extrapolate from repeating height differences
    parts = []
    for rock_count in 2022, 1_000_000_000_000:
        target_it = rock_count - 1
        target_mod, target_rem = divmod(target_it, period)

        ref_height = heights_in_period[0]  # height at rock index `prev_it`
        ref_mod, ref_rem = divmod(prev_it, period)

        # assume target_rem > ref_rem for now...
        remainder_offset = heights_in_period[target_rem - ref_rem] - ref_height

        period_offset = (target_mod - ref_mod) * sum(deltas_in_period)
        #remainder_offset = sum(deltas_in_period[:target_rem])
        parts.append(ref_height + period_offset + remainder_offset)


    return tuple(parts)


if __name__ == "__main__":
    testinp = open('day17.testinp').read()
    inp = open('day17.inp').read()
    #print(day17(testinp))  # doesn't work due to assumptions (no full rows in test); infinite loop
    print(day17(inp))
