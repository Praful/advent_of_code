using AdventOfCodeUtils
using Test
# using Memoize
# using Combinatorics

# Puzzle description: https://adventofcode.com/2018/day/04


mutable struct SleepRecord
  minutes_asleep
  total_sleep_time
end

function parse(log)
  extract_number(re, s) = to_int((match(re, s))[1])

  guard = nothing
  asleep_at = 0
  wakes_up = 0
  result = Dict()

  for (time, desc) in log
    if contains(desc, "Guard")
      guard = extract_number(r"\#(\d+)", desc)
      if !haskey(result, guard)
        result[guard] = SleepRecord(fill(0, 60), 0)
      end
    elseif contains(desc, "falls asleep")
      asleep_at = extract_number(r":(\d+)", time)
    elseif contains(desc, "wakes up")
      wakes_up = extract_number(r":(\d+)", time)
      record = result[guard]
      record.total_sleep_time += wakes_up - asleep_at
      [record.minutes_asleep[i] += 1 for i in asleep_at+1:wakes_up]
    end
  end

  result
end

function part1(input)
  worst_guard = 0
  max_sleep_time = 0
  for (guard, record) in input
    if record.total_sleep_time > max_sleep_time
      max_sleep_time = record.total_sleep_time
      worst_guard = guard
    end
  end

  worst_guard * (argmax(input[worst_guard].minutes_asleep) - 1)
end

function part2(input)
  worst_guard = 0
  max_minute = 0
  max_times_asleep = 0
  for (guard, record) in input
    max = argmax(record.minutes_asleep)

    if record.minutes_asleep[max] > max_times_asleep
      max_times_asleep = record.minutes_asleep[max]
      max_minute = max
      worst_guard = guard
    end
  end
  worst_guard * (max_minute - 1)
end

function read_input(input_file)
  log = Dict()
  for l in readlines(input_file)
    m = match(r"(\[.+\])\s(.*)", l)
    log[m[1]] = m[2]
  end

  parse(sort(collect(log), by = x -> x[1]))
end

function main()
  main_input = read_input("../data/day04.txt")
  test_input = read_input("../data/day04-test.txt")

  @test part1(test_input) == 240
  @test part2(test_input) == 4455

  @show part1(main_input) # 8421
  @show part2(main_input) # 83359
end

@time main()
