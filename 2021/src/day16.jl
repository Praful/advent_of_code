using AdventOfCodeUtils
using DelimitedFiles
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/16


struct Packet
  version::Int
  type_id::Int
  value::Int
  subpackets::Vector{Packet}
end

const TYPE_ID_SUM = 0
const TYPE_ID_PROD = 1
const TYPE_ID_MIN = 2
const TYPE_ID_MAX = 3
const TYPE_ID_LITERAL = 4
const TYPE_ID_GT = 5
const TYPE_ID_LT = 6
const TYPE_ID_EQ = 7

const LEN_TYPE_BITS = 0 # 15 bits giving length of subpacket
const LEN_TYPE_PACKETS = 1 # 11 bits giving subpacket count in packet

function print_packet(packet, level = 0)
  println(" "^level, "Version $(packet.version), value $(packet.value), id $(packet.type_id)")
  [print_packet(p, level + 1) for p in packet.subpackets]
end

function test_hex_to_binary_conversion()
  @assert hex2bin("D2FE28") |> join == "110100101111111000101000"
  @assert hex2bin("38006F45291200") |> join ==
          "00111000000000000110111101000101001010010001001000000000"
  @assert hex2bin("EE00D40C823060") |> join ==
          "11101110000000001101010000001100100000100011000001100000"
end

function version_sum(packet)
  result = 0
  if packet.type_id !== TYPE_ID_LITERAL
    result = mapreduce(version_sum, +, packet.subpackets)
  end

  packet.version + result
end

function calculate(packet)
  result = 0
  values = map(calculate, packet.subpackets)

  if packet.type_id == TYPE_ID_SUM
    result = sum(values)
  elseif packet.type_id == TYPE_ID_PROD
    result = prod(values)
  elseif packet.type_id == TYPE_ID_MIN
    result = minimum(values)
  elseif packet.type_id == TYPE_ID_MAX
    result = maximum(values)
  elseif packet.type_id == TYPE_ID_LITERAL
    result = packet.value
  elseif packet.type_id == TYPE_ID_GT
    result = values[1] > values[2] ? 1 : 0
  elseif packet.type_id == TYPE_ID_LT
    result = values[1] < values[2] ? 1 : 0
  elseif packet.type_id == TYPE_ID_EQ
    result = values[1] == values[2] ? 1 : 0
  end

  result
end

function part1(input)
  # @show hex2bin(input) |> join
  (packet, _) = decode(hex2bin(input))
  # print_packet(packet)
  version_sum(packet)
end

function part2(input)
  (packet, _) = decode(hex2bin(input))
  calculate(packet)
end

function decode_literal(bin)
  value = []
  last_index = 0
  for i in Iterators.countfrom(7, 5)
    last_index = i
    (i > 7 && bin[i-5] == 0) && break
    push!(value, bin[i+1:i+4]...)
  end
  bin2dec(value), last_index - 1
end

function decode(bin)
  version = bin2dec(bin[1:3])
  type_id = bin2dec(bin[4:6])

  if type_id == TYPE_ID_LITERAL
    (value, last_index) = decode_literal(bin)
    return Packet(version, type_id, value, []), last_index
  else # operator
    length_type_index = 7
    length_type = bin[length_type_index]
    subpackets = []

    if length_type == LEN_TYPE_BITS
      offset = length_type_index + 16 # 15 bits from index 8
      bit_length_end = bin2dec(bin[length_type_index+1:offset-1]) + offset

      while offset < bit_length_end
        (packet, last_index) = decode(bin[offset:end])
        push!(subpackets, packet)
        offset += last_index
      end
    else # if length_type == LEN_TYPE_PACKETS
      offset = length_type_index + 12  # 11 bits from index 8
      num_subpackets = bin2dec(bin[length_type_index+1:offset-1])

      for _ = 1:num_subpackets
        (packet, last_index) = decode(bin[offset:end])
        push!(subpackets, packet)
        offset += last_index
      end
    end
    return Packet(version, type_id, 0, subpackets), (offset - 1)
  end
end

function read_input(input_file)
  result = []
  [push!(result, l) for l in eachline(input_file)]
  result
end

function main()
  main_input = read_input("../data/day16.txt")[1]

  @assert part1("8A004A801A8002F478") == 16
  @assert part1("620080001611562C8802118E34") == 12
  @assert part1("C0015000016115A2E0802F182340") == 23
  @assert part1("A0016C880162017C3686B18A3D4780") == 31

  @assert part2("C200B40A82") == 3
  @assert part2("CE00C43D881120") == 9
  @assert part2("9C0141080250320F1802104A08") == 1

  @show part1(main_input) # 940
  @show part2(main_input) # 13476220616073
end

@time main()
