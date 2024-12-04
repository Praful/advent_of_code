using AdventOfCodeUtils
using Test
import Base: copy, deleteat!, isempty

# Puzzle description: https://adventofcode.com/2018/day/7

# Terminology:
#  before - is the step that must be finished before 'after' can begin
#  after - is the step that must wait for 'before' to finish.
#  incoming - are the 'before' steps for a step
#  outgoing - are the 'after' steps for a step

struct Steps
  before::Vector{String}
  after::Vector{String}
end
copy(s::Steps) = Steps(copy(s.before), copy(s.after))
isempty(s::Steps) = isempty(s.before) && isempty(s.after)
function deleteat!(s::Steps, i)
  Base.deleteat!(s.before, i)
  Base.deleteat!(s.after, i)
end

# Topological sort using Kahn's s_algorithm. See
# https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
function part1(steps::Steps)
  mutable_steps = copy(steps)

  # true if all steps s depends on are complete
  prereqs_done(s) = isempty(incoming(s))

  # return indices not the actual step values
  incoming(s) = findall(==(s), mutable_steps.after)
  outgoing(s) = findall(==(s), mutable_steps.before)

  ready_steps = Set(filter(prereqs_done, mutable_steps.before))
  result = []

  function update_ready_steps(done)
    delete!(ready_steps, done)
    push!(result, done)

    # reverse order so that indices remain valid after deleting
    # elements from the 'from' and 'to' arrays
    for im in sort(outgoing(done), rev=true)
      s_after = mutable_steps.after[im]
      deleteat!(mutable_steps, im)
      prereqs_done(s_after) && push!(ready_steps, s_after)
    end
  end

  while !isempty(ready_steps)
    # This is an addition to Kahn to ensure lexicographical (A-Z) sorting
    s_before = sort([ready_steps...])[1]
    update_ready_steps(s_before)
  end

  !isempty(mutable_steps) && throw("Error: graph has at least one cycle")

  join(result)
end

# This solution is the same as part1 except that we need loops to countdown working workers and to
# assign steps to workers.
function part2(steps, num_workers, min_duration=0)
  IDLE = '-'
  STEP_INDEX = 1
  TIME_ELAPSED_INDEX = 2

  workers = []
  mutable_steps = copy(steps)

  duration(c) = c[1] - 'A' + min_duration + 1
  is_idle(w) = w == IDLE
  # note: fill() can't be used because it creates the object once then adds n references to so
  # changing one change all elements!
  [push!(workers, [IDLE, 0]) for _ in 1:num_workers]
  workers_busy() = length(findall(w -> !is_idle(w[STEP_INDEX]), workers))
  all_workers_busy() = workers_busy() == num_workers
  some_workers_busy() = workers_busy() > 0
  next_free_worker() = findfirst(w -> is_idle(w[STEP_INDEX]), workers)

  # true if all steps s depends on are complete
  prereqs_done(s) = isempty(incoming(s))

  # return indices not the actual step values
  incoming(s) = findall(==(s), mutable_steps.after)
  outgoing(s) = findall(==(s), mutable_steps.before)

  # ready_steps are the steps awaiting processing
  ready_steps = Set(filter(prereqs_done, mutable_steps.before))
  in_progress = []
  result = []

  # This is the same as part 1 except we remove from in_progress queue instead of the ready_steps
  function update_ready_steps(done)
    filter!(e -> e != done, in_progress)
    push!(result, done)

    # reverse order so that indices remain valid after deleting
    # elements from the 'from' and 'to' arrays
    for im in sort(outgoing(done), rev=true)
      s_after = mutable_steps.after[im]
      deleteat!(mutable_steps, im)
      prereqs_done(s_after) && push!(ready_steps, s_after)
    end
  end

  t = 0

  # we're done when all workers are idle and we have no more steps awaiting processing
  while some_workers_busy() || !isempty(ready_steps)

    # count down steps whilst 
    while (workers_busy() > 0) && (all_workers_busy() || isempty(ready_steps))
      t += 1
      for w in workers
        if !is_idle(w[STEP_INDEX])
          w[TIME_ELAPSED_INDEX] -= 1
          if w[TIME_ELAPSED_INDEX] == 0
            update_ready_steps(w[STEP_INDEX])
            w[STEP_INDEX] = IDLE
          end
        end
      end
    end

    # assign steps to workers if we have steps that are reading for processing and idle worker(s)
    while !all_workers_busy() && !isempty(ready_steps)
      w = workers[next_free_worker()]

      # This is an addition to Kahn to ensure lexicographical (A-Z) sorting
      # available_steps = filter(e->!(e in in_progress), ready_steps)
      # s_before = sort([available_steps...])[1]
      s_before = sort([ready_steps...])[1]

      delete!(ready_steps, s_before)

      w[STEP_INDEX] = s_before
      w[TIME_ELAPSED_INDEX] = duration(s_before)

      push!(in_progress, s_before)
    end

  end

  !isempty(mutable_steps) && throw("Error: graph has at least one cycle")

  # @show join(result)
  t
end


function read_input(input_file)
  before = []
  after = []

  # eg line: Step U must be finished before step A can begin.
  for l in readlines(input_file)
    m = match(r"Step (.).* step (.)", l)
    push!(before, m[1])
    push!(after, m[2])
  end
  Steps(before, after)
end

function main()

  main_input = read_input("../data/day07.txt")
  test_input = read_input("../data/day07-test.txt")

  @test part1(test_input) == "CABDFE"
  @test part2(test_input, 2) == 15

  @show part1(main_input) # "BHMOTUFLCPQKWINZVRXAJDSYEG"
  @show part2(main_input, 5, 60) #  877, BHTUMOFLQZCPWKIVNRXASJDYEG 
end

@time main()
