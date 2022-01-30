using AdventOfCodeUtils
using DelimitedFiles
using Test

# using TimerOutputs

# Puzzle description: https://adventofcode.com/2021/day/22

# For part 1, I set a 3D matrix to on or off depending on the cuboid.
# This was too slow for part 2. Part 2 finds the intersection of cuboids,
# building up a list and then checking against that. The built list will
# add or subtract cuboids to reflect overlapping cupoids depending on 
# whether they are in an on or off state.

# const to =TimerOutput()

struct Cuboid
  on::Bool
  xyz::Vector{UnitRange{Int}} # x, y, z ranges as vector 
end

VALID = -50:50 # for part 1
# Return true if xyz is in the range specified for part 1
in_range(xyz) = map(c -> (c[1] in VALID) && (c[end] in VALID),
  xyz) |> all

# Return cubes switched on after stepping through all cuboids.
function cubes_on_part1(cuboids::Vector{Cuboid})
  size = length(VALID) + 1
  cubes = falses(size, size, size)

  for cuboid in cuboids
    !in_range(cuboid.xyz) && continue

    # shift to ensure all values are >0 so that we can directly
    # update a 3D matrix
    shifted = []
    [push!(shifted, s[1]+VALID[end]+1:s[end]+VALID[end]+1)
     for s in cuboid.xyz]

    cubes[shifted[1], shifted[2], shifted[3]] .= cuboid.on
  end

  count(==(true), cubes)
end

# Return intersection of two cuboids or nothing if they don't intersect
function intersection(c1::Cuboid, c2::Cuboid)
  result = []
  for (e1, e2) ∈ zip(c1.xyz, c2.xyz)
    overlap = intersect(e1, e2)
    length(overlap) == 0 ? (return nothing) : push!(result, overlap)
  end
  result
end

# Return cubes in cuboid (=volume)
cubes(cuboid::Cuboid) = prod(length, cuboid.xyz) * (cuboid.on ? 1 : -1)

# limit_range is to test this works for part1 as well
# Return cubes switched on after stepping through all cuboids.
function cubes_on_part2(input::Vector{Cuboid}, limit_range = false)
  cuboids = copy(input)
  cuboids_deduped = []

  while !isempty(cuboids)
    c = popfirst!(cuboids)
    limit_range && !in_range(c.xyz) && continue

    single_dedup = []
    for cd in cuboids_deduped
      overlap = intersection(c, cd)
      !isnothing(overlap) && push!(single_dedup, Cuboid(!cd.on, overlap))
    end
    append!(cuboids_deduped, single_dedup)
    c.on && push!(cuboids_deduped, c)
  end
  sum(cubes, cuboids_deduped)
end

part1(input) = cubes_on_part1(input)
part2(input, limit_range = false) = cubes_on_part2(input, limit_range)

function read_input(input_file)
  function range(r)
    m = match(r"=(-?\d+)\.\.(-?\d+)", r)
    to_int(m[1]):to_int(m[2])
  end

  function to_cuboid(line)
    s = split(line, ",")
    on = contains(s[1], "on ")
    Cuboid(on, [range(s[1]), range(s[2]), range(s[3])])
  end

  map(to_cuboid, readlines(input_file))
end

function main()
  main_input = read_input("../data/day22.txt")
  test_input = read_input("../data/day22-test.txt")
  test_input2 = read_input("../data/day22-test-2.txt")

  @test part1(test_input) == 590784
  @test part2(test_input, true) == 590784
  @test part2(test_input2) == 2758514936282235

  @show part1(main_input) # 503864
  @show part2(main_input) # 1255547543528356
end

@time main()
