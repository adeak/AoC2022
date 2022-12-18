def day18(inp):
    lines = inp.rstrip().splitlines()
    coordses = [tuple(map(int, line.split(','))) for line in lines]

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

    return part1#, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(day18(testinp))
    inp = open('day18.inp').read()
    print(day18(inp))
