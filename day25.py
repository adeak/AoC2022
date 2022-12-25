from itertools import count


def snafu_to_decimal(snafu):
    digits = snafu[::-1]
    mapping = dict(zip('=-012', range(-2, 3)))
    decimal_digits = [mapping[digit] for digit in digits]
    return sum(int(digit)*5**power for digit, power in zip(decimal_digits, count()))


def decimal_to_snafu(decimal):
    # convert to regular base-5 first
    num = decimal
    base_5_digits = []
    power_bound = 2 * len(str(decimal))  # generous upper bound, don't want logarithms
    for power in range(power_bound)[::-1]:
        digit = num // 5**power
        base_5_digits.append(digit)
        num -= digit * 5**power
    # strip away needless leading zeros
    base_5_digits = ''.join(map(str, base_5_digits)).lstrip('0')  # string, highest first
    base_5_digits = list(map(int, base_5_digits))[::-1]  # list of ints, lowest first

    # now start from the end and replace too large digits with carry
    # a*5^(n+1) + 3*5^n = a*5^(n+1) - 2*5^n + 5*5^n = (a + 1)*5^(n+1) - 2*5^n (then carry a + 1)
    # a*5^(n+1) + 4*5^n = a*5^(n+1) - 1*5^n + 5*5^n = (a + 1)*5^(n+1) - 1*5^n (then carry a + 1)
    # a*5^(n+1) + 5*5^n = (a + 1)*5^(n+1) + 0*5^n (for carrying a + 1)
    snafu_digits = []
    for i, digit in enumerate(base_5_digits):  # mutated on the fly on purpose
        if digit < 3:
            snafu_digits.append(digit)
            continue
        if digit == 3:
            snafu_digits.append(-2)
        elif digit == 4:
            snafu_digits.append(-1)
        elif digit == 5:
            snafu_digits.append(0)
        else:
            raise ValueError(f'Unexpected base-5-semi-SNAFU digit {digit}.')
        base_5_digits[i + 1] += 1

    # go from integers to SNAFU string
    mapping = dict(zip(range(-2, 3), '=-012'))
    return ''.join(mapping[snafu_digit] for snafu_digit in snafu_digits)[::-1]


def day25(inp):
    lines = inp.rstrip().splitlines()
    decimal_sum = sum(snafu_to_decimal(line) for line in lines)
    fuel_req = decimal_to_snafu(decimal_sum)

    return fuel_req


if __name__ == "__main__":
    testinp = open('day25.testinp').read()
    print(day25(testinp))
    inp = open('day25.inp').read()
    print(day25(inp))
