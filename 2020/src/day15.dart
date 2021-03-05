import '../../shared/dart/src/utils.dart';

const bool DEBUG = true;
const int TURN_COUNT_1 = 2020;
const int TURN_COUNT_2 = 30000000;
// const int TURN_COUNT = 11;

void findLastSpokenNumber(String name, List<int> input,
    [turnCount = TURN_COUNT_1]) {
  printHeader(name);

  var history = <int, int>{};
  for (var i = 0; i < input.length - 1; i++) {
    history[input[i]] = i + 1;
  }

  var lastNumberSpoken = input.last;

  for (var turn = input.length + 1; turn <= turnCount; turn++) {
    var turnSpoken = history[lastNumberSpoken] ?? 0;
    history[lastNumberSpoken] = turn - 1;
    lastNumberSpoken = turnSpoken == 0 ? 0 : turn - 1 - turnSpoken;
  }
  print(lastNumberSpoken);
}

void main(List<String> arguments) {
  if (DEBUG) {
    findLastSpokenNumber('15 test part 1', [0, 3, 6]); //: 436

    findLastSpokenNumber(
        '15 test part 1a', [1, 3, 2]); // 2020th number spoken is 1.
    findLastSpokenNumber(
        '15 test part 1b', [2, 1, 3]); // 2020th number spoken is 10.
    findLastSpokenNumber(
        '15 test part 1c', [1, 2, 3]); // 2020th number spoken is 27.
    findLastSpokenNumber(
        '15 test part 1d', [2, 3, 1]); // 2020th number spoken is 78.
    findLastSpokenNumber(
        '15 test part 1e', [3, 2, 1]); // 2020th number spoken is 438.
    findLastSpokenNumber(
        '15 test part 1f', [3, 1, 2]); // 2020th number spoken is 1836.
  }
  //Answer: part 1: 1696, part 2: 37385
  findLastSpokenNumber('15 part 1', [12, 1, 16, 3, 11, 0], TURN_COUNT_1);
  findLastSpokenNumber('15 part 2', [12, 1, 16, 3, 11, 0], TURN_COUNT_2);
}
