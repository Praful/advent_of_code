
import numpy as np

# return list of strings, one line per list entry


def read_file_str(filename, strip=False):
    result = []
    with open(filename) as f:
        for line in f:
            l = line
            if strip:
                l = line.strip()
            result.append(l)

    return result

# filename consists of a single row of numbers


def read_file_int(filename):
    result = []
    with open(filename) as f:
        line = f.readline()
        for s in line.split():
            result.append(int(s))

    return result


# Boolean, unsigned integer, signed integer, float, complex.
NUMERIC_KINDS = set('buifc')
NOT_NUMERIC = [object(), 'string', u'unicode', None]

# Return true if string is not defined or empty


def is_blank(s):
    return not (s and s.strip())


def is_numeric(array):
    return np.asarray(array).dtype.kind in NUMERIC_KINDS

# checks if s is a valid value for an enum class
def is_valid(enum, s):
    for l in list(enum):
        if l.value==s:
            return True

    return False

def print_np_info(a):
    print('size: ', a.size)
    print('shape: ', a.shape)
    if is_numeric(a):
        print('max:', a.max(axis=0))
        print('min:', a.min(axis=0))
