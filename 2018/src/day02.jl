using AdventOfCodeUtils
using Test
using DataStructures
using Combinatorics

# Puzzle description: https://adventofcode.com/2018/day/02



function part1(input)
  twos = 0
  threes = 0

  for id in input
    freq = DefaultDict{Char,Int}(0)
    [freq[c] += 1 for c in id]
    (in(2, values(freq))) && (twos += 1)
    (in(3, values(freq))) && (threes += 1)
  end
  twos * threes
end

function part2(input)

  for (first, second) in combinations(input, 2)
    (length(first) != length(second)) && continue
    id_length = length(first)

    diff_count = diff_pos = 0

    for i in 1:id_length
      if first[i] != second[i]
        diff_pos = i
        diff_count += 1
      end
      diff_count > 1 && break
    end
    (diff_count == 1) && (return deleteat!(collect(first), diff_pos) |> join)
  end
end

function read_input(input_file)
  readlines(input_file)
end

function main()
  main_input = read_input("../data/day02.txt")
  test_input = read_input("../data/day02-test.txt")
  test_input2 = read_input("../data/day02-test-2.txt")

  @test part1(test_input) == 12
  @test part2(test_input2) == "fgij"

  @show part1(main_input) # 6474
  @show part2(main_input) # mxhwoglxgeauywfkztndcvjqr
end

@time main()
