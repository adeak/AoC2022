from collections import deque


def tuple_add_at(inp, index, val):
    """Add `val` to `inp` tuple item `index`."""
    if val == 0:
        return inp
    out = list(inp)
    out[index] += val
    return tuple(out)


def day18(inp):
    lines = inp.rstrip().splitlines()
    coordses = set(tuple(map(int, line.split(','))) for line in lines)

    # part 1: add or remove open face count as we add cubes
    lava_faces = {}  # coordinates -> free faces mapping
    for coords in coordses:
        lava_faces[coords] = 6  # start from 6
        # check each neighbour and remove free face count
        for dim in range(3):
            for delta in -1, 1:
                other_coords = list(coords)
                other_coords[dim] += delta
                other_coords = tuple(other_coords)
                if other_coords in lava_faces:
                    lava_faces[coords] -= 1
                    lava_faces[other_coords] -= 1
    part1 = sum(lava_faces.values())

    # part 2: pretend to be the steam and do BFS
    start_face = min(lava_faces)  # lowest face has to be a surface one
    start = tuple_add_at(start_face, 0, -1)  # initial coordinates of steam
    assert start not in coordses  # check we're outside
    edge = {start}
    seen = set()
    surface_counts = deque([0], maxlen=3)
    while True:
        # check each edge cube
        # collect new edge front
        # if we were to cross a face: add face to surface faces
        # if we didn't cross any faces: we've processed the entire surface
        next_edge = set()
        seen |= edge
        new_surface_count = 0
        for current in edge:
            # consider 6 neighbour cubes
            for dim in range(3):
                for delta in -1, 1:
                    neighb = tuple_add_at(current, dim, delta)
                    if neighb in seen:
                        continue
                    if neighb in coordses:
                        # we would've gone through a surface face
                        new_surface_count += 1
                        continue
                    # otherwise continue BFS
                    next_edge.add(neighb)
        surface_counts.append(surface_counts[-1] + new_surface_count)
        if len(set(surface_counts)) == 1:
            # we're done
            break
        edge = next_edge
    part2 = surface_counts[-1]

    return part1, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(day18(testinp))
    inp = open('day18.inp').read()
    print(day18(inp))
