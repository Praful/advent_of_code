using AdventOfCodeUtils
using DelimitedFiles
using Test
using LinearAlgebra
using Combinatorics

# Puzzle description: https://adventofcode.com/2021/day/19

# min overlapping beacons between two scanners if they overlap
const MIN_MATCHES = 12
# number of pairs we can expect to match between two scanners
const PAIR_MATCHES = (MIN_MATCHES * (MIN_MATCHES - 1)) ÷ 2

mutable struct Scanner
  beacons::Vector{Vector{Int}} # list of beacons
  location # scanner location (x,y,z)
  rotation # rotation matrix to align with first scanner
  distances::Vector{Int} # distances between pairs of beacons seen by this scanner
  dist_beacon_map::Dict{Int,Vector{Vector{Int}}} # mapping between dist between two beacons and the pair of beacons
end

function get_rotations()
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
function matches(scanners)
  is_matched(i, j) = haskey(result, [i, j]) ||
                     haskey(result, [j, i]) || i == j
  result = Dict{Vector{Int},Vector{Int}}()
  for (i, s1) in enumerate(scanners), (j, s2) in enumerate(scanners)
    is_matched(i, j) && continue
    common_beacons = intersect(s1.distances, s2.distances)
    if length(common_beacons) >= PAIR_MATCHES
      result[[i, j]] = common_beacons
      # println("$i and $j match")
    end
  end
  result
end

# Let A and B be beacons in scanner 1; C and D for scanner 2.
# The distance between A and B = dist between C and D, as worked
# out in matches(). So we know line AB is line CD. We just don't
# know which ends match. This function works out whether beacon A
# is C or D; and conversely whether beacon B is D or C by
# comparing the differences.
# Below A = beacon_pair1[1], B = beacon_pair1[2]
#       C = beacon_pair2[1], D = beacon_pair2[2]
# If the differences don't match then the correct rotation hasn't 
# been found, in which case return nothing.
# To see why this works, look at the 2D example on AoC, find a 
# common point and take the difference from the two scanners'
# perspective.
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
function locations(scanners, matches)
  one_scanner_unprocessed(id1, id2) = xor(isnothing(scanners[id1].location), isnothing(scanners[id2].location))

  rotations = get_rotations()
  unique_beacons = Set(scanners[1].beacons)

  locations_found = 1
  while (locations_found < length(scanners))
    for (match, dist) in matches
      id1, id2 = match[1], match[2]

      # We want one of the two scanners to not yet be processed
      !one_scanner_unprocessed(id1, id2) && continue

      # The first scanner is the reference scanner, which the 
      # second is aligned to. So it must have a location.
      if isnothing(scanners[id1].location)
        id1, id2 = id2, id1
      end

      # we only need to compare a pair from each scanner to work
      # out the second scanner's orientation and location.
      s1_beacon_pair = scanners[id1].dist_beacon_map[dist[1]]
      s2_beacon_pair = scanners[id2].dist_beacon_map[dist[1]]

      rotate1 = [scanners[id1].rotation] .* s1_beacon_pair

      for r in rotations
        rotate2 = [r] .* s2_beacon_pair
        location = scanner_location(rotate1, rotate2)

        if !isnothing(location) # we've found location for scanner 2
          location += scanners[id1].location
          scanners[id2].location = location
          scanners[id2].rotation = r

          union!(unique_beacons,
            Set([r] .* scanners[id2].beacons .+ [location]))

          locations_found += 1
          break
        end
      end
    end
  end
  unique_beacons
end

# Return number of unique beacons
part1(scanners) = length(locations(scanners, matches(scanners)))

# Return max manhatten distance between scanners
part2(scanners) = maximum((sum(abs.(s1.location - s2.location))
                           for s1 ∈ scanners, s2 ∈ scanners))


distance(p1, p2) = sum((p1 - p2) .^ 2)

function read_input(input_file)
  input = readlines(input_file)
  scanners = Vector{Scanner}()
  beacons = Vector{Vector{Int}}()

  for l in input
    if contains(l, "scanner")
      beacons = Vector{Vector{Int}}()
      push!(scanners, Scanner(beacons, nothing, nothing, [], Dict()))
    elseif !isempty(l)
      push!(beacons, parse.(Int, split(l, ",")))
    end
  end

  scanners[1].location = [0, 0, 0] # fix to origin
  # identity matrix: no rotation required for first scanner
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

  @test part1(test_input) == 79
  @test part2(test_input) == 3621

  @show part1(main_input) # 338 
  @show part2(main_input) # 9862
end

@time main()