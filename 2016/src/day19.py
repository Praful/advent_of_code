from utils import nearest_power_of

# Puzzle description: https://adventofcode.com/2016/day/19

DEBUG = True
#  DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


# This will be fine for small inputs  < 1000
# For larger numbers it's too slow.
# It's used with pattern_part1 to work out the formula
def winner_part1_slow(input):
    l = [True for _ in range(input)]

    while True:
        for i in range(input):
            pos = i
            if l[i]:
                while True:
                    pos += 1
                    if pos >= input:
                        pos = 0

                    if pos == i:
                        break

                    if l[pos]:
                        l[pos] = False
                        break

            if l.count(True) == 1:
                return i + 1


# This will be fine for small inputs  < 4000
# It's used by pattern_part2 to work out the formula
def winner_part2_slow(input):
    l = list(range(1, input + 1))
    idx = 0

    while len(l) > 1:
        opp_idx = (idx + len(l) // 2) % len(l)

        del l[opp_idx]

        if opp_idx < idx:
            idx -= 1

        idx = (idx + 1) % len(l)

    return l[0]


# winner_part1() took too long to run with just a 1000 so this looks for
# a pattern in the results. Then works out a formula.
#
# The winner resets at powers of 2
#    [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, ...]
# then the results repeat 1, 3, 5, ... until the next reset
def pattern_part1():
    resets = []
    prev_reset = 0
    for i in range(1, 700):
        w = winner_part1_slow(i)
        if w == 1:
            resets.append(i)
            print(i - prev_reset, "---------------")
            prev_reset = i

        print(i, w, winner_part1(i))

    print(resets)


def winner_part1(n):
    _, p = nearest_power_of(2, n)

    # using pattern_part1, this is the formula; it's apparently something called
    # the Josephus problem
    return 2 * (n - p) + 1


def winner_part2(n):
    _, p = nearest_power_of(3, n)
    if p == n:
        return p
    elif p < n <= 2 * p:  # winner increases by 1
        return n - p
    elif 2 * p < n < 3 * p:  # winner increases by 2
        return 2 * (n - p) - p
    else:
        return 1

# winnner resets at powers of 3 + 1
# [1, 2, 4, 10, 28, 82, 244, 730, ...]
# Eg 3^2 = 9 (add 1 = 10), 3^3 = 27 (add 1 = 28), etc
def pattern_part2():
    resets = []
    prev_reset = 0
    for i in range(1, 2000):
        w = winner_part2_slow(i)
        if w == 1:
            resets.append(i)
            print(i - prev_reset, "---------------")
            prev_reset = i

        print(i, w, winner_part2(i))

    print(resets)


def part1(input):
    return winner_part1(input)


def part2(input):
    return winner_part2(input)


def main():
    input = 3001330
    test_input = 5

    #  pattern_part1()
    #  pattern_part2()

    assert (res := part1(test_input)) == 3, f"Actual: {res}"
    print(f"Part 1 {part1(input)}")  # 1808357

    print(f"Part 2 {part2(input)}")  # 1407007


if __name__ == "__main__":
    main()
