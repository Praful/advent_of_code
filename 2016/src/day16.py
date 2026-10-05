# Puzzle description: https://adventofcode.com/2016/day/16

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def fill_disk(disk_length, initial_state):
    a = initial_state

    while len(a) < disk_length:
        b = a
        b = "".join("1" if x == "0" else "0" for x in reversed(b))
        a = a + "0" + b

    return a


def is_even(n):
    return n % 2 == 0


def checksum(data):
    while True:
        checksum = ""
        for i in range(0, len(data), 2):
            if data[i] == data[i + 1]:
                checksum += "1"
            else:
                checksum += "0"

        data = checksum

        if not is_even(len(data)):
            break

    return data


def solve(input):
    disk_length, initial_state = input

    data = fill_disk(disk_length, initial_state)

    return checksum(data[:disk_length])


def main():
    input = (272, "11101000110010100")
    input2 = (35651584, "11101000110010100")
    test_input = (20, "10000")

    assert (res := solve(test_input)) == "01100", f"Actual: {res}"
    print(f"Part 1 {solve(input)}")  # 10100101010101101

    print(f"Part 2 {solve(input2)}")  # 01100001101101001


if __name__ == "__main__":
    main()
