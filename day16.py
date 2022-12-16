from collections import defaultdict
from itertools import count, permutations
from random import randint
import re


def compute_pressure(valves, path_lengths, flow_rates, root, maxtime=30):
    time = 0
    pressure_released = 0
    current = root
    valves_reached = 0
    for valve in valves:
        time += path_lengths[current][valve] + 1
        remaining_time = maxtime - time
        if remaining_time <= 0:
            break
        pressure_released += flow_rates[valve] * remaining_time
        current = valve
        valves_reached += 1
    return pressure_released, valves_reached


def day16(inp):
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

    # walk the graph starting from root
    # initial state: start with higher flow rates first
    # then keep swapping valve pairs
    n_valves = len(path_lengths) - 1  # number of working valves
    nonzero_valves = sorted(flow_rates, key=flow_rates.get, reverse=True)[:n_valves]
    best_pressure, valves_reached = compute_pressure(nonzero_valves, path_lengths, flow_rates, root)
    valves_now = nonzero_valves.copy()
    seen_valves = {tuple(valves_now[:valves_reached])}
    bestest_best = best_pressure
    while True:
        # choose three valves and swap them (2-swaps get stuck too early)

        # estimate number of swaps to try before starting from scratch
        n_iterations = 10 * n_valves ** 2 * valves_reached
        for _ in range(n_iterations):
            i, j, k = [randint(0, n_valves - 1) for _ in range(3)]
            if all(val >= valves_reached for val in [i, j, k]) or len({i, j, k}) < 3:
                # (near) pointless swap
                continue
            next_valves = valves_now.copy()
            next_valves[i], next_valves[j], next_valves[k] = next_valves[j], next_valves[k], next_valves[i]
            if tuple(next_valves) in seen_valves:
                # already been here
                continue
            seen_valves.add(tuple(next_valves))
            break
        else:
            # we seem to be stuck, restart from random
            valves_now = sorted(nonzero_valves, key=lambda _: randint(0, 1000))
            valves_reached = len(nonzero_valves)
            best_pressure = 0
            continue

        new_pressure, new_reached = compute_pressure(next_valves, path_lengths, flow_rates, root)
        if new_pressure > best_pressure:
            # keep this configuration
            best_pressure = new_pressure
            valves_now = next_valves
            valves_reached = new_reached
            if best_pressure > bestest_best:
                bestest_best = new_pressure
                print(f'Bestest best record: {new_pressure} ({next_valves}, {new_reached})')
        # then wait...


def day16b(inp):
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

    # walk the graph starting from root
    # initial state: start with higher flow rates first
    #                and alternating me/elephant/me/elephant... assignment
    #                (but this will be kept fixed! not a degree of freedom)
    #                (this assumes that n_elephant ~ n_me will work as a heuristic)
    # then keep swapping valve pairs
    n_valves = len(path_lengths) - 1  # number of working valves
    nonzero_valves = sorted(flow_rates, key=flow_rates.get, reverse=True)[:n_valves]
    best_pressure = 0
    valves_reached = 0
    for index in 0, 1:
        best_subpressure, valves_subreached = compute_pressure(nonzero_valves[index::2], path_lengths, flow_rates, root, 26)
        best_pressure += best_subpressure
        valves_reached = max(valves_reached, 2*valves_subreached)

    valves_now = nonzero_valves.copy()
    seen_valves = {tuple(valves_now[:valves_reached])}
    bestest_best = best_pressure
    while True:
        # choose three valves and swap them (2-swaps get stuck too early)

        # estimate number of swaps to try before starting from scratch
        n_iterations = 10 * n_valves ** 2 * valves_reached
        for _ in range(n_iterations):
            i, j, k = [randint(0, n_valves - 1) for _ in range(3)]
            if all(val >= valves_reached for val in [i, j, k]) or len({i, j, k}) < 3:
                # (near) pointless swap
                continue
            next_valves = valves_now.copy()
            next_valves[i], next_valves[j], next_valves[k] = next_valves[j], next_valves[k], next_valves[i]
            if tuple(next_valves) in seen_valves:
                # already been here
                continue
            seen_valves.add(tuple(next_valves))
            break
        else:
            # we seem to be stuck, restart from random
            valves_now = sorted(nonzero_valves, key=lambda _: randint(0, 1000))
            valves_reached = len(nonzero_valves)
            best_pressure = 0
            continue

        new_pressure = new_reached = 0
        for index in 0, 1:
            new_subpressure, new_subreached = compute_pressure(next_valves[index::2], path_lengths, flow_rates, root, 26)
            new_pressure += new_subpressure
            new_reached = max(new_reached, 2*new_subreached)
        if new_pressure > best_pressure:
            # keep this configuration
            best_pressure = new_pressure
            valves_now = next_valves
            valves_reached = new_reached
            if best_pressure > bestest_best:
                bestest_best = new_pressure
                print(f'Bestest best record: {new_pressure} ({next_valves}, {new_reached})')
        # then wait...


if __name__ == "__main__":
    testinp = open('day16.testinp').read()
    inp = open('day16.inp').read()
    #print(day16(testinp))  # runs forever, finds best in a few seconds
    #print(day16(inp))  # runs forever, finds best in half a minute or so
    #print(day16b(testinp))  # runs forever, finds best in a few seconds
    print(day16b(inp))  # runs forever, finds best in 10 seconds or so
