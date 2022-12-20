from collections import deque

def get_coordinate_sum(order, nums):
    # find index corresponding to 0, find 3 successors-by-1000-modulo-size
    origin = next(i for i, index in enumerate(order) if nums[index] == 0)
    return sum(nums[order[i % len(nums)]] for i in range(origin + 1000, origin + 3001, 1000))


def mix_nums(order, nums):
    # deque does the heavy lifting
    for i, num in enumerate(nums):
        index_now = order.index(i)  # find where current number's index is
        order.rotate(-index_now)  # move it to the left
        order.popleft()  # == i
        order.rotate(-num)  # let deque do the math for large numbers
        order.appendleft(i)  # insert at new position
    return order


def day20(inp, part2=False):
    lines = inp.rstrip().splitlines()
    nums = list(map(int, lines))

    if part2:
        n_iters = 10
        nums = [num * 811589153 for num in nums]
    else:
        n_iters = 1

    # operate on original indices instead of raw numbers for uniqueness
    order = deque(range(len(nums)), maxlen=len(nums))
    for it in range(n_iters):
        order = mix_nums(order, nums)

    coordinate_sum = get_coordinate_sum(order, nums)
    return coordinate_sum


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    print(day20(testinp), day20(testinp, part2=True))
    inp = open('day20.inp').read()
    print(day20(inp), day20(inp, part2=True))
