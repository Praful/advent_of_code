using DelimitedFiles

# Puzzle description: https://adventofcode.com/2021/day/6

global max_x = max_y = 0

function part1_original(input)
  timers = input[1, :]
  for day = 1:80
    new_fish = length(timers[timers.==0])
    timers .-= 1
    timers[timers.==-1] .= 6
    [push!(timers, 8) for _ = 1:new_fish]
  end
  length(timers)
end

# part1_original takes too long for exponential increase in fish; keep 
# just a count of the fish of each timer value instead of tracking each fish
# individually.
function solve(input, days)
  # where zero count is stored; can't be element 0 since Julia arrays starts at 1
  ZERO = 9

  # fish[timer value] = number of fish with that timer value.
  fish = zeros(Int, 9)
  [fish[n] += 1 for n in input[1, :]]

  for day = 1:days
    new_fish = fish[ZERO]
    fish[ZERO] = fish[1]
    [fish[c] = fish[c+1] for c = 1:7]
    fish[6] += new_fish
    fish[8] = new_fish
  end
  sum(fish[1:9])
end

part1(input) = solve(input, 80)
part2(input) = solve(input, 256)

function main()
  main_input = readdlm("../data/day06.txt", ',', Int)
  test_input = readdlm("../data/day06-test.txt", ',', Int)


  @assert part1(test_input) == 5934
  @assert part2(test_input) == 26984457539

  @show part1(main_input) # 379114
  @show part2(main_input) # 1702631502303
end

@time main()
