module Day12

# To use this, add path of AdventOfCodeUtils.jl to 
# ~/.julia/config.startup.jl, eg the line
# push!(LOAD_PATH, "/users/me/dev/shared/src)
using AdventOfCodeUtils

using DelimitedFiles

# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/12

struct Cave
  id::String
  connections::Vector{Cave}
  is_small::Bool

  function Cave(id)
    new(id, Vector{Cave}(), is_lowercase(id))
  end
end

add_connection(from, to) = push!(from.connections, to)
is_start(c) = c.id == START
is_end(c) = c.id == END

START = "start"
END = "end"
visited = Dict{Cave,Int}()

function traverse(cave, part2 = false)
  was_visited() = cave.is_small && visited[cave] > 0 &&
                  (part2 ? small_cave_twice() : true)

  small_cave_twice() = length(filter(kv -> kv[1].is_small && kv[2] > 1,
    visited)) > 0

  result = 0
  get!(visited, cave, 0)

  is_end(cave) && (return 1)
  was_visited() && (return 0)

  visited[cave] += 1

  result = mapreduce(c -> traverse(c, part2), +, filter(!is_start, cave.connections))

  # Chaining (alternative)
  # result = cave.connections |>
  #          c -> filter(!is_start, c) |>
  #               f -> mapreduce(c -> traverse(c, part2), +, f)

  visited[cave] -= 1

  result
end

function solve(cave_system, part2 = false)
  empty!(visited)
  @show traverse(cave_system[START], part2)
end

function read_input(input_file)
  cave_system = Dict{String,Cave}()
  input = readdlm(input_file, String)
  for line in input
    from_id, to_id = split(line, "-")
    from_cave = get!(cave_system, from_id, Cave(from_id))
    to_cave = get!(cave_system, to_id, Cave(to_id))
    add_connection(from_cave, to_cave)
    add_connection(to_cave, from_cave)
  end
  cave_system
end

function main()
  main_input = read_input("../data/day12.txt")
  test_input1 = read_input("../data/day12-test-1.txt")
  test_input2 = read_input("../data/day12-test-2.txt")
  test_input3 = read_input("../data/day12-test-3.txt")

  @assert solve(test_input1) == 10
  @assert solve(test_input2) == 19
  @assert solve(test_input3) == 226

  @assert solve(test_input1, true) == 36
  @assert solve(test_input2, true) == 103
  @assert solve(test_input3, true) == 3509

  @show solve(main_input) # 4186
  @show solve(main_input, true) # 92111
end

@time main()
end