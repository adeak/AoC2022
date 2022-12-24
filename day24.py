from collections import defaultdict


class Blizzard:
    deltas = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }

    def __init__(self, pos, orientation, width, height):
        self.initpos = pos
        self.delta = self.deltas[orientation]
        self.boardsize = height, width

    def predict(self, step):
        """Compute where this blizzard is after `step` steps."""
        predicted_pos = tuple(
            (pos + step * dpos) % size
            for pos, dpos, size in zip(self.initpos, self.delta, self.boardsize)
        )
        return predicted_pos


def get_neighbs(pos, width, height):
    """Get all valid neighbour tiles of a given position."""
    neighbs = set()
    for delta in (1, 0), (-1, 0), (0, 1), (0, -1):
        next_pos = pos[0] + delta[0], pos[1] + delta[1]
        if 0 <= next_pos[0] < height and 0 <= next_pos[1] < width:
            # this is a valid tile
            neighbs.add(next_pos)
    return neighbs


def day24(inp):
    lines = inp.rstrip().splitlines()

    # parse inputs
    width, height = len(lines[0]) - 2, len(lines) - 2
    start = (-1, lines[0][1:].index('.'))
    end = (height, lines[-1][1:].rindex('.'))
    blizzards_by_row = defaultdict(set)  # row index -> blizzards mapping
    blizzards_by_col = defaultdict(set)  # col index -> blizzards mapping
    for i, line in enumerate(lines[1:-1]):
        # strip away walls
        line = line[1:-1]
        for j, c in enumerate(line):
            if c == '.':
                continue
            blizzard = Blizzard((i, j), c, width, height)
            blizzards_by_row[i].add(blizzard)
            blizzards_by_col[j].add(blizzard)

    # part 2 shenanigans
    true_start = start
    true_end = end

    # BFS, hoping that most paths will run into blizzards and die
    min_times = []
    for start, end in (true_start, true_end), (true_end, true_start), (true_start, true_end):
        paths = [(start,)]
        seens = defaultdict(set)  # times at which a position was already visited
        seens[start].add(0)
        while True:
            next_paths = []
            for path in paths:
                time = len(path) - 1
                pos = path[-1]
                # end condition
                if abs(pos[0] - end[0]) + abs(pos[1] - end[1]) == 1:
                    # we'll be there in the next step; done for this trip
                    min_times.append(time + 1)
                    break

                next_time = time + 1
                # get valid neighbour tiles
                neighbs = get_neighbs(pos, width, height)
                # ignore neighbour tiles if we were already there
                # (turns out to be super important for pruning the state space)
                neighbs = {
                    neighb
                    for neighb in neighbs
                    if next_time not in seens[neighb]
                }
                # add "this" tile (waiting)
                neighbs.add(pos)
                # keep tiles that won't coincide with blizzards
                trip_offset = sum(min_times)  # delay from any earlier trips (part 2)
                neighbs = {
                    neighb
                    for neighb in neighbs
                    if all(
                        blizzard.predict(next_time + trip_offset) != neighb
                        for blizzard in blizzards_by_row[neighb[0]]
                    ) and all(
                        blizzard.predict(next_time + trip_offset) != neighb
                        for blizzard in blizzards_by_col[neighb[1]]
                    )
                }
                # for any valid neighbs we can keep going that way
                for neighb in neighbs:
                    next_paths.append(path + (neighb,))
                    seens[neighb].add(next_time)
            else:
                # we have to keep going
                paths = next_paths
                continue
            # we've found a shortest path
            break

    return min_times[0], sum(min_times)


if __name__ == "__main__":
    testinp = open('day24.testinp').read()
    print(day24(testinp))
    inp = open('day24.inp').read()
    print(day24(inp))
