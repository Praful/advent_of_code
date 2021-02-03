import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/16

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

//for a digit return list of length count eg for inputs 3 and 5,
//return [3,3,3,3,3]
List repeatDigit(digit, count) => [for (var _ in range(0, count)) digit];

//if list is [1,2,3,4], return [1,2,3,4,1,2,3,4,...] repeated count times
List<int> repeatList(List<int> list, int count) =>
    [for (var _ in range(0, count)) ...list];

List<int> basePattern(int pos, int len) {
  var basePattern = [0, 1, 0, -1];

  var valueRepeat = List<int>.from(
      basePattern.map(((p) => repeatDigit(p, pos))).expand((e) => e));

  var groupRepeatCount = len ~/ valueRepeat.length;

  var result = repeatList(valueRepeat, groupRepeatCount + 1);

  result.removeAt(0);
  return result;
}

String lastDigit(int n) => n.toString().last;

String fft(String input, int phaseCount) {
  var phaseResult = input;
  for (var _ in range(0, phaseCount)) {
    var signal = phaseResult;
    phaseResult = range(0, input.length).map((j) {
      var pattern = basePattern(j + 1, input.length);

      return lastDigit(range(0, input.length)
          .fold(0, (acc, i) => acc + signal[i].toInt() * pattern[i]));
    }).join();
  }
  return phaseResult;
}

String part1(String header, input, phaseCount) {
  printHeader(header);

  return fft(input, phaseCount);
}

Object part2(String header, List input) {
  printHeader(header);

  //TODO return something
  return null;
}

void main(List<String> arguments) {
  var mainInput = FileUtils.asString('../data/day16.txt');

  //Answer:
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

  assertEqual(part1('16 test part 2', '03036732577212944063491565474664', 100),
      84462026);

  assertEqual(part1('16 test part 2', '00000000', 100), 1);

  // printAndAssert(
  // part1('16 part 1', mainInput, 100).substring(0, 8), '52611030');

  //Answer:
  // printAndAssert(part2('16 part 2', mainInput));
}
