using DelimitedFiles

# Return true if all elements in a row or column consists only of -1 values
winner(board) = any(all(==(-1), board, dims = 1)) || any(all(==(-1), board, dims = 2))

score(board, last_draw) = sum(board[board.!==-1]) * last_draw

function part1(input_file)
  (draw, boards) = read_input(input_file)

  for n in draw
    for board_index = 1:size(boards, 3)
      board = view(boards, :, :, board_index)
      board[board.==n] .= -1
      if winner(board)
        return score(board, n)
      end
    end
  end
end

function part2(input_file)
  (draw, boards) = read_input(input_file)
  board_count = size(boards, 3)
  winners = []

  for n in draw
    for board_index = 1:board_count
      board = view(boards, :, :, board_index)
      board[board.==n] .= -1
      if !(board_index in winners) && winner(board)
        append!(winners, board_index)
        if length(winners) == board_count
          return score(board, n)
        end
      end
    end
  end
end

function read_input(filename)
  open(filename, "r") do f
    draw = parse.(Int, split(readline(f), ","))
    boards = split(replace(read(f, String), "\n" => " ", "\r\n" => " "), " ", keepempty = false)
    boards = reshape(parse.(Int, boards), 5, 5, :)
    (draw, boards)
  end
end

function main()
  test_input = "../data/day04-test.txt"
  main_input = "../data/day04.txt"

  @assert part1(test_input) == 4512
  @assert part2(test_input) == 1924

  @show part1(main_input) # 55770
  @show part2(main_input) # 2980 
end

main()
