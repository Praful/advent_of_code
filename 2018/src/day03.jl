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

function solve(claims::Array{Claim})
  claimed = DefaultDict(0)

  for c in claims
    for x = c.x:c.x+c.width-1, y = c.y:c.y+c.height-1
      claimed[(x, y)] += 1
    end
  end
  overlap_count = count(values(claimed) .> 1)

  # This could be made more efficient by changing part 1 above. But it's 
  # good (and fast) enough
  for c in claims
    has_overlaps = false
    for x = c.x:c.x+c.width-1, y = c.y:c.y+c.height-1
      (claimed[(x, y)] != 1) && (has_overlaps = true) && break
    end
    !has_overlaps && return (overlap_count, c.id)
  end
end

function read_input(input_file)
  to_claim(s) = Claim((map(to_int, match(r"\#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", s)))...)

  map(to_claim, readlines(input_file))
end

function main()
  main_input = read_input("../data/day03.txt")
  test_input = read_input("../data/day03-test.txt")

  (part1, part2) = solve(test_input)
  @test part1 == 4
  @test part2 == 3

  (part1, part2) = solve(main_input)
  @show part1 # 118858
  @show part2 # 1100
end

@time main()
