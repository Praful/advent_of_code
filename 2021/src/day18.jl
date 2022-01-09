using AdventOfCodeUtils
using DelimitedFiles
using Test
using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/18

# There are a number of ways to do this. Initially, I thought of building
# a tree but thought it would be fiddly moving up and down it to find
# various nodes. So I experimented with just manipulating the string
# representation, which turned out to be straightforward. The initial
# nested pair (5-deep) is found by counting brackets. After that
# the string is scanned on either side to find the numbers that need to
# incremented. Then it's a matter of finding and replacing elements
# in the string. 
# The magnitude is also a repeated search and replace operation.


const DIGITS = '0':'9'

# Return indices of brackets for deepest nested pair
# eg return (5,9) for [[[[[9,8],1],2],3],4]
function deepest_nested_pair(s, target_depth = 4)
  depth = 0
  for (i, a) in enumerate(s)
    if a == '['
      depth += 1
    elseif a == ']'
      depth -= 1
    end
    (depth > target_depth) && return (i, findnext(==(']'), s, i))
  end
  nothing
end

# Return start and end indces for value left of exploring pair. The
# value can be more than one digit.
# eg pair is [7,3] so return indices for 1 (9,9) for 
# [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
function left_num_index(s, from_index)
  start_index = end_index = nothing
  for i = from_index:-1:1
    if s[i] in DIGITS
      if isnothing(start_index)
        start_index = end_index = i
      else
        start_index = i
      end
    else
      !isnothing(start_index) && return (start_index, end_index)
    end
  end
  nothing
end

# Return start and end indices for value right of exploring pair. The
# value can be more than one digit.
# eg pair is [7,3] so return indices of 6 (21,21) for
# [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
function right_num_index(s, from_index)
  start_index = end_index = nothing
  for i = from_index:length(s)
    if s[i] in DIGITS
      if isnothing(start_index)
        start_index = end_index = i
      else
        end_index = i
      end
    else
      !isnothing(start_index) && return (start_index, end_index)
    end
  end
  nothing
end


function explode(s, nested_pair_index, left_num_index, right_num_index)
  m = match(r"\[(\d+),(\d+)\]", s[nested_pair_index[1]:nested_pair_index[2]])
  nested_num_left = parse(Int, m[1])
  nested_num_right = parse(Int, m[2])
  sfs = s

  # Do updates from right to left so that calculated indexes aren't
  # shifted.

  # Update number right of pair (if there is one)
  if !isnothing(right_num_index)
    new_right_num = parse(Int, s[right_num_index[1]:right_num_index[2]]) + nested_num_right

    sfs = replace_from_index(s, r"\d+" => new_right_num, right_num_index[1])
  end

  # Replace nested pair with zero
  sfs = replace_from_index(sfs, r"\[\d+,\d+\]" => "0", nested_pair_index[1])

  # Update number left of pair (if there is one)
  if !isnothing(left_num_index)
    new_left_num = "$((parse(Int, s[left_num_index[1]:left_num_index[2]]) + nested_num_left))"
    sfs = replace_from_index(sfs, r"\d+" => new_left_num, left_num_index[1])
  end

  return sfs
end

function explode_wrapper(s)
  nest_pair_index = deepest_nested_pair(s)
  if !isnothing(nest_pair_index)
    left_value_index = left_num_index(s, nest_pair_index[1])
    right_value_index = right_num_index(s, nest_pair_index[2])
    return explode(s, nest_pair_index, left_value_index, right_value_index)
  end
  return nothing
end

can_split(s) = match(r"\d\d", s) !== nothing
can_explode(s) = deepest_nested_pair(s) !== nothing

function split(s)
  m = match(r"\d\d", s)
  isnothing(m) && return nothing
  num = parse(Int, s[m.offset:m.offset+1])

  string(s[1:m.offset-1], "[", Int(floor(num / 2)), ",",
    Int(ceil(num / 2)), "]", s[m.offset+2:end])
end

# Return [s1,s2]
function add(s1, s2)
  string("[", s1, ",", s2, "]")
end


# Always explode until we can't; then split once; then back to 
# attempt to explode.
function reduce(s)
  sfs = s
  while true
    if can_explode(sfs)
      sfs = explode_wrapper(sfs)
      continue
    end

    if can_split(sfs)
      sfs = split(sfs)
      continue
    end

    break
  end
  sfs
end

reduce_add(a, b) = reduce(add(a, b))
reduce_list(l) = foldl(reduce_add, l[2:end]; init = l[1])

function magnitude(s)
  while true
    m = match(r"\[(\d+),(\d+)\]", s)
    isnothing(m) && (return parse(Int, s))
    pair_magnitude = 3parse(Int, m[1]) + 2parse(Int, m[2])
    left_str = m.offset < 2 ? "" : s[1:m.offset-1]
    right_str = m.offset + length(m.match) > length(s) ? "" :
                s[m.offset+length(m.match):end]
    s = string(left_str, pair_magnitude, right_str)
  end
end

function part1(input)
  magnitude(reduce_list(input))
end

function part2(input)
  maximum(part1, permutations(input, 2))
end

function read_input(input_file)
  readlines(input_file)
end

function main()
  main_input = read_input("../data/day18.txt")
  test_input = read_input("../data/day18-test.txt")


  @test part1(test_input) == 4140
  @test part2(test_input) == 3993

  @show part1(main_input) # 4347
  @show part2(main_input) # 4721
end

@time main()
