import numpy as np


def get_neighbs(edge, board):
    """Find neighbours of index `edge` in `board`."""
    neighbs = []
    for delta in np.array([[1, 0], [-1, 0], [0, 1], [0, -1]]):
        neighb = edge + delta
        if ((neighb < 0) | (neighb >= board.shape)).any():
            # our of bounds index
            continue
        neighb = tuple(neighb)
        if board[neighb] > board[edge] + 1:
            # too high
            continue
        neighbs.append(neighb)

    # sort neighbs with highest last so we can choose with that preference
    heights = board[tuple(np.array(neighbs).T)]
    inds = heights.argsort()
    return [neighbs[ind] for ind in inds]
        

def day12(inp):
    # turn map into 2d array of heights, 0 is lowest
    board = np.array([[ord(c) - ord('a') for c in line] for line in inp.splitlines()])

    # handle start and end
    start = tuple(np.ravel((board == ord('S') - ord('a')).nonzero()))
    board[start] = 0
    end = tuple(np.ravel((board == ord('E') - ord('a')).nonzero()))
    board[end] = ord('z') - ord('a')

    # handle part 2 too
    true_start = start
    overall_shortest_lengths = {}

    starts = set(zip(*(board == 0).nonzero()))  # all lowest points
    start = true_start
    starts.remove(start)  # necessary because we could skip this later
    while starts:
        # walk the climb
        shortests = {start: 0}  # position -> shortest path length
        comefrom = {}  # position -> shortest-length predecessor position
        target = end
        edges = {start}  # candidates for next step
        while edges:
            # find "closest" edge
            edge = min(edges, key=shortests.get)
            steps_now = shortests[edge]
            if edge == target:
                # we're done for this starting point
                overall_shortest_lengths[start] = steps_now
                # if there are any lowest points along the shortest path:
                # only keep last one
                current = edge
                lowests = []
                while current != start:
                    current = comefrom[current]
                    if board[current] == 0:
                        # we have a lowest point
                        lowests.append(current)
                # now we have a list of "lowests" in reverse order that excludes "start"
                # no point in checking all but the first value later for part 2
                # (and we know for sure part 1 is what we start with)
                starts -= set(lowests[1:])
                break

            # get all potential next fields
            candidates = get_neighbs(edge, board)

            # filter out already visited fields if shorter
            candidates = [
                candidate
                for candidate in candidates
                if shortests.get(candidate, np.inf) > steps_now + 1
            ]

            if not candidates:
                # nowhere to go from here
                edges.remove(edge)
                continue

            # choose highest candidate
            next_field = candidates[-1]
            shortests[next_field] = steps_now + 1
            comefrom[next_field] = edge
            edges.add(next_field)

        # prepare for next starting point
        start = starts.pop()

    part1 = overall_shortest_lengths[true_start]
    part2 = min(overall_shortest_lengths.values())

    return part1, part2


if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(day12(testinp))
    inp = open('day12.inp').read()
    print(day12(inp))
