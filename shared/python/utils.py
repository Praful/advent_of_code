

# return list of strings, one line per list entry
def read_file_str(filename):
    result = []
    with open(filename) as f:
        for line in f:
            result.append(line)

    return result

# filename consists of a single row of numbers


def read_file_int(filename):
    result = []
    with open(filename) as f:
        line = f.readline()
        for s in line.split():
            result.append(int(s))

    return result
