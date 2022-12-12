import numpy as np

def get_neighbs(edge, board, part2):
    """Find neighbours of index `edge` in `board`.

    If `part2`, step at most one level down. Otherwise step at most one level up.
    """
    neighbs = []
    for delta in np.array([[1, 0], [-1, 0], [0, 1], [0, -1]]):
        neighb = edge + delta
        if ((neighb < 0) | (neighb >= board.shape)).any():
            # our of bounds index
            continue
        neighb = tuple(neighb)
        if part2 and board[neighb] < board[edge] - 1:
            # too low
            continue
        if not part2 and board[neighb] > board[edge] + 1:
            # too high
            continue
        neighbs.append(neighb)

    # sort neighbs with highest last so we can choose with that preference
    heights = board[tuple(np.array(neighbs).T)]
    inds = heights.argsort()
    return [neighbs[ind] for ind in inds]


def day12(inp, part2=False):
    # turn map into 2d array of heights, 0 is lowest
    board = np.array([[ord(c) - ord('a') for c in line] for line in inp.splitlines()])

    # handle start and end
    start = tuple(np.ravel((board == ord('S') - ord('a')).nonzero()))
    board[start] = 0
    end = tuple(np.ravel((board == ord('E') - ord('a')).nonzero()))
    board[end] = ord('z') - ord('a')

    # part2: start from end, walk until ground level hit
    if part2:
        start, end = end, start

    # walk the climb
    shortests = {start: 0}  # position -> shortest path length
    comefrom = {}  # position -> shortest-length predecessor position
    target = end  # only used for part 1
    edges = {start}  # candidates for next step
    while edges:
        # find "closest" edge
        edge = min(edges, key=shortests.get)
        steps_now = shortests[edge]
        if (part2 and board[edge] == 0) or (not part2 and edge == target):
            shortest = steps_now
            break

        # get all potential next fields
        candidates = get_neighbs(edge, board, part2)

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

    return shortest


if __name__ == "__main__":
    testinp = open('day12.testinp').read()
    print(day12(testinp), day12(testinp, part2=True))
    inp = open('day12.inp').read()
    print(day12(inp), day12(inp, part2=True))
