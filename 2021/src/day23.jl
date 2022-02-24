using AdventOfCodeUtils
using DelimitedFiles
using Test
using Memoize
# using ResumableFunctions
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/23

# Solution is based on this Python write-up:
# https://github.com/mebeim/aoc/blob/master/2021/README.md#day-23---amphipod
# The equivalent of Python generators is Julia Channel. There already
# commented out sections that use Channel. The solution works but is slower
# than using plain enumeration and passing the result.

struct Home
  rooms::Vector{Vector{Int}}
  hallway::Vector{Int}
end

ROOM_DISTANCE = [
  [2, 1, 1, 3, 5, 7, 8], # from/to room 1
  [4, 3, 1, 1, 3, 5, 6], # from/to room 2
  [6, 5, 3, 1, 1, 3, 4], # from/to room 3
  [8, 7, 5, 3, 1, 1, 2], # from/to room 4
]

function done(rooms::Vector, room_size::Int)
  for (r, room) in enumerate(rooms)
    if any(!=(r), room) || length(room) != room_size
      return false
    end
  end
  true
end

#location is rooms or hallway
function update_home(location, index, occupant)
  new_location = copy(location)
  new_location[index] = occupant
  new_location
end

const EMPTY = 0
is_empty(occupant) = occupant == EMPTY

# h is the hallway spot index; r is the room index
function move_cost(room::Vector, hallway::Vector, r::Int, h::Int, room_size::Int, to_room = false)
  start_ = 0
  end_ = 0
  if r + 1 < h
    start_ = r + 2
    end_ = h + (to_room ? 0 : 1) - 1
  else
    start_ = h + (to_room ? 1 : 0)
    end_ = r + 1
  end
  any(!is_empty, hallway[start_:end_]) && return Inf

  obj = to_room ? hallway[h] : room[1]

  return 10^(obj - 1) * (ROOM_DISTANCE[r][h] + ((to_room ? 1 : 0) + room_size) - length(room))
end

function move_to_room(home, room_size)
  # Channel() do channel
  # Channel{Tuple{Int64,Home}}() do channel
  result = []
  for (h, obj) in enumerate(home.hallway)
    is_empty(obj) && continue # hallway spot empty

    room = home.rooms[obj]
    any(!=(obj), room) && continue # diff apod occupies room

    cost = move_cost(room, home.hallway, obj, h, room_size, true)
    isinf(cost) && continue # can't move eg another apod in way

    # create new state with apod moved from slot h to room
    new_rooms = update_home(home.rooms, obj, [obj, room...])
    new_hallway = update_home(home.hallway, h, EMPTY)

    # put!(channel, (cost, Home(new_rooms, new_hallway)))
    push!(result, (cost, Home(new_rooms, new_hallway)))
  end
  # end
  result
end

function move_to_hallway(home, room_size)
  result = []

  # Channel() do channel
  for (r, room) in enumerate(home.rooms)
    all(==(r), room) && continue # occupants correct

    for h in 1:length(home.hallway)
      cost = move_cost(room, home.hallway, r, h, room_size, false)
      isinf(cost) && continue # can't move eg another apod in way

      # create new state with apod moved from room r to slot h in hallway
      new_rooms = update_home(home.rooms, r, [room[2:end]...])
      new_hallway = update_home(home.hallway, h, room[1])

      # put!(channel, (cost, Home(new_rooms, new_hallway)))
      push!(result, (cost, Home(new_rooms, new_hallway)))
    end
  end
  # end
  result
end

function possible_moves(home, room_size)
  Channel() do channel
    for (cost, new_home) in move_to_room(home, room_size)
      put!(channel, (cost, new_home))
    end

    for (cost, new_home) in move_to_hallway(home, room_size)
      put!(channel, (cost, new_home))
    end
  end
end

@memoize Dict function solve(rooms::Vector, hallway::Vector, room_size::Int)
  done(rooms, room_size) && return 0

  best = Inf
  # for (cost, next_home) in possible_moves(Home(rooms, hallway), room_size)
  #   cost += solve(next_home.rooms, next_home.hallway, room_size)

  #   if cost < best
  #     best = cost
  #   end
  # end
  for (cost, next_home) in move_to_room(Home(rooms, hallway), room_size)
    cost += solve(next_home.rooms, next_home.hallway, room_size)

    if cost < best
      best = cost
    end
  end

  for (cost, next_home) in move_to_hallway(Home(rooms, hallway), room_size)
    cost += solve(next_home.rooms, next_home.hallway, room_size)

    if cost < best
      best = cost
    end
  end
  best
end

function part1(home::Home)
  solve(home.rooms, home.hallway, 2)
end

function part2(input)
  0
end

function read_input(input_file)
  APOD_IDS = "ABCD"
  lines = readlines(input_file)

  room_occupants(loc) =
    [findfirst(lines[3][loc], APOD_IDS), findfirst(lines[4][loc], APOD_IDS)]


  hallway = fill(EMPTY, 7)
  rooms = fill([EMPTY, EMPTY], 4)

  rooms[1] = room_occupants(4)
  rooms[2] = room_occupants(6)
  rooms[3] = room_occupants(8)
  rooms[4] = room_occupants(10)

  # @show rooms, hallway
  Home(rooms, hallway)
end

function main()
  main_input = read_input("../data/day23.txt")
  test_input = read_input("../data/day23-test.txt")

  @test part1(test_input) == 12521
  # @test_skip part2(test_input) == 0 broken = true

  @show part1(main_input) # 16508
  # @show part2(main_input) # 43626
end

@time main()
