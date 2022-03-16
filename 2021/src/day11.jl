using AdventOfCodeUtils

using DelimitedFiles
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/11


# rename to avoid clash with AdventOfCodeUtils
function adjacent2(coord)
  r, c = Tuple(coord)
  [
    CartesianIndex(r - 1, c),
    CartesianIndex(r + 1, c),
    CartesianIndex(r, c + 1),
    CartesianIndex(r, c - 1),
    CartesianIndex(r - 1, c + 1),
    CartesianIndex(r - 1, c - 1),
    CartesianIndex(r + 1, c + 1),
    CartesianIndex(r + 1, c - 1)
  ]
end

function flash(octopuses, has_flashed = Vector())
  octopus_coords = keys(octopuses)
  flashers = setdiff(findall(.>(9), octopuses), has_flashed)

  if length(flashers) > 0
    for coord in flashers
      adj = intersect(adjacent2(coord), octopus_coords)
      octopuses[CartesianIndex.(adj)] .+= 1
      push!(has_flashed, coord)
    end
    flash(octopuses, has_flashed)
  end
  length(has_flashed)
end

function part1(input, steps = 100)
  octopuses = copy(input)
  flash_count = 0

  for _ = 1:steps
    octopuses .+= 1
    flash_count += flash(octopuses)
    octopuses[octopuses.>9] .= 0
  end
  @show flash_count
end

function part2(input)
  octopuses = copy(input)
  step = 0

  while true
    step += 1
    octopuses .+= 1
    flash(octopuses)
    flashed = (octopuses[octopuses.>9] .= 0)
    if length(flashed) == length(octopuses)
      return step
    end
  end
end

read_input(input_file)= read_string_matrix(input_file)

function main()
  main_input = read_input("../data/day11.txt")
  test_input = read_input("../data/day11-test.txt")

  @assert part1(test_input) == 1656
  @assert part2(test_input) == 195

  @show part1(main_input) # 1640
  @show part2(main_input) # 312
end

@time main()
