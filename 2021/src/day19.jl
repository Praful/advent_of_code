using AdventOfCodeUtils
using DelimitedFiles
using Test
using LinearAlgebra
using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/19

# This is more straightforward than it seems. The only maths you need
# is how to rotate a point in 3D. For reference see
# https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
# The algorithm is:
# 1. For each scanner, find the square distance between each
#    pair of beacons.
# 2. Compare these distances between scanners. That tells you which 
#    scanners overlap.
# 3. For each of these overlapping scanners (s1 and s2, say), use a
#    pair of beacons to find the correct rotation of beacons in s2
#    so that they align to beacons in s1. As part of finding the 
#    rotation, the location of the scanner (relative to the first scanner)
#    pops out. 


# min overlapping beacons between two scanners if they overlap
const MIN_MATCHES = 12

# number of pairs we can expect to match between two scanners
const PAIR_MATCHES = (MIN_MATCHES * (MIN_MATCHES - 1)) ÷ 2

const Point = Vector{Int}

mutable struct Scanner
  beacons::Vector{Point} # list of beacons
  location # scanner location (x,y,z) 
  rotation # rotation matrix to align with first scanner
  distances::Vector{Int} # distances between pairs of beacons seen by this scanner
  dist_beacon_map::Dict{Int,Vector{Point}} # mapping between dist between two beacons and the pair of beacons

  Scanner(beacons) = new(beacons, nothing, nothing, [], Dict())
end


function generate_rotations()
  R1 = [0 0 -1; 0 1 0; 1 0 0]
  R2 = [1 0 0; 0 0 -1; 0 1 0]
  R3 = [0 -1 0; 1 0 0; 0 0 1]
  result = []
  for x = 0:3, y = 0:3, z = 0:3
    m = R1^x * R2^y * R3^z
    push!(result, m)
  end
  unique(result)
end

# Return scanner pairs with the beacons distances they share.
function overlapping_scanners(scanners)
  is_matched(i, j) = haskey(result, [i, j]) ||
                     haskey(result, [j, i]) || i == j

  result = Dict{Vector{Int},Vector{Int}}()
  for (i, s1) in enumerate(scanners), (j, s2) in enumerate(scanners)
    is_matched(i, j) && continue
    common_beacon_distances = intersect(s1.distances, s2.distances)
    if length(common_beacon_distances) >= PAIR_MATCHES
      result[[i, j]] = common_beacon_distances
    end
  end
  result
end

# Return the location of the scanner.
#
# Let A and B be beacons in scanner 1; C and D for scanner 2.
# The distance between A and B = dist between C and D, as worked
# out in overlapping_scanners(). So we know line AB is line CD.
# We just don't know which ends match and we don't know their
# orientations. This function works out whether beacon A is C or D;
# and similarly whether beacon B is D or C by comparing the differences.
# Below A = beacon_pair1[1], B = beacon_pair1[2]
#       C = beacon_pair2[1], D = beacon_pair2[2]
# If the differences don't match then the correct rotation hasn't 
# been found, in which case return nothing.
#
# To see why this works, look at the 2D example on AoC. Find a 
# common point and take the difference from the two scanners'
# perspective eg relative to S1 at [0,0], one B is at [4,1]. relative
# to S2 at [5,2], B is at [-1,-1]. Then [4,1] - [-1,-1] = [5,2], which
# is the location of S2. Note S2 is relative to S1 already so no
# rotation is required.

function scanner_location(beacon_pair1, beacon_pair2)
  loc1 = beacon_pair1[1] - beacon_pair2[1]
  loc2 = beacon_pair1[2] - beacon_pair2[2]
  (loc1 == loc2) && return loc1

  loc1 = beacon_pair1[1] - beacon_pair2[2]
  loc2 = beacon_pair1[2] - beacon_pair2[1]
  (loc1 == loc2) && return loc1

  return nothing
end

# Return unqiue beacons and find locations of scanners
function unique_beacons(scanners)
  one_scanner_unprocessed(id1, id2) = xor(isnothing(scanners[id1].location), isnothing(scanners[id2].location))
  found_rotation_and_location(location) = !isnothing(location)

  rotations = generate_rotations()
  overlaps = overlapping_scanners(scanners)

  result = Set(scanners[1].beacons)

  scanners_processed = 1
  while (scanners_processed < length(scanners))
    for ((id1, id2), dist) in overlaps
      # We want one of the two scanners to not yet be processed
      !one_scanner_unprocessed(id1, id2) && continue

      # The first scanner is the reference scanner, which the 
      # second is aligned to. So it must have a location.
      if isnothing(scanners[id1].location)
        id1, id2 = id2, id1
      end

      # we only need to compare a pair from each scanner to work
      # out the second scanner's orientation and location.
      # @show dist
      s1_beacon_pair = scanners[id1].dist_beacon_map[dist[1]]
      s2_beacon_pair = scanners[id2].dist_beacon_map[dist[1]]

      rotate1 = [scanners[id1].rotation] .* s1_beacon_pair

      for r in rotations
        rotate2 = [r] .* s2_beacon_pair
        location = scanner_location(rotate1, rotate2)

        if found_rotation_and_location(location)
          # We need to adjust the location so that it is relative to
          # the first scanner (ie scanners[1]), which is
          # what scanner[id1] has been aligned to.
          location += scanners[id1].location

          scanners[id2].location = location
          scanners[id2].rotation = r

          union!(result,
            Set([r] .* scanners[id2].beacons .+ [location]))

          scanners_processed += 1
          break
        end
      end
    end
  end
  result
end

# Return number of unique beacons
part1(scanners) = length(unique_beacons(scanners))

# Return max manhatten distance between scanners
part2(scanners) = maximum((sum(abs.(s1.location - s2.location))
                           for s1 ∈ scanners, s2 ∈ scanners))


distance(p1, p2) = sum((p1 - p2) .^ 2)

function read_input(input_file)
  input = readlines(input_file)
  scanners = Vector{Scanner}()
  beacons = Vector{Point}()

  for l in input
    if contains(l, "scanner")
      beacons = Vector{Point}()
      push!(scanners, Scanner(beacons))
    elseif !isempty(l)
      push!(beacons, parse.(Int, split(l, ",")))
    end
  end

  scanners[1].location = [0, 0, 0] # fix to origin
  # Identity matrix: no rotation required for first scanner
  scanners[1].rotation = Matrix{Int}(I, 3, 3)

  # calc distances between pairs of beacons for each scanner
  for s in scanners, pair in combinations(s.beacons, 2)
    d = distance(pair[1], pair[2])
    s.dist_beacon_map[d] = pair
    push!(s.distances, d)
  end
  scanners
end

function main()
  main_input = read_input("../data/day19.txt")
  test_input = read_input("../data/day19-test.txt")

  # @test part1(test_input) == 79
  # @test part2(test_input) == 3621

  @show part1(main_input) # 338 
  @show part2(main_input) # 9862
end

@time main()
