import 'dart:io';
import './utils.dart';

const bool DEBUG = false;

final List<int> TEST_INPUT = File('../data/day09-test.txt')
    .readAsLinesSync()
    .map((l) => int.parse(l))
    .toList();

final List<int> MAIN_INPUT = File('../data/day09.txt')
    .readAsLinesSync()
    .map((l) => int.parse(l))
    .toList();

//Find number that doesn't have a pair in the preceding list (size preambleLength)
//that doesn't add up to number.
int findOutlier(List<int> input, int preambleLength) {
  bool summedPairExists(List<int> candidates, int target) {
    //we can ignore the last element because
    //it would have been matched if complement existed.
    for (var i = 0; i < candidates.length - 1; i++) {
      var complement = target - candidates[i];
      if (candidates.sublist(i + 1).toSet().contains(complement)) return true;
    }
    return false;
  }

  for (var i = preambleLength; i < input.length; i++) {
    if (!summedPairExists(input.sublist(i - preambleLength, i), input[i])) {
      return input[i];
    }
  }
  return null;
}

int findEncryptionWeakness(List<int> input, int target) {
  var emptyList = <int>[];

  List<int> continguousSum(start) {
    var sum = 0;
    for (var i = start; i < input.length; i++) {
      sum += input[i];
      if (sum > target) return emptyList;
      if (sum == target) return input.sublist(start, i + 1);
    }
    return emptyList;
  }

  var continguousList = emptyList;
  for (var i = 0; i < input.length; i++) {
    continguousList = continguousSum(i);
    if (continguousList.isNotEmpty && continguousList.length > 1) {
      return (continguousList.min + continguousList.max);
    }
  }
  return null;
}

void test() {
  printHeader('9 test');
  //Answer: 127
  print(findOutlier(TEST_INPUT, 5));
  //Answer: 62
  print(findEncryptionWeakness(TEST_INPUT, findOutlier(TEST_INPUT, 5)));
}

void part1() {
  printHeader('9 part 1');
  // Answer: 1309761972
  print(findOutlier(MAIN_INPUT, 25));
}

void part2() {
  printHeader('9 part 2');
  //Answer: 177989832
  print(findEncryptionWeakness(MAIN_INPUT, findOutlier(MAIN_INPUT, 25)));
}

void main(List<String> arguments) {
  test();
  part1();
  part2();
}
