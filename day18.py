def day18(inp):
    lines = inp.rstrip().splitlines()
    coordses = [tuple(map(int, line.split(','))) for line in lines]

    lava_faces = set()  # set of open faces, where a face is a (reference_point, normal_axis) tuple
    for coords in coordses:
        # generate 6 possible faces
        for dim in range(3):
            for delta in -1, 1:
                if delta == 1:
                    ref_point = list(coords)
                    ref_point[dim] += 1
                    ref_point = tuple(ref_point)
                else:
                    ref_point = coords
                face = (ref_point, dim)
                if face in lava_faces:
                    # we have overlap, this is not an open face
                    lava_faces.remove(face)
                else:
                    # this might be a new open face
                    lava_faces.add(face)
    part1 = len(lava_faces)

    return part1#, part2


if __name__ == "__main__":
    testinp = open('day18.testinp').read()
    print(day18(testinp))
    inp = open('day18.inp').read()
    print(day18(inp))
