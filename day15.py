from itertools import combinations
from operator import attrgetter
import re

def manhattan(pos0, pos1):
    xs, ys = pos0
    xb, yb = pos1
    return abs(xb - xs) + abs(yb - ys)


def compute_ranges(distances, y0):
    """Compute a set of merged ranges covered by any sensor in a given row at y.

    Returns a list of ranges (these might still contain beacons).
    """
    # for the given y0, gather the intervals that are covered by each sensor
    covered_ranges = set()
    for (x, y), dist in distances.items():
        dy = y0 - y
        if abs(dy) > dist:
            # y0 is too far from this sensor
            continue
        xmin = x - (dist - abs(dy))
        xmax = x + (dist - abs(dy))
        covered_ranges.add(range(xmin, xmax + 1))

    # pre-process ranges: merge overlaps
    while True:
        # keep comparing all pairs as long as we find any overlaps
        for first, second in combinations(covered_ranges, 2):
            # check if first and second overlap
            # or just touch!
            overlap = first.start in second or second.start in first
            touching = first.start == second.stop or second.start == first.stop
            if overlap or touching:
                # merge these
                start = min(first.start, second.start)
                stop = max(first.stop, second.stop)
                merged_range = range(start, stop)
                covered_ranges = (covered_ranges - {first, second}) | {merged_range}
                break
        else:
            # there were no overlaps among any pairs
            break

    # now we have non-overlapping ranges, sort them by start point
    covered_ranges = sorted(covered_ranges, key=attrgetter('start'))
    return covered_ranges


def day15(inp, testing=False):
    lines = inp.rstrip().splitlines()
    pattern = re.compile(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)')

    beacons = set()  # beacon positions
    distances = {}  # sensor pos -> closest beacon distance mapping
    for line in lines:
        xs, ys, xb, yb = map(int, pattern.match(line).groups())
        beacons.add((xb, yb))
        distances[xs, ys] = manhattan((xs, ys), (xb, yb))

    if testing:
        special_y = 10
    else:
        special_y = 2_000_000
    ymax = 2*special_y
    y0s = range(ymax + 1)

    for y0 in y0s:
        # compute merged ranges from each beacon
        covered_ranges = compute_ranges(distances, y0)
        if y0 == special_y:
            # part 1: find length of merged ranges sans beacons
            #         (and hope that part 2's answer comes later)
            covereds = sum(len(rng) for rng in covered_ranges)
            beaconeds = sum(
                1
                for beacon in beacons
                if beacon[1] == y0 and any(beacon[0] in rng for rng in covered_ranges)
            )
            excludeds = covereds - beaconeds
        # part 2: find lonely beacon
        if len(covered_ranges) == 2:
            # there's a hole in the middle
            lonely_beacon = (covered_ranges[0].stop, y0)
            break
        elif 0 not in covered_ranges[0]:
            # uncovered left edge
            lonely_beacon = (0, y0)
            break
        elif ymax not in covered_ranges[0]:
            # uncovered right edge; ymax is also xmax
            lonely_beacon = (ymax, y0)
            break
    tuning_freq = lonely_beacon[0] * 4_000_000 + lonely_beacon[1]

    return excludeds, tuning_freq


if __name__ == "__main__":
    testinp = open('day15.testinp').read()
    print(day15(testinp, testing=True))
    inp = open('day15.inp').read()
    print(day15(inp))
