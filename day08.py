import numpy as np

def day08(inp):
    board = np.array([[int(c) for c in line] for line in inp.strip().splitlines()])

    visibles = np.zeros_like(board, dtype=bool)
    for axis in range(2):
        # check rows or columns
        for i in range(board.shape[axis]):
            # check each row or each column
            for sl in slice(None), slice(None, None, -1):
                # check forward and backward
                subhighest = -1
                for j in range(board.shape[1 - axis])[sl]:
                    index = (i, j) if axis == 0 else (j, i)
                    if board[index] > subhighest:
                        visibles[index] = True
                        subhighest = board[index]
    part1 = visibles.sum()

    return part1


def day08b(inp):
    board = np.array([[int(c) for c in line] for line in inp.strip().splitlines()])

    highest_scenic = 0
    for i0, j0 in np.indices(board.shape).reshape(2, -1).T:
        scenic_score = 1
        for delta in np.array([[0, 1], [0, -1], [1, 0], [-1, 0]]):
            i, j = i0, j0
            viewing_distance = 0
            subhighest = -1
            while True:
                i, j = (i, j) + delta
                if not (0 <= i < board.shape[0] and 0 <= j < board.shape[1]):
                    break
                viewing_distance += 1
                if board[i, j] >= board[i0, j0]:
                    # this is the edge
                    break
            scenic_score *= viewing_distance
        highest_scenic = max(highest_scenic, scenic_score)
    part2 = highest_scenic

    return part2


if __name__ == "__main__":
    testinp = open('day08.testinp').read()
    print(day08(testinp))
    print(day08b(testinp))
    inp = open('day08.inp').read()
    print(day08(inp))
    print(day08b(inp))
