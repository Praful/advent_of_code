using DelimitedFiles

global max_x = max_y = 0

struct Point
  x::Int
  y::Int
  function Point(s) # "x,y"
    x, y = parse.(Int, split(s, ","))
    new(x, y)
  end
  Point(x, y) = new(x, y)
end

struct Line
  start::Point
  end_::Point
  points_on_line::Vector{Point}
end

is_horiz(start, end_) = start.y == end_.y
is_vert(start, end_) = start.x == end_.x
is_diag(start, end_) = !(is_horiz(start, end_) || is_vert(start, end_))

function update_maxes(p)
  global max_x = max(max_x, p.x)
  global max_y = max(max_y, p.y)
end

# We add 1 to x and y values because Julia arrays start at 1 whereas the
# input can start at 0
function plot(lines)
  diagram = zeros(Int, max_x + 1, max_y + 1)
  for l in lines
    [diagram[p.x+1, p.y+1] += 1 for p in l.points_on_line]
  end
  length(diagram[diagram.>1])
end

function part1(input_file)
  global max_x = max_y = 0
  lines = read_input(input_file)
  plot(lines)
end

function part2(input_file)
  global max_x = max_y = 0
  lines = read_input(input_file, true)
  plot(lines)
end

function read_input(filename, include_diags = false)
  lines = Vector{Line}()

  open(filename, "r") do f
    for line in readlines(f)
      start, end_ = split(line, "->")
      p1 = Point(start)
      p2 = Point(end_)
      update_maxes(p1)
      update_maxes(p2)

      if !is_diag(p1, p2) || include_diags
        push!(lines, points_on_line(p1, p2))
      end
    end
  end
  lines
end

function points_on_line(start, end_)
  x_start, x_end = sort([start.x, end_.x])
  y_start, y_end = sort([start.y, end_.y])
  points = Vector{Point}()

  if is_horiz(start, end_)
    [push!(points, Point(x, y_start)) for x = x_start:x_end]
  elseif is_vert(start, end_)
    [push!(points, Point(x_start, y)) for y = y_start:y_end]
  else # is diag 
    slope_start, slope_end = start.x > end_.x ? (end_, start) : (start, end_)
    slope = slope_start.y > slope_end.y ? -1 : 1

    [push!(points, Point(slope_start.x + inc, slope_start.y + (slope * inc))) for inc = 0:abs(slope_end.x - slope_start.x)]
  end

  Line(start, end_, points)
end


function main()
  test_input = "../data/day05-test.txt"
  main_input = "../data/day05.txt"

  @assert part1(test_input) == 5
  @assert part2(test_input) == 12

  @show part1(main_input) # 5197
  @show part2(main_input) # 18605
end

@time main()
