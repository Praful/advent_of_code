using AdventOfCodeUtils
using DelimitedFiles

# Puzzle description: https://adventofcode.com/2021/day/17


function solve(input)
  xtarget_range = input[1]
  ytarget_range = input[2]

  hit_target(px, py) = px in xtarget_range && py in ytarget_range
  missed(px, py) = px > xtarget_range[end] || py < ytarget_range[1]

  # This is a guess that suits my input; change for other input.
  n = 500

  max = 0
  hit_target_count = 0

  for sim_x = -n:n, sim_y = -n:n
    xprobe = yprobe = 0
    xvel, yvel = sim_x, sim_y
    simulation_max = 0
    while !missed(xprobe, yprobe)
      xprobe += xvel
      yprobe += yvel
      xvel += (xvel > 0 ? -1 : 0)
      yvel -= 1
      simulation_max = yprobe > simulation_max ? yprobe : simulation_max

      if hit_target(xprobe, yprobe)
        max = simulation_max > max ? simulation_max : max
        hit_target_count += 1
        break
      end
    end
  end
  max, hit_target_count
end

function read_input(input_file)
  readlines(input_file)[1]
end

function target_area(s)
  m = match(r"x=(-?\d+)\.\.(-?\d+).*?(-?\d+)\.\.(-?\d+)", s)
  x1, x2 = parse(Int, m[1]), parse(Int, m[2])
  y1, y2 = parse(Int, m[3]), parse(Int, m[4])

  x1:x2, y1:y2
end

function main()
  main_input = target_area(read_input("../data/day17.txt"))
  test_input = target_area("target area: x=20..30, y=-10..-5")

  @assert solve(test_input)[1] == 45
  @assert solve(test_input)[2] == 112

  @show solve(main_input) # 11175, 3540
end

@time main()
