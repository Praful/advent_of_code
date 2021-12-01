using DelimitedFiles

read_input(filename) = filename |> readlines .|> x -> parse(Int, x)

function part1(input)
  prev = Inf
  result = 0
  for i in input
    if i > prev
      result += 1
    end
    prev = i
  end

  result
end

# Return array for sum of elements in sliding window of 3
function part2(input)
  result =[]
  input_size = size(input,1)  
  for i in eachindex(input)
    if i+2<=input_size
      push!(result, input[i]+input[i+1]+input[i+2])
    end
  end 
  result
end

function main()
  main_input = readdlm("../data/day01.txt", Int)
  test_input = readdlm("../data/day01-test.txt", Int)

  @assert part1(test_input)== 7 "01 test part 1 should be 7"
  @assert part1(part2(test_input)) == 5 "01 test part 2 should be 5"

  part1_solution = part1(main_input)
  @show part1_solution

  part2_solution = part1(part2(main_input))
  @show part2_solution

  # (part1_solution, part2_solution)
end

main()

# @time (part1_solution, part2_solution) = main()
# @show part1_solution
# @show part2_solution