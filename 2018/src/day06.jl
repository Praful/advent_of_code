using AdventOfCodeUtils
using DelimitedFiles
using Test
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2018/day/6

manhattan_distance(x1, y1, x2, y2) = abs(x1 - x2) + abs(y1 - y2)

const MULTIPLE = -1
const UNPROCESSED = 0

function solve(input, max_distance)
  cols = maximum(input[:, 1])
  rows = maximum(input[:, 2])

  # grid was defined for debugging
  # grid = fill(UNPROCESSED, (rows, cols))
  # [grid[c[2], c[1]] = n for (n, c) in enumerate(eachrow(input))]

  closest_count = Dict()
  max_region = 0

  perimeter = Set()

  for r in 1:rows, c in 1:cols
    min_dist = Inf
    points_found = 0
    point_id = 0
    total_dist = 0

    for (n, p) in enumerate(eachrow(input))
      dist = manhattan_distance(c, r, p[1], p[2])
      total_dist += dist
      if dist == min_dist
        points_found += 1
      elseif dist < min_dist
        min_dist = dist
        points_found = 1
        point_id = n
      end
    end

    if total_dist < max_distance
      max_region += 1
    end

    on_perimeter(r, c) = r == 1 || r == rows || c == 1 || c == cols

    if points_found == 1
      # grid[r, c] = point_id
      area = get(closest_count, point_id, 1)
      closest_count[point_id] = area + 1
      on_perimeter(r, c) && push!(perimeter, point_id)
    elseif points_found > 1
      # grid[r, c] = MULTIPLE
    end
  end

  # println.(eachrow(grid))

  # take away 1 because we increment count for when we get dist from
  # location to itself 
  maximum(kv -> kv[1] in perimeter ? 0 : kv[2], closest_count) - 1, max_region
end

function read_input(input_file)
  readdlm(input_file, ',', Int)
end

function main()
  main_input = read_input("../data/day06.txt")
  test_input = read_input("../data/day06-test.txt")

  @test solve(test_input, 32) == (17, 16)

  @show solve(main_input, 10_000) # 5941, 40244
end

@time main()
