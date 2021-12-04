using DelimitedFiles

function part1(input)
  gamma_str = ""
  half_way = length(input) / 2
  for c = 1:length(input[1])
    num_ones = length(filter(==('1'), map(x -> x[c], input)))
    gamma_str *= num_ones > half_way ? "1" : "0"
  end

  gamma = parse(Int, gamma_str, base = 2)
  epsilon = parse(Int, replace(gamma_str, "0" => "1", "1" => "0"), base = 2)

  gamma * epsilon
end

function rating(input, bit_value)
  for c = 1:length(input[1])
    num_ones = length(filter(==('1'), map(x -> x[c], input)))
    target = num_ones >= length(input) / 2 ? bit_value[1] : bit_value[2]

    if length(input) > 1
      input = filter(x -> x[c] == target, input)
    else
      break
    end
  end
  parse(Int, input[1], base = 2)
end

function part2(input)
  rating(input, ['1', '0']) * rating(input, ['0', '1'])
end

function main()
  main_input = readdlm("../data/day03.txt", String)
  test_input = readdlm("../data/day03-test.txt", String)

  @assert part1(test_input) == 198
  @assert part2(test_input) == 230

  @show part1(main_input) # 3882564
  @show part2(main_input) # 3385170
end

main()
