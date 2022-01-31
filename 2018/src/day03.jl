using AdventOfCodeUtils
using DelimitedFiles
using Test
using DataStructures
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2018/day/03

struct Claim
  id::Int
  x::Int
  y::Int
  width::Int
  height::Int
end

function solve(input)
  claimed = DefaultDict(0)

  for c in input, x = c.x:c.x+c.width-1, y = c.y:c.y+c.height-1
      claimed[(x, y)] += 1
  end

  count(values(claimed) .> 1)
end

part1(input) = solve(input)

function part2(input) end


function read_input(input_file)
  to_claim(s) = Claim((map(to_int, match(r"\#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", s)))...)

  map(to_claim, readlines(input_file))
end

function main()
  main_input = read_input("../data/day03.txt")
  test_input = read_input("../data/day03-test.txt")

  @test part1(test_input) == 4
  # @test part2(test_input) == 3

  @show part1(main_input) # 118858
  # @show part2(main_input) # 
end

@time main()
