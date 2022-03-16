using AdventOfCodeUtils
using DelimitedFiles
using Test
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/25

EMPTY = '.'
SC_EAST = '>'
SC_SOUTH = 'v'

function single_step(current_map, sc_type, incX, incY)
  new_map = copy(current_map)
  maxY, maxX = size(current_map)
  did_move = false

  sc_locations = findall(==(sc_type), current_map)

  for c in sc_locations
    x = c[2]
    y = c[1]
    destX = incX > 0 ? (x % maxX) + 1 : x
    destY = incY > 0 ? (y % maxY) + 1 : y
    if current_map[destY, destX] == EMPTY
      did_move = true
      new_map[y, x] = EMPTY
      new_map[destY, destX] = sc_type
    end
  end
  did_move, new_map
end

function do_moves(sea_map)
  step = 0
  current_map = copy(sea_map)

  while true
    did_move1, current_map = single_step(current_map, SC_EAST, 1, 0)
    did_move2, current_map = single_step(current_map, SC_SOUTH, 0, 1)

    step += 1

    !(did_move1 || did_move2) && return step
  end
end

function print_map(m)
  # println.(eachrow(m))
  [println(join(i)) for i in eachrow(m)]
  println("================")
end

part1(input) = do_moves(input)

function read_input(input_file)
  read_string_matrix(input_file, false)
end

function main()
  main_input = read_input("../data/day25.txt")
  test_input = read_input("../data/day25-test.txt")

  @test part1(test_input) == 58

  @show part1(main_input) # 498
end

@time main()
