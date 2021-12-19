using AdventOfCodeUtils
using DelimitedFiles
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/17



function part1(input)
  0
end

function part2(input)
  0
end

function read_input(input_file)
  readdlm(input_file, String)
end

function main()
  main_input = read_input("../data/day17.txt")
  test_input = read_input("../data/day17-test.txt")

  @assert part1(test_input) == 0
  # @assert part2(test_input) == 0

  # @show part1(main_input) # 
  # @show part2(main_input) # 
end

@time main()
