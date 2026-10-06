from queue import SimpleQueue

from utils import (
    EAST,
    NORTH,
    SOUTH,
    WEST,
    in_grid,
    make_grid,
    md5_hash,
    next_neighbour2,
)

# Puzzle description: https://adventofcode.com/2016/day/17

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

DIR = [NORTH, SOUTH, WEST, EAST]


def hash_to_door_state(hash):
    return [is_open(hash[i]) for i in range(4)]


def dir_to_path(dir):
    return "U" if dir == NORTH else "D" if dir == SOUTH else "L" if dir == WEST else "R"


def is_open(door):
    return door in ["b", "c", "d", "e", "f"]


def bfs(input, part2=False):
    q = SimpleQueue()
    grid = make_grid(4, 4, True)
    VAULT = (3, 3)

    longest_path = 0
    q.put(((0, 0), ""))

    while not q.empty():
        p, path = q.get()

        if p == VAULT:
            if not part2:
                return path
            else:
                longest_path = max(longest_path, len(path))
                continue

        hash = md5_hash(input + path)

        door_state = hash_to_door_state(hash)

        for dir, door_open in zip(DIR, door_state):
            if door_open:
                adj = next_neighbour2(p, dir)
                if in_grid(adj, grid):
                    q.put((adj, path + dir_to_path(dir)))

    return longest_path


def part1(input):
    return bfs(input)


def part2(input):
    return bfs(input, True)


def main():
    input = "pxxbnzuo"

    #  assert (res := part1("hijkl")) == "", f"Actual: {res}"
    assert (res := part1("ihgpwlah")) == "DDRRRD", f"Actual: {res}"
    assert (res := part1("kglvqrro")) == "DDUDRLRRUDRD", f"Actual: {res}"
    assert (res := part1("ulqzkmiv")) == "DRURDRUDDLLDLUURRDULRLDUUDDDRR", (
        f"Actual: {res}"
    )

    print(f"Part 1 {part1(input)}")  # RDULRDDRRD

    assert (res := part2("ihgpwlah")) == 370, f"Actual: {res}"
    assert (res := part2("kglvqrro")) == 492, f"Actual: {res}"
    assert (res := part2("ulqzkmiv")) == 830, f"Actual: {res}"

    print(f"Part 2 {part2(input)}")  # 752


if __name__ == "__main__":
    main()
