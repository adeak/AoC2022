from itertools import tee

def peek(iterable):
    """Peek at the next value of an iterable, return copy and preview.

    Returns None preview value of the iterator is exhausted.
    """

    backup, throwaway = tee(iterable)
    try:
        return backup, next(throwaway)
    except StopIteration:
        return backup, None


def day07(inp):
    dat = inp.strip()

    tree = {'/': {}}  # dirs are dicts, files are ints of sizes, parent dict is __parent
    pwd = tree
    it = iter(dat.splitlines())
    while True:
        try:
            line = next(it)
        except StopIteration:
            break
        if line.startswith('$'):
            cmdline = line[2:]
            cmd, *args = cmdline.split()
            if cmd == 'cd':
                if args[0] == '/':
                    pwd = tree['/']
                elif args[0] == '..':
                    pwd = pwd['__parent']
                else:
                    pwd = pwd[args[0]]
            elif cmd == 'ls':
                if args:
                    raise ValueError(f'Unexpected argument to `ls`: {args[0]!r}.')
                while True:
                    it, next_line = peek(it)
                    if next_line is None or next_line.startswith('$'):
                        break
                    line = next(it)
                    metadata, name = line.split()
                    if metadata == 'dir':
                        pwd[name] = {'__parent': pwd}
                    else:
                        pwd[name] = int(metadata)

    # walk tree and collect directory sizes
    all_sizes = []
    def sum_sizes(dir_or_size):
        if isinstance(dir_or_size, int):
            return dir_or_size

        dir_size = sum(sum_sizes(subtree) for name, subtree in dir_or_size.items() if name != '__parent')
        all_sizes.append(dir_size)
        return dir_size
    total_size = sum_sizes(tree)  # size of root

    part1 = sum(size for size in all_sizes if size <= 100_000)
    available_space = 70_000_000 - total_size
    missing_space = 30_000_000 - available_space
    lowest = 70_000_000
    for size in all_sizes:
        if size >= missing_space and size < lowest:
            lowest = size
    part2 = lowest

    return part1, part2


if __name__ == "__main__":
    inp = open('day07.inp').read()
    print(day07(inp))
