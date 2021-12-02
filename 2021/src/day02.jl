using DelimitedFiles

function part1(input)
  pos = depth = 0
  # @show size(input)
  for (dir, qty) in eachrow(input)
    if dir == "forward"
      pos += qty
    elseif dir == "up"
      depth -= qty
    elseif dir == "down"
      depth += qty
    end
  end

  # @show pos, depth

  pos * depth
end

# alternative part 1 method using filtering
# this is much faster: ~ 0.0002 vs 0.02 for part1()
function part1_filter(input)
  forward = input[(input[:, 1].=="forward"), :]
  up = input[(input[:, 1].=="up"), :]
  down = input[(input[:, 1].=="down"), :]

  sum(forward[:, 2]) * (sum(down[:, 2]) - sum(up[:, 2]))
end

function part2(input)
  pos = depth = aim = 0
  for (dir, qty) in eachrow(input)
    if dir == "forward"
      pos += qty
      depth += aim * qty
    elseif dir == "up"
      aim -= qty
    elseif dir == "down"
      aim += qty
    end
  end

  pos * depth
end

function main()
  main_input = readdlm("../data/day02.txt")
  test_input = readdlm("../data/day02-test.txt")

  # @assert part1(test_input) == 150 "02 test part 1"
  @assert part1_filter(test_input) == 150 "02 test part 1 filter"
  @assert part2(test_input) == 900 "02 test part 2"

  # @show part1(main_input)
  @show part1_filter(main_input)
  @show part2(main_input)

  @time part1(main_input)
  @time part1_filter(main_input)

end

main()
