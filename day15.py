import re

def manhattan(pos0, pos1):
    xs, ys = pos0
    xb, yb = pos1
    return abs(xb - xs) + abs(yb - ys)


def day15(inp, y0=2_000_000):
    lines = inp.rstrip().splitlines()
    pattern = re.compile(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)')

    sensor_beacons = {}  # sensor pos -> closest beacon pos mapping
    distances = {}  # sensor pos -> closest beacon distance mapping
    for line in lines:
        xs, ys, xb, yb = map(int, pattern.match(line).groups())
        sensor_beacons[xs, ys] = xb, yb
        distances[xs, ys] = manhattan((xs, ys), (xb, yb))

    # part 1
    min_x = min(
        xs - dist
        for (xs, ys), dist in distances.items()
    )
    max_x = max(
        xs + dist
        for (xs, ys), dist in distances.items()
    )
    excludeds = 0  # number of excluded fields
    for x in range(min_x, max_x + 1):
        if any(manhattan((x, y0), pos) <= dist for pos, dist in distances.items()):
            # this position is closer to a sensor than the closest beacon
            # but exclude exact beacon hits...
            if (x, y0) not in sensor_beacons.values():
                excludeds += 1
    part1 = excludeds

    return part1#, part2


if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(day15(testinp, y0=10))
    inp = open('day15.inp').read()
    print(day15(inp))
