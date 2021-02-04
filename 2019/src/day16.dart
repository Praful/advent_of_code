import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/16
///
/// Part 1 uses brute force to find the result.
/// This can't be used (it would be too slow) for part 2 because the
/// signal is too long. However, there are two aspects of part 2 that
/// help you short circuit the calculation: (1) you can skip
/// some (most) of the signal by using the offset; (2) the pattern
/// and offset have been chosen carefully for us.
///
/// For part 2, look at this example for a 13-digit signal:
///
/// 1  2  3  4  5  6  7  8  9 10 11 12 13 | Phase output
/// --------------------------------------+-------------
/// 1  0 -1  0  1  0 -1  0  1  0 -1  0  1 | a
/// 0  1  1  0  0 -1 -1  0  0  1  1  0  0 | b
/// 0  0  1  1  1  0  0  0 -1 -1 -1  0  0 | c
/// 0  0  0  1  1  1  1  0  0  0  0 -1 -1 | d
/// 0  0  0  0  1  1  1  1  1  0  0  0  0 | e
/// 0  0  0  0  0  1  1  1  1  1  1  0  0 | f
/// 0  0  0  0  0  0  1  1  1  1  1  1  1 | g
/// 0  0  0  0  0  0  0  1  1  1  1  1  1 | h
/// 0  0  0  0  0  0  0  0  1  1  1  1  1 | i
/// 0  0  0  0  0  0  0  0  0  1  1  1  1 | j
/// 0  0  0  0  0  0  0  0  0  0  1  1  1 | k
/// 0  0  0  0  0  0  0  0  0  0  0  1  1 | l
/// 0  0  0  0  0  0  0  0  0  0  0  0  1 | m
///
/// There are 13 columns, one for each digit. The right column is the
/// output of a phase: abcdefghijklm.
///
/// The rows show the repeating pattern [0,1,0,-1]. Notice that
/// for half the rows (g-m), the outputs are produced using just the
/// final digits (cols 7-13). So we can calculate g-m without
/// having to apply the pattern to cols 1-6. To compute the next phase,
/// m is the last digit of the signal. l is the last digit added to
/// the second last digit, and so on. See phasePart2() for full
/// implementation.

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

String fftPart1(String input, int phaseCount) {
  var signal = input.split('').map((e) => e.toInt()).toList();
  range(0, phaseCount).forEach((_) => signal = phasePart1(signal));
  return signal.join();
}

List<int> phasePart1(List<int> signal) {
  var pattern = [0, 1, 0, -1];
  return List<int>.from(range(0, signal.length).map((pos) =>
      (range(0, signal.length).fold(
          0,
          (acc, i) =>
              acc +
              signal[i].toInt() * pattern[((i + 1) ~/ (pos + 1)) % 4])).abs() %
      10));
}

String fftPart2(String input, int signalCount, int phaseCount) {
  var offset = input.substring(0, 7).toInt();
  var signal = (input * signalCount)
      .substring(offset)
      .split('')
      .map((e) => e.toInt())
      .toList();

  range(0, phaseCount).forEach((_) => signal = phasePart2(signal));
  return signal.getRange(0, 8).join();
}

List<int> phasePart2(List<int> signal) {
  var previous = 0;
  var result = List.generate(signal.length, (i) => 0, growable: false);

  //compute cumulative sum starting from end of signal
  for (var i = signal.length - 1; i >= 0; i--) {
    previous = (signal[i] + previous) % 10;
    result[i] = previous;
  }
  return result;
}

String part1(String header, input, phaseCount) {
  printHeader(header);
  return fftPart1(input, phaseCount);
}

Object part2(String header, String input,
    [int signalCount = 10000, int phaseCount = 100]) {
  printHeader(header);
  return fftPart2(input, signalCount, phaseCount);
}

void main(List<String> arguments) {
  var mainInput = FileUtils.asString('../data/day16.txt');

  assertEqual(part1('16 test part 1', '12345678', 4), '01029498');
  assertEqual(
      part1('16 test part 1a', '80871224585914546619083218645595', 100)
          .substring(0, 8),
      '24176176');
  assertEqual(
      part1('16 test part 1b', '19617804207202209144916044189917', 100)
          .substring(0, 8),
      '73745418');
  assertEqual(
      part1('16 test part 1c', '69317163492948606335995924319873', 100)
          .substring(0, 8),
      '52432133');

  assertEqual(
      part2('16 test part 2a', '03036732577212944063491565474664'), '84462026');

  assertEqual(
      part2('16 test part 2b', '02935109699940807407585447034323'), '78725270');

  assertEqual(
      part2('16 test part 2c', '03081770884921959731165446850517'), '53553731');

  printAndAssert(
      part1('16 part 1', mainInput, 100).substring(0, 8), '52611030');

  printAndAssert(part2('16 part 2', mainInput), '52541026');
}
