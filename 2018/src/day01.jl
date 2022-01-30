using AdventOfCodeUtils
using Test

# Puzzle description: https://adventofcode.com/2018/day/01


part1(input) = sum(input)

function part2(input)
  seen = Set{Int}()
  freq = 0
  while true
    for n in input
      freq += n
      in(freq, seen) ? (return freq) : push!(seen, freq)
    end
  end
end

function read_input(input_file)
  value(s) = to_int((match(r"(-?\+?\d+)", s))[1])
  map(value, readlines(input_file))
end

function main()
  main_input = read_input("../data/day01.txt")

  test_input = [1, 1, 1]
  test_input2 = [-1, -2, -3]
  test_input3 = [+3, +3, +4, -2, -4]
  test_input4 = [-6, +3, +8, +5, -6]
  test_input5 = [+1, -2, +3, +1]

  @test part1(test_input) == 3
  @test part1(test_input2) == -6

  @test part2(test_input5) == 2
  @test part2(test_input3) == 10
  @test part2(test_input4) == 5

  @show part1(main_input) # 437
  @show part2(main_input) # 655
end

@time main()
