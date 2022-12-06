from functools import partial
from itertools import count, takewhile

def predicate(msg, length, index):
    """Check if `message` has a length-`length` unique substring at index `index`."""
    return len(set(msg[index : index + length])) < length


def day06(inp):
    dat = inp.strip()
    
    indices = count()  # index iterator
    parts = []
    for length in 4, 14:
        *_, index = takewhile(partial(predicate, dat, length), indices)
        parts.append(index + length + 1)

    return tuple(parts)


if __name__ == "__main__":
    inp = open('day06.inp').read()
    print(day06(inp))
