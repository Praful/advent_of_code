using DelimitedFiles
# using Memoize
using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/8

function part1(notes)
  count1478 = 0
  output = notes[:, 2]
  for l in output
    output_segments = split(strip(l), ' ')
    [count1478 += 1 for s in output_segments if length(s) in [2, 3, 4, 7]]
  end
  @show count1478
end

# element 1 is segment pattern for digit 0, element 2 is for digit 1, etc
const DIGITS = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]

function decode_output(output_values, map)
  result = ""
  [result *= "$(map[collect(v) |> sort |> join])" for v in output_values]
  parse(Int, result)
end

# We find the mapping corresponding to the longest signal pattern (=8) by
# going through all perms of "abcedfg". Once we have the mapping 
# from the provided pattern for 8 to the actual, we use it to decode
# the output.
# Output is a Dict of signal pattern => digit
# There'll be 10 entries in the output if this is the right perm.
function find_signal_mapping(patterns, perm)
  signal_pattern_to_digit_map = Dict{String,Int}()
  _, i = findmax(length, patterns)
  mangled_eight_pattern = patterns[i]

  for given_pat in patterns
    actual_digit_pattern = ""
    [actual_digit_pattern *= perm[findfirst(c, mangled_eight_pattern)]
     for c in given_pat]

    actual_digit_pattern = collect(actual_digit_pattern) |> sort |> join
    decoded_digit = findfirst(==(actual_digit_pattern), DIGITS)

    if isnothing(decoded_digit)
      break # this perm doesn't decode the patterns
    else
      signal_pattern_to_digit_map[join(sort(collect(given_pat)))] =
        decoded_digit - 1
    end
  end
  signal_pattern_to_digit_map
end

# A note is 2-element array, format:
#     "<pattern1> <pattern2>, ..., <pattern10>",
#     "<output pattern1>,..., <output pattern4>"
# eg "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb", "fdgacbe cefdb cefbgd gcbe"
# Return sum of the decoded outputs.
function output_value(note)
  output_value_sum = 0
  patterns = split(strip(note[1]), " ")
  for perm in permutations("abcdefg")
    map = find_signal_mapping(patterns, perm)
    if length(map) == 10 # we've found the mapping
      output_value_sum += decode_output(split(strip(note[2]), " "),
        map)
      break
    end
  end
  output_value_sum
end

function part2(notes)
  map(n -> output_value(n), eachrow(notes)) |> sum
end

function read_input(input_file)
  readdlm(input_file, '|', String)
end

function main()
  main_input = read_input("../data/day08.txt")
  test_input = read_input("../data/day08-test.txt")
  test_input2 = read_input("../data/day08-test-2.txt")


  @assert part1(test_input) == 26
  @assert part2(test_input2) == 5353
  @assert part2(test_input) == 61229

  @show part1(main_input) # 355
  @show part2(main_input) # 983030
end

@time main()
