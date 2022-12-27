from itertools import repeat

RIGHT, DOWN, LEFT, UP = range(4)
deltas = {
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1),
    UP: (-1, 0),
}


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
    num_fields = 0  # number of fields on the board for part 2
    for i, line in enumerate(boardspec.splitlines(), 1):
        for j, c in enumerate(line, 1):
            if c == ' ':
                # ignore this position
                continue
            num_fields += 1
            
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
        # hard-coded cube folding for now... doesn't work for test input
        # pair 7 pairs of edges in production output
        # pairs are defined by (edge1, edge2, reverse) triples
        # where each edge is a (*face_pos, side) tuple
        # where face_pos is the index of the given face (in a 4x3 grid)
        # and side is UP/DOWN/LEFT/RIGHT
        # and reverse is a bool whether the two edges are oppositely
        # oriented (the default is top to bottom and left to right)

        pairs = [
            ((2, 1, DOWN), (3, 0, RIGHT), False),
            ((1, 1, LEFT), (2, 0, UP), False),
            ((0, 2, DOWN), (1, 1, RIGHT), False),
            ((0, 2, RIGHT), (2, 1, RIGHT), True),
            ((0, 2, UP), (3, 0, DOWN), False),
            ((0, 1, UP), (3, 0, LEFT), False),
            ((0, 1, LEFT), (2, 0, LEFT), True),
        ]

        # generate correspondence to teleport with for each edge pair, both ways
        n_cube = int((num_fields // 6)**0.5)  # linear size of the cube
        for first, second, reverse in pairs:
            # get the indices of the edges that are part of the board
            row_inds = []
            col_inds = []
            for (n, m, edge) in first, second:
                if edge == LEFT:
                    row_inds.append(range(n*n_cube + 1, n*n_cube + 1 + n_cube))
                    col_inds.append(list(repeat(m*n_cube + 1, n_cube)))
                elif edge == RIGHT:
                    row_inds.append(range(n*n_cube + 1, n*n_cube + 1 + n_cube))
                    col_inds.append(list(repeat(m*n_cube + n_cube, n_cube)))
                elif edge == DOWN:
                    row_inds.append(list(repeat(n*n_cube + n_cube, n_cube)))
                    col_inds.append(range(m*n_cube + 1, m*n_cube + 1 + n_cube))
                else:
                    row_inds.append(list(repeat(n*n_cube + 1, n_cube)))
                    col_inds.append(range(m*n_cube + 1, m*n_cube + 1 + n_cube))

            # reverse one edge if necessary
            if reverse:
                row_inds[0] = row_inds[0][::-1]
                col_inds[0] = col_inds[0][::-1]

            # generate step from first to second
            from_orientation = first[-1]
            to_orientation = (second[-1] + 2) % 4  # up <-> down, left <-> right
            di, dj = deltas[from_orientation]
            for i1, j1, i2, j2 in zip(row_inds[0], col_inds[0], row_inds[1], col_inds[1]):
                correspondence[(i1 + di, j1 + dj), from_orientation] = (i2, j2), to_orientation

            # generate step from second to first
            from_orientation = second[-1]
            to_orientation = (first[-1] + 2) % 4  # up <-> down, left <-> right
            di, dj = deltas[from_orientation]
            for i1, j1, i2, j2 in zip(row_inds[1], col_inds[1], row_inds[0], col_inds[0]):
                correspondence[(i1 + di, j1 + dj), from_orientation] = (i2, j2), to_orientation

    else:
        # go 1 beyond row/col extents and jump to the other extent
        for i, minmax in row_extents.items():
            first, last = minmax
            # we only have right (0) and left (2) along rows
            correspondence[(i, last + 1), 0] = (i, first), 0
            correspondence[(i, first - 1), 2] = (i, last), 2
        for j, minmax in col_extents.items():
            first, last = minmax
            # we only have down (1) and up (3) along columns
            correspondence[(last + 1, j), 1] = (first, j), 1
            correspondence[(first - 1, j), 3] = (last, j), 3

    return walls, correspondence, initial_pos


def day22(inp, part2=False):
    boardspec, pathspec = inp.rstrip().split('\n\n')

    # parse path
    pathspec = pathspec.replace('R', ' R ').replace('L', ' L ').split()
    # parse board
    walls, correspondence, pos = parse_board(boardspec, part2=part2)

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

            # update position and orientation state
            pos = next_pos
            orientation = next_orientation
            delta = deltas[orientation]

    password = 1000 * pos[0] + 4 * pos[1] + orientation
    return password


if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    print(day22(testinp))
    inp = open('day22.inp').read()
    print(day22(inp), day22(inp, part2=True))
