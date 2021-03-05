import 'dart:io';
import '../../shared/dart/src/utils.dart';

const bool DEBUG = false;

final List<String> TEST_INPUT2 =
    File('../data/day06b-test.txt').readAsStringSync().split('\n\n');

final List<String> TEST_INPUT =
    File('../data/day06-test.txt').readAsStringSync().split('\n\n');

final List<String> MAIN_INPUT =
    File('../data/day06.txt').readAsStringSync().split('\n\n');

int findSumOfGroups2(input) {
  return input.map((group) => group.split('\n')).map((g) {
    var ll = (g.map((r) => r.split(''))).toList();
    return ll.fold(ll.first.toSet(),
        (a, b) => b == null ? null : a.intersection(b.isEmpty ? a : b.toSet()));
  }).fold(0, (acc, s) => acc + s.length);
}

int findSumOfGroups1(input) => input
    .map((group) => group.replaceAll('\n', '').split('').toSet().length)
    .reduce((acc, length) => acc + length);

void test6() {
  printHeader('6a test');
  print(findSumOfGroups1(TEST_INPUT));
  print(findSumOfGroups2(TEST_INPUT));
  print(findSumOfGroups2(TEST_INPUT2));
}

void day6() {
  printHeader('6');
  print('Part 1: ${findSumOfGroups1(MAIN_INPUT)}');
  print('Part 2: ${findSumOfGroups2(MAIN_INPUT)}');
}

void main(List<String> args) {
  test6();
  day6();
}
