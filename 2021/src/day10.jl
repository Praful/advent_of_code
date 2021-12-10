using DelimitedFiles
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/10


const MATCHING_OPENING_BRACKET = Dict(')' => '(', ']' => '[', '}' => '{', '>' => '<')

const SYNTAX_ERROR_POINTS = Dict(')' => 3, ']' => 57, '}' => 1197, '>' => 25137)

const AUTOCOMPLETE_POINTS = Dict(')' => 1, ']' => 2, '}' => 3, '>' => 4)

const OPENING_BRACKETS = "([{<"

incomplete_lines = Vector{String}()

function part1(input)
  empty!(incomplete_lines)
  stack = Vector{Char}()
  result = 0

  for line in input
    # assume line is incomplete (remove later if not)
    push!(incomplete_lines, line)

    for c in line
      if c in OPENING_BRACKETS
        push!(stack, c)
      elseif stack[end] == MATCHING_OPENING_BRACKET[c]
        pop!(stack)
      else
        result += SYNTAX_ERROR_POINTS[c]
        pop!(incomplete_lines)
        break
      end
    end
  end
  result
end

function part2(input)
  stack = Vector{Char}()
  total_scores = Vector{Int}()
  score_multiplier = 5
  MATCHING_CLOSED_BRACKET = Dict()
  [MATCHING_CLOSED_BRACKET[v] = k for (k, v) in MATCHING_OPENING_BRACKET]

  function process_unclosed(line_score, c = nothing)
    while true
      if isnothing(c)
        isempty(stack) && break
      elseif stack[end] == MATCHING_OPENING_BRACKET[c]
        pop!(stack) && break
      end

      line_score = line_score * score_multiplier +
                   AUTOCOMPLETE_POINTS[MATCHING_CLOSED_BRACKET[pop!(stack)]]
    end
    line_score
  end

  for line in input
    line_score = 0
    for c in line
      if c in OPENING_BRACKETS
        push!(stack, c)
      elseif stack[end] == MATCHING_OPENING_BRACKET[c]
        pop!(stack)
      else # we have unclosed open bracket on stack
        line_score = process_unclosed(line_score, c)
      end
    end
    # clear remaining unmatched opening brackets
    !isempty(stack) && (line_score = process_unclosed(line_score))
    push!(total_scores, line_score)
  end
  sort!(total_scores)
  # @show total_scores
  total_scores[Int((1 + length(total_scores)) / 2)]
end

function read_input(input_file)
  readdlm(input_file, String)
end

function main()
  main_input = read_input("../data/day10.txt")
  test_input = read_input("../data/day10-test.txt")

  @assert part1(test_input) == 26397
  @assert part2(["<{([{{}}[<[[[<>{}]]]>[]]"]) == 294
  @assert part2(incomplete_lines) == 288957

  @show part1(main_input) # 358737
  @show part2(incomplete_lines) # 4329504793
end

@time main()
