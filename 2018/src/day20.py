from collections import defaultdict, deque

from utils import (
    EAST,
    NORTH,
    SOUTH,
    WEST,
    add_pos,
    aoc_input_file,
    read_file_str,
)

# Puzzle description: https://adventofcode.com/2018/day/20

START = (0, 0)
DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


DIR = {"N": NORTH, "S": SOUTH, "E": EAST, "W": WEST}


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def print_graph(graph, start=START):
    rooms = set(graph)
    for neighbours in graph.values():
        rooms.update(neighbours)
    rooms.add(start)

    min_r = min(r for r, c in rooms)
    max_r = max(r for r, c in rooms)
    min_c = min(c for r, c in rooms)
    max_c = max(c for r, c in rooms)

    height = (max_r - min_r + 1) * 2 + 1
    width = (max_c - min_c + 1) * 2 + 1

    grid = [["#"] * width for _ in range(height)]

    def position(room):
        r, c = room
        return 2 * (r - min_r) + 1, 2 * (c - min_c) + 1

    for room in rooms:
        r, c = position(room)
        grid[r][c] = "X" if room == start else "."

    for room, neighbours in graph.items():
        r1, c1 = position(room)

        for neighbour in neighbours:
            r2, c2 = position(neighbour)

            door_r = (r1 + r2) // 2
            door_c = (c1 + c2) // 2

            grid[door_r][door_c] = "|" if r1 == r2 else "-"

    print("\n".join("".join(row) for row in grid))


def build_graph(regex, positions, graph, i=0):
    start = positions.copy()
    ends = set()

    while i < len(regex):
        ch = regex[i]

        if ch == "(":
            i, positions = build_graph(regex, positions, graph, i + 1)
        elif ch == "|":
            ends.update(positions)
            positions = start.copy()
        elif ch == ")":
            ends.update(positions)
            return i, ends
        elif ch in "NSWE":
            new_positions = set()
            for pos in positions:
                new_pos = add_pos(pos, DIR[ch])

                # make bidirectional
                graph[pos].add(new_pos)
                graph[new_pos].add(pos)

                new_positions.add(new_pos)

            positions = new_positions
        elif ch not in "^$":
            raise ValueError(f"Unexpected character: {ch}")

        i += 1

    return i, positions


def bfs(graph, start):
    distances = {start: 0}
    queue = deque([start])

    while queue:
        pos = queue.popleft()
        for adj in graph[pos]:
            if adj not in distances:
                distances[adj] = distances[pos] + 1
                queue.append(adj)

    return distances


def solve(input, part1=True):
    graph = defaultdict(set)

    for regex in input:
        build_graph(regex, {START}, graph)

    #  print_graph(graph)

    distances = bfs(graph, START)

    if part1:
        return max(distances.values())
    else:
        return sum(1 for v in distances.values() if v >= 1000)


def part2(input):
    result = 0
    return result


def main():
    input = read_input("day20.txt")
    test_input = ["^WNE$"]
    test_input2 = ["^ENWWW(NEEE|SSE(EE|N))$"]
    test_input3 = ["^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"]
    test_input4 = ["^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"]
    test_input5 = ["^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"]

    assert (res := solve(test_input)) == 3, f"Actual: {res}"
    assert (res := solve(test_input2)) == 10, f"Actual: {res}"
    assert (res := solve(test_input3)) == 18, f"Actual: {res}"
    assert (res := solve(test_input4)) == 23, f"Actual: {res}"
    assert (res := solve(test_input5)) == 31, f"Actual: {res}"

    print(f"Part 1 {solve(input)}")  # 3958

    print(f"Part 2 {solve(input, False)}")  # 8566


if __name__ == "__main__":
    main()
