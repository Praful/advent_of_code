using DelimitedFiles
# using Memoize

# Puzzle description: https://adventofcode.com/2021/day/7

function part1(crab_positions)
  min = Inf
  for p = 0:maximum(crab_positions)
    total = 0
    [total += abs(p - c) for c in crab_positions]
    total < min && (min = total)
  end
  BigInt(min)
end

# @memoize function calc_fuel(steps)
function calc_fuel(steps)
  (steps * (steps + 1)) / 2
end

function part2(crab_positions)
  min = Inf
  for p = 0:maximum(crab_positions)
    total = 0
    [total += calc_fuel(abs(p - c)) for c in crab_positions]
    total < min && (min = total)
  end
  BigInt(min)
end

function read_input(input_file)
  input = readdlm(input_file, ',', Int)
  input[1, :]
end

function main()
  main_input = read_input("../data/day07.txt")
  test_input = read_input("../data/day07-test.txt")


  @assert part1(test_input) == 37
  @assert part2(test_input) == 168

  @show part1(main_input) # 349357
  @show part2(main_input) #96708205
end

@time main()
