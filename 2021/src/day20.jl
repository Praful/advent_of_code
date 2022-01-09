using AdventOfCodeUtils
using DelimitedFiles
using Test
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/20

# Rather than gradually expand the image at each enhancement, I create
# the expanded image in one go. This means I don't have to check whether
# the bounds of the 3x3 box around a pixel being enhanced is within
# bounds. I don't bother converting to bits either since the complete
# run is about 2s, including part 2.

const DARK = '.'
const LIGHT = '#'

print_image(image) = println.(image)

# Return expanded image, padded out with background.
function expand_image(image, background, width = 2)
  result = []
  border_row = background^(length(image[1]) + (width * 2))

  [push!(result, border_row) for _ ∈ 1:width]
  append!(result, map(r -> background^width * r * background^width, image))
  [push!(result, border_row) for _ ∈ 1:width]

  result
end

enhance_pixel(alg, square) = alg[bin2dec(replace(square, DARK => '0',
  LIGHT => '1'))+1]

# Return number of light pixels
function enhance_image((algorithm, image), enhance_count = 1)
  background = DARK
  border = enhance_border = enhance_count + 3
  # We do this once to allow for all iterations of the enhancment process
  img = expand_image(image, background, border)

  for i ∈ 1:enhance_count
    enhanced_image = []
    for r = enhance_border:(length(img)-enhance_border+1)
      new_row = ""
      for c = enhance_border:(length(img[1])-enhance_border+1)
        square = img[r-1][c-1:c+1] *
                 img[r][c-1:c+1] *
                 img[r+1][c-1:c+1]
        new_row *= enhance_pixel(algorithm, square)
      end
      push!(enhanced_image, new_row)
    end

    background = algorithm[background == DARK ? 1 : end]
    fill!(img, "$background"^length(img[1]))

    sides = background^(enhance_border - 1)
    [img[i+enhance_border-1] = sides * row * sides
     for (i, row) ∈ enumerate(enhanced_image)]

    # Enhance 1 pixel more around image for next iteration.
    enhance_border -= 1
  end

  mapreduce(c -> count(LIGHT, c), +, img)
end

part1(input) = enhance_image(input, 2)
part2(input) = enhance_image(input, 50)

# Return algorithm and image
function read_input(input_file)
  lines = readlines(input_file)
  (lines[1], Vector{String}(lines[3:end]))
end

function main()
  main_input = read_input("../data/day20.txt")
  test_input = read_input("../data/day20-test.txt")

  @test part1(test_input) == 35
  @test part2(test_input) == 3351

  @show part1(main_input) # 4968   
  @show part2(main_input) # 16793
end

@time main()
