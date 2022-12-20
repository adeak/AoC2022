from collections import deque

def get_coordinate_sum(order, nums):
    origin = next(i for i, index in enumerate(order) if nums[index] == 0)
    coords = []
    order = deque(order)
    order.rotate(-origin)
    for _ in range(3):
        order.rotate(-1000)
        coords.append(nums[order[0]])
    return sum(coords)

def mix_nums(order, nums):
    # brute force for part 1...
    for i, num in enumerate(nums):
        index_now = order.index(i)
        order.rotate(-index_now)
        ind_sanitycheck = order.popleft()
        assert ind_sanitycheck == i
        order.rotate(-num)
        order.appendleft(i)
    return order


def day20(inp):
    lines = inp.rstrip().splitlines()
    nums = list(map(int, lines))

    # operate on original indices for uniqueness
    order = deque(range(len(nums)), maxlen=len(nums))
    for it in range(1):
        order = mix_nums(order, nums)

        if it == 0:
            part1 = get_coordinate_sum(order, nums)

    return part1#, part2


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    print(day20(testinp))
    inp = open('day20.inp').read()
    print(day20(inp))
