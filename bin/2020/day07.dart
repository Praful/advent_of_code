import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;

final String TEST_INPUT = File('./data/day07-test.txt').readAsStringSync();

final String MAIN_INPUT = File('./data/day07.txt').readAsStringSync();

Iterable<String> findOuterBag(input, bag) {
  var outerBagRegex =
      RegExp(r'(?<outerBag>.*)s contain.*' + bag, multiLine: true);
  var result = <String>{};
  outerBagRegex.allMatches(input).forEach((match) {
    var outerBag = match.namedGroup('outerBag');
    result.add(outerBag);
    result.addAll(findOuterBag(input, outerBag));
  });
  return result;
}

void part1Test() {
  printHeader('7a test');
  //Answer: 4
  print(findOuterBag(TEST_INPUT, 'shiny gold bag').length);
}

void part1() {
  //Answer: 115
  printHeader('7a');
  print(findOuterBag(MAIN_INPUT, 'shiny gold bag').length);
}

void part2() {
  printHeader('7b');
}

void main(List<String> arguments) {
  part1Test();
  part1();
  part2();
}
