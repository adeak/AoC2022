from itertools import count

def day14(inp):
    lines = inp.rstrip().splitlines()

    ROCK, SAND = '#', 'o'

    # parse cave
    cave = {}
    for line in lines:
        pairs = line.split(' -> ')
        for x0y0, x1y1 in zip(pairs, pairs[1:]):
            x0, y0 = map(int, x0y0.split(','))
            x1, y1 = map(int, x1y1.split(','))
            if x0 == x1:
                y0, y1 = sorted([y0, y1])
                for y in range(y0, y1 + 1):
                    cave[x0, y] = ROCK
            elif y0 == y1:
                x0, x1 = sorted([x0, x1])
                for x in range(x0, x1 + 1):
                    cave[x, y0] = ROCK
            else:
                raise ValueError(f'Invalid rock section found: {(x0, y0)} -> {(x1, y1)}')
    bottom = max(key[1] for key in cave)

    # start simulation
    part1 = None
    for sands in count(0):
        pos = (500, 0)
        while True:
            for delta in 0, -1, 1:
                # check below, left below, right below in this order
                next_pos = pos[0] + delta, pos[1] + 1
                if next_pos not in cave:
                    # fall down
                    break
            else:
                # all 3 positions were blocked; sediment and go to next grain of sand
                cave[pos] = SAND
                break
            # we could move
            pos = next_pos

            if pos[1] == bottom:
                # we've reached the bottom
                part1 = sands
                break
            
        if part1 is not None:
            break

    return part1#, part2


if __name__ == "__main__":
    testinp = open('day14.testinp').read()
    print(day14(testinp))
    inp = open('day14.inp').read()
    print(day14(inp))
