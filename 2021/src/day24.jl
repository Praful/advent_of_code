using AdventOfCodeUtils
using DelimitedFiles
using Test

# Puzzle description: https://adventofcode.com/2021/day/24

# This is a custom solution based on analysing my input. It may
# not work with other input.
# The complete input is split up into 14 units, each with 18 instructions.
#
# The monad of the puzzle name refers to the two types of units:
#
#   1: the divisor is 1. We try digits 1-9 for each unit,
#      working out the next z.
#   2: the divisor is 26. If the ALU returns a valid digit (the
#      x value), we proceed with processing this unit.

struct Instruction
  op::String
  a
  b
end

const UNIT_SIZE = 18
const TOTAL_UNITS = 14
const UNIT_TYPE_1 = 1
const UNIT_TYPE_2 = 26

# This is a simplied ALU based on my input. I don't know if it will
# work with other input.
function alu(w::Int, z::Int, offset1::Int, offset2::Int, type::Int)
  if type == UNIT_TYPE_1
    return 26z + w + offset2
  elseif type == UNIT_TYPE_2
    return (z % 26) + offset1 #x
  else
    throw("Invalid type $type")
  end
end

function try_model(program, unit_number, model_number, z, digits)
  unit_type(unit) = unit[5].b

  unit_number > TOTAL_UNITS && return true

  program_unit = program[(unit_number-1)*UNIT_SIZE+1:unit_number*UNIT_SIZE]
  type = unit_type(program_unit)
  offset1 = program_unit[6].b
  offset2 = program_unit[16].b

  if type == UNIT_TYPE_1
    for w in digits
      push!(model_number, w)

      z1 = alu(w, z, offset1, offset2, type)
      is_valid_digit = try_model(program, unit_number + 1, model_number, z1, digits)
      if is_valid_digit
        return is_valid_digit
      else
        pop!(model_number)
        continue
      end
    end

    return false
  elseif type == UNIT_TYPE_2
    w1 = alu(0, z, offset1, offset2, type)
    # For w1 to be a valid digit in the model number, it must be 1-9.
    # So for type 2, if w1 is valid it is our w, which we add to model_number.
    # And if w1 is valid, our next z is z ÷ 26.
    !(w1 in 1:9) && return false
    push!(model_number, w1)
    is_valid_digit = try_model(program, unit_number + 1, model_number, z ÷ 26, digits)
    !is_valid_digit && pop!(model_number)
    return is_valid_digit
  else
    throw("Invalid unit type: $type")
  end
end

function part1(input)
  model_number = []
  try_model(input, 1, model_number, 0, 9:-1:1)
  join(model_number)
end

function part2(input)
  model_number = []
  try_model(input, 1, model_number, 0, 1:9)
  join(model_number)
end

function read_input(input_file)
  function to_instruction(l)
    args = split(l, ' ')
    b = args[1] == "inp" ? nothing : args[3]
    if !isnothing(b) && (isdigit(b[1]) || (b[1] == '-'))
      b = to_int(b)
    end
    Instruction(args[1], args[2], b)
  end

  map(to_instruction, readlines(input_file))
end

function main()
  main_input = read_input("../data/day24.txt")

  @show part1(main_input) # 92967699949891
  @show part2(main_input) # 91411143612181
end

@time main()
