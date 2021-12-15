using AdventOfCodeUtils
using DelimitedFiles
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/14



function test()
  a = collect("abcd")
  for i = 1:1000
    i
    pos = rand(1:length(a))
    c = rand('a':'z')
    insert!(a, pos, c)
  end
  @show length(a)

  l = 4
  for i = 1:10
    l = 2l
  end
  @show l

end

# Used in part1 but is too slow for part2
function solve_slow(template, rules, steps = 10)
  count = Dict{Char,Int}()
  for c in template
    get!(count, c, 0)
    count[c] += 1
  end

  for _ = 1:steps
    step_result = template[1]
    for pos = 1:(length(template)-1)
      pair = template[pos:pos+1]
      ins = rules[template[pos:pos+1]]
      get!(count, ins, 0)
      count[ins] += 1
      step_result *= ins * pair[2]
    end
    template = step_result
  end

  maximum(values(count)) - minimum(values(count))

end

function solve(template, rules, steps = 10)
  function update_counters(dict, key, inc_value)
    get!(dict, key, 0)
    dict[key] += inc_value
  end

  count = Dict{Char,Int}()
  pairs = Dict{String,Int}()

  [update_counters(pairs, template[pos:pos+1], 1) for pos = 1:(length(template)-1)]

  [update_counters(count, c, 1) for c in template]

  for _ = 1:steps
    new_pairs = Dict{String,Int}()
    for (pair, value) in pairs
      new_char = rules[pair]
      update_counters(new_pairs, pair[1] * new_char, value)
      update_counters(new_pairs, new_char * pair[2], value)
      update_counters(count, new_char, value)
    end
    pairs = new_pairs
  end

  @show maximum(values(count)) - minimum(values(count))
end

function part1((template, rules))
  solve(template, rules)
end

function part2((template, rules))
  solve(template, rules, 40)
end

function read_input(input_file)
  rules = Dict{String,Char}()
  input = readdlm(input_file, String)
  template = input[1]
  [rules[input[r, 1]] = input[r, 3][1] for r = 2:size(input)[1]]

  (template, rules)
end

function main()
  main_input = read_input("../data/day14.txt")
  test_input = read_input("../data/day14-test.txt")

  @assert part1(test_input) == 1588
  @assert part2(test_input) == 2188189693529

  @show part1(main_input) # 2587
  @show part2(main_input) # 3318837563123
end

@time main()
