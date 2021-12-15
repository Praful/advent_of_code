using AdventOfCodeUtils
using DelimitedFiles
using DataStructures

# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/15


# Dijkstra's algorithm is here:
# https://www.redblobgames.com/pathfinding/a-star/introduction.html
function lowest_risk(cave, start, target)
  cave_size = size(cave)

  in_cave(p) = (p[1] in 1:cave_size[1]) && (p[2] in 1:cave_size[2])

  pq = PriorityQueue()
  enqueue!(pq, start, 0)

  # came_from = Dict()
  risk_so_far = Dict()
  # came_from[start] = nothing
  risk_so_far[start] = 0

  while !isempty(pq)
    current = dequeue!(pq)

    (current == target) && break

    risk_so_far_points = keys(risk_so_far)
    current_risk = risk_so_far[current]

    for adj in adjacent(current)
      if in_cave(adj)
        new_risk = current_risk + cave[adj]
        if !(adj in risk_so_far_points) || (new_risk < risk_so_far[adj])
          risk_so_far[adj] = new_risk
          enqueue!(pq, adj, new_risk)
          # came_from[adj] = current
        end
      end
    end
  end
  @show risk_so_far[target]
end

# input (10x10) = one tile, we need to create 25 tiles for a 50x50 cave
# we copy across to get 10 x 50 then down to get 50 x 50
function expanded_cave(input)
  function copy_tile(tile, copy_across = true)
    result = copy(tile)
    work_tile = copy(tile)
    for i = 1:4
      work_tile .+= 1
      work_tile[work_tile.==10] .= 1
      result = copy_across ? hcat(result, work_tile) :
               vcat(result, work_tile)
    end
    result
  end

  tile_row_1 = copy_tile(input)
  copy_tile(tile_row_1, false)
end

function part1(input)
  lowest_risk(input, CartesianIndex(1, 1), CartesianIndex(size(input)))
end

function part2(input)
  new_input = expanded_cave(input)
  lowest_risk(new_input, CartesianIndex(1, 1),
    CartesianIndex(size(new_input)))
end

function read_input(input_file)
  read_string_matrix(input_file)
end

function main()
  main_input = read_input("../data/day15.txt")
  test_input = read_input("../data/day15-test.txt")
  test_input2 = read_input("../data/day15-test-2.txt")

  @assert part1(test_input) == 40
  @assert expanded_cave(test_input) == test_input2
  @assert part2(test_input) == 315

  @show part1(main_input) # 562
  @show part2(main_input) # 2874
end

@time main()
