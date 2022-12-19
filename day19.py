from collections import defaultdict, deque
from itertools import product
from math import ceil
from operator import itemgetter
import re


def parse_blueprints(lines):
    """Parse inputs into a dict of dicts, one dict for each blueprint."""
    pattern = re.compile(
        r"Blueprint (?P<index>\d+): "
        r"Each ore robot costs (?P<ore_ore>\d)+ ore. "
        r"Each clay robot costs (?P<clay_ore>\d)+ ore. "
        r"Each obsidian robot costs (?P<obsidian_ore>\d+) ore and (?P<obsidian_clay>\d+) clay. "
        r"Each geode robot costs (?P<geode_ore>\d+) ore and (?P<geode_obsidian>\d+) obsidian."
    )
    blueprints = {}
    for line in lines:
        m = pattern.match(line)
        if m is None:
            raise ValueError(f'Invalid line: {line!r}')
        blueprint = {
            'ore': {'ore': int(m.group('ore_ore'))},
            'clay': {'ore': int(m.group('clay_ore'))},
            'obsidian': {'ore': int(m.group('obsidian_ore')), 'clay': int(m.group('obsidian_clay'))},
            'geode': {'ore': int(m.group('geode_ore')), 'obsidian': int(m.group('geode_obsidian'))},
        }
        blueprints[int(m.group('index'))] = blueprint
    return blueprints


def assess_options(time, resources, bots, blueprint, maxtime):
    """Determine the kind of bots we can buy, given current `time`, `resources` and `bots`.

    Returns three lists of length `n` if there are `n` potential future bots to buy.

    Returns
    -------
    new_times : list
        The times until each bot choice will be done.

    new_resources : list
        The resources we'll have when each bot is done.

    new_bots : list
        The bot counts we'll have when each bot is done.
    """
    new_times = []
    new_resources = []
    new_bots = []
    for next_bot in 'ore clay obsidian geode'.split():
        # quick check: no point buying a bot if we already have
        # as many as we need to buy any bot in one step
        if next_bot != 'geode':
            highest_req = max(reqs.get(next_bot, 0) for reqs in blueprint.values())
            if bots[next_bot] >= highest_req:
                continue

        reqs = blueprint[next_bot]
        # for each resource we solve
        #
        #     resource_now + resource_bot * dt = resource_cost
        #     dt = (resource_cost - resource_now) / resource_bot
        #
        # so if resource_bot == 0: no chance to buy a bot
        # (and if resource_bot > 0, we can eventually buy this bot as far
        # as this resource is concerned)
        dt_for_bot = 0
        for material, req in reqs.items():
            if req < resources[material]:
                # we already have material in stock
                continue
            if bots[material] == 0:
                # we can't buy this bot, ever
                break
            dt = ceil((req - resources[material]) / bots[material])
            dt_for_bot = max(dt_for_bot, dt)
        else:
            # all materials will be present eventually, after dt_for_bot steps
            # but we might still be out of time
            new_time = time + dt_for_bot + 1
            if new_time >= maxtime:
                # impossible or pointless to buy
                continue
            new_times.append(new_time)
            new_bots.append(bots.copy())
            new_bots[-1][next_bot] += 1

            # compute resources at new time
            new_resource = resources.copy()
            # generation
            for material in new_resource:
                new_resource[material] += (dt_for_bot + 1) * bots[material]
            # construction cost
            for material, req in reqs.items():
                new_resource[material] -= req
            new_resources.append(new_resource)

    return new_times, new_resources, new_bots


def maximize_geodes(blueprint, maxtime=24):
    """Compute max number of geodes generated with a given blueprint."""
    # Attempt BFS-ish, but the key question is not "what do we do in the
    # next timestep", but rather "what bot do we buy next?"! See hint
    # in https://www.reddit.com/r/adventofcode/comments/zpnkbm/comment/j0vao0v
    # i.e. maintain a collection of histories built from a chain of "what bot
    # to build in what step". If all bots eventually take too long to build,
    # the given history is reaped.
    resources = dict.fromkeys(blueprint, 0)
    bots = resources.copy()
    bots['ore'] = 1

    max_geodes = 0
    # start from 0 minute mark
    #resources['ore'] = 1
    timelines = {(0, tuple(resources.items()), tuple(bots.items()))}  # set of construction choices, (time, resources, bots)
    seen = {} # bots -> shortest time mapping to prune useless states with
    while timelines:
        time, resources_items, bots_items = timelines.pop()
        resources = dict(resources_items)
        bots = dict(bots_items)

        # find our options for next purchase, given current resources and bots and time
        # all three return values are n-length lists for n bot purchase options
        new_times, new_resources, new_bots = assess_options(time, resources, bots, blueprint, maxtime)
        # if there are no more options: we're out of time
        if not new_times:
            # count geodes in this history
            geodes_here = resources['geode'] + (maxtime - time) * bots['geode']
            if geodes_here > max_geodes:
                max_geodes = geodes_here
            continue

        # otherwise add new timelines
        for new_time, new_resource, new_bot in zip(new_times, new_resources, new_bots):
            # ignore pointless states
            new_bot_items = tuple(new_bot.items())
            if seen.get(new_bot_items, float('inf')) < new_time:
                # no point going on
                continue
            seen[new_bot_items] = new_time
            timelines.add((new_time, tuple(new_resource.items()), tuple(new_bot.items())))

    return max_geodes


def day19(inp):
    lines = inp.rstrip().splitlines()

    blueprints = parse_blueprints(lines)

    # part 1: check quality level of each blueprint
    total_quality = 0
    for index, blueprint in blueprints.items():
        max_geodes = maximize_geodes(blueprint)
        quality = max_geodes * index
        total_quality += quality

    # part 2: more time for first 3 blueprints, different score
    geode_product = 1
    for index in range(1, 4):
        if index not in blueprints:
            # test input
            break
        blueprint = blueprints[index]
        max_geodes = maximize_geodes(blueprint, maxtime=32)
        geode_product *= max_geodes

    part1 = total_quality
    part2 = geode_product

    return part1, part2


if __name__ == "__main__":
    testinp = open('day19.testinp').read()
    print(day19(testinp))
    inp = open('day19.inp').read()
    print(day19(inp))
