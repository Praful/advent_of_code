import collections
import re

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2018/day/17

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None

SOURCE = "+"
CLAY = "#"
WATER_STATIC = "~"
WATER_FLOWING = "|"
SAND = "."


# return clay set of (row, col)
def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)

    result = set()

    for line in input:
        axis1, value, axis2, start, end = re.fullmatch(
            r"([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)", line
        ).groups()

        value, start, end = map(int, (value, start, end))

        for n in range(start, end + 1):
            if axis1 == "x":
                result.add((n, value))
            else:
                result.add((value, n))

    return result


def get_bounds(clay):
    min_y = min(y for y, x in clay)
    max_y = max(y for y, x in clay)
    min_x = min(500, *(x for y, x in clay)) - 1
    max_x = max(500, *(x for y, x in clay)) + 1

    return min_y, max_y, min_x, max_x


# water is a dict of (row, col) -> WATER_FLOWING or WATER_STATIC
def print_grid(clay, water=None):
    if not DEBUG:
        return

    if water is None:
        water = {}

    min_y, max_y, min_x, max_x = get_bounds(clay)

    for y in range(0, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            pos = (y, x)

            if pos == (0, 500):
                char = SOURCE
            elif pos in clay:
                char = CLAY
            elif pos in water:
                char = water[pos]
            else:
                char = SAND

            row.append(char)

        print("".join(row))


# input is clay set of (row, col)
def solve(input):
    # x = col, y = row
    def is_clay(r, c):
        return (r, c) in input

    def is_flowing_water(r, c):
        return (r, c) in water and water[(r, c)] == WATER_FLOWING

    def is_settled_water(r, c):
        return (r, c) in water and water[(r, c)] == WATER_STATIC

    def can_flow_to(r, c):
        return not is_clay(r, c) and not is_settled_water(r, c)

    def can_settle(r, c):
        return is_clay(r, c) or is_settled_water(r, c)

    def find_clay_wall(r, c, direction):
        ic = c + direction

        while min_c <= ic <= max_c:
            if is_clay(r, ic):
                return ic

            if not can_settle(r + 1, ic):
                break

            ic += direction

        return None

    # settle water if both ends are clay
    def settle(r, c):
        left = find_clay_wall(r, c, -1)
        right = find_clay_wall(r, c, 1)

        if left is None or right is None:
            return False

        for ic in range(left + 1, right):
            water[(r, ic)] = WATER_STATIC

        return True

    # one or both ends is open; fill with flowing water
    def add_flowing_water(r, c):
        result = set()

        for direction in (-1, 1):
            ic = c

            while min_c <= ic <= max_c and not is_clay(r, ic):
                if not is_flowing_water(r, ic):
                    water[(r, ic)] = WATER_FLOWING
                    result.add((r, ic))

                if not can_settle(r + 1, ic):
                    break

                ic += direction

        return result

    min_r, max_r, min_c, max_c = get_bounds(input)

    # q is a queue of (row, col)
    q = collections.deque([(0, 500)])

    # water is (row, col)
    water = {}
    while q:
        r, c = q.popleft()

        print_debug(r, c, "------------------------")
        if is_settled_water(r, c):
            print_debug("already water")
            # re-evaluate above in case new static water has appeared
            if is_flowing_water(r - 1, c):
                q.append((r - 1, c))
            continue

        if is_clay(r, c):
            print_debug("already clay")
            continue

        if r > max_r:
            print_debug("out of bounds")
            continue

        if can_flow_to(r + 1, c):
            print_debug("flow to", r + 1, c)
            water[(r, c)] = WATER_FLOWING
            q.append((r + 1, c))

        if can_settle(r + 1, c):
            print_debug("settle")
            if settle(r, c):
                # re-evaluate above item to let water fill upwards
                q.append((r - 1, c))
            else:
                for p in add_flowing_water(r, c):
                    print_debug("add flowing water", p)
                    q.append(p)

        print_grid(input, water)

    print_grid(input, water)

    p1 = sum(1 for k in water if min_r <= k[0] <= max_r)
    p2 = sum(1 for v in water.values() if v == WATER_STATIC)

    return p1, p2


def main():
    input = read_input("day17.txt")
    test_input = read_input("day17-test.txt")

    assert (res := solve(test_input)) == (57, 29), f"Actual: {res}"
    print(f"Part 1 & 2 {solve(input)}")  # 31383, 25376


if __name__ == "__main__":
    main()
