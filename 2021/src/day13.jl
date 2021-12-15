using AdventOfCodeUtils
using DelimitedFiles
using Plots

# Puzzle description: https://adventofcode.com/2021/day/13

function plot_code(coords)
  #TODO reflect plot on x-axis 
  plotlyjs()
  scatter([c[1] for c in coords], [c[2] for c in coords])
end

function print_code(coords)
  BLOCK = '\u2588'
  SPACE = ' '
  xmin, xmax = minimum(x -> x[1], coords), maximum(x -> x[1], coords)
  ymin, ymax = minimum(x -> x[2], coords), maximum(x -> x[2], coords)
  diffx, diffy = 1 - xmin, 1 - ymin

  output = fill(SPACE, xmax - xmin + 1, ymax - ymin + 1)
  output[[c + CartesianIndex(diffx, diffy) for c in coords]] .= BLOCK
  output = reverse(rotl90(output), dims = (1))

  for r in eachrow(output)
    println()
    [print(c) for c in r]
  end
  println()
end

function solve(coords, folds)
  for f in folds
    (fx, fy) = Tuple(f)
    is_xfold = f[1] > 0

    for (i, c) in enumerate(coords)
      (cx, cy) = Tuple(c)

      if is_xfold
        new_coord = cx > fx ? (cx - (2 * (cx - fx)), cy) : (cx, cy)
        coords[i] = CartesianIndex(new_coord)
      else
        new_coord = cy > fy ? (cx, cy - (2 * (cy - fy))) : (cx, cy)
        coords[i] = CartesianIndex(new_coord)
      end
    end
    unique!(coords)
  end
  (length(coords), coords)
end

function part1((coords, folds))
  @show solve(coords, [folds[1]])[1]
end

function part2((coords, folds))
  _, result = solve(coords, folds)
  # plot_code(result)
  print_code(result)
end

function read_input(input_file)
  is_coord(s) = !startswith(s[1], "fold")
  is_xfold(s) = s[end] == 'x'

  input = readdlm(input_file, ',', String)
  coords = Vector{CartesianIndex}()
  folds = Vector{CartesianIndex}()
  for r in eachrow(input)
    if is_coord(r)
      push!(coords, CartesianIndex(parse(Int, r[1]), parse(Int, r[2])))
    else
      fold_line = split(r[1], "=")
      fold_value = parse(Int, fold_line[2])
      if is_xfold(fold_line[1])
        push!(folds, CartesianIndex(fold_value, 0))
      else
        push!(folds, CartesianIndex(0, fold_value))
      end
    end
  end
  (coords, folds)
end

function main()
  main_input = read_input("../data/day13.txt")
  test_input = read_input("../data/day13-test.txt")

  @assert part1(test_input) == 17

  @show part1(main_input) # 621
  part2(main_input) # HKUJGAJZ
end

@time main()
