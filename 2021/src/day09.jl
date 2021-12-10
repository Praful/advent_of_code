using DelimitedFiles
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/9


LOWPOINTS = Vector()
inrange(r, c, h, w) = 1 <= c <= w && 1 <= r <= h

function adj_coords(r, c)
  n = (r - 1, c)
  e = (r, c + 1)
  s = (r + 1, c)
  w = (r, c - 1)
  [n, e, s, w]
end

function islowpoint(input, pv, adj)
  h, w = size(input)
  for (r, c) in adj
    inrange(r, c, h, w) && input[r, c] <= pv && return false
  end
  true
end

function part1(input)
  h, w = size(input)
  lowpoints = 0

  for r = 1:h, c = 1:w
    adj = adj_coords(r, c)
    if islowpoint(input, input[r, c], adj)
      lowpoints += input[r, c] + 1
      push!(LOWPOINTS, (r, c))
    end
  end
  @show lowpoints
end

function count_adj_higher(input, (start_r, start_c))
  h, w = size(input)
  result = Set()

  for (adj_r, adj_c) in adj_coords(start_r, start_c)
    if inrange(adj_r, adj_c, h, w) &&
       input[adj_r, adj_c] < 9 &&
       input[adj_r, adj_c] > input[start_r, start_c]

      push!(result, (adj_r, adj_c))
      union!(result, count_adj_higher(input, (adj_r, adj_c)))
    end
  end
  result
end

function part2(input)
  result = Vector{Int}()

  [push!(result, length(count_adj_higher(input, p)) + 1) for p in LOWPOINTS]

  sort!(result, rev = true)
  result[1] * result[2] * result[3]
end

# return 2D matrix of ints
function read_input(input_file)
  input = readdlm(input_file, String)
  # convert 1D matrix of strings to 2D matrix of ints
  # https://discourse.julialang.org/t/converting-a-array-of-strings-to-an-array-of-char/35123/2
  input = reduce(vcat, permutedims.(collect.(input)))
  parse.(Int, input)
end

function main()
  main_input = read_input("../data/day09.txt")
  test_input = read_input("../data/day09-test.txt")

  @assert part1(test_input) == 15
  @assert part2(test_input) == 1134

  @show part1(main_input) # 550 
  @show part2(main_input) # 1100682
end

@time main()
