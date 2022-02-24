using AdventOfCodeUtils
using DelimitedFiles
using Test
using Memoize
# using ResumableFunctions
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/23

# Solution is based on this Python write-up:
# https://github.com/mebeim/aoc/blob/master/2021/README.md#day-23---amphipod

# The equivalent of Python generators is Julia channels or the ResumableFunctions
# package. There are commented out sections that use channel and ResumableFunctions.
# However, ResumableFunctions was similar speed to and channels much slower than 
# using plain enumeration and passing the result.

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

function done(rooms::Vector{Vector{Int}}, room_size::Int)
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
function move_cost(room::Vector{Int64}, hallway::Vector{Int64}, r::Int, h::Int, room_size::Int, to_room = false)
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

function move_to_room(home::Home, room_size::Int)
  # Channel() do channel
  # Channel{Tuple{Int64,Home}}(2) do channel
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
    # @yield (cost, Home(new_rooms, new_hallway))
    push!(result, (cost, Home(new_rooms, new_hallway)))
  end
  # end
  result
end

function move_to_hallway(home::Home, room_size::Int)
  result = []

  # Channel() do channel
  # Channel{Tuple{Int64,Home}}(2) do channel
  for (r, room) in enumerate(home.rooms)
    all(==(r), room) && continue # occupants correct

    for h in 1:length(home.hallway)
      cost = move_cost(room, home.hallway, r, h, room_size, false)
      isinf(cost) && continue # can't move eg another apod in way

      # create new state with apod moved from room r to slot h in hallway
      new_rooms = update_home(home.rooms, r, [room[2:end]...])
      new_hallway = update_home(home.hallway, h, room[1])

      # put!(channel, (cost, Home(new_rooms, new_hallway)))
      # @yield (cost, Home(new_rooms, new_hallway))
      push!(result, (cost, Home(new_rooms, new_hallway)))
    end
  end
  # end
  result
end

# not used in this version but for the Channel version if above uncommented
# function possible_moves(home, room_size)
#   # Channel() do channel
#   Channel{Tuple{Int64,Home}}(2) do channel
#     for (cost, new_home) in move_to_room(home, room_size)
#       put!(channel, (cost, new_home))
#     end

#     for (cost, new_home) in move_to_hallway(home, room_size)
#       put!(channel, (cost, new_home))
#     end
#   end
# end

# the Dict parameter memoizes arrays
@memoize Dict function solve(rooms::Vector{Vector{Int64}}, hallway::Vector{Int64}, room_size::Int)
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

function read_input(input_file::String, room_size = 2)
  APOD_IDS = "ABCD"
  ROOM_START_LINE = 3
  lines = readlines(input_file)

  function room_occupants(pos)
    occ(n) = findfirst(lines[n][pos], APOD_IDS)

    result = []
    [result = [result...; occ(i)]
     for i in ROOM_START_LINE:(ROOM_START_LINE+room_size-1)]

    result
  end

  if room_size == 4
    lines = [lines[1:3]...; "  #D#C#B#A#  "; "  #D#B#A#C#  "; lines[4:end]]
  end


  hallway = fill(EMPTY, 7)
  rooms = fill([EMPTY, EMPTY], 4)

  rooms[1] = room_occupants(4)
  rooms[2] = room_occupants(6)
  rooms[3] = room_occupants(8)
  rooms[4] = room_occupants(10)

  # @show rooms, hallway
  Home(rooms, hallway)
end

function solve(input_file, room_size = 2)
  home = read_input(input_file, room_size)
  solve(home.rooms, home.hallway, room_size)
end

part1(input_file) = solve(input_file, 2)
part2(input_file) = solve(input_file, 4)

function main()
  main_input = "../data/day23.txt"
  test_input = "../data/day23-test.txt"

  @test part1(test_input) == 12521
  @test part2(test_input) == 44169

  @show part1(main_input) # 16508
  @show part2(main_input) # 43626
end

@time main()
