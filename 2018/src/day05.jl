using AdventOfCodeUtils
using Test

# Puzzle description: https://adventofcode.com/2018/day/05

# I was expecting to have to use a linked list but Julia turns out to 
# be fast deleting elements in large vectors. The total run time is 0.3 secs.

const LOWER_UPPER_GAP = abs('a' - 'A')

function react(input)
  opp_polarity(c1, c2) = abs(c1 - c2) == LOWER_UPPER_GAP

  polymer = collect(input)
  i = 1

  while i < length(polymer)
    if opp_polarity(polymer[i], polymer[i+1])
      deleteat!(polymer, i)
      deleteat!(polymer, i)
      i = i == 1 ? 1 : i - 1
    else
      i += 1
    end
  end

  length(polymer)
end

function part1(input)
  react(input)
end

function part2(input)
  letter_pairs = map(a -> [a, uppercase(a)], 'a':'z')
  new_polymer(pair) = filter(letter -> letter ∉ pair, input)

  # The commented out lines are other ways to express the same
  # solution. These are experiments in piping and broadcasting.
  # See https://docs.julialang.org/en/v1/manual/functions/
  # map(pair -> react(new_polymer(pair)), letter_pairs) |> minimum
  # [react(new_polymer(pair)) for pair in letter_pairs] |> minimum
  # react.(new_polymer.(letter_pairs)) |> minimum

  letter_pairs .|> new_polymer .|> react |> minimum
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
