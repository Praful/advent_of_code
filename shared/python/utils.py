

# filename consists of a single row of numbers
def read_file_int(filename):
  result =[]
  with open(filename) as f:
    line = f.readline()
    for s in line.split():
      result.append(int(s))

  return result