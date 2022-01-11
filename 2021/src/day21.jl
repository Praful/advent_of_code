using AdventOfCodeUtils
using DelimitedFiles
using Test
using Memoize
using Printf
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/21

# For the second part, I got help on Reddit. The method is, for each
# combinaton of three dice (one die splitting into three dice), work out
# the new position and score for each player.


# Return new position
function new_roll(pos, score, throw_value)
  new_pos = ((pos + throw_value - 1) % 10) + 1
  new_score = score + new_pos
  (new_pos, new_score)
end

function deterministic_dice(input)
  pos = copy(input)
  score = [0, 0]
  rolled = 1 # number rolled by die
  previous_player = 2 # the last player who moved
  roll_count = 3

  while true
    throw_value = 3rolled + 3
    current_player = previous_player == 2 ? 1 : 2

    pos[current_player], score[current_player] =
      new_roll(pos[current_player], score[current_player], throw_value)
    score[current_player] >= 1000 && break

    previous_player = current_player
    rolled = (rolled + 3) % 100
    roll_count += 3
  end
  minimum(score) * roll_count
end

const DIE_RANGE = 1:3
@memoize function new_universe(player, pos1, score1, pos2, score2)
  # Is there a winner yet?
  score1 >= 21 && return (1, 0) # player 1 won 
  score2 >= 21 && return (0, 1) # player 2 won

  wins = [0, 0]

  for die1 ∈ DIE_RANGE, die2 ∈ DIE_RANGE, die3 ∈ DIE_RANGE
    if player == 1
      new_pos, new_score = new_roll(pos1, score1, die1 + die2 + die3)
      wins1, wins2 = new_universe(2, new_pos, new_score, pos2, score2)
    else
      new_pos, new_score = new_roll(pos2, score2, die1 + die2 + die3)
      wins1, wins2 = new_universe(1, pos1, score1, new_pos, new_score)
    end
    wins[1] += wins1
    wins[2] += wins2
  end
  wins
end

function dirac_dice(input)
  maximum(new_universe(1, input[1], 0, input[2], 0))
end

part1(input) = deterministic_dice(input)
part2(input) = dirac_dice(input)

function read_input(input_file)
  start_pos(player) = parse(Int, match(r"\: (\d+)", player)[1])

  input = readlines(input_file)
  [start_pos(input[1]), start_pos(input[2])]
end

function main()
  main_input = read_input("../data/day21.txt")
  test_input = read_input("../data/day21-test.txt")

  @test part1(test_input) == 739785
  @test part2(test_input) == 444356092776315
  @show part1(main_input) # 506466
  @show part2(main_input) # 632979211251440
end

@time main()
