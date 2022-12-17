from collections import defaultdict
from itertools import count, combinations, product
import re


def evaluate_path(valves, path_lengths, flow_rates, root, maxtime=30):
    """Return the pressure from the given path, or None if the path is too long."""
    time = 0
    pressure_released = 0
    current = root
    for valve in valves:
        time += path_lengths[current][valve] + 1
        remaining_time = maxtime - time
        if remaining_time <= 0:
            pressure_released = None
            break
        pressure_released += flow_rates[valve] * remaining_time
        current = valve
    return pressure_released


def day16(inp, part2=False):
    lines = inp.rstrip().splitlines()

    # parse input
    pattern = re.compile(r'Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)')
    flow_rates = {}  # valve -> flow rate mapping
    adjacency = {}  # valve -> list of connected valves
    for line in lines:
        valve, rate, tail = pattern.match(line).groups()
        rate = int(rate)
        neighbs = tail.split(', ')
        flow_rates[valve] = rate
        adjacency[valve] = neighbs

    # pre-processing: reduce graph to nonzero rates (zero rates are just for transit)
    valves_keep = {valve for valve, rate in flow_rates.items() if rate}
    # but also keep starting point...
    root = 'AA'
    valves_keep.add(root)
    path_lengths = defaultdict(dict)  # source -> {target -> path length} mapping
    while valves_keep:
        valve = valves_keep.pop()  # search closest paths to this valve
        other_valves = {other_valve for other_valve in valves_keep if other_valve not in path_lengths[valve]}
        edges = {valve}  # frontline of BFS
        seen = set()
        for length in count(1):
            # find neighbour of every edge valve
            seen |= edges
            edges = {neighb for edge in edges for neighb in adjacency[edge]}
            # remove already seen edges
            edges -= seen
            # if everything seen: we're done
            if not edges:
                break
            # find potential new valves
            new_valves = edges & other_valves
            for new_valve in new_valves:
                path_lengths[valve][new_valve] = length
                path_lengths[new_valve][valve] = length

    if part2:
        maxtime = 26
    else:
        maxtime = 30

    # walk the graph starting from root
    # try BFS but only keeping a given number of best paths
    # part 2: keep the same paths, but walk even and odd valves independently!
    n_valves = len(path_lengths) - 1  # number of working valves
    nonzero_valves = set(sorted(flow_rates, key=flow_rates.get, reverse=True)[:n_valves])
    n_candidates = 10_000  # number of "best" subpaths to keep in each step; need this high for part2
    if part2:
        # start from any pair of valves; order doesn't matter
        candidates = set(combinations(nonzero_valves, 2))
    else:
        # start from any valve
        candidates = {(valve,) for valve in nonzero_valves}  # set of tuple of valves
    best_pressure = 0
    while candidates:
        # generate new candidates
        candidates = {
            candidate + (next_valve,)
            for candidate in candidates
            for next_valve in nonzero_valves - set(candidate)
        }

        # evaluate each new candidate
        candidate_pressures = {}
        for candidate in candidates:
            if part2:
                # even and odd valves are two distinct paths
                # bug: it might happen that the optimal path has different path lengths
                #      for the two parity-based subpaths
                #      this is probably why the solution is non-deterministic, and needs
                #      several reruns to find the optimal solutions...
                pressure = 0
                for parity in range(2):
                    subpressure = evaluate_path(candidate[parity::2], path_lengths, flow_rates, root, maxtime)
                    if subpressure is None:
                        pressure = None
                        break
                    pressure += subpressure
            else:
                # there's a single path
                pressure = evaluate_path(candidate, path_lengths, flow_rates, root, maxtime)

            if pressure is None:
                # forget about this candidate, path too long
                continue

            best_pressure = max(best_pressure, pressure)
            candidate_pressures[candidate] = pressure

        # keep n_candidates best candidates
        candidates = set(sorted(candidate_pressures, key=candidate_pressures.get)[-n_candidates:])

    return best_pressure


if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    inp = open('day16.inp').read()
    print(day16(testinp), day16(testinp, part2=True))
    print(day16(inp), day16(inp, part2=True))  # will get the right result about 50% of the time
