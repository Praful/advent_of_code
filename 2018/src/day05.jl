using AdventOfCodeUtils
using Test

# Puzzle description: https://adventofcode.com/2018/day/05

const CHAR_LOWER_UPPER_GAP = 32

function react(input)
  polymer = collect(input)
  i = 1

  while i < length(polymer)
    ((i + 1) > length(polymer)) && break

    if abs(polymer[i] - polymer[i+1]) == CHAR_LOWER_UPPER_GAP
      deleteat!(polymer, i)
      deleteat!(polymer, i)
      i = i == 1 ? 1 : i - 1
    else
      i += 1
    end
  end

  polymer
end

function part1(input)
  length(react(input))
end

function part2(input)
  pairs = map(a -> [a, uppercase(a)], 'a':'z')
  minimum(map(p -> length(react(filter(e -> e ∉ p, input))), pairs))
end

function read_input(input_file)
  readlines(input_file)[1]
end

function main()
  main_input = read_input("../data/day05.txt")
  test_input = read_input("../data/day05-test.txt")

  @test part1(test_input) == 10
  @test part2(test_input) == 4

  @show part1(main_input) # 10762
  @show part2(main_input) # 6946 
end

@time main()
