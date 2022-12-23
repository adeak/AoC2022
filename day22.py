def day22(inp):
    boardspec, pathspec = inp.rstrip().split('\n\n')

    # parse path
    pathspec = pathspec.replace('R', ' R ').replace('L', ' L ').split()
    # parse board
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
    pos = x0, y0

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
            next_pos = [pos[0] + delta[0], pos[1] + delta[1]]
            if delta[0] == 0:
                # walk along row
                if next_pos[1] > row_extents[pos[0]][1]:
                    # wrap to left
                    next_pos[1] = row_extents[pos[0]][0]
                elif next_pos[1] < row_extents[pos[0]][0]:
                    # wrap to right
                    next_pos[1] = row_extents[pos[0]][1]
            else:
                # walk along column
                if next_pos[0] > col_extents[pos[1]][1]:
                    # wrap to top
                    next_pos[0] = col_extents[pos[1]][0]
                elif next_pos[0] < col_extents[pos[1]][0]:
                    # wrap to bottom
                    next_pos[0] = col_extents[pos[1]][1]
            next_pos = tuple(next_pos)

            if next_pos in walls:
                break
            pos = next_pos

    password = 1000 * pos[0] + 4 * pos[1] + orientation
    return password


if __name__ == "__main__":
    testinp = open('day22.testinp').read()
    print(day22(testinp))
    inp = open('day22.inp').read()
    print(day22(inp))
