from itertools import combinations
from operator import attrgetter
import re

def manhattan(pos0, pos1):
    xs, ys = pos0
    xb, yb = pos1
    return abs(xb - xs) + abs(yb - ys)


def compute_ranges(distances, y0):
    """Compute a set of merged "ranges" covered by any sensor in a given row at y.

    Returns a list of inclusive (from, to) tuples (these might still contain beacons).
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
        covered_ranges.add((xmin, xmax))

    # pre-process ranges: merge overlaps
    covered_ranges = sorted(covered_ranges)
    merged_ranges = []
    current_range = covered_ranges[0]
    for next_range in covered_ranges[1:]:
        # check if current and next overlap
        # or just touch!
        overlap_or_touching = next_range[0] <= current_range[1] + 1
        if overlap_or_touching:
            # merge these
            end = max(current_range[1], next_range[1])
            current_range = (current_range[0], end)
        else:
            # no overlap
            merged_ranges.append(current_range)
            current_range = next_range
    # handle last merged range
    merged_ranges.append(current_range)

    return merged_ranges


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
            covereds = sum(rng[1] - rng[0] + 1 for rng in covered_ranges)
            beaconeds = sum(
                1
                for beacon in beacons
                if beacon[1] == y0 and any(rng[0] <= beacon[0] <= rng[1] for rng in covered_ranges)
            )
            excludeds = covereds - beaconeds

        # part 2: find lonely beacon
        first_range = covered_ranges[0]
        # (premise: we have either one or two ranges)
        if len(covered_ranges) == 2:
            # there's a hole in the middle
            lonely_beacon = (first_range[1] + 1, y0)
            break
        elif first_range[0] > 0:
            # uncovered left edge
            lonely_beacon = (0, y0)
            break
        elif first_range[1] < ymax:
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
