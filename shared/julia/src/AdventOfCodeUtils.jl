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


end