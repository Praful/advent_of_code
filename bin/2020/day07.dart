import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;

final String TEST_INPUT = File('./data/day07-test.txt').readAsStringSync();
final String TEST_INPUT2 = File('./data/day07b-test.txt').readAsStringSync();

final String MAIN_INPUT = File('./data/day07.txt').readAsStringSync();

Iterable<String> findOuterBags(input, bag) {
  var result = <String>{};
  RegExp(r'(?<outerBag>.*)s contain.*' + bag)
      .allMatches(input)
      .forEach((match) {
    var outerBag = match.namedGroup('outerBag');
    result.add(outerBag);
    result.addAll(findOuterBags(input, outerBag));
  });
  return result;
}

int findInnerBagCount(input, bag) {
  var result = 0;
  RegExp(bag + r's contain (?<innerBags>.*).')
      .allMatches(input)
      .forEach((match) {
    match.namedGroup('innerBags').split(',').forEach((innerBags) {
      RegExp(r'(?<count>\d+) (?<name>.*bag)s?')
          .allMatches(innerBags)
          .forEach((bag) {
        var count = int.parse(bag.namedGroup('count'));
        result +=
            count + (count * findInnerBagCount(input, bag.namedGroup('name')));
      });
    });
  });
  return result;
}

void test() {
  printHeader('7a test');
  //Answer: 4
  print(findOuterBags(TEST_INPUT, 'shiny gold bag').length);
  //Answer: 32
  print(findInnerBagCount(TEST_INPUT, 'shiny gold bag'));
  //Answer: 126
  print(findInnerBagCount(TEST_INPUT2, 'shiny gold bag'));
}

void part1() {
  //Answer: 115
  printHeader('7a');
  print(findOuterBags(MAIN_INPUT, 'shiny gold bag').length);
}

void part2() {
  printHeader('7b');
  print(findInnerBagCount(MAIN_INPUT, 'shiny gold bag'));
}

void main(List<String> arguments) {
  test();
  part1();
  part2();
}
