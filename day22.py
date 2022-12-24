def parse_board(boardspec, part2=False):
    """Parse the board input.

    Returns
    -------
    walls : set
        Coordinates where there are walls.

    correspondence : dict
        Dict defining where states teleport when walking off the edge.
        Keys are (position, orientation), values are the teleported
        (position, orientation). For part 1 the orientation never changes.

    initial_pos : tuple
        Starting position.
    """
    row_extents = {}  # row index -> [min, max] col indices, inclusive
    col_extents = {}  # col index -> [min, max] row indices, inclusive
    walls = set()  # set of wall positions
    for i, line in enumerate(boardspec.splitlines(), 1):
        for j, c in enumerate(line, 1):
            if c == ' ':
                # ignore this position
                continue
            
            # keep track of walls
            if c == '#':
                walls.add((i, j))
            
            # handle row logistics
            if i not in row_extents:
                # we're at the first column of this row
                row_extents[i] = [j, j]  # [min, max], latter will be updated
            row_extents[i][1] = j  # eventually the max valid index

            # handle column logistics
            if j not in col_extents:
                # we're at the first row of this column
                col_extents[j] = [i, i]
            col_extents[j][1] = i  # eventually the max
    # find initial position
    x0 = 1
    y0 = next(
        y for y in range(row_extents[1][0], row_extents[1][1] + 1)
        if (x0, y) not in walls
    )
    initial_pos = x0, y0

    # prepare for part 2: define correspondence from each edge coordinate
    correspondence = {}
    if part2:
        pass
    else:
        # go 1 beyond row/col extents and jump to the other extent
        for i, minmax in row_extents.items():
            first, last = minmax
            # we only have right (0) and left (2) along rows
            correspondence[((i, last + 1), 0)] = (i, first), 0
            correspondence[((i, first - 1), 2)] = (i, last), 2
        for j, minmax in col_extents.items():
            first, last = minmax
            # we only have down (1) and up (3) along columns
            correspondence[((last + 1, j), 1)] = (first, j), 1
            correspondence[((first - 1, j), 3)] = (last, j), 3

    return walls, correspondence, initial_pos


def day22(inp):
    boardspec, pathspec = inp.rstrip().split('\n\n')

    # parse path
    pathspec = pathspec.replace('R', ' R ').replace('L', ' L ').split()
    # parse board
    walls, correspondence, pos = parse_board(boardspec)

    deltas = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0),
    }

    orientation = 0
    for path_item in pathspec:
        if path_item in 'LR':
            # rotate
            rotation = path_item
            if rotation == 'R':
                orientation = (orientation + 1) % 4
            else:
                orientation = (orientation - 1) % 4
            continue

        # walk
        num_steps = int(path_item)
        delta = deltas[orientation]
        for _ in range(num_steps):
            next_pos = pos[0] + delta[0], pos[1] + delta[1]
            # teleport if necessary
            if (next_pos, orientation) in correspondence:
                next_pos, next_orientation = correspondence[next_pos, orientation]
            else:
                next_orientation = orientation

            # check if step is valid
            if next_pos in walls:
                break
            pos = next_pos
            orientation = next_orientation

    password = 1000 * pos[0] + 4 * pos[1] + orientation
    return password


if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    print(day22(testinp))
    inp = open('day22.inp').read()
    print(day22(inp))
