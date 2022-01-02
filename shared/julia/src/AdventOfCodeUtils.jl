module AdventOfCodeUtils

using DelimitedFiles

is_lowercase(s) = !isnothing(match(r"^[a-z]+$", s))
export is_lowercase

# read file with lines like
#
#   123456789 
#   657657657
#   563565635
#
# and return, in this example, a 3x9 matrix of Ints.
function read_string_matrix(input_file)
  input = readdlm(input_file, String)
  # convert 1D matrix of strings to 2D matrix of ints
  # https://discourse.julialang.org/t/converting-a-array-of-strings-to-an-array-of-char/35123/2
  input = reduce(vcat, permutedims.(collect.(input)))
  parse.(Int, input)
end
export read_string_matrix

function adjacent(point, include_diagonals = false)
  r, c = Tuple(point)
  result = [
    CartesianIndex(r - 1, c),
    CartesianIndex(r + 1, c),
    CartesianIndex(r, c + 1),
    CartesianIndex(r, c - 1),
  ]
  if include_diagonals
    union!(result, [
      CartesianIndex(r - 1, c + 1),
      CartesianIndex(r - 1, c - 1),
      CartesianIndex(r + 1, c + 1),
      CartesianIndex(r + 1, c - 1)
    ])
  end
  result
end
export adjacent

# Replace first match starting from index.
function replace_from_index(s, regex, index)
  left_text = s[1:index-1]
  right_text = replace(s[index:end], regex; count = 1)
  string(left_text, right_text)
end
export replace_from_index

hex2dec(s) = parse(BigInt, s, base = 16)
export hex2dec

dec2bin(n, padding = 1) = reverse(digits(n, base = 2, pad = padding))
export dec2bin

hex2bin(s) = dec2bin(hex2dec(s), length(s) * 4)
export hex2bin

bin2dec(n) = parse(Int, n |> join, base = 2)
export bin2dec

end